from app.enum import KlinesInterval
from app.orm.database import ENGINE
from app.orm.models.base import Base
from app.orm.models.klines import *


KLINES_TABLE_MAPPER = {
    "BTCUSDT": {
        KlinesInterval.KLINE_INTERVAL_15MINUTE: SpotKlines15mBTCUSDT,
        KlinesInterval.KLINE_INTERVAL_5MINUTE: SpotKlines5mBTCUSDT,
        KlinesInterval.KLINE_INTERVAL_3MINUTE: SpotKlines3mBTCUSDT,
        KlinesInterval.KLINE_INTERVAL_1MINUTE: SpotKlines1mBTCUSDT,
    },
    "ETHUSDT": {
        KlinesInterval.KLINE_INTERVAL_15MINUTE: SpotKlines15mETHUSDT,
        KlinesInterval.KLINE_INTERVAL_5MINUTE: SpotKlines5mETHUSDT,
        KlinesInterval.KLINE_INTERVAL_3MINUTE: SpotKlines3mETHUSDT,
        KlinesInterval.KLINE_INTERVAL_1MINUTE: SpotKlines1mETHUSDT,
    },
}

KLINES_INTERVAL_MAPPER = {
    # seconds
    KlinesInterval.KLINE_INTERVAL_1MINUTE: 60,
    KlinesInterval.KLINE_INTERVAL_3MINUTE: 180,
    KlinesInterval.KLINE_INTERVAL_5MINUTE: 300,
    KlinesInterval.KLINE_INTERVAL_15MINUTE: 900,
    KlinesInterval.KLINE_INTERVAL_1DAY: 86400,
}

if __name__ == "__main__":
    Base.metadata.create_all(ENGINE)
