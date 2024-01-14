import pandas as pd
from typing import List, Dict, Any
from sqlalchemy.orm import Session, InstrumentedAttribute, DeclarativeBase
from sqlalchemy.dialects.postgresql import insert
from binance import Client


class DataHandler:
    def __init__(self, session: Session, client: Client) -> None:
        self._session = session
        self._client = client

    def _upsert_data(
        self,
        table: DeclarativeBase,
        index_elements: List[InstrumentedAttribute],
        values: List[Dict],
    ) -> None:
        stmt = insert(table).values(values)
        for value in values:
            stmt = stmt.on_conflict_do_update(index_elements=index_elements, set_=value)
        self._session.execute(stmt)
        self._session.flush()
