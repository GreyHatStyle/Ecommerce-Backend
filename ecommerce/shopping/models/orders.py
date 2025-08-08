import uuid

from django.db import models
from django.db.models import F, Sum

from account.models import User, UserAddress

from .products import Product


class StatusChoices(models.TextChoices):
    CANCELLED = "Cancelled"
    DELIVERED = "Delivered"
    PENDING = "Pending"
    
class PaymentChoices(models.TextChoices):
    CARD = "Card"
    COD = "Cash on Delivery"
    UPI = "UPI"
             
        
class Order(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Will store snap shot of ordered address, just in case if current user address is changed
    delivery_address = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
    )
    
    payment_type = models.CharField(
        max_length=30,
        choices=PaymentChoices.choices,
        default=PaymentChoices.CARD,
    )

    products = models.ManyToManyField(Product, through="OrderItem", related_name='orders')
    
    @property
    def total_price(self):
        total = self.items.aggregate(
            total=Sum(F("price") * F("quantity"))
        )['total']
        return total if total else 0
    
    def __str__(self):
        return f"Order {self.order_id} : by {self.user.username}"
    
    class Meta:
        db_table = 'Order'
    
    
    
    
class OrderItem(models.Model):
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    
    # To ensure ordered item 'price' remains same, if actual product price changes in future
    price = models.DecimalField(max_digits=10, decimal_places=3)


    @property
    def item_subtotal(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return f"{self.quantity} x {self.product.title} in Order {self.order.order_id}"
    
    class Meta:
        db_table = 'OrderItem'