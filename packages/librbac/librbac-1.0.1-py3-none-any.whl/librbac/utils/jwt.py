from typing import Generator
from typing import Iterable
import json

from jwcrypto import jwt

from librbac.types import Permission
from librbac.types import TokenPermissionDict


def get_jwt_permissions(
    perms: Iterable[TokenPermissionDict]
) -> Generator[Permission, None, None]:
    """Генератор разрешений пользователя.

    Преобразует разрешения словаря в объект разрешений.
    Возвращает генератор объектов разрешений.
    """
    for perm in perms:
        namespace, resource = perm['resource_set_id'].split(':')
        for action_scope in perm['scopes']:
            action, scope = (
                action_scope.split(':')
                if ':' in action_scope
                else (action_scope, None)
            )
            yield Permission(namespace, resource, action, scope)


def set_current_user_permissions(token: str, request):
    """
    Извлекает из токена и присваивает пользователю информацию о разрешениях.
    """
    jwt_obj = jwt.JWT(jwt=token, key=request.client.jwk_key)
    claims = json.loads(jwt_obj.claims)
    perms: Iterable[TokenPermissionDict] = claims.get('permissions', [])
    request.user.permissions = list(get_jwt_permissions(perms))
