from django.urls import path, include
from .views import (
    CurrencyListApiView,
    CurrencyPriceListApiView
)

urlpatterns = [
    path('', CurrencyListApiView.as_view()),
    path('prices/', CurrencyPriceListApiView.as_view())
]
