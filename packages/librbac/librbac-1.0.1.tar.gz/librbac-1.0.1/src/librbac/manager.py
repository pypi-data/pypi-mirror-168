from collections import defaultdict
from importlib import import_module
from itertools import chain
from types import ModuleType
from typing import TYPE_CHECKING
from typing import Dict
from typing import Iterable
from typing import Set
from typing import Tuple

from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.functional import cached_property

from librbac.types import Permission
from librbac.utils.rbac import _get_rbac_viewsets


if TYPE_CHECKING:
    from rest_framework.viewsets import GenericViewSet


def _get_app_permissions_modules():
    """Возвращает модули permissions из приложений системы.

    :rtype: generator
    """
    for app_config in apps.get_app_configs():
        try:
            yield import_module('.permissions', app_config.name)
        except ImportError as error:
            if 'No module named' not in error.args[0]:
                raise
            continue


class RBACManager(object):

    """Менеджер системы контроля доступа RBAC."""

    _msg_perm_not_found = 'Разрешение "{}" не востребовано'

    def __init__(self):
        self.partitions = defaultdict(set)  # Разделы системы
        self.groups = {}  # Группы разрешений
        self.permissions: Dict[Permission, str] = {}
        self.permission_dependencies = defaultdict(set)
        self.permission_rules = defaultdict(list)

    def _collect_partitions(self, permission_modules: Tuple[ModuleType, ...]):
        """Сбор информации о разделах системы.

        Разделами системы являются объединения групп разрешений.
        """
        self.partitions.clear()

        processed_groups = set()

        for module in permission_modules:
            partitions = getattr(module, 'partitions', None)
            if partitions is None:
                continue

            for title, perm_groups in partitions.items():
                for perm_group in perm_groups:
                    assert perm_group not in processed_groups, (
                        f'Группа разрешений "{perm_group}" уже '
                        f'закреплена за другим разделом системы.'
                    )
                    self.partitions[title].add(perm_group)
                    processed_groups.add(perm_group)

    def _collect_groups(self, permission_modules: Tuple[ModuleType, ...]):
        """Сбор информации о группах разрешений."""
        self.groups.clear()

        for module in permission_modules:
            groups = getattr(module, 'groups', None)
            if groups is None:
                continue

            for code, title in groups.items():
                assert code not in self.groups, (
                    f'Группа разрешений "{code}" ({title}) '
                    'уже описана в другом приложении.'
                )

                self.groups[code] = title

    def _collect_permissions(
        self,
        permissions_modules: Tuple[ModuleType, ...]
    ):
        """Сбор разрешений системы."""
        self.permissions.clear()

        # Сбор названий разрешений всей системы
        for viewset in _get_rbac_viewsets():
            for permission in chain.from_iterable(viewset.perm_map.values()):
                self.permissions[permission] = ''

        # Заполнение параметров разрешений
        for module in permissions_modules:
            for params in getattr(module, 'permissions', ()):
                if len(params) == 2:
                    permission, title = params
                else:
                    raise ValueError(
                        f'Некорректные параметры разрешения:  {repr(params)}'
                    )

                assert permission in self.permissions, (
                    self._msg_perm_not_found.format(permission)
                )

                self.permissions[permission] = (
                    self.permissions[permission] or title or ''
                )

    def _collect_dependencies(
        self,
        permissions_modules: Tuple[ModuleType, ...]
    ):
        """Сбор зависимостей между разрешениями."""
        self.permission_dependencies.clear()

        for module in permissions_modules:
            module_dependencies = getattr(module, 'dependencies', {})
            if callable(module_dependencies):
                module_dependencies = module_dependencies()

            for permission, dependencies in module_dependencies.items():
                assert permission in self.permissions, (
                    self._msg_perm_not_found.format(permission)
                )

                self.permission_dependencies[permission].update(dependencies)

    def _collect_rules(self, permissions_modules: Tuple[ModuleType, ...]):
        """Сбор обработчиков правил для разрешений системы."""
        self.permission_rules.clear()

        for module in permissions_modules:
            for permission, handlers in getattr(module, 'rules', {}).items():
                if not isinstance(handlers, Iterable):
                    handlers = (handlers,)

                for handler in handlers:
                    assert callable(handler), handler
                    self.permission_rules[permission].append(handler)

    def _push_permissions(self):
        """
        Обновление списка разрешений в хранилище основе разрешений системы.
        """
        # TODO: пропускать в миграциях
        self._backend.push_permissions()

    def get_dependent_permissions(
        self,
        permission: 'Permission',
        _result: Set = None
    ) -> Set[Permission]:
        """Возвращает разрешения, от которых зависит указанное разрешение."""
        if _result is None:
            primary_permission = permission
            _result = {permission}
        else:
            primary_permission = None

        for dependency in self.permission_dependencies[permission]:
            if dependency not in _result:
                _result.add(dependency)
                _result.update(
                    self.get_dependent_permissions(dependency, _result)
                )

        if primary_permission:
            _result.remove(primary_permission)

        return _result

    def init(self, push_permissions: bool = True):
        """Инициализация модуля контроля доступа.

        1. Загружает из приложений системы списки правил и разрешений. Их поиск
           осуществляется в модуле ``permissions``.
        2. Для каждого правила и разрешения создает/обновляет запись
            в хранилище.

        :param bool push_permissions: Определяет необходимость синхронизации
            прав доступа системы с хранилищем.
        """
        modules = tuple(_get_app_permissions_modules())

        # Сбор разрешений системы и зависимостей между ними
        self._collect_permissions(modules)
        self._collect_dependencies(modules)

        # Сбор обработчиков правил для разрешений системы
        self._collect_rules(modules)

        # Сбор групп разрешений и разделов системы
        self._collect_groups(modules)
        self._collect_partitions(modules)

        if push_permissions:
            self._push_permissions()

    @cached_property
    def _backend(self):
        backend_name = getattr(settings, 'RBAC_BACKEND', None) or (
            __name__.rpartition('.')[0] + '.backends.remote.RemoteBackend'
        )
        module_name, class_name = backend_name.rsplit('.', 1)

        try:
            module = import_module(module_name)
        except ImportError as e:
            raise ImproperlyConfigured(
                f'Не удалось импортировать бэкенд RBAC {module_name}: "{e}"'
            )

        try:
            backend_class = getattr(module, class_name)
        except AttributeError:
            raise ImproperlyConfigured(
                f'Модуль "{module}" не содержит бэкенд RBAC"{class_name}"'
            )
        else:
            backend = backend_class(self)

        return backend

    def has_access(self, viewset: 'GenericViewSet', request) -> bool:
        """Проверяет наличие у пользователя доступа (с учётом правил)."""
        return self._backend.has_access(viewset, request)

    def has_perm(self, user, permission: Permission) -> bool:
        """Проверяет наличие у пользователя разрешения (без учёта правил)."""
        return self._backend.has_perm(user, permission)


rbac = RBACManager()
