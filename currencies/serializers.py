from rest_framework import serializers
from .models import Currency, CurrencyPrice


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ["id", "symbol", "name", "created_at"]


class CurrencyPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyPrice
        fields = ["date", "open", "high", "low", "close", "volume", "currency"]
