"""
backend/app/schemas/drift.py

Why this file exists:
Defines Pydantic schemas for request payload validation and API response serialization across all endpoints:
- IngestRequest & IngestResponse
- AnalyzeResponse
- DriftHistoryResponse
- AnomaliesResponse
- DashboardDataResponse
- ModelInfoResponse
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, date
from pydantic import BaseModel, Field


class SMSItem(BaseModel):
    message: str
    label: Optional[str] = "unknown"


class BatchIngestPayload(BaseModel):
    batch_name: Optional[str] = "Daily SMS Batch"
    messages: List[SMSItem]


class MessageScoreDetail(BaseModel):
    message_id: int
    message: str
    anomaly_score: float
    is_anomaly: bool
    char_length: Optional[int] = 0
    digit_count: Optional[int] = 0
    upper_ratio: Optional[float] = 0.0
    special_char_ratio: Optional[float] = 0.0


class BatchAnalysisResult(BaseModel):
    batch_id: str
    batch_name: str
    total_messages: int
    anomaly_count: int
    anomaly_percentage: float
    avg_anomaly_score: float
    drift_score: float
    drift_status: str
    created_at: str
    top_anomalies: List[MessageScoreDetail]


class DailyDriftRecord(BaseModel):
    id: int
    date: str
    total_messages: int
    anomaly_count: int
    anomaly_percentage: float
    avg_anomaly_score: float
    drift_score: float
    drift_status: str


class DashboardSummary(BaseModel):
    total_messages_analyzed: int
    total_anomalies_detected: int
    latest_drift_score: float
    latest_drift_status: str
    overall_anomaly_percentage: float
    drift_threshold: float
    daily_trend: List[DailyDriftRecord]
    top_suspicious_messages: List[MessageScoreDetail]


class ModelInfoResponse(BaseModel):
    model_name: str
    pipeline_type: str
    vectorizer: Dict[str, Any]
    svd: Dict[str, Any]
    isolation_forest: Dict[str, Any]
    baseline_ham_samples: int
    drift_threshold: float
    justification_svd_vs_pca: str
