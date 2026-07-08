from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class CartViewSet(viewsets.ViewSet):
    permission_classes=[IsAuthenticated]
    serializer_class=CartSerializer


    def get_cart(self, request):
        cart, created =CartModel.objects.get_or_create(user=request.user)

        return cart
    
    def list(self, request):
        cart=self.get_cart(request)
        serializer=self.serializer_class(cart)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def add_item(self, request):

        product_id=request.data.get('product')
        quantity=request.data.get('quantity', 1)
        cart=self.get_cart(request)

        product=ProductModel.objects.get(id=product_id)

        cart_item, created=CartItemModel.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_item.quantity+=int(quantity)

        else:
            cart_item.quantity=int(quantity)

        cart_item.save()
        return Response({'message': 'Item added to cart successfully.'}, status=201)
    
    @action(detail=False, methods=['post'])
    def remove_item(self, request):
        product_id=request.data.get('product')
        cart=self.get_cart(request)

        CartItemModel.objects.filter(cart=cart, product_id=product_id).delete()
        return Response({'message': 'Item removed from cart successfully.'}, status=200)
    
    @action(detail=False, methods=['post'])
    def update_quantity(self, request):
        product_id=request.data.get("product")
        quantity=request.data.get("quantity")
        cart=self.get_cart(request)

        cart_item=CartItemModel.objects.get(cart=cart, product_id=product_id)
        cart_item.quantity=int(quantity)
        cart_item.save()
        return Response({'message': 'Item quantity updated successfully.'}, status=200)
    
    @action(detail=False, methods=['delete'])
    def clear_cart(self, request):
        cart=self.get_cart(request)
        cart.items.all().delete()
        return Response({'message': 'Cart cleared successfully.'}, status=200)



    
