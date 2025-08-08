from django.urls import path

from . import views

urlpatterns = [
    path('health/', views.HealthAPI.as_view(), name='health'),
    path('login/', views.LoginAPI.as_view(), name='login'),
]