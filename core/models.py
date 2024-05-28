# models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

from hospital.models import Hospital


class User(AbstractUser):
    email = models.EmailField(unique=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='users', null=True, blank=True)
    is_hospital_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username
