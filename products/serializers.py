from rest_framework import serializers
from .models import *


class ProductSerializer(serializers.ModelSerializer):
    business_name=serializers.CharField(source="business.business_name", read_only=True)
    class Meta:
        model=ProductModel
        fields='__all__'
        read_only_fields=['business_name']
    
    