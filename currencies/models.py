from django.db import models
from django.contrib.auth.models import User


class Currency(models.Model):
    symbol = models.CharField(max_length=50, null=False)
    company = models.CharField(max_length=250, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    def __str__(self) -> str:
        return self.symbol
