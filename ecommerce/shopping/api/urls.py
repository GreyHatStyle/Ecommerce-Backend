from django.urls import path

from . import views

urlpatterns = [
    path('product/review/', views.ProductReviewAPI.as_view(), name='product_review'),
    path('product/home/<int:count>/', views.HomeProductsAPI.as_view(), name='product_home'),
    path('product/search/<int:count>/', views.SearchProductsAPI.as_view(), name='product_search'),
    path('cart/', views.CartAPI.as_view(), name='cart'),
    path('order/', views.OrderAPI.as_view(), name='order'),
]