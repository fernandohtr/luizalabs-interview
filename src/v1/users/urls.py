from django.urls import path

from v1.users.views import (
    CustomUserLoginAPIView,
    CustomUserLogoutAPIView,
    CustomUserRegistrationAPIView,
    CustomUserRetrieveUpdateDestroy,
)

urlpatterns = [
    path("", CustomUserRetrieveUpdateDestroy.as_view(), name="user_retrieve_update_destroy"),
    path("auth/register/", CustomUserRegistrationAPIView.as_view(), name="register_user"),
    path("auth/login/", CustomUserLoginAPIView.as_view(), name="login_user"),
    path("auth/logout/", CustomUserLogoutAPIView.as_view(), name="logout_user"),
]
