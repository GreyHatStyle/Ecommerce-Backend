# Project URL directory

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
]

# Custom Apps url
urlpatterns += [
    path('account/', include('account.urls')),
    path('shopping/', include('shopping.urls')),
]