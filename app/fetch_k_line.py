from binance import Client
from app.settings_local import API_KEY, API_SECRETE

client = Client(API_KEY, API_SECRETE)

klines = client.get_historical_klines(
    "BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, "10 Jan, 2024"
)
print(klines)
