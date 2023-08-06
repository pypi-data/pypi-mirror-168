from typing import TYPE_CHECKING
from typing import Optional
from typing import Union

from explicit.domain.model import Unset
from explicit.domain.model import unset
from explicit.messagebus.events import Event


if TYPE_CHECKING:
    from dataclasses import dataclass  # noqa
else:
    from pydantic.dataclasses import dataclass  # noqa


@dataclass
class PermissionPushed(Event):

    namespace: Union[str, Unset] = unset
    resource: Union[str, Unset] = unset
    action: Union[str, Unset] = unset
    scope: Optional[str] = None
    title: Union[str, Unset] = unset
    module: Union[str, Unset] = unset
