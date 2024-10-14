from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

DRF_SPECTACULAR_URLS = [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger"),
    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
LOCAL_URLS = [
    path("api/v1/customers/", include("v1.customers.urls")),
    path("api/v1/favorites/", include("v1.favorites.urls")),
    path("api/v1/users/", include("v1.users.urls")),
]
urlpatterns = DRF_SPECTACULAR_URLS + LOCAL_URLS
