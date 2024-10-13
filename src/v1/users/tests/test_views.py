import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from v1.users.tests.factories import CustomUserFactory

User = get_user_model()


@pytest.mark.django_db
def test_user_register_successs(api_client):
    url = reverse("register_user")
    data = {"name": "John", "email": "test@example.com", "password1": "12345678", "password2": "12345678"}

    response = api_client.post(
        path=url,
        data=data,
    )

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_user_register_fail_with_same_email(api_client):
    email = "test@example.com"
    password = "12345678"

    CustomUserFactory(email=email, password=password)

    url = reverse("register_user")
    data = {"name": "John", "email": email, "password1": password, "password2": password}

    response = api_client.post(
        path=url,
        data=data,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["email"][0] == "user with this email already exists."


@pytest.mark.django_db
def test_user_login_success(api_client):
    email = "test@example.com"
    password = "12345678"

    CustomUserFactory(email=email, password=password)

    url = reverse("login_user")
    data = {
        "email": email,
        "password": password,
    }
    response = api_client.post(path=url, data=data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert "tokens" in response.data
    assert "refresh" in response.data["tokens"]
    assert "access" in response.data["tokens"]
    assert response.data["email"] == email


@pytest.mark.django_db
def test_user_login_incorrect_credentials(api_client):
    CustomUserFactory(email="test@example.com", password="12345678")

    url = reverse("login_user")
    data = {
        "email": "test@example.com",
        "password": "wrongpassword",
    }
    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "non_field_errors" in response.data
    assert response.data["non_field_errors"][0] == "Incorrect credentials"


@pytest.mark.django_db
def test_user_logout_success(api_client):
    user = CustomUserFactory()
    refresh = RefreshToken.for_user(user)
    url = reverse("logout_user")
    data = {
        "refresh": str(refresh),
    }

    api_client.force_authenticate(user=user)
    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_205_RESET_CONTENT


@pytest.mark.django_db
def test_user_logout_invalid_token(api_client):
    user = CustomUserFactory()
    RefreshToken.for_user(user)
    url = reverse("logout_user")
    data = {
        "refresh": "invalidtoken",
    }

    api_client.force_authenticate(user=user)
    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_user_logout_missing_token(api_client):
    user = CustomUserFactory()
    RefreshToken.for_user(user)
    url = reverse("logout_user")
    data = {}

    api_client.force_authenticate(user=user)
    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_retrieve_user_info(api_client):
    user = CustomUserFactory()
    api_client.force_authenticate(user=user)

    url = reverse("user_retrieve_update_destroy")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] == user.email


@pytest.mark.django_db
def test_user_info_unauthenticated(api_client):
    url = reverse("user_retrieve_update_destroy")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_update_user_info(api_client):
    user = CustomUserFactory(email="test@example.com", password="12345678")
    new_email = "newemail@example.com"

    api_client.force_authenticate(user=user)

    url = reverse("user_retrieve_update_destroy")
    data = {
        "email": new_email,
    }
    response = api_client.patch(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    user.refresh_from_db()
    assert user.email == new_email


@pytest.mark.django_db
def test_delete_user_data(api_client):
    user = CustomUserFactory()

    api_client.force_authenticate(user=user)

    url = reverse("user_retrieve_update_destroy")
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not User.objects.filter(id=user.id).exists()
