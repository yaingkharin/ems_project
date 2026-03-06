from typing import Optional
from rest_framework import serializers
from .role_response import RoleResponse # Now a serializer
from .permission_response import PermissionResponse # Now a serializer

class RolePermissionResponse(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    role = RoleResponse(read_only=True) # Nested serializer
    permission = PermissionResponse(read_only=True) # Nested serializer