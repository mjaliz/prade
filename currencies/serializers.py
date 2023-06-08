from rest_framework import serializers
from .models import Currency, CurrencyPrice


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ["symbol", "name"]


class CurrencyPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyPrice
        fields = ["date", "open", "high", "low", "close", "volume", "currency"]
