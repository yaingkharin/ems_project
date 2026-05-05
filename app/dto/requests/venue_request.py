
from rest_framework import serializers


class CreateVenueRequest(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=255, trim_whitespace=True)
    address = serializers.CharField(required=True, trim_whitespace=True)
    contact_info = serializers.CharField(required=False, allow_blank=True, allow_null=True, trim_whitespace=True)

