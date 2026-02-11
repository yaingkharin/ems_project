from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models.category import Category
from app.models.venue import Venue


class Event(models.Model):
    """
    Represents an event in the system.
    """
    STATUS_CHOICES = [
        ('planned', _('Planned')),
        ('ongoing', _('Ongoing')),
        ('completed', _('Completed')),
    ]

    event_name = models.CharField(max_length=255, verbose_name=_('Event Name'))
    description = models.TextField(verbose_name=_('Description'))
    location = models.CharField(max_length=255, verbose_name=_('Location'))
    event_date = models.DateField(verbose_name=_('Event Date'))
    start_time = models.TimeField(verbose_name=_('Start Time'))
    end_time = models.TimeField(verbose_name=_('End Time'))
    organizer = models.CharField(max_length=255, verbose_name=_('Organizer'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='events', verbose_name=_('Category'))
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='events', verbose_name=_('Venue'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned', verbose_name=_('Status'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    def __str__(self):
        return self.event_name

    class Meta:
        db_table = "events"
        ordering = ['-created_at']
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
