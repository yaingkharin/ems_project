from rest_framework import serializers
from app.models.image import Image


class ImageResponse(serializers.ModelSerializer):
    """
    Serializer for the Image model.
    """

    class Meta:
        model = Image
        fields = ['id', 'url']
