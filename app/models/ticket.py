from django.db import models
from app.models.event import Event


class Ticket(models.Model):
    """
    Represents a ticket for an event.
    """
    TICKET_TYPE_CHOICES = [
        ('VIP', 'VIP'),
        ('Premium', 'Premium'),
        ('Standard', 'Standard'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    ticket_type = models.CharField(max_length=50, choices=TICKET_TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    sold = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.ticket_type} - {self.event.event_name}"

    class Meta:
        db_table = "tickets"
        ordering = ['-created_at']