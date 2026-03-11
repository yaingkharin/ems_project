from rest_framework import serializers
from app.dto.responses.booking_response import BookingResponse
from app.dto.responses.user_response import UserResponse


class InvoiceResponse(serializers.ModelSerializer):
    """
    Serializer for the Invoice model, including related Booking and User details.
    """
    booking = BookingResponse(read_only=True)
    user = UserResponse(read_only=True)

    class Meta:
        from app.models.invoice import Invoice
        model = Invoice
        fields = [
            'id', 'invoice_no', 'booking', 'user', 'total_amount', 'payment_method',
            'issue_date', 'qr_code', 'created_at', 'updated_at'
        ]
