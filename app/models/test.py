from django.db import models

class Test(models.Model):
    test_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.test_name