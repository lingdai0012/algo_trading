from datetime import datetime

BINANCE_DATE_FORMAT = "%d %b, %Y"
KLINES_RECORD_START = datetime.strptime("27 Aug, 2017", BINANCE_DATE_FORMAT)
KLINES_RECORD_END = datetime.utcnow()
