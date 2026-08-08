"""
backend/app/services/drift_service.py

Why this file exists:
Provides business logic for scoring incoming SMS batches, persisting analysis runs to DB, and generating dashboard summaries.
"""

import uuid
import json
from datetime import datetime, date
from typing import List, Dict, Any, Optional
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.app.db.models import BatchRun, SMSMessage, DailyDrift
from ml.inference import SMSInferencePipeline
from backend.app.core.config import settings


class DriftService:
    """Service orchestrator for SMS drift analysis and database operations."""

    def __init__(self, inference_pipeline: SMSInferencePipeline):
        self.pipeline = inference_pipeline

    def process_and_save_batch(
        self,
        db: Session,
        messages_raw: List[Dict[str, str]],
        batch_name: str = "Ingested SMS Batch"
    ) -> Dict[str, Any]:
        """Runs ML inference on batch and persists results to database."""
        messages_text = [item.get("message", "") for item in messages_raw if item.get("message")]
        if not messages_text:
            raise ValueError("No valid non-empty SMS messages provided.")

        batch_id = f"batch_{uuid.uuid4().hex[:12]}"
        
        # 1. Run ML inference pipeline
        ml_results = self.pipeline.predict_batch(messages_text)

        # 2. Save BatchRun record
        batch_record = BatchRun(
            id=batch_id,
            batch_name=batch_name,
            total_messages=ml_results["total_messages"],
            anomaly_count=ml_results["anomaly_count"],
            anomaly_percentage=ml_results["anomaly_percentage"],
            avg_anomaly_score=ml_results["avg_anomaly_score"],
            drift_score=ml_results["drift_score"],
            drift_status=ml_results["drift_status"],
            created_at=datetime.utcnow()
        )
        db.add(batch_record)

        # 3. Save SMSMessage records
        message_objects = []
        for idx, item in enumerate(ml_results["all_results"]):
            raw_item = messages_raw[idx] if idx < len(messages_raw) else {}
            msg_obj = SMSMessage(
                batch_id=batch_id,
                label=raw_item.get("label", "unknown"),
                message=item["message"],
                char_length=item.get("char_length", len(item["message"])),
                digit_count=item.get("digit_count", 0),
                upper_ratio=item.get("upper_ratio", 0.0),
                special_char_ratio=item.get("special_char_ratio", 0.0),
                anomaly_score=item["anomaly_score"],
                is_anomaly=item["is_anomaly"],
                created_at=datetime.utcnow()
            )
            message_objects.append(msg_obj)

        db.add_all(message_objects)

        # 4. Upsert DailyDrift for today's date
        today_date = date.today()
        daily_record = db.query(DailyDrift).filter(DailyDrift.date == today_date).first()
        
        top_anomalies_json = json.dumps(ml_results["top_anomalies"])

        if daily_record:
            # Recompute aggregate metrics for today
            daily_record.total_messages += ml_results["total_messages"]
            daily_record.anomaly_count += ml_results["anomaly_count"]
            daily_record.anomaly_percentage = round((daily_record.anomaly_count / float(daily_record.total_messages)) * 100, 2)
            daily_record.avg_anomaly_score = round((daily_record.avg_anomaly_score + ml_results["avg_anomaly_score"]) / 2.0, 4)
            daily_record.drift_score = ml_results["drift_score"]
            daily_record.drift_status = ml_results["drift_status"]
            daily_record.top_anomalies_json = top_anomalies_json
        else:
            daily_record = DailyDrift(
                date=today_date,
                total_messages=ml_results["total_messages"],
                anomaly_count=ml_results["anomaly_count"],
                anomaly_percentage=ml_results["anomaly_percentage"],
                avg_anomaly_score=ml_results["avg_anomaly_score"],
                drift_score=ml_results["drift_score"],
                drift_status=ml_results["drift_status"],
                top_anomalies_json=top_anomalies_json,
                created_at=datetime.utcnow()
            )
            db.add(daily_record)

        db.commit()

        return {
            "batch_id": batch_id,
            "batch_name": batch_name,
            "total_messages": ml_results["total_messages"],
            "anomaly_count": ml_results["anomaly_count"],
            "anomaly_percentage": ml_results["anomaly_percentage"],
            "avg_anomaly_score": ml_results["avg_anomaly_score"],
            "drift_score": ml_results["drift_score"],
            "drift_status": ml_results["drift_status"],
            "created_at": batch_record.created_at.isoformat(),
            "top_anomalies": ml_results["top_anomalies"]
        }

    def get_drift_history(self, db: Session, limit: int = 30) -> List[Dict[str, Any]]:
        """Retrieve timeline history of daily drift scores."""
        records = db.query(DailyDrift).order_by(DailyDrift.date.desc()).limit(limit).all()
        results = []
        for rec in reversed(records):
            results.append({
                "id": rec.id,
                "date": rec.date.isoformat(),
                "total_messages": rec.total_messages,
                "anomaly_count": rec.anomaly_count,
                "anomaly_percentage": rec.anomaly_percentage,
                "avg_anomaly_score": rec.avg_anomaly_score,
                "drift_score": rec.drift_score,
                "drift_status": rec.drift_status
            })
        return results

    def get_anomalies(self, db: Session, limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieve top anomalous messages ordered by anomaly_score descending."""
        messages = db.query(SMSMessage).filter(SMSMessage.is_anomaly == True)\
            .order_by(SMSMessage.anomaly_score.desc()).limit(limit).all()
        
        results = []
        for idx, msg in enumerate(messages):
            results.append({
                "message_id": msg.id,
                "message": msg.message,
                "anomaly_score": msg.anomaly_score,
                "is_anomaly": msg.is_anomaly,
                "char_length": msg.char_length,
                "digit_count": msg.digit_count,
                "upper_ratio": msg.upper_ratio,
                "special_char_ratio": msg.special_char_ratio
            })
        return results

    def get_dashboard_summary(self, db: Session) -> Dict[str, Any]:
        """Aggregate summary metrics for the main dashboard."""
        total_msgs = db.query(func.sum(DailyDrift.total_messages)).scalar() or 0
        total_anoms = db.query(func.sum(DailyDrift.anomaly_count)).scalar() or 0
        
        latest_drift = db.query(DailyDrift).order_by(DailyDrift.date.desc()).first()
        
        latest_score = latest_drift.drift_score if latest_drift else 0.0
        latest_status = latest_drift.drift_status if latest_drift else "NORMAL TRAFFIC"

        overall_anomaly_pct = round((total_anoms / float(total_msgs)) * 100, 2) if total_msgs > 0 else 0.0

        daily_history = self.get_drift_history(db, limit=90)
        top_suspicious = self.get_anomalies(db, limit=10)

        return {
            "total_messages_analyzed": int(total_msgs),
            "total_anomalies_detected": int(total_anoms),
            "latest_drift_score": float(latest_score),
            "latest_drift_status": latest_status,
            "overall_anomaly_percentage": overall_anomaly_pct,
            "drift_threshold": settings.DRIFT_THRESHOLD,
            "daily_trend": daily_history,
            "top_suspicious_messages": top_suspicious
        }
