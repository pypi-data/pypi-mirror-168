from importlib import import_module
from inspect import currentframe

from django.core.management import ManagementUtility


def is_in_management_command() -> bool:
    """
    Возвращает True, если код выполняется в рамках миграций Django.
    """
    from django.core.management import ManagementUtility

    def is_in_command(command):
        frame = currentframe()
        while frame:
            if 'self' in frame.f_locals:
                self_object = frame.f_locals['self']
                if isinstance(self_object, command):
                    return True

                if isinstance(self_object, ManagementUtility):
                    # Срабатывает при использовании функции в AppConfig
                    if 'subcommand' in frame.f_locals:
                        subcommand = frame.f_locals['subcommand']
                        return subcommand in ['migrate', 'test']

            frame = frame.f_back

    modules = (
        'django.core.management.commands.migrate',
        'django.core.management.commands.makemigrations',
        'django.core.management.commands.sqlmigrate',
        'django.core.management.commands.showmigrations',
        'django.core.management.commands.test',
    )

    for module_name in modules:
        if is_in_command(import_module(module_name).Command):  # type: ignore
            return True

    return False
