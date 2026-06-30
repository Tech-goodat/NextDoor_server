from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import *
from .models import *

# Create your views here.

class NotificationsViewSet(viewsets.ViewSet):
    permission_classes=[IsAuthenticated]
    serializer_class=NotificationsSerializer
    
    def list(self, request):
        notifications=NotificationsModel.objects.filter(recipient=request.user)
        
        serializer=self.serializer_class(notifications, many=True)
        
        return Response(serializer.data)
