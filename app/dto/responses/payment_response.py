from rest_framework import serializers
from app.dto.responses.booking_response import BookingResponse
from app.models.payment import Payment


class PaymentResponse(serializers.ModelSerializer):
    """
    Serializer for the Payment model, including related Booking details.
    """
    booking = BookingResponse(read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id', 'booking', 'amount', 'payment_method', 'qr_method', 'currency',
            'merchant_name', 'merchant_city', 'description',
            'status', 'qr', 'md5', 'bakongHash',
            'toAccountId', 'fromAccountId', 'paid', 'paid_at', 'expire_at',
            'deep_link', 'deep_link_web',
            'external_ref', 'created_at', 'updated_at'
        ]