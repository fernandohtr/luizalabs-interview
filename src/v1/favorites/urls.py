from django.urls import path

from v1.favorites.views import ProductCreateDestroyView, ProductListView

urlpatterns = [
    path("favorites/products/", ProductListView.as_view(), name="user_product_list"),
    path("favorites/products/<int:product_id>/", ProductCreateDestroyView.as_view(), name="product_create_destroy"),
]
