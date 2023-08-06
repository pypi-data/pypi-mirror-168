from dataclasses import dataclass
from typing import TYPE_CHECKING
from typing import Tuple
from typing import Union
from uuid import UUID


if TYPE_CHECKING:
    from librbac.types import Permission


@dataclass
class OIDCUser:
    pk: Union[str, UUID]
    aud: str
    client_id: str
    exp: int
    iat: int
    iss: str
    sub: Union[str, UUID]
    uid: Union[str, UUID]
    permissions: Tuple['Permission']

    # пользователь по-умолчанию считается аутентифицированным
    is_authenticated = True


def get_user_from_token(request, id_token) -> OIDCUser:
    """Возвращает объект пользователя с разрешениями."""
    from librbac.utils.jwt import get_jwt_permissions

    token_data = {**id_token, 'pk': id_token['uid']}
    permissions = tuple(get_jwt_permissions(token_data.pop('permissions')))
    return OIDCUser(**token_data, permissions=permissions)
