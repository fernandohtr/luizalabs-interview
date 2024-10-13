import pytest
import responses
from django.core.cache import cache
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from v1.favorites.models import FavoriteProduct, Product
from v1.favorites.serializers import ProductSerializer
from v1.users.tests.factories import CustomUserWithProductsFactory


@responses.activate
@pytest.mark.django_db
def test_add_existing_product_to_favorites(api_client_authenticated, normal_user, product):
    url = reverse("product_create_destroy", args=[product.id])

    response = api_client_authenticated.post(url)

    favorite = normal_user.favorite

    assert response.status_code == status.HTTP_201_CREATED
    assert FavoriteProduct.objects.filter(favorite=favorite, product=product).exists()


@responses.activate
@pytest.mark.django_db
def test_add_new_product_to_favorites(api_client_authenticated, normal_user):
    product_id = 2
    url = reverse("product_create_destroy", args=[product_id])
    api_url = f"http://challenge-api.luizalabs.com/api/product/{product_id}/"
    favorite = normal_user.favorite

    responses.add(
        responses.GET,
        api_url,
        json={
            "id": product_id,
            "title": "New Product",
            "image": "http://example.com/new_image.jpg",
            "price": "49.99",
            "reviewScore": 4,
        },
        status=200,
    )

    response = api_client_authenticated.post(url)

    assert response.status_code == status.HTTP_201_CREATED
    new_product = Product.objects.get(id=product_id)
    assert FavoriteProduct.objects.filter(favorite=favorite, product=new_product).exists()


@responses.activate
@pytest.mark.django_db
def test_add_non_existent_product(api_client_authenticated, normal_user):
    product_id = 3
    url = reverse("product_create_destroy", args=[product_id])
    api_url = f"http://challenge-api.luizalabs.com/api/product/{product_id}/"

    responses.add(responses.GET, api_url, status=404)

    response = api_client_authenticated.post(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert not Product.objects.filter(id=product_id).exists()


@responses.activate
@pytest.mark.django_db
def test_add_duplicate_product_to_favorites(api_client_authenticated, normal_user, product):
    favorite = normal_user.favorite
    FavoriteProduct.objects.create(favorite=favorite, product=product)
    url = reverse("product_create_destroy", args=[product.id])

    response = api_client_authenticated.post(url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert FavoriteProduct.objects.filter(favorite=favorite, product=product).count() == 1


@pytest.mark.django_db
@responses.activate
def test_product_create_destroy_fetch_and_cache_product(api_client_authenticated, normal_user):
    product_id = 1
    api_url = f"http://challenge-api.luizalabs.com/api/product/{product_id}/"
    product_data = {
        "id": product_id,
        "title": "Fetched Product",
        "image": "http://example.com/image.jpg",
        "price": "99.99",
        "reviewScore": 5,
    }

    responses.add(responses.GET, api_url, json=product_data, status=status.HTTP_200_OK)
    url = reverse("product_create_destroy", kwargs={"product_id": product_id})

    assert Product.objects.filter(id=product_id).count() == 0

    response = api_client_authenticated.post(url)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["detail"] == "Product added to favorites."

    product = Product.objects.get(id=product_id)
    assert product.title == product_data["title"]
    assert product.image == product_data["image"]
    assert str(product.price) == product_data["price"]
    assert product.review_score == product_data["reviewScore"]

    cache_key = f"product_{product_id}"
    cached_product_data = cache.get(cache_key)
    assert cached_product_data == product_data


@pytest.mark.django_db
@responses.activate
def test_product_create_destroy_product_not_found(api_client_authenticated, normal_user):
    product_id = 999
    api_url = f"http://challenge-api.luizalabs.com/api/product/{product_id}/"
    responses.add(responses.GET, api_url, json={"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    url = reverse("product_create_destroy", kwargs={"product_id": product_id})
    response = api_client_authenticated.post(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data["detail"] == "Product not found."


@pytest.mark.django_db
def test_product_create_destroy_already_in_favorites(api_client_authenticated, normal_user):
    favorite = normal_user.favorite
    product = Product.objects.create(
        id=1,
        title="Existing Product",
        image="http://example.com/image1.jpg",
        price="99.99",
        review_score=5,
        link="http://example.com/product/1",
    )
    FavoriteProduct.objects.create(favorite=favorite, product=product)
    url = reverse("product_create_destroy", kwargs={"product_id": product.id})
    response = api_client_authenticated.post(url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["detail"] == "Product is already in favorites."


@pytest.mark.django_db
def test_list_user_products():
    user = CustomUserWithProductsFactory()
    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse("user_product_list")

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    number_of_products = 5
    assert len(response.data) == number_of_products
    assert "id" in response.data[0]
    assert "title" in response.data[0]
    assert "image" in response.data[0]
    assert "price" in response.data[0]
    assert "review_score" in response.data[0]


@pytest.mark.django_db
def test_list_user_products_no_review_score(api_client_authenticated, normal_user):
    favorite = normal_user.favorite
    product = Product.objects.create(
        id=1,
        title="Product With Review Score",
        image="http://example.com/image1.jpg",
        price="99.99",
        link="http://example.com/product/1",
    )
    FavoriteProduct.objects.create(favorite=favorite, product=product)

    ProductSerializer(product)

    url = reverse("user_product_list")

    response = api_client_authenticated.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert "id" in response.data[0]
    assert "title" in response.data[0]
    assert "image" in response.data[0]
    assert "price" in response.data[0]
    assert "review_score" not in response.data[0]


@pytest.mark.django_db
def test_remove_from_favorites(api_client_authenticated, normal_user):
    favorite = normal_user.favorite
    product = Product.objects.create(
        id=1,
        title="Existing Product",
        image="http://example.com/image1.jpg",
        price="99.99",
        review_score=5,
        link="http://example.com/product/1",
    )
    FavoriteProduct.objects.create(favorite=favorite, product=product)

    url = reverse("product_create_destroy", kwargs={"product_id": product.id})

    response = api_client_authenticated.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert FavoriteProduct.objects.filter(favorite=favorite, product=product).count() == 0


@pytest.mark.django_db
def test_remove_nonexistent_product(api_client_authenticated, normal_user):
    url = reverse("product_create_destroy", kwargs={"product_id": 999})

    response = api_client_authenticated.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data["detail"] == "No Product matches the given query."


@pytest.mark.django_db
def test_remove_product_not_in_favorites(api_client_authenticated, normal_user):
    product = Product.objects.create(
        id=1,
        title="Existing Product",
        image="http://example.com/image1.jpg",
        price="99.99",
        review_score=5,
        link="http://example.com/product/1",
    )

    url = reverse("product_create_destroy", kwargs={"product_id": product.id})

    response = api_client_authenticated.delete(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["detail"] == "Product is not in favorites."
