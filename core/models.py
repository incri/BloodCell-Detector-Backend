# models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

class Hospital(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.name

class User(AbstractUser):
    email = models.EmailField(unique=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='users',)
    is_hospital_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username
