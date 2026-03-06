# api/models/user.py
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from .role import Role
from app.utils.bycrypt import hash_password # Added this import

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.username = email  # Added this line to set username
        if password:
            user.password = hash_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    status = models.CharField(max_length=10 ,default='active')
    password = models.CharField(max_length=255) 

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    EMAIL_FIELD = 'email'

    objects = CustomUserManager() # Assign our custom manager

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email