from typing import Optional
from rest_framework import serializers

class CategoryResponse(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        category_name = serializers.CharField(read_only=True, max_length=150)
        description = serializers.CharField(read_only=True, allow_blank=True, allow_null=True)