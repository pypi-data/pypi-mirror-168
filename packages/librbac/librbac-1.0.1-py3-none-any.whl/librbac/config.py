from abc import ABC
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from explicit.contrib.adapters.messaging.kafka import Adapter
    from explicit.messagebus import MessageBus


class IConfig(ABC):
    """Конфигурация модуля управления доступом на основе ролей."""

    bus: 'MessageBus'
    """Внутренняя шина сервиса."""

    adapter: 'Adapter'
    """Адаптер к kafka"""


rbac_config: IConfig
