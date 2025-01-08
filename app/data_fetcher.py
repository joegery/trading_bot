import ccxt
import pandas as pd

class DataFetcher:
    def __init__(self):
        # Change the exchange here
        self.exchange = ccxt.kraken()

    def fetch_historical_data(self, symbol: str, timeframe: str, since: int):
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, since)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            return df
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None
