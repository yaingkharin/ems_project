from rest_framework import serializers


class CreateCheckinRequest(serializers.Serializer):
    """
    Serializer for creating a new check-in.
    """
    booking_id = serializers.IntegerField()
    ticket_code = serializers.CharField(max_length=255)
    status = serializers.ChoiceField(choices=['pending', 'checked_in', 'cancelled'], default='pending')


class UpdateCheckinRequest(serializers.Serializer):
    """
    Serializer for updating an existing check-in.
    """
    booking_id = serializers.IntegerField(required=False)
    ticket_code = serializers.CharField(max_length=255, required=False)
    status = serializers.ChoiceField(choices=['pending', 'checked_in', 'cancelled'], required=False)
