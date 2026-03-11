from typing import Optional
from rest_framework import serializers
from app.dto.requests.pagination_request import PaginationRequest # new import

class CreateUserRequest(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    role_id = serializers.IntegerField(required=False, allow_null=True)
    status = serializers.CharField(required=False, default='active')

class UpdateUserRequest(serializers.Serializer):
    email = serializers.EmailField(required=False)
    password = serializers.CharField(required=False, write_only=True)
    role_id = serializers.IntegerField(required=False, allow_null=True)
    status = serializers.CharField(required=False)

