from rest_framework import serializers
from app.models.booking import Booking
from app.models.event import Event
from app.models.event_ticket import EventTicket

class EventBookingReportItemSerializer(serializers.ModelSerializer):
    booking_id = serializers.IntegerField(source='id')
    event_name = serializers.CharField(source='event.event_name', read_only=True)
    customer_name = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    booking_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    quantity = serializers.IntegerField()
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    payment_method = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = [
            'booking_id', 'event_name', 'customer_name', 'username', 
            'booking_date', 'quantity', 'total_amount', 'payment_method', 'status'
        ]

    def get_customer_name(self, obj):
        if obj.customer:
            first = obj.customer.first_name or ""
            last = obj.customer.last_name or ""
            return f"{first} {last}".strip() or obj.customer.email
        return "N/A"

    def get_username(self, obj):
        if obj.customer and obj.customer.email:
            return obj.customer.email.split('@')[0]
        return "N/A"

    def get_payment_method(self, obj):
        # Taking the most recent payment's method
        payment = obj.payments.order_by('-created_at').first()
        return payment.payment_method.upper() if payment and payment.payment_method else "N/A"

    def get_status(self, obj):
        payment = obj.payments.order_by('-created_at').first()
        if payment and payment.status == 'completed':
            return 'Confirmed'
        return 'Pending'

class CheckInReportItemSerializer(serializers.ModelSerializer):
    ticket_code = serializers.CharField()
    event_name = serializers.CharField(source='booking.event.event_name', read_only=True)
    customer_name = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    booking_date = serializers.DateTimeField(source='booking.booking_date', format="%Y-%m-%d %H:%M:%S", read_only=True)
    status = serializers.CharField()

    class Meta:
        model = EventTicket
        fields = [
            'booking_id', 'ticket_code', 'event_name', 'customer_name', 'username', 
            'booking_date', 'status'
        ]

    def get_customer_name(self, obj):
        customer = obj.booking.customer
        if customer:
            first = customer.first_name or ""
            last = customer.last_name or ""
            return f"{first} {last}".strip() or customer.email
        return "N/A"

    def get_username(self, obj):
        customer = obj.booking.customer
        if customer and customer.email:
            return customer.email.split('@')[0]
        return "N/A"
