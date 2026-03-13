from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True)
    picture = models.URLField(max_length=500, null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True)
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True, blank=True, related_name='customers')

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    class Meta:
        db_table = 'customer'
