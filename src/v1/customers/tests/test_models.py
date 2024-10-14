import pytest
from django.db import IntegrityError

from v1.customers.models import Customer
from v1.favorites.models import Favorite


@pytest.mark.django_db
def test_create_customer(customer):
    assert customer.id is not None


@pytest.mark.django_db
def test_favorite_creation_on_customer_save(customer):
    assert Favorite.objects.filter(customer=customer).exists()


@pytest.mark.django_db
def test_duplicate_email(customer):
    with pytest.raises(IntegrityError):
        Customer.objects.create(name="Test", email=customer.email)
