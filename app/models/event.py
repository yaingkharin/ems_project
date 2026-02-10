from django.db import models

from app.models.category import Category
from app.models.venue import Venue


class Event(models.Model):
    """
    Represents an event in the system.
    """
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
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
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.event_name

    class Meta:
        db_table = "events"
        ordering = ['-created_at']
