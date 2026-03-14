from django.db import models
from django.utils import timezone
from app.models.booking import Booking


class Checkin(models.Model):
    """
    Represents a check-in record for a booking.
    """
    STATUS_CHOICES = [
        ('checked_in', 'Checked In'),
        ('not_checked', 'Not Checked'),
    ]

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='checkins')
    ticket_code = models.CharField(max_length=255)
    checkin_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_checked')
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Check-in for Booking {self.booking.id} - {self.ticket_code}"

    class Meta:
        db_table = "checkins"
        ordering = ['-checkin_time']