import uuid

from django.db import models
from django.db.models import Sum

from account.models import User

from .products import Product


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f"{self.user.username}'s Cart"
    
    @property
    def total_price(self):
        value = self.items.aggregate(
            total=Sum("product__price"),
        )['total']
        
        return value if value else 0
    
    class Meta:
        db_table = "Cart"
        
        
class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "CartItems"