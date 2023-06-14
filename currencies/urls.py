from django.urls import path, include
from .views import (
    CurrencyListApiView,
    CurrencyPriceListApiView,
    CurrencyPriceDetailApiView
)

urlpatterns = [
    path('', CurrencyListApiView.as_view()),
    path('<str:currency__name>/', CurrencyPriceDetailApiView.as_view()),
    path('prices/', CurrencyPriceListApiView.as_view()),

]
