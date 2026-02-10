from typing import Optional
from rest_framework import serializers

class VenueResponse(serializers.Serializer):
    venue_id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True, max_length=255)
    address = serializers.CharField(read_only=True)
    capacity = serializers.IntegerField(read_only=True)
    contact_info = serializers.CharField(read_only=True, allow_blank=True)