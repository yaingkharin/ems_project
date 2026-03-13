from rest_framework import serializers


class CreatePaymentRequest(serializers.Serializer):
    """
    Serializer for creating a new payment.
    """
    booking_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    payment_method = serializers.CharField(max_length=255)
    qr_method = serializers.CharField(max_length=255, required=False)
    currency = serializers.CharField(max_length=255, required=False)
    status = serializers.ChoiceField(choices=['pending', 'completed', 'failed'], default='pending')


class UpdatePaymentRequest(serializers.Serializer):
    """
    Serializer for updating an existing payment.
    """
    booking_id = serializers.IntegerField(required=False)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    payment_method = serializers.CharField(max_length=255, required=False)
    qr_method = serializers.CharField(max_length=255, required=False)
    currency = serializers.CharField(max_length=255, required=False)
    status = serializers.ChoiceField(choices=['pending', 'completed', 'failed'], required=False)
