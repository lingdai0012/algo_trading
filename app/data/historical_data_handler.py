import pandas as pd
from typing import List, Dict
from binance import Client
from sqlalchemy import Session, insert
from app import API_KEY, API_SECRETE
from app.orm.models import Base


class HistoricalDataHandler:
    def __init__(
        self,
        session: Session,
        client: Client,
    ) -> None:
        self._session = session
        self._client = client

    def upsert_historical_data(self, values: List[Dict]) -> None:
        klines = self._client.get_historical_klines(
            "BTCUSDT", Client.KLINE_INTERVAL_15MINUTE, "13 Jan, 2024"
        )
        klines = pd.DataFrame(
            klines,
            columns=[
                "open_time",
                "open",
                "high",
                "low",
                "close",
                "volume",
                "close_time",
                "base_asset_volume",
                "number_of_trades",
                "taker_buy_volume",
                "taker_buy_base_asset_volume",
                "ignore",
            ],
        )
        klines[
            [
                "open",
                "high",
                "low",
                "close",
                "volume",
                "base_asset_volume",
                "number_of_trades",
                "taker_buy_volume",
                "taker_buy_base_asset_volume",
            ]
        ] = klines[
            [
                "open",
                "high",
                "low",
                "close",
                "volume",
                "base_asset_volume",
                "number_of_trades",
                "taker_buy_volume",
                "taker_buy_base_asset_volume",
            ]
        ].astype(
            float
        )
        return
