from django.db import models
from app.models.user import User


class UserProfile(models.Model):
    """
    Represents a user's profile with additional information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    address = models.TextField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=50, blank=True, null=True)
    preferences = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.email}"

    class Meta:
        db_table = "user_profiles"
