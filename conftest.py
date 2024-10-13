import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from v1.users.tests.factories import CustomUserFactory

register(CustomUserFactory)


@pytest.fixture
def normal_user(db, custom_user_factory):
    new_user = custom_user_factory.create()
    return new_user


@pytest.fixture
def super_user(db, custom_user_factory):
    new_user = custom_user_factory.create(is_superuser=True, is_staff=True)
    return new_user


@pytest.fixture
def api_client():
    return APIClient()
