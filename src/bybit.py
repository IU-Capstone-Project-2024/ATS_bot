from pybit.unified_trading import HTTP
import uuid
import pandas as pd
import config


class BybitAPI:
    def __init__(self):
        self.api_key = config.BYBIT_API_KEY
        self.secret_key = config.BYBIT_API_SECRET
        self.client = HTTP(testnet=True, api_key=self.api_key, api_secret=self.secret_key)

    def create_order(self, payload):
        response = self.client.place_order(**payload)
        return response

    def get_unfilled_orders(self, category: str, symbol: str, open_only: int = 0, limit: int = 1):
        payload = {
            "category": category,
            "symbol": symbol,
            "openOnly": open_only,
            "limit": limit
        }
        response = self.client.get_open_orders(category=category, symbol=symbol, openOnly=open_only, limit=limit)
        return response

    def cancel_order(self, category: str, symbol: str, order_link_id: str):
        payload = {
            "category": category,
            "symbol": symbol,
            "orderLinkId": order_link_id
        }
        response = self.client.cancel_order(**payload)
        return response

    def get_historical_data(self, symbol: str, interval: str, start_time: int, limit: int = 200):
        params = {
            "category": "linear",
            "symbol": symbol,
            "interval": interval,
            "start": start_time,
            "limit": limit
        }
        response = self.client.get_kline(**params)
        data = response['result']['list']
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        return df
