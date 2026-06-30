from rest_framework import serializers
from .models import *


class NotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        
        model=NotificationsModel
        fields='__all__'
        read_only_fields=['recipient', 'created_at']