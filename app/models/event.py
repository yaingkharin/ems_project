import datetime

from django.conf import settings
from django.db import models
from django.utils import timezone

from app.models.category import Category
from app.models.venue import Venue


class Event(models.Model):
    """
    Represents an event in the system.
    """
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    event_name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    event_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    organizer = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='events')
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='events')
    image = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_computed_status(self) -> str:
        """
        Dynamically compute the event status based on current date/time.

        Rules:
          - 'cancelled' stored in the DB is always honoured (manual override).
          - today < event_date                              => 'upcoming'
          - today == event_date and within start/end time  => 'ongoing'
          - today > event_date OR end_time has passed      => 'completed'
        """
        # Honour manual cancellation
        if self.status == 'cancelled':
            return 'cancelled'

        now_local = timezone.localtime(timezone.now())
        today = now_local.date()
        current_time = now_local.time()

        if today < self.event_date:
            return 'upcoming'

        if today == self.event_date:
            if self.start_time <= current_time <= self.end_time:
                return 'ongoing'
            elif current_time < self.start_time:
                return 'upcoming'
            else:
                # current_time > end_time
                return 'completed'

        # today > event_date
        return 'completed'

    def __str__(self):
        return self.event_name

    class Meta:
        db_table = "events"
        ordering = ['-created_at']
