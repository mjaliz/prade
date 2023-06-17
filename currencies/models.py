from django.db import models
from django.contrib.auth.models import User


class Currency(models.Model):
    symbol = models.CharField(max_length=50, unique=True, null=False)
    name = models.CharField(max_length=250, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    def __str__(self) -> str:
        return self.symbol


class CurrencyPrice(models.Model):
    date = models.DateTimeField(null=False)
    open = models.FloatField(null=False)
    high = models.FloatField(null=False)
    low = models.FloatField(null=False)
    close = models.FloatField(null=False)
    volume = models.FloatField(null=False)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)


class Strategy(models.Model):
    name = models.CharField(max_length=250, null=False)


class CurrencyStrategy(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)
