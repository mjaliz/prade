import ccxt
import time
import pandas as pd
import yfinance


class Exchange:
    def __init__(self):
        self._exchange = ccxt.kucoin()

    def load_markets(self):
        return self._exchange.load_markets()

    def fetch_ohlcv(self, symbol):
        if self._exchange.has['fetchOHLCV']:
            time.sleep(3)  # time.sleep wants seconds
            # one day
            return self._exchange.fetch_ohlcv(symbol, '1d', limit=500)

    def yf(self):
        return yfinance.download(tickers="BTC-USD", interval='1d', ignore_tz=True)


if __name__ == "__main__":
    ex = Exchange()
    print(ex.yf())
