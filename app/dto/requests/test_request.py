from typing import Optional
from rest_framework import serializers
from app.dto.requests.pagination_request import PaginationRequest # new import

class CreateTestRequest(serializers.Serializer):
    test_name = serializers.CharField(required=True, max_length=100)
    description = serializers.CharField(required=False, allow_blank=True)
    status = serializers.BooleanField(required=False, default=True)