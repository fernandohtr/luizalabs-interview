from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from v1.customers.models import Customer


class Favorite(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name="favorite")
    products = models.ManyToManyField("Product", through="FavoriteProduct", blank=True)


class Product(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    title = models.CharField(max_length=255)
    image = models.URLField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    review_score = models.PositiveSmallIntegerField(blank=True, null=True)
    link = models.CharField(max_length=255)
    favorites = models.ManyToManyField("Favorite", through="FavoriteProduct", blank=True)


@receiver(pre_save, sender=Product)
def create_product_link(sender, instance, **kwargs):
    if not instance.link:
        instance.link = f"http://challenge-api.luizalabs.com/api/product/{instance.id}/"


class FavoriteProduct(models.Model):
    favorite = models.ForeignKey(Favorite, on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        unique_together = ["favorite", "product"]


@receiver(pre_save, sender=FavoriteProduct)
def prevent_duplicate_favorite(sender, instance, **kwargs):
    if FavoriteProduct.objects.filter(favorite=instance.favorite, product=instance.product).exists():
        raise ValidationError(f"The product {instance.product.id} is already in the favorites.")
