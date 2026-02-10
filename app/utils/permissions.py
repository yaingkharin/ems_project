# api/utils/permissions.py
from django.contrib.auth import get_user_model
from app.models.role_permission import RolePermission
from functools import wraps # Still needed for other decorators if any
from django.http import HttpResponseForbidden # Still needed if CheckPermission or has_permission could return it
from rest_framework import permissions # For DRF permission class

User = get_user_model()

def has_permission(user: User, permission_name: str) -> bool:
    """
    Checks if the given user has the specified permission.
    """
    if not user or not user.is_authenticated:
        return False

    # Superusers bypass all permission checks
    if user.is_superuser:
        return True
    
    if user.role:
        # Check if the user's role has the 'all_permissions' permission
        if RolePermission.objects.filter(role=user.role, permission__name='all_permissions').exists():
            return True

        # Check if the user's role has the specific permission
        return RolePermission.objects.filter(
            role=user.role,
            permission__name=permission_name
        ).exists()
    
    return False

class CheckPermission(permissions.BasePermission):

    """

    Custom DRF permission class to check if a user has a specific permission.

    The view must define a `method_permissions` dictionary mapping HTTP methods to required permissions.

    """

    def has_permission(self, request, view):

        if not request.user or not request.user.is_authenticated:

            return False

        # Get method-specific permissions from the view

        method_permissions = getattr(view, 'method_permissions', {})

        # Determine the required permission for the current HTTP method

        # DRF's request.method is uppercase (e.g., 'GET', 'POST')

        required_permission = method_permissions.get(request.method)

        if not required_permission:

            # If no specific permission is required for this method, allow access.

            # This can happen if a method is intentionally left open or misconfigured.

            return True

        return has_permission(request.user, required_permission)