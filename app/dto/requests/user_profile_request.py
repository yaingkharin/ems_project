from rest_framework import serializers


class CreateUserProfileRequest(serializers.Serializer):
    """
    Serializer for creating a new user profile.
    """
    user_id = serializers.IntegerField()
    address = serializers.CharField(allow_blank=True, required=False)
    dob = serializers.DateField(required=False)
    gender = serializers.CharField(max_length=50, allow_blank=True, required=False)
    preferences = serializers.CharField(allow_blank=True, required=False)


class UpdateUserProfileRequest(serializers.Serializer):
    """
    Serializer for updating an existing user profile.
    """
    address = serializers.CharField(allow_blank=True, required=False)
    dob = serializers.DateField(required=False)
    gender = serializers.CharField(max_length=50, allow_blank=True, required=False)
    preferences = serializers.CharField(allow_blank=True, required=False)
