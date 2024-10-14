from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

from v1.favorites.serializers import FavoriteSerializer

CustomUser = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    favorite = FavoriteSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "favorite",
        )


class CustomUserLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    @classmethod
    def validate(cls, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect credentials")
