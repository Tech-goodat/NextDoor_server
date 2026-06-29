from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.decorators import action


# Create your views here.

class BusinessViewSet(viewsets.ViewSet):
    permission_classes=[IsAuthenticated]
    serializer_class=BusinessSerializer
    
    
    def create(self, request):
        if hasattr(request.user, "business"):
            return Response({"error":"You already own a business"}, status=404)
        serializer=self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            serializer.save(owner=request.user)
            
            return Response(serializer.data, status=201)
        
        else:
            return Response(serializer.errors, status=400)
    
    def list(self, request):
        business=BusinessModel.objects.all()
        serializer=self.serializer_class(business, many=True)
        
        if not business:
            return Response({"Error":"businesses not found"})
        
        else:
            return Response(serializer.data, status=200)
        
       
    
    
    @action(detail=False, methods=["get"])
    def my_business(self, request):
        try:
            business = BusinessModel.objects.get(owner=request.user)
            
        except BusinessModel.DoesNotExist:
            return Response(
            {"error": "You do not have a business yet"},
            status=404,
        )
            
        serializer = self.serializer_class(business)
        return Response(serializer.data)
        
            
    def retrieve(self, request, pk=None):
        try:
            business=BusinessModel.objects.get(pk=pk)
            
            
        except BusinessModel.DoesNotExist:
            return Response({"error":"Business Not Found !"}, status=404)
        
        serializer=self.serializer_class(business)
        return Response(serializer.data, status=200)
    
    def update(self, request, pk=None):
        
        try:
            business=BusinessModel.objects.get(pk=pk)
            
        except BusinessModel.DoesNotExist:
            
            return Response({"error":"Business not found !"}, status=404)
        
        if business.owner != request.user:
            return Response({"error":"you don't own this business"}, status=403)
        
        serializer=self.serializer_class(business, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        
        else:
            return Response(serializer.errors, status=400)
        
    def destroy(self, request, pk=None):
        try:
            business=BusinessModel.objects.get(pk=pk)
        except BusinessModel.DoesNotExist:
            return Response({"error":"Business not found!"}, status=404)
        
        if business.owner !=request.user:
            return Response({"error":"You don't own this business"}, status=403)
        
        else:
            business.delete()
            
            return Response(status=204)
    
