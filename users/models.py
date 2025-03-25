from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=100, null=False, blank=False, unique=True)

    def __str__(self):
        return self.username
