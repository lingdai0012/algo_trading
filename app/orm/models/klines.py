from sqlalchemy import BIGINT, Column
from sqlalchemy.orm import Mapped, mapped_column
from app.orm.database import ENGINE
from app.orm.models.base import Base


class Klines:
    open_time = Column(BIGINT, primary_key=True)
    open: Mapped[float] = mapped_column(nullable=True)
    high: Mapped[float] = mapped_column(nullable=True)
    low: Mapped[float] = mapped_column(nullable=True)
    close: Mapped[float] = mapped_column(nullable=True)
    volume: Mapped[float] = mapped_column(nullable=True)
    close_time = Column(BIGINT, nullable=False)
    base_asset_volume: Mapped[float] = mapped_column(nullable=True)
    number_of_trades: Mapped[int] = mapped_column(nullable=True)
    taker_buy_volume: Mapped[float] = mapped_column(nullable=True)
    taker_buy_base_asset_volume: Mapped[float] = mapped_column(nullable=True)


class SpotKlines15mBTCUSDT(Base, Klines):
    __tablename__ = "t_spot_klines_15m_btc_usdt"
