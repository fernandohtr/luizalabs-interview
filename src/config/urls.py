from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/users/", include("v1.users.urls")),
    path("api/v1/favorites/", include("v1.favorites.urls")),
]
