
from rest_framework import serializers


class CreateCategoryRequest(serializers.Serializer):
    category_name = serializers.CharField(max_length=150)
    description = serializers.CharField(max_length=150,blank=True, null=True)

class UpdateCategoryRequest(serializers.Serializer):
    category_name = serializers.CharField(max_length=150)
    description = serializers.CharField(max_length=150,blank=True, null=True)
