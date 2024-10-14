import pytest
import responses
from django.core.cache import cache
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from v1.customers.tests.factories import CustomerWithProductsFactory
from v1.favorites.models import FavoriteProduct, Product
from v1.favorites.tests.factories import ProductFactory


@pytest.mark.django_db
def test_add_product_to_favorites_from_cache(api_user_authenticated, customer, product):
    cache.set(
        product.id,
        {
            "id": product.id,
            "title": product.title,
            "image": product.image,
            "price": str(product.price),
            "review_score": product.review_score,
        },
    )

    url = reverse("add_favorite_product", args=[customer.id])
    response = api_user_authenticated.post(url, {"product_id": product.id})

    assert response.status_code == status.HTTP_201_CREATED
    assert FavoriteProduct.objects.filter(favorite=customer.favorite, product=product).exists()


@pytest.mark.django_db
def test_add_product_to_favorites_from_database(api_user_authenticated, customer, product):
    url = reverse("add_favorite_product", args=[customer.id])
    response = api_user_authenticated.post(url, {"product_id": product.id})

    assert response.status_code == status.HTTP_201_CREATED
    assert FavoriteProduct.objects.filter(favorite=customer.favorite, product=product).exists()


@pytest.mark.django_db
@responses.activate
def test_add_product_to_favorites_from_external_api(api_user_authenticated, customer):
    product = ProductFactory()

    responses.add(
        responses.GET,
        f"http://challenge-api.luizalabs.com/api/product/{product.id}/",
        json={
            "id": product.id,
            "title": product.title,
            "image": product.image,
            "price": product.price,
            "review_score": product.review_score,
        },
        status=200,
    )

    url = reverse("add_favorite_product", args=[customer.id])
    response = api_user_authenticated.post(url, {"product_id": product.id})

    assert response.status_code == status.HTTP_201_CREATED
    assert FavoriteProduct.objects.filter(favorite=customer.favorite, product__id=product.id).exists()


@pytest.mark.django_db
def test_add_product_without_product_id(api_user_authenticated, customer):
    url = reverse("add_favorite_product", args=[customer.id])
    response = api_user_authenticated.post(url, {})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json().get("error") == "product_id is required."


@pytest.mark.django_db
def test_add_duplicate_product_to_favorites(api_user_authenticated, customer, product):
    FavoriteProduct.objects.create(favorite=customer.favorite, product=product)

    url = reverse("add_favorite_product", args=[customer.id])
    response = api_user_authenticated.post(url, {"product_id": product.id})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json().get("error") == "Product is already in favorites."


@pytest.mark.django_db
@responses.activate
def test_add_product_from_external_api(api_user_authenticated, customer):
    product_id = 2
    product_data = {
        "id": product_id,
        "title": "New Product",
        "image": "http://example.com/new_image.jpg",
        "price": 150.00,
        "review_score": 4,
    }

    responses.add(
        responses.GET, f"http://challenge-api.luizalabs.com/api/product/{product_id}/", json=product_data, status=200
    )

    url = reverse("add_favorite_product", args=[customer.id])
    response = api_user_authenticated.post(url, {"product_id": product_id})

    assert response.status_code == status.HTTP_201_CREATED

    product = Product.objects.get(id=product_id)
    assert product.title == product_data["title"]
    assert product.image == product_data["image"]
    assert product.price == product_data["price"]
    assert product.review_score == product_data["review_score"]

    cached_product = cache.get(product_id)
    assert cached_product is not None
    assert cached_product["id"] == product_data["id"]
    assert cached_product["title"] == product_data["title"]
    assert cached_product["image"] == product_data["image"]
    assert cached_product["price"] == str(product_data["price"])
    assert cached_product["review_score"] == product_data["review_score"]

    assert FavoriteProduct.objects.filter(favorite=customer.favorite, product=product).exists()


@pytest.mark.django_db
@responses.activate
def test_product_not_found_in_api(api_user_authenticated, customer):
    responses.add(responses.GET, "http://challenge-api.luizalabs.com/api/product/999/", status=404)

    url = reverse("add_favorite_product", args=[customer.id])
    response = api_user_authenticated.post(url, {"product_id": 999})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json().get("error") == "Product not found."


@pytest.mark.django_db
def test_add_product_with_nonexistent_customer(api_user_authenticated, customer, product):
    url = reverse("add_favorite_product", args=[9999])
    response = api_user_authenticated.post(url, {"product_id": product.id})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json().get("error") == "Customer not found."


@pytest.mark.django_db
def test_add_product_to_favorites_non_authenticated(customer, product):
    api_client = APIClient()
    url = reverse("add_favorite_product", args=[customer.id])
    response = api_client.post(url, {"product_id": product.id})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_successful_delete_favorite_product(api_user_authenticated, customer, product):
    customer = CustomerWithProductsFactory()
    favorite = customer.favorite
    existent_product = favorite.products.first()

    url = reverse("delete_favorite_product", args=[customer.id, existent_product.id])
    response = api_user_authenticated.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not FavoriteProduct.objects.filter(favorite=favorite, product=product).exists()


@pytest.mark.django_db
def test_delete_favorite_product_nonexistent_customer(api_user_authenticated, product):
    url = reverse("delete_favorite_product", args=[9999, product.id])
    response = api_user_authenticated.delete(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json().get("detail") == "No Customer matches the given query."


@pytest.mark.django_db
def test_delete_favorite_product_not_in_favorites(api_user_authenticated, customer, product):
    customer = CustomerWithProductsFactory()
    non_existent_product = ProductFactory()

    url = reverse("delete_favorite_product", args=[customer.id, non_existent_product.id])
    response = api_user_authenticated.delete(url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json().get("detail") == "Product is not in favorites."


@pytest.mark.django_db
def test_get_favorite_products_from_customer(api_user_authenticated):
    customer = CustomerWithProductsFactory()

    url = reverse("add_favorite_product", args=[customer.id])
    response = api_user_authenticated.get(url)

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()

    number_of_products = 5
    assert len(response_data) == number_of_products
    for product_data in response_data:
        assert "title" in product_data
        assert "image" in product_data
        assert "price" in product_data
        assert "link" in product_data
        assert "review_score" in product_data


@pytest.mark.django_db
def test_get_favorite_products_without_review_score(api_user_authenticated, customer):
    favorite = customer.favorite
    product = ProductFactory(review_score=None)
    FavoriteProduct.objects.create(favorite=favorite, product=product)

    url = reverse("add_favorite_product", args=[customer.id])
    response = api_user_authenticated.get(url)

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()

    number_of_products = 1
    assert len(response_data) == number_of_products
    product_data = response_data[0]
    assert "review_score" not in product_data
