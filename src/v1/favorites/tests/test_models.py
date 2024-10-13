import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from v1.favorites.models import FavoriteProduct
from v1.favorites.tests.factories import ProductFactory
from v1.users.tests.factories import CustomUserFactory, CustomUserWithProductsFactory

CustomUser = get_user_model()


@pytest.mark.django_db
def test_product_creation():
    product = ProductFactory()
    assert product.id is not None
    assert isinstance(product.title, str)
    assert isinstance(product.image, str)
    assert isinstance(product.price, float)
    assert isinstance(product.review_score, int)
    assert isinstance(product.link, str)


@pytest.mark.django_db
def test_favorite_creation(normal_user):
    favorite = normal_user.favorite
    assert favorite.user is not None
    assert favorite.products.count() == 0

    user = CustomUserWithProductsFactory()
    favorite = user.favorite
    number_of_products = 5
    assert favorite.user is not None
    assert favorite.products.count() == number_of_products


@pytest.mark.django_db
def test_favorite_with_specific_products(normal_user):
    product1 = ProductFactory(title="Video Game")
    product2 = ProductFactory(title="TV")
    favorite = normal_user.favorite
    FavoriteProduct.objects.create(favorite=favorite, product=product1)
    FavoriteProduct.objects.create(favorite=favorite, product=product2)

    assert favorite.user is not None
    number_of_products = 2
    assert favorite.products.count() == number_of_products
    assert product1 in favorite.products.all()
    assert favorite.products.filter(id=product1.id).first().title == product1.title
    assert product2 in favorite.products.all()
    assert favorite.products.filter(id=product2.id).first().title == product2.title


@pytest.mark.django_db
def test_favorite_product_in_two_favorite_lists():
    product = ProductFactory(title="Video Game")

    user1 = CustomUserFactory()
    favorite1 = user1.favorite
    FavoriteProduct.objects.create(favorite=favorite1, product=product)

    user2 = CustomUserFactory()
    favorite2 = user2.favorite
    FavoriteProduct.objects.create(favorite=favorite2, product=product)

    assert favorite1.products.first().title == product.title
    assert favorite2.products.first().title == product.title


@pytest.mark.django_db
def test_favorite_two_products_favorite_lists_raise_error(normal_user):
    product = ProductFactory()
    favorite = normal_user.favorite

    FavoriteProduct.objects.create(favorite=favorite, product=product)

    with pytest.raises(ValidationError, match=f"The product {product.id} is already in the favorites."):
        FavoriteProduct.objects.create(favorite=favorite, product=product)


@pytest.mark.django_db
def test_product_link_generation():
    product = ProductFactory(link="")
    assert product.link == f"http://challenge-api.luizalabs.com/api/product/{product.id}/"
