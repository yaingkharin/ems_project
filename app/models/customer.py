from django.db import models


class Customer(models.Model):
    """
    Represents a customer in the system.
    """
    username = models.CharField(max_length=255)
    gmail = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username

    class Meta:
        db_table = "customer"
