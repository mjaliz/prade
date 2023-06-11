from django.contrib import admin
from django.urls import path, include
from currencies import urls as currencies_url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth-api/', include('rest_framework.urls')),
    path('currencies/', include(currencies_url))
]
