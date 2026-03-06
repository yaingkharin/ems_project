from rest_framework import serializers
from app.dto.responses.user_response import UserResponse


class UserProfileResponse(serializers.ModelSerializer):
    """
    Serializer for the UserProfile model, including related User details.
    """
    user = UserResponse(read_only=True)

    class Meta:
        from app.models.user_profile import UserProfile
        model = UserProfile
        fields = [
            'id', 'user', 'address', 'dob', 'gender', 'preferences',
            'created_at', 'updated_at'
        ]
