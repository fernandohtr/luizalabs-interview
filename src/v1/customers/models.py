from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, db_index=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        from v1.favorites.models import Favorite

        if not hasattr(self, "favorite"):
            Favorite.objects.get_or_create(customer=self)
