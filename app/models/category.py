from django.db import models

class Category(models.Model):
    category_name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.category_name
    
    class Meta:
        db_table ="category"