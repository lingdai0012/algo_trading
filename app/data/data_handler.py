import pandas as pd
from typing import List, Dict
from sqlalchemy import delete, insert
from sqlalchemy.orm import Session, InstrumentedAttribute
from binance import Client


class TimeSeriesDataHandler:
    def __init__(self, session: Session, client: Client) -> None:
        self._session = session
        self._client = client

    def _upsert_series_data(
        self,
        table,
        primary_key: InstrumentedAttribute,
        values: List[Dict],
        unique_keys: List[int] | None = None,
    ) -> None:
        if unique_keys is not None:
            stmt = delete(table).where(primary_key.in_(unique_keys))
            self._session.execute(stmt)
            self._session.flush()
        stmt = insert(table).values(values)
        self._session.execute(stmt)
        self._session.flush()
