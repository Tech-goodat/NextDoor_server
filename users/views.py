from django.shortcuts import render
from rest_framework.response import Response
from django.contrib.auth import get_user_model, authenticate
from .serializers import *
from .models import *
from rest_framework import viewsets, permissions
from knox.models import AuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings

User=get_user_model()

# Create your views here.

class ReqisterViewSet(viewsets.ViewSet):
    permission_classes=[permissions.AllowAny]
    queryset=User.objects.all()
    serializer_class=SignUpSerializer
    
    def create(self, request):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        
        else:
            return Response(serializer.errors)
        
class LoginViewSet(viewsets.ViewSet):
    permission_classes=[permissions.AllowAny]
    serializer_class=LoginSerializer
    
    
    def create(self, request):
        serializer=self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            email=serializer.validated_data['email']
            password=serializer.validated_data['password']
            
            user=authenticate(request, email=email, password=password)
            
            if user:
                _, token=AuthToken.objects.create(user)
                
                return Response({"user":UserSerializer(user).data, "token":token})
            
            else:
                return Response({"error":"Invalid credentials"}, status=400)
            
        else:
            return Response(serializer.errors, status=400)
        
class GoogleLoginViewSet(viewsets.ViewSet):
    permission_classes=[permissions.AllowAny]
    def create(self, request):
        
        google_token=request.data.get("token")
        
        if not google_token:
            return Response({"error":"Token is required"}, status=400)
        
        try:
            idinfo=id_token.verify_oauth2_token(
                google_token,
                requests.Request(),
                settings.GOOGLE_CLIENT_ID
            )
        except ValueError:
            return Response({"error":"Invalid token"}, status=400)
        email=idinfo["email"]
        first_name=idinfo.get("given_name", "")
        last_name=idinfo.get("family_name", "")
        
        user, created=User.objects.get_or_create(
            email=email,
            defaults={
                "first_name":first_name,
                "last_name":last_name
            },
        )
        
        _, token=AuthToken.objects.create(user)
        
        return Response({"user":UserSerializer(user).data, "token":token})
        
class UserViewSet(viewsets.ViewSet):
    permission_classes=[IsAuthenticated]
    serializer_class=UserSerializer
    
    def list(self, request):
        users=User.objects.all()
        serializer=self.serializer_class(users, many=True)
        
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer=self.serializer_class(request.user)
        return Response(serializer.data)
        

