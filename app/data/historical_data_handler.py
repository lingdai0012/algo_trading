import pandas as pd
import numpy as np
from binance import Client
from sqlalchemy.orm import Session
from app.data.data_handler import TimeSeriesDataHandler
from app.enum import KlineInterval
from app.orm.models import KLINES_MAPPER


class HistoricalDataHandler(TimeSeriesDataHandler):
    def __init__(self, session: Session, client: Client) -> None:
        super().__init__(session=session, client=client)

    def upsert_historical_kline_data(
        self,
        symbol: str,
        kline_interval: KlineInterval = KlineInterval.KLINE_INTERVAL_15MINUTE,
        start_utc: str | None = None,
        end_utc: str | None = None,
    ) -> int:
        values = self._client.get_historical_klines(
            symbol=symbol,
            interval=kline_interval.value,
            start_str=start_utc,
            end_str=end_utc,
        )
        target_table = KLINES_MAPPER[symbol][kline_interval]
        columns = target_table.__table__.columns
        columns = [col.name for col in columns]
        values = pd.DataFrame(np.array(values)[:, :-1], columns=columns).astype(
            float
        )  # remove field ignore
        self._upsert_series_data(
            table=target_table,
            primary_key=target_table.open_time,
            values=values.to_dict(orient="records"),
            unique_keys=values["open_time"].tolist(),
        )
        return values["close_time"].iloc[-1]
