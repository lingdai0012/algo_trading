from dataclasses import dataclass
from app.enum import KlineInterval


@dataclass
class LoadingHistoricalDataDependencies:
    symbol: str
    kline_interval: KlineInterval
