from django.db import models
from business.models import BusinessModel


# Create your models here.
class ProductModel(models.Model):
    product_name = models.CharField(max_length=30)
    description = models.TextField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    business = models.ForeignKey(BusinessModel, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.product_name
    
