from django.db import models
from django.utils import timezone
from app.models.booking import Booking


class EventTicket(models.Model):
    """
    Represents an event ticket for a booking.
    """
    STATUS_CHOICES = [
        ('USED', 'Used'),
        ('UNUSED', 'Unused'),
    ]

    id = models.AutoField(primary_key=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='event_tickets')
    ticket_code = models.CharField(max_length=255, unique=True)
    qr_code = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='UNUSED')
    
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ticket {self.ticket_code} for Booking {self.booking_id}"

    class Meta:
        db_table = "event_tickets"
        ordering = ['-created_at']