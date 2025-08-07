import uuid

from django.db import models


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=3)
    stock = models.PositiveIntegerField()
    
    # Will store bucket URLs here
    image_url = models.URLField(max_length=500, blank=True, null=True)

    REQUIRED_FIELDS = [
        "name",
    ]

    @property
    def in_stock(self):
        return self.stock > 0
    
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'Product'
        
