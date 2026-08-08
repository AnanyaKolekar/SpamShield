"""
backend/app/db/database.py

Why this file exists:
Manages SQLAlchemy engine initialization, database sessions, and table creation.
Supports PostgreSQL (for production/Docker) and automatically falls back to SQLite for local standalone development.
"""

import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from backend.app.core.config import settings

logger = logging.getLogger(__name__)

os.makedirs("database", exist_ok=True)

Base = declarative_base()


def init_db_engine():
    """Initialize database engine with PostgreSQL fallback to SQLite."""
    try:
        engine = create_engine(
            settings.DATABASE_URL,
            pool_pre_ping=True,
            connect_args={"connect_timeout": 3}
        )
        # Test connection
        with engine.connect() as conn:
            logger.info("Successfully connected to PostgreSQL Database!")
        return engine
    except Exception as e:
        logger.warning(f"PostgreSQL connection failed ({e}). Falling back to SQLite database at {settings.SQLITE_FALLBACK_URL}...")
        engine = create_engine(
            settings.SQLITE_FALLBACK_URL,
            connect_args={"check_same_thread": False}
        )
        return engine


engine = init_db_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Dependency yield generator for database sessions in FastAPI."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Create all defined ORM tables."""
    Base.metadata.create_all(bind=engine)
