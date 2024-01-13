from app import API_KEY, API_SECRETE
from binance import Client


client = Client(API_KEY, API_SECRETE)

klines = client.get_historical_klines(
    "BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, "10 Jan, 2024"
)

print(klines)
