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
        
    def list(self, request):
        product=ProductModel.objects.filter(business__owner=request.user)
        serializer=self.serializer_class(product, many=True)
        
        if not product:
            return Response({"Error":"product not found"})
        
        return Response(serializer.data, status=200)
    
    
       