from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    nickname = models.CharField(max_length=30, blank=True)
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.username
