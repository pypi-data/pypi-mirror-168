from typing import TYPE_CHECKING

from rest_framework.permissions import BasePermission

from librbac.manager import rbac


class HasAccess(BasePermission):

    def has_permission(self, request, view):
        """Проверяет наличие доступа."""
        from librbac.drf.viewsets import RBACMixin
        if not isinstance(view, RBACMixin):
            return True
        return rbac.has_access(view, request)
