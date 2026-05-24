from rest_framework.permissions import BasePermission
from .models import ROLE_RANK


class IsAgencyMember(BasePermission):
    """User must have an active Membership (any role) for the agency in JWT context."""

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        if getattr(request.user, "is_staff_immoview", False):
            return True
        membership = getattr(request, "active_membership", None)
        return membership is not None and membership.is_active


class _RoleRequired(BasePermission):
    min_role: str = "viewer"

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        if getattr(request.user, "is_staff_immoview", False):
            return True
        membership = getattr(request, "active_membership", None)
        if not membership:
            return False
        return ROLE_RANK.get(membership.role, -1) >= ROLE_RANK.get(self.min_role, 99)


def require_role(min_role: str) -> type[_RoleRequired]:
    return type(f"Require_{min_role.capitalize()}", (_RoleRequired,), {"min_role": min_role})


OwnerRequired = require_role("owner")
AdminRequired = require_role("admin")
AgentRequired = require_role("agent")
ViewerRequired = require_role("viewer")
