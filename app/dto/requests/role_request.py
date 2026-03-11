from typing import Optional
from rest_framework import serializers
from app.dto.requests.pagination_request import PaginationRequest # new import

class CreateRoleRequest(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=255)
    display_name = serializers.CharField(required=False, allow_blank=True, max_length=255)
    status = serializers.BooleanField(required=False, default=True)

class UpdateRoleRequest(serializers.Serializer):
    name = serializers.CharField(required=False, max_length=255)
    display_name = serializers.CharField(required=False, allow_blank=True, max_length=255)
    status = serializers.BooleanField(required=False)

