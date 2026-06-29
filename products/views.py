from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response
from business.models import BusinessModel
from rest_framework.decorators import action

# Create your views here.

class ProductViewSet(viewsets.ViewSet):
    permission_classes=[IsAuthenticated]
    serializer_class=ProductSerializer
    
    
    def create(self, request):
        try:
             business=BusinessModel.objects.get(owner=request.user)
             
        except BusinessModel.DoesNotExist:
            return Response({"error":"user has no business"}, status=404)
            
       
        serializer=self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            serializer.save(business=business)
            
            return Response(serializer.data, status=201)
        
        else:
            return Response(serializer.errors, status=400)
    @action(detail=False, methods=['get'])   
    def my_products(self, request):
        product=ProductModel.objects.filter(business__owner=request.user)
        serializer=self.serializer_class(product, many=True)
        
        if not product:
            return Response({"Error":"product not found"})
        
        return Response(serializer.data, status=200)
   
    def list(self, request):
        products=ProductModel.objects.all()
        if not products.exists():
            return Response({'error':'products not found'}, status=404)
        
        serializer=self.serializer_class(products, many=True)
        return Response(serializer.data, status=200)
    
    def retrieve(self, request, pk=None):
        try:
            product=ProductModel.objects.get(pk=pk)
            
        except ProductModel.DoesNotExist:
            return Response({"error":"product does not exist"}, status=404)
        
        serializer=self.serializer_class(product)
        
        return Response(serializer.data, status=200)
    
    
    def update(self, request, pk=None):
        try:
            product=ProductModel.objects.get(pk=pk, business__owner=request.user)
                
        except ProductModel.DoesNotExist:
            return Response({"error":"product not found"}, status=404)
        
        serializer=self.serializer_class(product, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status=200)
        
        else:
            return Response(serializer.errors)
        
    def destroy(self, request, pk=None):
        
        try:
            product=ProductModel.objects.get(pk=pk, business__owner=request.user)
            
        except ProductModel.DoesNotExist:
            return Response({"error":"product not found"}, status=404)
        
        product.delete()
        
        return Response({"success":"Product deleted successfully"}, status=200)
        

    
    
       