from rest_framework import serializers
from .models import *

class CartItemSerializer(serializers.ModelSerializer):
    product_name=serializers.CharField(source="product.product_name", read_only=True)
    price=serializers.CharField(source="product.price", read_only=True)
    business_name=serializers.CharField(source="product.business.business_name", read_only=True)


    class Meta:
        model=CartItemModel
        fields=["id", "product", "product_name", "business_name", "price", "quantity"]

class CartSerializer(serializers.ModelSerializer):
    items=CartItemSerializer(many=True, read_only=True)

    class Meta:
        model=CartModel
        fields=["id", "user", "items", "total_price", "total_items"]


