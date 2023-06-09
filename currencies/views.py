from django.utils.timezone import make_aware
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Currency, CurrencyPrice
from .serializers import CurrencySerializer, CurrencyPriceSerializer
from utils.price_data import Exchange
import time
import datetime

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
        try:
            for currency in currencies:
                currency_price = CurrencyPrice.objects.filter(currency=currency["id"]).values_list("date").order_by(
                    "-date")
                currency_last_update = datetime.datetime.now() - datetime.timedelta(10 * 365)
                if len(currency_price) > 0:
                    currency_last_update = currency_price[0][0]
                prices = ex.fetch_ohlcv(currency["symbol"])
                for price in prices:
                    if price[0] > currency_last_update.timestamp():
                        print(price)
                        data.append(
                            {
                                "currency": currency['id'],
                                "date": datetime.datetime.fromtimestamp(price[0] / 1000.0),
                                "open": price[1],
                                "high": price[2],
                                "low": price[3],
                                "close": price[4],
                                "volume": price[5]
                            }
                        )
        except Exception as e:
            print(e)
            serializer = CurrencyPriceSerializer(many=True, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response("ok", status=status.HTTP_200_OK)
