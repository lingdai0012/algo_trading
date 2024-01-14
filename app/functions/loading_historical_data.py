import binance
from sqlalchemy.orm import Session
from app import API_KEY, API_SECRETE
from app.orm.database import with_session
from app.data import HistoricalDataHandler
from app.functions.arguments import LoadingHistoricalDataDependencies


@with_session
def loading_historical_data(
    event: LoadingHistoricalDataDependencies, session: Session
) -> None:
    client = binance.Client(api_key=API_KEY, api_secret=API_SECRETE)
    historical_data_handler = HistoricalDataHandler(session=session, client=client)
    historical_data_handler.upsert_historical_kline_data(
        symbol=event.symbol,
        kline_interval=event.kline_interval,
        start_timestamp=event.start_timestamp,
        end_timestamp=event.end_timestamp,
    )
    pass


if __name__ == "__main__":
    from app.enum.kline_interval import KlineInterval
    from app.orm.database import SESSION

    event = LoadingHistoricalDataDependencies(
        symbol="BTCUSDT", kline_interval=KlineInterval.KLINE_INTERVAL_15MINUTE
    )
    loading_historical_data(event)
