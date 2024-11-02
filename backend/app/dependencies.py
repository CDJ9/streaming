# app/dependencies.py

"""
This file contains the SQLAlchemy engine and session maker
used to connect to the MySQL database.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.settings import settings

# Create the SQLAlchemy engine using MySQL
engine = create_engine(settings.database_url)

# Session factory for creating new database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Dependency to provide a database session to request handlers.
    Ensures the session is closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
