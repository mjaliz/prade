from django.urls import path, include
from .views import (
    CurrencyListApiView,
)

urlpatterns = [
    path('', CurrencyListApiView.as_view()),
]
