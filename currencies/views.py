from django.utils.timezone import make_aware
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Currency
from .serializers import CurrencySerializer, CurrencyPriceSerializer
from utils.price_data import Exchange
from datetime import datetime

ex = Exchange()


class CurrencyListApiView(APIView):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        currencies = Currency.objects.all()
        serializer = CurrencySerializer(currencies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        markets = ex.load_markets()
        data = []
        for market in markets:
            data.append(
                {
                    "symbol": market,
                    "name": markets[market]["info"]["name"]
                }
            )
        serializer = CurrencySerializer(many=True, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CurrencyPriceListApiView(APIView):

    def post(self, request):
        currencies = Currency.objects.all().values()
        data = []
        for currency in currencies:
            prices = ex.fetch_ohlcv(currency["symbol"])
            for price in prices:
                print(price)
                data.append(
                    {
                        "currency": currency['id'],
                        "date": datetime.fromtimestamp(price[0]/1000.0),
                        "open": price[1],
                        "high": price[2],
                        "low": price[3],
                        "close": price[4],
                        "volume": price[5]
                    }
                )

        serializer = CurrencyPriceSerializer(many=True, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response("ok", status=status.HTTP_200_OK)
