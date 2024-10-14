import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from v1.customers.models import Customer
from v1.customers.tests.factories import CustomerFactory


@pytest.mark.django_db
def test_create_customer(api_user_authenticated):
    data = {
        "name": "New Customer",
        "email": "test@example.com",
    }
    response = api_user_authenticated.post(reverse("customer_list_create"), data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Customer.objects.count() == 1
    assert Customer.objects.get().email == "test@example.com"


@pytest.mark.django_db
def test_list_customers(api_user_authenticated):
    CustomerFactory()
    CustomerFactory()

    response = api_user_authenticated.get(reverse("customer_list_create"))
    assert response.status_code == status.HTTP_200_OK
    number_of_customers = 2
    assert len(response.data) == number_of_customers


@pytest.mark.django_db
def test_retrieve_customer(customer, api_user_authenticated):
    response = api_user_authenticated.get(reverse("customer_retrieve_update_destroy"), {"email": customer.email})
    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] == customer.email


@pytest.mark.django_db
def test_retrieve_customer_no_email(api_user_authenticated):
    response = api_user_authenticated.get(reverse("customer_retrieve_update_destroy"))
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data["detail"] == "Error: email query parameter is required"


@pytest.mark.django_db
def test_retrieve_customer_not_found(api_user_authenticated):
    response = api_user_authenticated.get(
        reverse("customer_retrieve_update_destroy"), {"email": "nonexistent@example.com"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data["detail"] == "Error: Customer with this email not found"


@pytest.mark.django_db
def test_update_customer(customer, api_user_authenticated):
    data = {
        "name": "Updated Customer",
    }
    url = f"{reverse('customer_retrieve_update_destroy')}?email={customer.email}"
    response = api_user_authenticated.patch(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    customer.refresh_from_db()
    assert customer.name == "Updated Customer"


@pytest.mark.django_db
def test_delete_customer(customer, api_user_authenticated):
    url = f"{reverse('customer_retrieve_update_destroy')}?email={customer.email}"
    response = api_user_authenticated.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Customer.objects.filter(email=customer.email).count() == 0
