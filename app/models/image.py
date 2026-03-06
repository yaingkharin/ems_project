from django.db import models


class Image(models.Model):
    """
    Represents an image in the system.
    """
    url = models.CharField(max_length=255)

    def __str__(self):
        return self.url

    class Meta:
        db_table = "image"
