from rest_framework import serializers
from app.dto.responses.booking_response import BookingResponse


class PaymentResponse(serializers.ModelSerializer):
    """
    Serializer for the Payment model, including related Booking details.
    """
    booking = BookingResponse(read_only=True)

    class Meta:
        from app.models.payment import Payment
        model = Payment
        fields = [
            'id', 'booking', 'amount', 'method', 'transaction_ref', 'status', 'payment_date',
            'created_at', 'updated_at'
        ]