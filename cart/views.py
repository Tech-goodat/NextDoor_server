from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import CartModel, CartItemModel
from .serializers import CartSerializer
from products.models import ProductModel


class CartViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_cart(self, request):

        cart, created = CartModel.objects.get_or_create(
            user=request.user
        )

        return CartModel.objects.prefetch_related(
            "items__product__business"
        ).get(id=cart.id)

    def list(self, request):

        cart = self.get_cart(request)

        serializer = self.serializer_class(cart)

        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def add_item(self, request):

        product_id = request.data.get("product")
        quantity = int(request.data.get("quantity", 1))

        if quantity < 1:
            return Response(
                {"error": "Quantity must be at least 1."},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart = self.get_cart(request)

        product = get_object_or_404(
            ProductModel,
            id=product_id
        )

        cart_item, created = CartItemModel.objects.get_or_create(
            cart=cart,
            product=product
        )

        if created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity

        cart_item.save()

        serializer = self.serializer_class(cart)

        return Response(
            {
                "message": "Item added successfully.",
                "cart": serializer.data
            },
            status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=["post"])
    def remove_item(self, request):

        product_id = request.data.get("product")

        cart = self.get_cart(request)

        cart_item = get_object_or_404(
            CartItemModel,
            cart=cart,
            product_id=product_id
        )

        cart_item.delete()

        serializer = self.serializer_class(cart)

        return Response(
            {
                "message": "Item removed successfully.",
                "cart": serializer.data
            },
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=["post"])
    def update_quantity(self, request):

        product_id = request.data.get("product")
        quantity = int(request.data.get("quantity"))

        if quantity < 1:
            return Response(
                {"error": "Quantity must be at least 1."},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart = self.get_cart(request)

        cart_item = get_object_or_404(
            CartItemModel,
            cart=cart,
            product_id=product_id
        )

        cart_item.quantity = quantity
        cart_item.save()

        serializer = self.serializer_class(cart)

        return Response(
            {
                "message": "Quantity updated successfully.",
                "cart": serializer.data
            },
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=["delete"])
    def clear_cart(self, request):

        cart = self.get_cart(request)

        cart.items.all().delete()

        serializer = self.serializer_class(cart)

        return Response(
            {
                "message": "Cart cleared successfully.",
                "cart": serializer.data
            },
            status=status.HTTP_200_OK
        )