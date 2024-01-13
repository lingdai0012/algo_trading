from app.orm.database import ENGINE
from app.orm.models.base import Base
from app.orm.models.klines import SpotKlines15mBTCUSDT


if __name__ == "__main__":
    Base.metadata.create_all(ENGINE)
