from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Currency, CurrencyPrice
from .serializers import CurrencySerializer, CurrencyPriceSerializer
from django.db.models import Max
from django.db.models import F
from django.db import connection
from utils.price_data import Exchange
import datetime

ex = Exchange()


class CurrencyListApiView(APIView):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        query_dict = request.GET
        print(query_dict.get("filter"))
        if 'filter' in query_dict:
            if query_dict.get('filter') == 'new_closing_highs':
                with connection.cursor() as cursor:
                    cursor.execute("""
                    SELECT id, symbol, name, created_at
                    FROM
                        (
                            SELECT t1.currency_id, max_close, date
                            FROM
                                (
                                    SELECT currency_id, MAX(close) as max_close
                                    FROM
                                        currencies_currencyprice
                                    GROUP BY
                                        currency_id
                                ) t1
                                JOIN currencies_currencyprice t2 ON t1.currency_id = t2.currency_id
                                AND t1.max_close = t2.close
                        ) t3
                        JOIN currencies_currency c ON c.id = t3.currency_id
                    WHERE
                        t3.date = %s""", [datetime.datetime.today().strftime('%Y-%m-%d')])
                    rows = cursor.fetchall()
                    currencies = []
                    for row in rows:
                        currencies.append({
                            "id": row[0],
                            "symbol": row[1],
                            "name": row[2],
                            "created_at": row[3]
                        })
                    return Response(currencies, status=status.HTTP_200_OK)
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
        currencies = Currency.objects.values("id", "symbol")
        data = []
        try:
            for currency in currencies:
                currency_price = CurrencyPrice.objects.filter(currency_id=currency["id"]).values_list("date").order_by(
                    "-date")
                currency_last_update = datetime.datetime.now() - datetime.timedelta(10 * 365)
                if len(currency_price) > 0:
                    currency_last_update = currency_price[0][0]
                prices = ex.fetch_ohlcv(currency["symbol"])
                for price in prices:
                    print(price[0], currency_last_update.timestamp()*1000)
                    if price[0] > currency_last_update.timestamp()*1000:
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


class CurrencyPriceDetailApiView(APIView):

    def get_object(self, currency__name):
        try:
            return CurrencyPrice.objects.filter(currency__name=currency__name).order_by('-date')
        except CurrencyPrice.DoesNotExist:
            return None

    def get(self, request, currency__name, *args, **kwargs):

        currency_instance = self.get_object(currency__name)
        if not currency_instance:
            return Response(
                {"res": "Object with currency id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = CurrencyPriceSerializer(currency_instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
