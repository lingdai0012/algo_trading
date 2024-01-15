import logging
import binance
from datetime import timedelta
from sqlalchemy.orm import Session
from app import API_KEY, API_SECRETE
from app.helper import (
    KLINES_RECORD_START,
    KLINES_RECORD_END,
    BINANCE_DATE_FORMAT,
)
from app.orm.database import with_session
from app.data import HistoricalDataHandler
from app.functions.arguments import LoadingHistoricalDataDependencies

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


@with_session
def loading_historical_data(
    event: LoadingHistoricalDataDependencies, session: Session
) -> None:
    client = binance.Client(api_key=API_KEY, api_secret=API_SECRETE)
    historical_data_handler = HistoricalDataHandler(session=session, client=client)
    start_timestamp = KLINES_RECORD_START

    while start_timestamp < KLINES_RECORD_END:
        logging.info(
            f"Processing data for {start_timestamp.strftime(BINANCE_DATE_FORMAT)}"
        )
        # Move to the next 10-day chunk
        end_timestamp = start_timestamp + timedelta(days=10)
        # Upsert historical kline data
        historical_data_handler.upsert_historical_kline_data(
            symbol=event.symbol,
            kline_interval=event.kline_interval,
            start_utc=start_timestamp.strftime(BINANCE_DATE_FORMAT),
            end_utc=end_timestamp.strftime(BINANCE_DATE_FORMAT),
        )
        start_timestamp = end_timestamp
    logging.info("Loading historical data completed.")
    return


if __name__ == "__main__":
    from app.enum.kline_interval import KlineInterval
    from app.orm.database import SESSION

    # Define loading event
    event = LoadingHistoricalDataDependencies(
        symbol="BTCUSDT", kline_interval=KlineInterval.KLINE_INTERVAL_15MINUTE
    )

    # Execute loading_historical_data with a database session
    with SESSION.begin() as session:
        logging.info("Starting loading process...")
        loading_historical_data(event, session=session)
