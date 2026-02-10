from django.db import models
from app.models.booking import Booking


class Checkin(models.Model):
    """
    Represents a check-in record for a booking.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('checked_in', 'Checked In'),
        ('cancelled', 'Cancelled'),
    ]

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='checkins')
    ticket_code = models.CharField(max_length=255)
    checkin_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Check-in for Booking {self.booking.id} - {self.ticket_code}"

    class Meta:
        db_table = "checkins"
        ordering = ['-checkin_time']