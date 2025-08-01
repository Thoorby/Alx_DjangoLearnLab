from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager  # Make sure this import is valid

class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.username
