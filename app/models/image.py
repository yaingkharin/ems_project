from django.db import models
from django.utils import timezone


class Image(models.Model):
    """
    Represents an image in the system.
    """
    url = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.url

    class Meta:
        db_table = "image"
