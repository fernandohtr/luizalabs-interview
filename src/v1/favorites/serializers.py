from rest_framework import serializers

from v1.favorites.models import Favorite, FavoriteProduct, Product


class ProductSerializer(serializers.ModelSerializer):
    review_score = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "title", "image", "price", "review_score", "link"]

    @classmethod
    def get_review_score(cls, obj):
        return obj.review_score

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation.get("review_score") is None:
            representation.pop("review_score")
        return representation


class FavoriteProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = FavoriteProduct
        fields = ["product"]


class FavoriteSerializer(serializers.ModelSerializer):
    favorite_products = FavoriteProductSerializer(source="favoriteproduct_set", many=True, read_only=True)

    class Meta:
        model = Favorite
        fields = [
            "id",
            "favorite_products",
        ]
