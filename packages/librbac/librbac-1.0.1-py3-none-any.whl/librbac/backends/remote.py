from typing import TYPE_CHECKING
import json

from pydantic.json import pydantic_encoder as encoder

from librbac.backends.base import BackendBase
from librbac.constants import TOPICNAME__PERMISSION_PUSHED


if TYPE_CHECKING:
    from librbac.events import PermissionPushed


class RemoteBackend(BackendBase):

    """Бэкенд RBAC с публикацией разрешений в межсервисную шину."""

    def push_permission(self, event: 'PermissionPushed'):
        from librbac.config import rbac_config
        rbac_config.adapter.publish(
            TOPICNAME__PERMISSION_PUSHED,
            json.dumps(event, default=encoder)
        )

