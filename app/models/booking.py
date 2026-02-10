from django.db import models
from app.models.user import User
from app.models.event import Event
from app.models.ticket import Ticket


class Booking(models.Model):
    """
    Represents a booking made by a user for an event.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='bookings')
    quantity = models.IntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    booking_date = models.DateTimeField(auto_now_add=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking {self.id} by {self.user.email} for {self.event.event_name}"

    class Meta:
        db_table = "bookings"
        ordering = ['-booking_date']