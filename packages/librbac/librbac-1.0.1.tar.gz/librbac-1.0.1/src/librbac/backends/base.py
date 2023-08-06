from abc import ABCMeta
from abc import abstractmethod
from typing import TYPE_CHECKING
from typing import Generator
from typing import Tuple

from librbac.events import PermissionPushed
from librbac.manager import RBACManager
from librbac.types import Permission
from librbac.types import PermissionGroup


if TYPE_CHECKING:
    from rest_framework.viewsets import GenericViewSet


class BackendBase(metaclass=ABCMeta):

    """Базовый класс для бэкендов RBAC."""

    def __init__(self, manager):
        self._manager: RBACManager = manager

    def _need_check_access(self, viewset: 'GenericViewSet') -> bool:
        """Возвращает True, если ``viewset`` предполагает проверку доступа."""
        result = False
        if perm_map := getattr(viewset, 'perm_map'):
            result = viewset.action in perm_map
        return result

    def _get_current_user(self, request):
        """Возвращает текущего пользователя."""
        return request.user

    def _get_user_permissions(self, user) -> Tuple['Permission', ...]:
        """Возвращает все доступные пользователю разрешения."""
        return getattr(user, 'permissions', ())

    def _get_viewset_permissions(
        self,
        viewset: 'GenericViewSet'
    ) -> Tuple[Permission]:
        """Возвращает имена разрешений ViewSet'а."""
        return viewset.perm_map.get(viewset.action, ())

    def _check_permission(
        self,
        permission: 'Permission',
        viewset: 'GenericViewSet',
        request,
        user,
    ):
        """Проверяет возможность предоставления доступа.

        Если для указанного разрешения определены правила, то выполняет их
        проверку.
        """
        if permission in self._manager.permission_rules:
            for handler in self._manager.permission_rules[permission]:
                if handler(viewset, request, user):
                    result = True
                    break
            else:
                result = None
        else:
            # Для разрешения не определено правил, значит достаточно
            # только наличия у пользователя разрешения как такового.
            result = True

        return result

    def _get_push_events(self) -> Generator[PermissionPushed, None, None]:
        """Генерирует события для обновления разрешений в хранилище."""
        module_perm_group_mapping = {
            perm_group: module
            for module, perm_groups in self._manager.partitions.items()
            for perm_group in perm_groups
        }
        for permission, title in self._manager.permissions.items():
            yield PermissionPushed(
                namespace=permission.namespace,
                resource=permission.resource,
                action=permission.action,
                scope=permission.scope,
                title=title,
                module=module_perm_group_mapping[
                    PermissionGroup(permission.namespace, permission.resource)
                ],
            )

    @abstractmethod
    def push_permission(self, event: PermissionPushed):
        """Обновляет одно разрешение в хранилище."""

    def push_permissions(self):
        """
        Обновление списка разрешений в хранилище основе разрешений системы.
        """
        for event in self._get_push_events():
            self.push_permission(event)

    def has_access(self, viewset: 'GenericViewSet', request) -> bool:
        """
        Проверяет наличие у текущего пользователя доступа (включая правила).
        """
        if not self._need_check_access(viewset):
            return True

        user = self._get_current_user(request)
        if user is None:
            return False

        return any(
            self._check_permission(permission, viewset, request, user)
            for permission in self._get_user_permissions(user)
            if permission in self._get_viewset_permissions(viewset)
        )

    def has_perm(self, user, permission: 'Permission') -> bool:
        """Проверяет наличие у пользователя разрешения."""
        return permission in self._get_user_permissions(user)
