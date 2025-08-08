from django.urls import path

from . import views

urlpatterns = [
    path('health/', views.HealthAPI.as_view(), name='health'),
    path('login/', views.LoginAPI.as_view(), name='login'),
    path('address/', views.UserAddressAPI.as_view(), name='user_address'),
    path('address/<uuid:address_id>/', views.UserAddressManageAPI.as_view(), name='user_address_manage'),
]