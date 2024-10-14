import pytest

from v1.users.serializers import CustomUserLoginSerializer, CustomUserSerializer
from v1.users.tests.factories import CustomUserFactory


@pytest.mark.django_db
def test_custom_user_serializer(normal_user):
    serializer = CustomUserSerializer(normal_user)
    assert "id" in serializer.data
    assert "email" in serializer.data


@pytest.mark.django_db
def test_custom_user_login_serializer_valid_user():
    email = "test@example.com"
    password = "12345678"
    user = CustomUserFactory(email=email, password=password, is_active=True)

    valid_data = {
        "email": email,
        "password": password,
    }
    serializer = CustomUserLoginSerializer(data=valid_data)
    assert serializer.is_valid()
    assert serializer.validated_data == user


@pytest.mark.django_db
def test_custom_user_login_serializer_inactive_user():
    email = "test@example.com"
    password = "12345678"
    CustomUserFactory(email=email, password=password, is_active=False)

    valid_data = {
        "email": email,
        "password": password,
    }
    serializer = CustomUserLoginSerializer(data=valid_data)
    assert not serializer.is_valid()
    assert "Incorrect credentials" in str(serializer.errors)


@pytest.mark.django_db
def test_custom_user_login_serializer_incorrect_credentials():
    email = "test@example.com"
    CustomUserFactory(email=email, password="12345678", is_active=True)

    invalid_data = {
        "email": email,
        "password": "wrongpassword",
    }
    serializer = CustomUserLoginSerializer(data=invalid_data)
    assert not serializer.is_valid()
    assert "Incorrect credentials" in str(serializer.errors)
