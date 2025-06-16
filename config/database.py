from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# Load environment variables from .env file
try:
    load_dotenv()
except:
    pass

# Read the database URL from the environment variable
DATABASE_URL = os.getenv("DATABASE_URL")
# Create the SQLAlchemy engine with the database URL
engine = create_engine(DATABASE_URL)
# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base is the base class for all the SQLAlchemy ORM models.
# It tells SQLAlchemy that a model maps to a real table.
# Without inheriting from Base, the class won’t be recognized by SQLAlchemy’s ORM.
Base = declarative_base()

# Dependency to get a DB session for FastAPI routes (used in controllers)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
