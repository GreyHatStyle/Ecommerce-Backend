from django.urls import path

from . import views

urlpatterns = [
    path('product/review/', views.ProductReviewAPI.as_view(), name='product_review'),
    path('product/home/<int:count>/', views.HomeProductsAPI.as_view(), name='product_review'),
]