import pytest
from django.core.cache import cache
from pytest_factoryboy import register
from rest_framework.test import APIClient

from v1.customers.tests.factories import CustomerFactory
from v1.favorites.tests.factories import ProductFactory
from v1.users.tests.factories import CustomUserFactory

register(CustomerFactory)
register(CustomUserFactory)


@pytest.fixture
def normal_user(custom_user_factory):
    user = custom_user_factory.create()
    return user


@pytest.fixture
def super_user(custom_user_factory):
    user = custom_user_factory.create(is_superuser=True, is_staff=True)
    return user


@pytest.fixture
def customer(customer_factory):
    customer = customer_factory.create()
    return customer


@pytest.fixture
def api_user_authenticated(normal_user):
    api_client = APIClient()
    api_client.force_authenticate(user=normal_user)
    api_client.force_login(user=normal_user)
    return api_client


@pytest.fixture
def product():
    return ProductFactory()


@pytest.fixture(autouse=True)
def clear_cache():
    cache.clear()
