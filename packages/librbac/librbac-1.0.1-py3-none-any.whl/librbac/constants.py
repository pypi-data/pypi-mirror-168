TOPIC_NAMESPACE = 'edu'
TOPIC_SERVICE = 'rbac'

OBJ_PERMISSION = 'permission'
OBJ_ROLE = 'role'

# наименование топика в который публикуется событие "разрешение выгружено".
TOPICNAME__PERMISSION_PUSHED = (
    f'{TOPIC_NAMESPACE}.{TOPIC_SERVICE}.{OBJ_PERMISSION}.pushed'
)
# наименование топика в который публикуется событие "разрешение загружено".
TOPICNAME__PERMISSION_LOADED = (
    f'{TOPIC_NAMESPACE}.{TOPIC_SERVICE}.{OBJ_PERMISSION}.loaded'
)

# наименование топика в который публикуется событие "роль создана".
TOPICNAME__ROLE_CREATED = (
    f'{TOPIC_NAMESPACE}.{TOPIC_SERVICE}.{OBJ_ROLE}.created'
)
# наименование топика в который публикуется событие "роль обновлена".
TOPICNAME__ROLE_UPDATED = (
    f'{TOPIC_NAMESPACE}.{TOPIC_SERVICE}.{OBJ_ROLE}.updated'
)
# наименование топика в который публикуется событие "роль удалена".
TOPICNAME__ROLE_DELETED = (
    f'{TOPIC_NAMESPACE}.{TOPIC_SERVICE}.{OBJ_ROLE}.deleted'
)
