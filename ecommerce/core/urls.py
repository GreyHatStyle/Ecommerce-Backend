# Project URL directory
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
]

# Custom Apps url
urlpatterns += [
    path('account/', include('account.urls')),
    path('shopping/', include('shopping.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    
    
    # Doc UI's
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]