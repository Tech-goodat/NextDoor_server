from collections import defaultdict
from rest_framework import serializers
from .models import *


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source="product.product_name",
        read_only=True
    )
    price = serializers.DecimalField(
        source="product.price",
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    business_name = serializers.CharField(
        source="product.business.business_name",
        read_only=True
    )
    subtotal = serializers.ReadOnlyField()

    class Meta:
        model = CartItemModel
        fields = [
            "id",
            "product",
            "product_name",
            "business_name",
            "price",
            "quantity",
            "subtotal",
        ]


class CartSerializer(serializers.ModelSerializer):
    businesses = serializers.SerializerMethodField()

    class Meta:
        model = CartModel
        fields = [
            "id",
            "user",
            "businesses",
            "total_price",
            "total_items",
        ]

    def get_businesses(self, cart):
        grouped = defaultdict(lambda: {
            "business_id": None,
            "business_name": "",
            "subtotal": 0,
            "items": [],
        })

        for item in cart.items.all():
            business = item.product.business

            group = grouped[business.id]

            group["business_id"] = business.id
            group["business_name"] = business.business_name
            group["subtotal"] += item.subtotal
            group["items"].append(
                CartItemSerializer(item).data
            )

        return list(grouped.values())