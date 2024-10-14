from django.urls import path

from v1.favorites.views import AddFavoriteProductView, DeleteFavoriteProductView

urlpatterns = [
    path("customers/<int:customer_id>/", AddFavoriteProductView.as_view(), name="add_favorite_product"),
    path(
        "customers/<int:customer_id>/products/<int:product_id>/",
        DeleteFavoriteProductView.as_view(),
        name="delete_favorite_product",
    ),
]
