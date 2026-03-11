from django.db import models
from django.utils import timezone

class Category(models.Model):
    category_name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return self.category_name
    
    class Meta:
        db_table ="category"