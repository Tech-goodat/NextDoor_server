from django.db import models
from business.models import BusinessModel
from products.models import ProductModel


# Create your models here.

class AnnouncementModel(models.Model):
    class AnnouncementType(models.TextChoices):
        NEW_BUSINESS='NEW_BUSINESS', 'New Business'
        NEW_PRODUCT ='NEW_PRODUCT', 'New Product'
        
    business=models.ForeignKey(BusinessModel, on_delete=models.CASCADE, related_name='announcements')
    product=models.ForeignKey(ProductModel, on_delete=models.CASCADE, null=True, blank=True)
    
    title=models.CharField(max_length=200)
    message=models.TextField()
    
    announcement_type=models.CharField(max_length=40, choices=AnnouncementType.choices)
    created_at=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering=["-created_at"]