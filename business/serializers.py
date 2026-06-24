from rest_framework import serializers
from .models import *

class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model=BusinessModel
        fields='__all__'
        read_only_fields=['owner']