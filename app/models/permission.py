from django.db import models

class Permission(models.Model):
    name = models.CharField(max_length=100, unique=True)
    display_name = models.CharField(max_length=100, blank=True, null=True)
    group = models.CharField(max_length=100, blank=True, null=True)
    sort = models.IntegerField(default=0)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'permissions'
