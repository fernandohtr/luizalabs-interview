import requests
from django.core.cache import cache
from django.db import transaction

# import JsonResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from v1.customers.models import Customer
from v1.favorites.models import FavoriteProduct, Product


class AddFavoriteProductView(APIView):
    permission_classes = (IsAuthenticated,)

    @classmethod
    def post(cls, request, customer_id):
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return JsonResponse({"error": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)

        product_id = request.data.get("product_id")

        if not product_id:
            return JsonResponse({"error": "product_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        cached_product = cache.get(product_id)

        if cached_product:
            product = Product(**cached_product)
        else:
            try:
                product = Product.objects.get(id=product_id)
                cache.set(
                    product_id,
                    {
                        "id": product.id,
                        "title": product.title,
                        "image": product.image,
                        "price": str(product.price),
                        "review_score": product.review_score,
                    },
                )
            except Product.DoesNotExist:
                response = requests.get(f"http://challenge-api.luizalabs.com/api/product/{product_id}/")

                if response.status_code == status.HTTP_200_OK:
                    product_data = response.json()
                    with transaction.atomic():
                        product = Product.objects.create(
                            id=product_data["id"],
                            title=product_data["title"],
                            image=product_data["image"],
                            price=product_data["price"],
                            review_score=product_data.get("review_score", None),
                        )
                        cache.set(
                            product_id,
                            {
                                "id": product.id,
                                "title": product.title,
                                "image": product.image,
                                "price": str(product.price),
                                "review_score": product.review_score,
                            },
                        )
                else:
                    return JsonResponse({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        customer = Customer.objects.get(id=customer_id)

        if FavoriteProduct.objects.filter(favorite__customer=customer, product=product).exists():
            return JsonResponse({"error": "Product is already in favorites."}, status=status.HTTP_400_BAD_REQUEST)

        FavoriteProduct.objects.create(favorite=customer.favorite, product=product)
        return JsonResponse({"message": "Product added to favorites successfully."}, status=status.HTTP_201_CREATED)

    @classmethod
    def get(cls, request, customer_id):
        customer = get_object_or_404(Customer, id=customer_id)
        favorite_products = FavoriteProduct.objects.filter(favorite__customer=customer)
        products_data = []

        for favorite_product in favorite_products:
            product = favorite_product.product
            product_data = {
                "title": product.title,
                "image": product.image,
                "price": str(product.price),
                "link": product.link,
            }
            if product.review_score is not None:
                product_data["review_score"] = product.review_score

            products_data.append(product_data)

        return Response(products_data, status=status.HTTP_200_OK)


class DeleteFavoriteProductView(APIView):
    permission_classes = (IsAuthenticated,)

    @classmethod
    def delete(cls, request, customer_id, product_id):
        customer = get_object_or_404(Customer, id=customer_id)

        product = get_object_or_404(Product, id=product_id)
        favorite = customer.favorite

        favorite_product = FavoriteProduct.objects.filter(favorite=favorite, product=product).first()
        if not favorite_product:
            return Response({"detail": "Product is not in favorites."}, status=status.HTTP_400_BAD_REQUEST)

        favorite_product.delete()
        return Response({"detail": "Product removed from favorites."}, status=status.HTTP_204_NO_CONTENT)
