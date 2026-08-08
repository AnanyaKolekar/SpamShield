"""
backend/app/core/config.py

Why this file exists:
Centralizes application settings, environment variable management, CORS policies, database connection strings, and ML model paths.
"""

import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "SMS Shield - Drift Monitoring & Emerging Campaign Detection"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Database Settings
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "sms_shield")
    
    # Primary DB URL (PostgreSQL) or fallback SQLite
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )
    SQLITE_FALLBACK_URL: str = "sqlite:///./database/sms_shield.db"

    # ML Settings
    MODELS_DIR: str = os.getenv("MODELS_DIR", "models")
    DATA_DIR: str = os.getenv("DATA_DIR", "data")
    DRIFT_THRESHOLD: float = float(os.getenv("DRIFT_THRESHOLD", "0.35"))

    # CORS Settings
    CORS_ORIGINS: List[str] = ["*"]

    class Config:
        case_sensitive = True


settings = Settings()
