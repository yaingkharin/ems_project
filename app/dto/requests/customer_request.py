from rest_framework import serializers


class CreateCustomerRequest(serializers.Serializer):
    """
    Serializer for creating a new customer.
    """
    username = serializers.CharField(max_length=255)
    gmail = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)


class UpdateCustomerRequest(serializers.Serializer):
    """
    Serializer for updating an existing customer.
    """
    username = serializers.CharField(max_length=255, required=False)
    gmail = serializers.CharField(max_length=255, required=False)
    password = serializers.CharField(max_length=255, required=False)
