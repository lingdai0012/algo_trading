import wrapt
from app import DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

ENGINE = create_engine(DATABASE_URL)
SESSION = sessionmaker(bind=ENGINE, autoflush=False, autocommit=False)


@wrapt.decorator
def with_session(wrapped, instance, args, kwargs):
    with SESSION.begin() as session:
        return wrapped(*args, **kwargs, session=session)
