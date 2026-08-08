"""
ml/drift_detector.py

Why this file exists:
This module calculates per-message anomaly scores, identifies suspicious SMS messages, and computes overall batch drift metrics.
- Computes per-message anomaly score normalized between 0.0 (normal) and 1.0 (highly anomalous)
- Computes Daily Drift Score: percentage of anomalous messages + average anomaly score
- Determines Alert Status: 'HIGH DRIFT DETECTED' if drift score > threshold, else 'NORMAL TRAFFIC'
"""

from typing import List, Dict, Any
import numpy as np


class SMSDriftDetector:
    """Calculates anomaly scores, drift metrics, and alert triggers for SMS batches."""

    def __init__(self, drift_threshold: float = 0.35, baseline_score_mean: float = -0.42):
        self.drift_threshold = drift_threshold
        self.baseline_score_mean = baseline_score_mean

    def calculate_normalized_anomaly_scores(self, raw_decision_scores: np.ndarray) -> np.ndarray:
        """
        Convert IsolationForest score_samples into normalized anomaly scores in range [0.0, 1.0].
        In IsolationForest, score_samples range typically from -0.8 (extreme anomaly) to -0.3 (normal).
        Formula maps score_samples: score_norm = (baseline_mean - score) * 5.0
        High values indicate high anomaly.
        """
        if len(raw_decision_scores) == 0:
            return np.array([])
        
        # Distance from normal baseline (positive when more anomalous than average ham)
        diff = self.baseline_score_mean - raw_decision_scores
        # Apply sigmoid or clipped linear scaling
        scores = 1.0 / (1.0 + np.exp(-diff * 12.0))
        return np.clip(scores, 0.0, 1.0)

    def analyze_batch(
        self,
        raw_decision_scores: np.ndarray,
        predictions: np.ndarray,
        messages: List[str]
    ) -> Dict[str, Any]:
        """
        Analyze a batch of processed predictions and decision scores.
        predictions: 1 for normal, -1 for anomaly
        """
        total_messages = len(messages)
        if total_messages == 0:
            return {
                "total_messages": 0,
                "anomaly_count": 0,
                "anomaly_percentage": 0.0,
                "avg_anomaly_score": 0.0,
                "drift_score": 0.0,
                "drift_status": "NORMAL TRAFFIC",
                "top_anomalies": [],
                "all_results": []
            }

        normalized_scores = self.calculate_normalized_anomaly_scores(raw_decision_scores)
        
        # A message is an anomaly if IsolationForest predicted -1 OR anomaly_score > 0.5
        anomaly_mask = (predictions == -1) | (normalized_scores > 0.55)
        anomaly_count = int(np.sum(anomaly_mask))
        anomaly_percentage = anomaly_count / float(total_messages)

        avg_anomaly_score = float(np.mean(normalized_scores)) if len(normalized_scores) > 0 else 0.0

        # Drift score formula: (percentage of anomalous messages * 0.5) + (average anomaly score * 0.5)
        raw_drift = (anomaly_percentage * 0.5) + (avg_anomaly_score * 0.5)
        drift_score = round(float(raw_drift), 4)

        drift_status = "HIGH DRIFT DETECTED" if drift_score >= self.drift_threshold else "NORMAL TRAFFIC"

        message_results = []
        for idx, (msg, score, is_anom) in enumerate(zip(messages, normalized_scores, anomaly_mask)):
            message_results.append({
                "message_id": idx + 1,
                "message": msg,
                "anomaly_score": round(float(score), 4),
                "is_anomaly": bool(is_anom)
            })

        # Sort suspicious messages by anomaly score descending
        top_anomalies = sorted(message_results, key=lambda x: x["anomaly_score"], reverse=True)

        return {
            "total_messages": total_messages,
            "anomaly_count": anomaly_count,
            "anomaly_percentage": round(anomaly_percentage * 100, 2),
            "avg_anomaly_score": round(avg_anomaly_score, 4),
            "drift_score": drift_score,
            "drift_status": drift_status,
            "top_anomalies": top_anomalies[:20],
            "all_results": message_results
        }
