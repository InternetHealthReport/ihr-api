from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os
from dotenv import load_dotenv
import warnings

# Load environment variables from .env file
try:
    load_dotenv()
except:
    pass

POOL_SIZE = int(os.getenv("POOL_SIZE"))
MAX_OVERFLOW = int(os.getenv("MAX_OVERFLOW"))
POOL_TIMEOUT = int(os.getenv("POOL_TIMEOUT"))
POOL_RECYCLE = int(os.getenv("POOL_RECYCLE"))
REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT"))
_statement_timeout_ms = int(REQUEST_TIMEOUT * 1000)

# Read the database URL from the environment variable
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is not None:
    # Create the SQLAlchemy engine with the database URL.
    # pool_size / max_overflow cap concurrent DB connections so one slow
    # query can't starve the whole server.  statement_timeout kills any
    # single query that runs longer than N sec so a runaway request doesn't
    # hold a connection indefinitely.
    engine = create_engine(
    DATABASE_URL,
        pool_size=POOL_SIZE,
        max_overflow=MAX_OVERFLOW,
        pool_timeout=POOL_TIMEOUT,
        pool_recycle=POOL_RECYCLE,
        pool_pre_ping=True,
        connect_args={"options": f"-c statement_timeout={_statement_timeout_ms}"},
    )
    # Create a session factory
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
else:
    warnings.warn("DATABASE_URL is not configured in the ENV")

# Base is the base class for all the SQLAlchemy ORM models.
# It tells SQLAlchemy that a model maps to a real table.
# Without inheriting from Base, the class won’t be recognized by SQLAlchemy’s ORM.
class Base(DeclarativeBase):
    pass

# Dependency to get a DB session for FastAPI routes (used in controllers)
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
