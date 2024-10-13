import pytest
from rest_framework.exceptions import ValidationError

from v1.users.serializers import CustomUserLoginSerializer, CustomUserRegistrationSerializer, CustomUserSerializer
from v1.users.tests.factories import CustomUserFactory


@pytest.mark.django_db
def test_custom_user_serializer(normal_user):
    serializer = CustomUserSerializer(normal_user)
    assert "id" in serializer.data
    assert "email" in serializer.data
    assert "name" in serializer.data


@pytest.mark.django_db
def test_custom_register_serializer_validate_data():
    valid_data = {
        "email": "test@example.com",
        "name": "John",
        "password1": "test_password",
        "password2": "test_password",
    }
    serializer = CustomUserRegistrationSerializer(data=valid_data)
    assert serializer.is_valid()

    user = serializer.save()
    assert user.email == valid_data["email"]
    assert user.name == valid_data["name"]


@pytest.mark.django_db
def test_custom_register_serializer_raise_error_wrong_password():
    invalid_data = {
        "email": "test@example.com",
        "name": "John",
        "password1": "test_password",
        "password2": "wrong_password",
    }
    serializer = CustomUserRegistrationSerializer(data=invalid_data)

    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_custom_register_serializer_raise_error_password_with_less_then_8_chars():
    invalid_data = {
        "email": "test@example.com",
        "name": "John",
        "password1": "1234",
        "password2": "1234",
    }
    serializer = CustomUserRegistrationSerializer(data=invalid_data)

    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


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
