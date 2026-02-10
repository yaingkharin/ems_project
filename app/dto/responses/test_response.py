from typing import Optional
from rest_framework import serializers

class TestResponse(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    test_name = serializers.CharField(read_only=True ,max_length=100)
    description = serializers.CharField(read_only=True ,allow_blank=True)
    status = serializers.BooleanField(read_only=True)