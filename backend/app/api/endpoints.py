"""
backend/app/api/endpoints.py

Why this file exists:
Exposes REST API routes for ingestion, ML drift scoring, anomaly filtering, dashboard data, and model specifications.
"""

import io
import pandas as pd
from typing import List, Optional
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Body, Request
from sqlalchemy.orm import Session

from backend.app.db.database import get_db
from backend.app.services.drift_service import DriftService
from backend.app.schemas.drift import (
    BatchIngestPayload,
    BatchAnalysisResult,
    DailyDriftRecord,
    MessageScoreDetail,
    DashboardSummary,
    ModelInfoResponse
)

router = APIRouter()

# Global drift service instance injected at application startup
drift_service_instance: Optional[DriftService] = None


def get_drift_service() -> DriftService:
    """Dependency provider for DriftService."""
    if drift_service_instance is None:
        raise HTTPException(status_code=500, detail="DriftService not initialized!")
    return drift_service_instance


@router.post("/ingest", response_model=BatchAnalysisResult, summary="Upload daily SMS batch")
async def ingest_batch(
    request: Request,
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    service: DriftService = Depends(get_drift_service)
):
    """
    Ingest a batch of raw SMS messages via CSV upload or JSON body, run ML drift detection,
    and persist results into database tables.
    """
    raw_messages = []
    batch_name = "SMS Batch"

    content_type = request.headers.get("content-type", "")

    if "multipart/form-data" in content_type and file:
        batch_name = file.filename or "Uploaded CSV Batch"
        contents = await file.read()
        try:
            df = pd.read_csv(io.BytesIO(contents))
            col = "message" if "message" in df.columns else ("text" if "text" in df.columns else df.columns[0])
            for _, row in df.iterrows():
                lbl = str(row.get("label", "unknown")) if "label" in df.columns else "unknown"
                raw_messages.append({"message": str(row[col]), "label": lbl})
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid CSV file format: {str(e)}")
    elif "application/json" in content_type:
        try:
            body = await request.json()
            payload = BatchIngestPayload(**body)
            batch_name = payload.batch_name or "JSON Batch"
            for item in payload.messages:
                raw_messages.append({"message": item.message, "label": item.label or "unknown"})
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid JSON payload: {str(e)}")
    else:
        raise HTTPException(status_code=400, detail="Provide either a CSV file upload or JSON payload with messages.")

    if not raw_messages:
        raise HTTPException(status_code=400, detail="No valid messages found in batch.")

    try:
        result = service.process_and_save_batch(db, raw_messages, batch_name=batch_name)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process batch: {str(e)}")


@router.post("/analyze", response_model=BatchAnalysisResult, summary="Run drift analysis")
async def analyze_batch(
    payload: BatchIngestPayload,
    db: Session = Depends(get_db),
    service: DriftService = Depends(get_drift_service)
):
    """Run drift analysis on incoming message array."""
    raw_messages = [{"message": item.message, "label": item.label or "unknown"} for item in payload.messages]
    return service.process_and_save_batch(db, raw_messages, batch_name=payload.batch_name or "Analyzed Batch")


@router.get("/drift", response_model=List[DailyDriftRecord], summary="Return drift history")
def get_drift_history(
    limit: int = 30,
    db: Session = Depends(get_db),
    service: DriftService = Depends(get_drift_service)
):
    """Return historical daily drift scores timeline."""
    return service.get_drift_history(db, limit=limit)


@router.get("/anomalies", response_model=List[MessageScoreDetail], summary="Return anomalous messages")
def get_anomalies(
    limit: int = 50,
    db: Session = Depends(get_db),
    service: DriftService = Depends(get_drift_service)
):
    """Return top anomalous messages sorted by anomaly score descending."""
    return service.get_anomalies(db, limit=limit)


@router.get("/dashboard", response_model=DashboardSummary, summary="Return dashboard overview data")
def get_dashboard_data(
    db: Session = Depends(get_db),
    service: DriftService = Depends(get_drift_service)
):
    """Return comprehensive dashboard data: KPIs, daily trend, top suspicious messages, and alert status."""
    return service.get_dashboard_summary(db)


@router.get("/ml/model-info", response_model=ModelInfoResponse, summary="Get ML baseline model information")
def get_model_info(service: DriftService = Depends(get_drift_service)):
    """Return active model metadata and architecture specifications."""
    meta = service.pipeline.metadata
    return {
        "model_name": meta.get("model_name", "SMS-Shield-IsolationForest-SVD"),
        "pipeline_type": "Unsupervised Anomaly & Distribution Drift Monitoring Pipeline",
        "vectorizer": {
            "analyzer": "char",
            "ngram_range": meta.get("ngram_range", [3, 5]),
            "max_features": meta.get("max_features", 5000)
        },
        "svd": {
            "n_components": meta.get("svd_n_components", 100),
            "algorithm": "TruncatedSVD (Randomized SVD)"
        },
        "isolation_forest": {
            "n_estimators": meta.get("n_estimators", 150),
            "contamination": meta.get("contamination", 0.05)
        },
        "baseline_ham_samples": meta.get("train_samples_count", 4827),
        "drift_threshold": service.pipeline.drift_threshold,
        "justification_svd_vs_pca": (
            "TruncatedSVD is preferred over PCA because character N-Gram TF-IDF produces highly sparse matrices. "
            "Standard PCA requires explicit mean-centering, which converts sparse matrices into dense matrices ($O(N \\cdot D)$), "
            "destroying sparsity and leading to high memory consumption. TruncatedSVD operates directly on sparse matrices."
        )
    }


@router.post("/score/demo", response_model=BatchAnalysisResult, summary="Run scoring on demo dataset")
def score_demo(
    db: Session = Depends(get_db),
    service: DriftService = Depends(get_drift_service)
):
    """Inject and score a synthetic SMS batch representing an emerging spam campaign shift."""
    demo_messages = [
        {"message": "Hey John, are we meeting at the coffee shop today?", "label": "ham"},
        {"message": "Please review the attached project document when free.", "label": "ham"},
        {"message": "fr33 cl1ck h3r3 to w1n $$$ cash prize now!!! Call 0800999888!", "label": "spam"},
        {"message": "URGENT! Your bank account 4829 has been locked. Click http://bank-secure-update.com", "label": "spam"},
        {"message": "FREE GIFT CARD! Cl1ck now to claim $1000 Amazon voucher: http://bit.ly/claim-free", "label": "spam"},
        {"message": "Don't forget to buy milk on your way home.", "label": "ham"},
        {"message": "WINNER! You have won 500000USD. Reply WIN to claim now!", "label": "spam"}
    ]
    return service.process_and_save_batch(db, demo_messages, batch_name="Demo Emerging Campaign Batch")


@router.get("/health", summary="Health check endpoint")
def health_check():
    """Backend service health check."""
    return {"status": "healthy", "service": "SMS Shield Backend API"}
