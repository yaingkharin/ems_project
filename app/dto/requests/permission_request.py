from typing import Optional
from rest_framework import serializers
from app.dto.requests.pagination_request import PaginationRequest # new import

class CreatePermissionRequest(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=255)
    display_name = serializers.CharField(required=False, allow_blank=True, max_length=255)
    group = serializers.CharField(required=False, allow_blank=True, max_length=255)
    sort = serializers.IntegerField(required=False, default=0)
    status = serializers.BooleanField(required=False, default=True)

class UpdatePermissionRequest(serializers.Serializer):
    name = serializers.CharField(required=False, max_length=255)
    display_name = serializers.CharField(required=False, allow_blank=True, max_length=255)
    group = serializers.CharField(required=False, allow_blank=True, max_length=255)
    sort = serializers.IntegerField(required=False)
    status = serializers.BooleanField(required=False)

