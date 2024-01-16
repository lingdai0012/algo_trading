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
from app.orm.models import KLINES_INTERVAL_MAPPER
from app.orm.database import with_session
from app.data import HistoricalDataHandler
from app.functions.arguments import LoadingHistoricalDataDependencies


@with_session
def loading_historical_data(
    event: LoadingHistoricalDataDependencies, session: Session
) -> None:
    client = binance.Client(api_key=API_KEY, api_secret=API_SECRETE)
    historical_data_handler = HistoricalDataHandler(session=session, client=client)
    # Record start
    start_timestamp = KLINES_RECORD_START
    # Interval for one thousand record, seconds
    per_thousand_records_interval = KLINES_INTERVAL_MAPPER[event.klines_interval] * 1000
    while start_timestamp < KLINES_RECORD_END:  # Up to today
        logging.info(
            f"Processing data for {event.symbol} {event.klines_interval.value}: {start_timestamp.strftime(BINANCE_DATE_FORMAT)}"
        )
        # Move to the next chunk
        end_timestamp = start_timestamp + timedelta(
            seconds=per_thousand_records_interval
        )  # To fullfil the max records limit (1000)
        # Upsert historical kline data
        historical_data_handler.upsert_historical_kline_data(
            symbol=event.symbol,
            kline_interval=event.klines_interval,
            start_utc=start_timestamp.strftime(BINANCE_DATE_FORMAT),
            end_utc=end_timestamp.strftime(BINANCE_DATE_FORMAT),
        )
        start_timestamp = end_timestamp
    logging.info(
        f"Loading historical data for {event.symbol} {event.klines_interval.value} completed."
    )
    return


if __name__ == "__main__":
    from itertools import product
    import threading
    from app.enum.kline_interval import KlinesInterval
    from app.orm.database import SESSION

    tickers = ["ETHUSDT"]
    klines_intervals = [
        # KlinesInterval.KLINE_INTERVAL_1MINUTE,
        KlinesInterval.KLINE_INTERVAL_3MINUTE,
        # KlinesInterval.KLINE_INTERVAL_5MINUTE,
        # KlinesInterval.KLINE_INTERVAL_15MINUTE,
    ]
    with SESSION.begin() as session:
        logging.info("Starting loading process...")
        threads = []

        for ticker, klines_interval in product(tickers, klines_intervals):
            thread = threading.Thread(
                target=loading_historical_data,
                args=(
                    LoadingHistoricalDataDependencies(
                        symbol=ticker, klines_interval=klines_interval
                    ),
                ),
                kwargs={"session": session},
            )
            threads.append(thread)
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()
