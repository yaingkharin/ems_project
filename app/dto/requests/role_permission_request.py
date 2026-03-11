from rest_framework import serializers
from app.dto.requests.pagination_request import PaginationRequest # new import

class CreateRolePermissionRequest(serializers.Serializer):
    role_id = serializers.IntegerField(required=True)
    permission_id = serializers.IntegerField(required=True)

class UpdateRolePermissionRequest(serializers.Serializer):
    role_id = serializers.IntegerField(required=False)
    permission_id = serializers.IntegerField(required=False)
