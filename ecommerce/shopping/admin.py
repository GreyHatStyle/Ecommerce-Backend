from django.contrib import admin

from .models import Cart, CartItems, Order, OrderItem, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'stock')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    
@admin.register(CartItems)
class CartItemsAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product')
    
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'status', 'payment_type', 'created_at', 'total_items')
    
    def total_items(self, obj):
        return obj.items.all().count()
    
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'item_subtotal')