from rest_framework import serializers


class CreateCheckinRequest(serializers.Serializer):
    """
    Serializer for creating a new check-in.
    """
    booking_id = serializers.IntegerField(required=False)
    ticket_code = serializers.CharField(max_length=255)
    status = serializers.ChoiceField(choices=['SUCCESS', 'ALREADY_USED', 'INVALID'], default='SUCCESS')


class UpdateCheckinRequest(serializers.Serializer):
    """
    Serializer for updating an existing check-in.
    """
    booking_id = serializers.IntegerField(required=False)
    ticket_code = serializers.CharField(max_length=255, required=False)
    status = serializers.ChoiceField(choices=['SUCCESS', 'ALREADY_USED', 'INVALID'], required=False)


class ValidateTicketRequest(serializers.Serializer):
    """
    Serializer for validating an event ticket by its code.
    """
    ticket_code = serializers.CharField(max_length=255)


class ConfirmCheckinRequest(serializers.Serializer):
    """
    Serializer for confirming a check-in.
    """
    ticket_code = serializers.CharField(max_length=255)
