import wrapt
from app import DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

ENGINE = create_engine(DATABASE_URL)
SESSION = sessionmaker(bind=ENGINE, autoflush=False, autocommit=False)


@wrapt.decorator
def with_session(wrapped, *args, **kwargs):
    # If 'session' is not in kwargs, add it by creating a new session
    with SESSION.begin() as session:
        kwargs.update({"session": session})
        return wrapped(*args, **kwargs)
