from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    authcode = models.CharField(max_length=100, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)