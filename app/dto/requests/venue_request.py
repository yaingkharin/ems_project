
from rest_framework import serializers


class CreateVenueRequest(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=255)
    address = serializers.CharField(required=True)
    capacity = serializers.IntegerField(required=True)
    contact_info = serializers.CharField(required=False, allow_blank=True)
