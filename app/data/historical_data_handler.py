import pandas as pd
from typing import List, Dict
from binance import Client
from sqlalchemy.orm import Session
from app.data.data_handler import DataHandler
from app.enum import KlineInterval
from app.orm.models import KLINES_MAPPER


class HistoricalDataHandler(DataHandler):
    def __init__(self, session: Session, client: Client) -> None:
        super().__init__(session=session, client=client)

    def upsert_historical_kline_data(
        self,
        symbol: str,
        kline_interval: KlineInterval = KlineInterval.KLINE_INTERVAL_15MINUTE,
        start_timestamp: int | None = None,
        end_timestamp: int | None = None,
    ):
        values = self._client.get_historical_klines(
            symbol=symbol,
            interval=kline_interval.value,
            start_str=start_timestamp,
            end_str=end_timestamp,
        )
        target_table = KLINES_MAPPER[symbol][kline_interval]
        columns = target_table.__table__.columns
        columns = [col for col in columns]
        values = pd.DataFrame(pd.to_numeric(values), columns=columns)
        values = values.to_dict(orient="records")
        self._upsert_data(
            table=target_table, index_elements=[target_table.open_time], values=values
        )
        return
