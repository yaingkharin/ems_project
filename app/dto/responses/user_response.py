from typing import Optional
from rest_framework import serializers
from .role_response import RoleResponse # This will be updated later, but for now assuming it will also be a serializer

class UserResponse(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(read_only=True)
    role = RoleResponse(read_only=True) # Nested serializer, assuming RoleResponse becomes a serializer
    status = serializers.CharField(read_only=True)