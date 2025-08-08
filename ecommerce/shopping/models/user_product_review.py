import uuid

from django.db import models

from account.models import User

from .products import Product


class ReactionChoices(models.TextChoices):
    LIKE = "Like"
    DISLIKE = "Dislike"


#TODO: Add comment option also in future
class UserProductReview(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="product_review")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="user_review")
    
    reaction = models.CharField(max_length=10, choices=ReactionChoices.choices)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "UserProductReview"
        unique_together = ['user', 'product']
    
    def __str__(self):
        return f"{self.user.username} -> {self.reaction}ed  this product:{self.product.title}"