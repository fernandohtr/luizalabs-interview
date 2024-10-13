from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from v1.users.serializers import (
    CustomUserLoginSerializer,
    CustomUserRegistrationSerializer,
    CustomUserSerializer,
)


class CustomUserRegistrationAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CustomUserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user)
        data = serializer.data
        data["tokens"] = {
            "refresh": str(token),
            "access": str(token.access_token),
        }
        return Response(data, status=status.HTTP_201_CREATED)


class CustomUserLoginAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CustomUserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        serializer = CustomUserSerializer(user)
        token = RefreshToken.for_user(user)
        data = serializer.data
        data["tokens"] = {
            "refresh": str(token),
            "access": str(token.access_token),
        }
        return Response(data, status=status.HTTP_200_OK)


class CustomUserLogoutAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    @classmethod
    def post(cls, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            RefreshToken(refresh_token)
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CustomUserRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomUserSerializer

    def get_object(self):
        return self.request.user
