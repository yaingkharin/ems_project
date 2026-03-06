from rest_framework import serializers
from app.dto.responses.user_response import UserResponse # Import the UserResponseDTO

class LoginResponseDTO(serializers.Serializer):
    accessToken = serializers.CharField()
    refreshToken = serializers.CharField()