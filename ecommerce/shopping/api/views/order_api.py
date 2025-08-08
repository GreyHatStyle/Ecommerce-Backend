from typing import Any, Dict, cast

from django.db import transaction
from rest_framework.permissions import IsAuthenticated

from shopping.models import Cart, CartItems, Order, OrderItem
from shopping.utils import get_delivery_address

from .._serializers import (CreateOrderSerializer, OrderItemSerializer,
                            OrderSerializer)
from ..throttles import BurstRateThrottle, SustainedRateThrottle
from ._base import (BaseAPIView, Request, Response, api_exception_handler,
                    status)


class OrderAPI(BaseAPIView):
    """
    API to create orders from cart items
    """
    permission_classes = [IsAuthenticated]
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]
    
    @api_exception_handler
    def post(self, request: Request) -> Response:
        """
        Create order from cart items
        """
        serializer = CreateOrderSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "failed",
                "errors": serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = cast(Dict[str, Any], serializer.validated_data)
        
        payment_type = validated_data.get("payment_type")
        address_data = validated_data.get("address")
        
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = CartItems.objects.filter(cart=cart).select_related('product')
            
            if not cart_items.exists():
                return Response({
                    "status": "failed",
                    "message": "Cart is empty. Add products to cart before placing order."
                }, status=status.HTTP_400_BAD_REQUEST)
            

            for cart_item in cart_items:
                if not cart_item.product.in_stock:
                    return Response({
                        "status": "failed",
                        "message": f"Product '{cart_item.product.title}' is out of stock, please remove it from cart."
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            
            delivery_address = get_delivery_address(request.user, address_data)
            
            if not delivery_address:
                return Response({
                    "status": "failed",
                    "message": "No delivery address found. Please add an address or provide address details."
                }, status=status.HTTP_400_BAD_REQUEST)
            
            
            # Creating Order with transaction to ensure atomicity while sending Cart items to Order Items
            with transaction.atomic():
                order = Order.objects.create(
                    user=request.user,
                    delivery_address=delivery_address,
                    payment_type=payment_type
                )
                
                order_item_list: list[OrderItem] = []
                
                for cart_item in cart_items:
                    order_item_list.append(
                        OrderItem(
                            order=order,
                            product=cart_item.product,
                            quantity=1,
                            price=cart_item.product.price
                        )
                    )
                
                OrderItem.objects.bulk_create(order_item_list)
                
                # Now order is complete, so reset the cart
                cart_items.delete()
            
            order_serializer = OrderSerializer(order)
            
            order_items = OrderItem.objects.filter(order=order).select_related('product')
            order_item_serializer= OrderItemSerializer(order_items, many=True)
            
            return Response({
                "status": "success",
                "message": "Order placed successfully",
                "order": order_serializer.data,
                "total_items": order.items.count(),
                "order_items": order_item_serializer.data,
            }, status=status.HTTP_201_CREATED)
            
        except Cart.DoesNotExist:
            return Response({
                "status": "failed",
                "message": "Cart not found. Add products to cart first."
            }, status=status.HTTP_404_NOT_FOUND)
            
            
    # =============================================================================================
    
    @api_exception_handler
    def get(self, request: Request) -> Response:
        """
        Get user's order history
        """
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        order_serializer = OrderSerializer(orders, many=True)
        
        return Response({
            "status": "success",
            "orders": order_serializer.data,
            "total_orders": len(order_serializer.data)
        }, status=status.HTTP_200_OK)