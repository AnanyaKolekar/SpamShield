"""
backend/app/db/models.py

Why this file exists:
Defines SQLAlchemy ORM domain models matching the database schema requirements:
- SMSMessage: Stores per-message text, statistical features, and anomaly score
- DailyDrift: Stores aggregated daily drift score, anomaly counts, status, and top anomalies JSON
- BaselineModel: Stores baseline ML configuration and metadata
- BatchRun: Stores batch-level scoring run metrics
"""

from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.db.database import Base


class BatchRun(Base):
    """Batch run summary table."""
    __tablename__ = "batch_runs"

    id = Column(String(64), primary_key=True)
    batch_name = Column(String(255), nullable=False)
    total_messages = Column(Integer, default=0, nullable=False)
    anomaly_count = Column(Integer, default=0, nullable=False)
    anomaly_percentage = Column(Float, default=0.0, nullable=False)
    avg_anomaly_score = Column(Float, default=0.0, nullable=False)
    drift_score = Column(Float, default=0.0, nullable=False)
    drift_status = Column(String(50), default="NORMAL TRAFFIC", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    messages = relationship("SMSMessage", back_populates="batch", cascade="all, delete-orphan")


class SMSMessage(Base):
    """SMS message table storing text, engineered features, and anomaly score."""
    __tablename__ = "sms_messages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    batch_id = Column(String(64), ForeignKey("batch_runs.id"), nullable=True, index=True)
    label = Column(String(20), default="unknown")
    message = Column(Text, nullable=False)
    char_length = Column(Integer, default=0)
    digit_count = Column(Integer, default=0)
    upper_ratio = Column(Float, default=0.0)
    special_char_ratio = Column(Float, default=0.0)
    anomaly_score = Column(Float, default=0.0, index=True)
    is_anomaly = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    batch = relationship("BatchRun", back_populates="messages")


class DailyDrift(Base):
    """Daily drift aggregation table."""
    __tablename__ = "daily_drift"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(Date, unique=True, nullable=False, index=True)
    total_messages = Column(Integer, default=0, nullable=False)
    anomaly_count = Column(Integer, default=0, nullable=False)
    anomaly_percentage = Column(Float, default=0.0, nullable=False)
    avg_anomaly_score = Column(Float, default=0.0, nullable=False)
    drift_score = Column(Float, default=0.0, nullable=False)
    drift_status = Column(String(50), default="NORMAL TRAFFIC", nullable=False)
    top_anomalies_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class BaselineModel(Base):
    """Baseline model configuration and tracking table."""
    __tablename__ = "baseline_models"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    model_name = Column(String(100), nullable=False)
    ngram_min = Column(Integer, default=3)
    ngram_max = Column(Integer, default=5)
    max_features = Column(Integer, default=5000)
    svd_components = Column(Integer, default=100)
    contamination = Column(Float, default=0.05)
    ham_train_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
