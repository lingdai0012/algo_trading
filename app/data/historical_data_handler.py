import pandas as pd
import polars as pl
import numpy as np
from binance import Client
from sqlalchemy.orm import Session
from app.data.data_handler import TimeSeriesDataHandler
from app.enum import KlinesInterval
from app.orm.models import KLINES_TABLE_MAPPER


class HistoricalDataHandler(TimeSeriesDataHandler):
    def __init__(self, session: Session, client: Client) -> None:
        super().__init__(session=session, client=client)

    def upsert_historical_kline_data(
        self,
        symbol: str,
        kline_interval: KlinesInterval = KlinesInterval.KLINE_INTERVAL_15MINUTE,
        start_utc: str | None = None,
        end_utc: str | None = None,
    ) -> int:
        values = self._client.get_historical_klines(
            symbol=symbol,
            interval=kline_interval.value,
            start_str=start_utc,
            end_str=end_utc,
        )
        values = np.array(values)[:, :-1]
        target_table = KLINES_TABLE_MAPPER[symbol][kline_interval]
        columns = target_table.__table__.columns
        values = {columns[ii].name: values[:, ii] for ii in range(len(columns))}
        values = pl.DataFrame(values).cast(pl.Float64)  # remove field ignore
        self._upsert_series_data(
            table=target_table,
            primary_key=target_table.open_time,
            values=values.to_dicts(),
            unique_keys=values["open_time"].to_list(),
        )
        return values["close_time"][-1]
