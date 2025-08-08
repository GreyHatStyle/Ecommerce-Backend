from rest_framework import serializers

from account.models import AddressTypeChoices
from shopping.models import Order, OrderItem, PaymentChoices

from .search_product_ser import ProductSerializer


class AddressSerializer(serializers.Serializer):
    pincode = serializers.CharField(max_length=32)
    address_type = serializers.ChoiceField(
        choices=AddressTypeChoices.choices,
        default=AddressTypeChoices.HOME
    )
    main_address = serializers.CharField(max_length=300)
    city = serializers.CharField(max_length=30)
    state = serializers.CharField(max_length=30)
    country = serializers.CharField(max_length=30)



class CreateOrderSerializer(serializers.Serializer):
    payment_type = serializers.ChoiceField(
        choices=PaymentChoices.choices,
        error_messages={
            "invalid_choice": "Invalid payment type. Choose from Card, Cash on Delivery, or UPI",
            "required": "payment_type is required"
        }
    )
    address = AddressSerializer(required=False)
    


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ["product", "price"]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["order_id", "user", "delivery_address", "created_at", "status", "payment_type", "total_price"]
        read_only_fields = ["order_id", "user", "created_at", "total_price"]