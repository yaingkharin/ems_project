from typing import Optional
from rest_framework import serializers

class PermissionResponse(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    display_name = serializers.CharField(read_only=True)
    group = serializers.CharField(read_only=True)
    sort = serializers.IntegerField(read_only=True)
    status = serializers.BooleanField(read_only=True)