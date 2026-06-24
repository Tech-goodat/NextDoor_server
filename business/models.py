from django.db import models
from django.contrib.auth import get_user_model

User=get_user_model()

# Create your models here.
class BusinessModel(models.Model):
    owner=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="businesses"
    )
    business_type=models.CharField(max_length=100)
    business_name=models.CharField(max_length=200, unique=True)
    description=models.TextField(max_length=1000)
    shop_number=models.CharField(max_length=100)
    opens=models.CharField()
    closes=models.CharField()
    phone_number=models.CharField(max_length=20)
    created_at=models.DateTimeField(auto_now_add=True)
    modified=models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.business_name
    
    
