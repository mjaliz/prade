import ccxt
import time
import pandas as pd


class Exchange:
    def __init__(self):
        self._exchange = ccxt.kucoin()

    def load_markets(self):
        return self._exchange.load_markets()

    def fetch_ohlcv(self, symbol):
        if self._exchange.has['fetchOHLCV']:
            markets = self.load_markets()
            time.sleep(self._exchange.rateLimit / 1000)  # time.sleep wants seconds
            return self._exchange.fetch_ohlcv(symbol, '1d', limit=500)  # one day


if __name__ == "__main__":
    ex = Exchange()
    print(ex.fetch_ohlcv("BTC/USDT"))
