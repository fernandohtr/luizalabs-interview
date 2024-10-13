from django.contrib.auth.models import AbstractUser
from django.db import models

from v1.users.managers import CustomUserManager


class CustomUser(AbstractUser):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)

    username = None
    first_name = None
    last_name = None
    date_joined = None

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not hasattr(self, "favorite"):
            from v1.favorites.models import Favorite

            Favorite.objects.get_or_create(user=self)
