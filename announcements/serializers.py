from rest_framework import serializers
from .models import *


class AnnouncementsSerializers(serializers.ModelSerializer):
    business_name=serializers.CharField(source='business.business_name', read_only=True)
    product_name=serializers.CharField(source='products.product_name', read_only=True)
    class Meta:
        model=AnnouncementModel
        fields=['id', 'title', 'message', 'announcement_type', 'business', 'business_name', 'product', 'product_name', 'created_at']