from typing import Optional
from rest_framework import serializers
from .role_response import RoleResponse # This will be updated later, but for now assuming it will also be a serializer

class UserResponse(serializers.ModelSerializer):
    role = RoleResponse(read_only=True) # Nested serializer, assuming RoleResponse becomes a serializer

    class Meta:
        from app.models.user import User
        model = User
        fields = ['id', 'email', 'role', 'status']