from django.urls import path

from v1.customers.views import CustomerListCreate, CustomerRetrieveUpdateDestroy

urlpatterns = [
    path("", CustomerListCreate.as_view(), name="customer_list_create"),
    path("detail/", CustomerRetrieveUpdateDestroy.as_view(), name="customer_retrieve_update_destroy"),
]
