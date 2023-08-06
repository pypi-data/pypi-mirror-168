from typing import Iterable
from typing import NamedTuple
from typing import Optional
from typing import Tuple
from typing import TypedDict


class PermissionGroup(NamedTuple):

    """Структура группы разрешений."""

    namespace: str
    resource: str


class Permission(NamedTuple):

    """Структура разрешения."""

    namespace: str
    resource: str
    action: str
    scope: Optional[str] = None


class TokenPermissionDict(TypedDict):

    """Структура разрешения передаваемого в составе токена."""

    resource_set_id: str
    """Объект доступа, например `auth:role`"""
    scopes: Iterable[str]
    """Операции на которые пользователю выдан доступ, например `read`"""
    exp: int
    """Временная метка после которой набор прав должен быть обновлён"""


class TPermMapDict(TypedDict):

    """Структура сопоставления разрешений с действиями во ViewSet'е."""

    create: Tuple[Permission, ...]
    retrieve: Tuple[Permission, ...]
    update: Tuple[Permission, ...]
    partial_update: Tuple[Permission, ...]
    list: Tuple[Permission, ...]
    destroy: Tuple[Permission, ...]
