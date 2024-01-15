from functools import wraps
from app import DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

ENGINE = create_engine(DATABASE_URL)
SESSION = sessionmaker(bind=ENGINE, autoflush=False, autocommit=False)


def with_session(wrapped):
    @wraps(wrapped)
    def wrapper(*args, **kwargs):
        # Check if 'session' is already in kwargs
        if "session" in kwargs:
            # If 'session' is already present, call the function without modifying anything
            return wrapped(*args, **kwargs)

        # If 'session' is not in kwargs, add it by creating a new session
        with SESSION.begin() as session:
            return wrapped(*args, **kwargs, session=session)

    return wrapper
