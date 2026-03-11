from rest_framework import serializers


class CreateAuthenticationRequest(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=255)
    password = serializers.CharField(required=True, write_only=True)


class UpdateAuthenticationRequest(serializers.Serializer):
    username = serializers.CharField(required=False, max_length=255)
    password = serializers.CharField(required=False, write_only=True)


class LoginRequestDTO(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)