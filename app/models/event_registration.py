from django.db import models
from django.utils import timezone
from app.models.user import User
from app.models.event import Event


class EventRegistration(models.Model):
    """
    Represents a user's registration for an event.
    """
    STATUS_CHOICES = [
        ('registered', 'Registered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_registrations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='registered')
    registered_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} registered for {self.event.event_name}"

    class Meta:
        db_table = "event_registrations"
        ordering = ['-registered_at']
        unique_together = ('user', 'event')