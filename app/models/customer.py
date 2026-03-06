from django.db import models
from django.utils import timezone


class Customer(models.Model):
    """
    Represents a customer in the system.
    """
    username = models.CharField(max_length=255)
    gmail = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = "customer"
