from accounts.serializers import UserSerializer
from rest_framework import serializers

from .models import Product


class CreateProductSerializer(serializers.ModelSerializer):
    seller = UserSerializer(read_only=True, source="user")

    class Meta:
        model = Product
        fields = ["id", "description", "price", "quantity", "seller", "is_active"]
        read_only_fields = ["is_active"]


class ListProductSerializer(serializers.ModelSerializer):
    seller_id = serializers.IntegerField(source="user_id")

    class Meta:
        model = Product
        fields = ["description", "price", "quantity", "is_active", "seller_id"]
        read_only_fields = [
            "description",
            "price",
            "quantity",
            "is_active",
            "seller_id",
        ]
