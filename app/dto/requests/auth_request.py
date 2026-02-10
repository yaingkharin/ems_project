from rest_framework import serializers

class LoginRequestDTO(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)