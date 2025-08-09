from django.urls import path

from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('health/', views.HealthAPI.as_view(), name='health'),
    path('login/', views.LoginAPI.as_view(), name='login'),
    path('address/', views.UserAddressAPI.as_view(), name='user_address'),
    path('address/<uuid:address_id>/', views.UserAddressManageAPI.as_view(), name='user_address_manage'),
    
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]