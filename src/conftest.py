import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from v1.favorites.tests.factories import ProductFactory
from v1.users.tests.factories import CustomUserFactory

register(CustomUserFactory)


@pytest.fixture
def normal_user(custom_user_factory):
    new_user = custom_user_factory.create()
    return new_user


@pytest.fixture
def super_user(custom_user_factory):
    new_user = custom_user_factory.create(is_superuser=True, is_staff=True)
    return new_user


@pytest.fixture
def api_client_authenticated(normal_user):
    client = APIClient()
    client.force_authenticate(user=normal_user)
    return client


@pytest.fixture
def product():
    return ProductFactory()
