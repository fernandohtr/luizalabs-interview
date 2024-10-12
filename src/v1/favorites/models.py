from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

CustomUser = get_user_model()


class Favorite(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="favorite_products")
    products = models.ManyToManyField("Product", through="FavoriteProduct", blank=True)


class Product(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    title = models.CharField(max_length=255)
    image = models.URLField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    review_score = models.PositiveSmallIntegerField(blank=True, null=True)
    link = models.SlugField()
    favorites = models.ManyToManyField("Favorite", through="FavoriteProduct", blank=True)


@receiver(pre_save, sender=Product)
def create_product_link(sender, instance, **kwargs):
    if not instance.link:
        instance.link = f"http://challenge-api.luizalabs.com/api/product/{instance.id}/"


class FavoriteProduct(models.Model):
    favorite = models.ForeignKey(Favorite, on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
