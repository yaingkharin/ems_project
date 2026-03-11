from django.db import models
from django.utils import timezone

class Venue(models.Model):
    venue_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.TextField()
    capacity = models.IntegerField()
    contact_info = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    # Custom managers for soft delete
    objects = models.Manager()  # Default manager
    active_objects = models.Manager()  # Can be customized if needed

    def __str__(self):
        return self.name
    
    class Meta:
        db_table ="venue"