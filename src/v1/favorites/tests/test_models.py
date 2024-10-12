import pytest
from django.contrib.auth import get_user_model

from v1.favorites.tests.factories import (
    FavoriteFactory,
    FavoriteWithProductFactory,
    ProductFactory,
)

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
def test_favorite_creation():
    favorite = FavoriteFactory()
    assert favorite.user is not None
    assert favorite.products.count() == 0

    favorite = FavoriteWithProductFactory()
    number_of_products = 5
    assert favorite.user is not None
    assert favorite.products.count() == number_of_products


@pytest.mark.django_db
def test_favorite_with_specific_products():
    product1 = ProductFactory(title="Video Game")
    product2 = ProductFactory(title="TV")
    favorite = FavoriteFactory()
    favorite.products.add(product1)
    favorite.products.add(product2)

    assert favorite.user is not None
    number_of_products = 2
    assert favorite.products.count() == number_of_products
    assert product1 in favorite.products.all()
    assert favorite.products.filter(id=product1.id).first().title == product1.title
    assert product2 in favorite.products.all()
    assert favorite.products.filter(id=product2.id).first().title == product2.title


@pytest.mark.django_db
def test_product_link_generation():
    product = ProductFactory(link="")
    assert product.link == f"http://challenge-api.luizalabs.com/api/product/{product.id}/"
