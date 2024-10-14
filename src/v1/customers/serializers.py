from rest_framework import serializers

from v1.customers.models import Customer
from v1.favorites.serializers import FavoriteSerializer


class CustomerSerializer(serializers.ModelSerializer):
    favorite = FavoriteSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = (
            "id",
            "name",
            "email",
            "favorite",
        )
