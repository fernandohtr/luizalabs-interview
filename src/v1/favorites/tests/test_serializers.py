import pytest

from v1.favorites.models import Favorite, FavoriteProduct, Product
from v1.favorites.serializers import FavoriteProductSerializer, FavoriteSerializer, ProductSerializer
from v1.favorites.tests.factories import FavoriteProductFactory, ProductFactory
from v1.users.tests.factories import CustomUserFactory


@pytest.mark.django_db
def test_favorite_serializer():
    user = CustomUserFactory()
    favorite = Favorite.objects.get(id=user.id)
    serializer = FavoriteSerializer(favorite)
    assert "id" in serializer.data
    assert "favorite_products" in serializer.data


@pytest.mark.django_db
def test_product_serializer():
    product = ProductFactory()
    serializer = ProductSerializer(product)
    assert "id" in serializer.data
    assert "title" in serializer.data
    assert "image" in serializer.data
    assert "price" in serializer.data
    assert "review_score" in serializer.data
    assert "link" in serializer.data


@pytest.mark.django_db
def test_favorite_product_serializer():
    favorite_product = FavoriteProductFactory()
    serializer = FavoriteProductSerializer(favorite_product)
    assert "product" in serializer.data


@pytest.mark.django_db
def test_product_serializer_with_no_review_score(api_client_authenticated, normal_user):
    favorite = normal_user.favorite
    product = Product.objects.create(
        id=1,
        title="Product With Review Score",
        image="http://example.com/image1.jpg",
        price="99.99",
        link="http://example.com/product/1",
    )
    FavoriteProduct.objects.create(favorite=favorite, product=product)

    serializer = ProductSerializer(product)

    assert "review_score" not in serializer.data
    assert "id" in serializer.data
    assert "title" in serializer.data
    assert "image" in serializer.data
    assert "price" in serializer.data
    assert "link" in serializer.data
