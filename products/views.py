from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response
from business.models import BusinessModel

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