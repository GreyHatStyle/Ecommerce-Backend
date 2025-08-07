from django.urls import path

from . import views

urlpatterns = [
    path('health/', views.HealthAPI.as_view(), name='health'),
    
]