from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from .models import *
from .serializers import *

# Create your views here.

class AnnouncementsViewSet(viewsets.ViewSet):
    permission_classes=[IsAuthenticated]
    serializer_class=AnnouncementsSerializers
    
    
    def list(self, request):
        queryset=AnnouncementModel.objects.select_related('business', 'product')
        
        limit=request.query_params.get('limit')
        
        if limit:
            try:
                queryset=queryset[:int(limit)]
                
            except ValueError:
                return Response({'error':'invalid parameter'}, status=400)
        serializer=self.serializer_class(queryset, may=True)
        return Response(serializer.data, status=200)
    
    
    
