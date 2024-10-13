import requests
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from v1.favorites.models import Favorite, FavoriteProduct, Product
from v1.favorites.serializers import ProductSerializer

from .models import Product

CustomUser = get_user_model()


class ProductCreateDestroyView(APIView):
    permission_classes = (IsAuthenticated,)

    @classmethod
    def post(cls, request, product_id):
        user = request.user
        cache_key = f"product_{product_id}"

        product_data = cache.get(cache_key)
        if product_data:
            product, created = Product.objects.get_or_create(
                id=product_data["id"],
                defaults={
                    "title": product_data["title"],
                    "image": product_data["image"],
                    "price": product_data["price"],
                    "review_score": product_data.get("reviewScore"),
                },
            )
        else:
            product = Product.objects.filter(id=product_id).first()

            if not product:
                api_url = f"http://challenge-api.luizalabs.com/api/product/{product_id}/"
                response = requests.get(api_url)

                if response.status_code != status.HTTP_200_OK:
                    return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

                product_data = response.json()

                twenty_four_hours = 60 * 60 * 24
                cache.set(cache_key, product_data, timeout=twenty_four_hours)

                product = Product.objects.create(
                    id=product_data["id"],
                    title=product_data["title"],
                    image=product_data["image"],
                    price=product_data["price"],
                    review_score=product_data.get("reviewScore"),
                )

        favorite, created = Favorite.objects.get_or_create(user=user)
        _, created = FavoriteProduct.objects.get_or_create(favorite=favorite, product=product)

        if not created:
            return Response({"detail": "Product is already in favorites."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Product added to favorites."}, status=status.HTTP_201_CREATED)

    def delete(self, request, product_id):
        product_id = self.kwargs["product_id"]
        user = request.user

        product = get_object_or_404(Product, id=product_id)

        favorite = Favorite.objects.filter(user=user).first()

        favorite_product = FavoriteProduct.objects.filter(favorite=favorite, product=product).first()
        if not favorite_product:
            return Response({"detail": "Product is not in favorites."}, status=status.HTTP_400_BAD_REQUEST)

        favorite_product.delete()
        return Response({"detail": "Product removed from favorites."}, status=status.HTTP_204_NO_CONTENT)


class ProductListView(ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Product.objects.filter(favoriteproduct__favorite__user=user)
