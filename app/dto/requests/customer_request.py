from rest_framework import serializers

class CreateCustomerRequest(serializers.Serializer):
    first_name = serializers.CharField(max_length=255, required=False)
    last_name = serializers.CharField(max_length=255, required=False)
    email = serializers.EmailField()
    picture = serializers.URLField(required=False)

class UpdateCustomerRequest(serializers.Serializer):
    first_name = serializers.CharField(max_length=255, required=False)
    last_name = serializers.CharField(max_length=255, required=False)
    email = serializers.EmailField(required=False)
    picture = serializers.URLField(required=False)
    status = serializers.BooleanField(required=False)
