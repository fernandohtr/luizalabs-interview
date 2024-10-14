import pytest

from v1.customers.serializers import CustomerSerializer


@pytest.mark.django_db
def test_customer_serializer_serialization(customer):
    serializer = CustomerSerializer(customer)
    data = serializer.data

    assert data["id"] == customer.id
    assert data["name"] == customer.name
    assert data["email"] == customer.email
    assert data["favorite"] is not None


@pytest.mark.django_db
def test_customer_serializer_validation():
    serializer = CustomerSerializer(data={"name": "", "email": "invalid-email"})

    assert not serializer.is_valid()
    assert "name" in serializer.errors
    assert "email" in serializer.errors


@pytest.mark.django_db
def test_customer_serializer_successful_validation():
    data = {
        "name": "Valid Client",
        "email": "test@example.com",
    }
    serializer = CustomerSerializer(data=data)

    assert serializer.is_valid()
    assert serializer.validated_data["name"] == "Valid Client"
    assert serializer.validated_data["email"] == "test@example.com"
