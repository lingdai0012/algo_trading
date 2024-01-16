from dataclasses import dataclass
from app.enum import KlinesInterval


@dataclass
class LoadingHistoricalDataDependencies:
    symbol: str
    klines_interval: KlinesInterval
