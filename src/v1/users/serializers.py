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
            "name",
            "email",
            "favorite",
        )


class CustomUserRegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "name",
            "email",
            "password1",
            "password2",
        )
        extra_kwargs = {"password": {"write_only": True}}

    @classmethod
    def validate(cls, attrs):
        if attrs["password1"] != attrs["password2"]:
            raise serializers.ValidationError("Passwords do not match!")

        password = attrs.get("password1")
        minimum_length = 8
        if len(password) < minimum_length:
            raise serializers.ValidationError("Passwords must be at least 8 characters!")
        return attrs

    @classmethod
    def create(cls, validated_data):
        password = validated_data.pop("password1")
        validated_data.pop("password2")

        return CustomUser.objects.create_user(password=password, **validated_data)


class CustomUserLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    @classmethod
    def validate(cls, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect credentials")
