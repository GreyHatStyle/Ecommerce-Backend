from typing import Any, Dict, cast

from rest_framework.permissions import IsAuthenticated

from shopping.models import Cart, CartItems, Product

from .._serializers import CartItemSerializer, CartSerializer, CartValidate
from ..throttles import BurstRateThrottle, SustainedRateThrottle
from ._base import (BaseAPIView, Request, Response, api_exception_handler,
                    status)


class CartAPI(BaseAPIView):
    """
    API to add/remove products from user's cart
    """
    permission_classes = [IsAuthenticated]
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle]
    
    @api_exception_handler
    def post(self, request: Request) -> Response:
        """
        Add new product to cart (using product uuid)
        """
        
        serializer = CartValidate(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "failed",
                "errors": serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = cast(Dict[str, Any], serializer.validated_data)
        product_id = validated_data["product_id"]
        
        cart, created = Cart.objects.get_or_create(user=request.user)
        product = Product.objects.get(id=product_id)
        
        # Checking if product is already in cart
        cart_item, new_product_added = CartItems.objects.get_or_create(
            cart=cart,
            product=product
        )
        
        if new_product_added:
            return Response({
                "status": "success",
                "message": f"Product '{product.title}' added to cart",
                "cart_count": cart.items.count()
            }, status=status.HTTP_201_CREATED)
        
        
        return Response({
            "status": "info",
            "message": f"Product '{product.title}' already in cart",
            "cart_count": cart.items.count()
        }, status=status.HTTP_200_OK)
    
    #========================================================================================
    
    @api_exception_handler
    def delete(self, request: Request) -> Response:
        """
        Remove product from cart
        """
        
        serializer = CartValidate(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "failed",
                "errors": serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = cast(Dict[str, Any], serializer.validated_data)
        product_id = validated_data["product_id"]
        
        try:
            cart = Cart.objects.get(user=request.user)
            product = Product.objects.get(id=product_id)
            
            cart_item = CartItems.objects.get(cart=cart, product=product)
            cart_item.delete()
            
            return Response({
                "status": "success",
                "message": f"Product '{product.title}' removed from cart",
                "cart_items_count": cart.items.count()
            }, status=status.HTTP_200_OK)
            
        except Cart.DoesNotExist:
            return Response({
                "status": "failed",
                "message": "Cart not found"
            }, status=status.HTTP_404_NOT_FOUND)
            
        except CartItems.DoesNotExist:
            return Response({
                "status": "failed",
                "message": "Product not found in cart"
            }, status=status.HTTP_404_NOT_FOUND)
    
    
    #========================================================================================
    
    @api_exception_handler
    def get(self, request: Request) -> Response:
        """
        Get all cart items
        """
        
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = CartItems.objects.filter(cart=cart).select_related('product')
            
            c_serializer = CartSerializer(cart)
            ci_serializer = CartItemSerializer(cart_items, many=True)
            
            return Response({
                "status": "success",
                "cart": c_serializer.data,
                "total_items": len(ci_serializer.data),
                "cart_items": ci_serializer.data,
            }, status=status.HTTP_200_OK)
            
        except Cart.DoesNotExist:
            return Response({
                "status": "success",
                "cart_items": [],
                "total_items": 0
            }, status=status.HTTP_200_OK)