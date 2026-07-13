from django.db import models
from products.models import ProductModel
from django.contrib.auth import get_user_model

User=get_user_model()

# Create your models here.

class CartModel(models.Model):

    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    @property
    def total_price(self):
        return sum(item.subtotal for item in self.items.all())
    
    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())


    def __str__(self):
        return f"Cart for {self.user.username}"
    

class CartItemModel(models.Model):
    cart=models.ForeignKey(CartModel, on_delete=models.CASCADE, related_name='items')
    product=models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    @property
    def subtotal(self):
        return (self.product.price -self.product.discount) * self.quantity

    class Meta:
        unique_together=('cart', 'product')

    def __str__(self):
        return f"{self.quantity} of {self.product.product_name} in cart of {self.cart.user.username}"

