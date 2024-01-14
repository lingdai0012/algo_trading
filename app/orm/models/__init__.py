from app.enum import KlineInterval
from app.orm.database import ENGINE
from app.orm.models.base import Base
from app.orm.models.klines import SpotKlines15mBTCUSDT, Klines


# TODO: To be optimized to use namedtuple as the key to handle more combinations of keys
KLINES_MAPPER = {
    "BTCUSDT": {KlineInterval.KLINE_INTERVAL_15MINUTE: SpotKlines15mBTCUSDT}
}

if __name__ == "__main__":
    Base.metadata.create_all(ENGINE)
