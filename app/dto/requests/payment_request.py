from rest_framework import serializers


class CreatePaymentRequest(serializers.Serializer):
    """
    Serializer for creating a new payment.
    """
    booking_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    method = serializers.CharField(max_length=255)
    transaction_ref = serializers.CharField(max_length=255, allow_blank=True, required=False)
    status = serializers.ChoiceField(choices=['pending', 'paid', 'failed'], default='pending')


class UpdatePaymentRequest(serializers.Serializer):
    """
    Serializer for updating an existing payment.
    """
    booking_id = serializers.IntegerField(required=False)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    method = serializers.CharField(max_length=255, required=False)
    transaction_ref = serializers.CharField(max_length=255, allow_blank=True, required=False)
    status = serializers.ChoiceField(choices=['pending', 'paid', 'failed'], required=False)
