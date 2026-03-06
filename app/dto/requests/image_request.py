from rest_framework import serializers


class CreateImageRequest(serializers.Serializer):
    """
    Serializer for creating a new image.
    """
    url = serializers.CharField(max_length=255)


class UpdateImageRequest(serializers.Serializer):
    """
    Serializer for updating an existing image.
    """
    url = serializers.CharField(max_length=255, required=False)
