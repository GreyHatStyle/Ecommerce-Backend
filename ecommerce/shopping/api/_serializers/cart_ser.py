from rest_framework import serializers

from shopping.models import CartItems, Product

from .search_product_ser import ProductSerializer


class CartValidate(serializers.Serializer):
    product_id = serializers.UUIDField(
        error_messages={
            "invalid": "Invalid product ID format",
            "required": "product_id is required",
            "blank": "don't give blank fields in API"
        }
    )
    
    def validate_product_id(self, value):
        """
        Just checking if product really exists
        """
        try:
            Product.objects.get(id=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found")
        return value
    
    
    
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = CartItems
        fields = ["id", "cart", "product"]