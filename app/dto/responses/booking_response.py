from rest_framework import serializers
from .common_response import CustomerCustomResponse, EventCustomResponse, TicketCustomResponse


class BookingResponse(serializers.ModelSerializer):
    """
    Custom booking response with only essential data from related models.
    """
    customer = CustomerCustomResponse(read_only=True)
    event = EventCustomResponse(read_only=True)
    ticket = TicketCustomResponse(read_only=True)
    payment_method = serializers.SerializerMethodField()
    is_checked_in = serializers.SerializerMethodField()
    checkin_history = serializers.SerializerMethodField()

    class Meta:
        from app.models.booking import Booking
        model = Booking
        fields = [
            'id', 'customer', 'event', 'ticket', 'quantity', 'total_amount', 
            'status', 'booking_date', 'payment_method', 'is_checked_in',
            'checkin_history', 'created_at', 'updated_at'
        ]

    def get_payment_method(self, obj):
        # Taking the most recent payment's method
        payment = obj.payments.order_by('-created_at').first()
        return payment.payment_method.upper() if payment and payment.payment_method else "N/A"

    def get_is_checked_in(self, obj):
        # Check if there are any successful check-ins for this booking
        try:
            return obj.checkins.filter(status__in=['SUCCESS', 'checked_in', 'USED']).exists()
        except:
            return False

    def get_checkin_history(self, obj):
        # Return all check-in records for this booking
        try:
            return list(obj.checkins.all().values('id', 'ticket_code', 'checkin_time', 'status'))
        except:
            return []
