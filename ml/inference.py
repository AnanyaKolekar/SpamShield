"""
ml/inference.py

Why this file exists:
This module loads fitted model artifacts from models/ and runs batch inference and drift analysis on incoming SMS messages.
- Used directly by FastAPI endpoints to score raw uploaded SMS batches.
"""

import os
import json
import joblib
from typing import List, Dict, Any, Optional
import numpy as np
import pandas as pd

from ml.preprocessor import SMSPreprocessor
from ml.drift_detector import SMSDriftDetector


class SMSInferencePipeline:
    """Production inference pipeline for SMS drift and anomaly scoring."""

    def __init__(self, models_dir: str = "models", drift_threshold: float = 0.35):
        self.models_dir = models_dir
        self.drift_threshold = drift_threshold
        self.preprocessor = SMSPreprocessor()
        self.drift_detector = SMSDriftDetector(drift_threshold=self.drift_threshold)

        self.vectorizer = None
        self.svd = None
        self.scaler = None
        self.iso_forest = None
        self.metadata = {}
        self.is_loaded = False

    def load_artifacts(self) -> "SMSInferencePipeline":
        """Load fitted scikit-learn artifacts and metadata from disk."""
        vec_path = os.path.join(self.models_dir, "char_tfidf_vectorizer.joblib")
        svd_path = os.path.join(self.models_dir, "truncated_svd.joblib")
        scaler_path = os.path.join(self.models_dir, "feature_scaler.joblib")
        iso_path = os.path.join(self.models_dir, "isolation_forest.joblib")
        meta_path = os.path.join(self.models_dir, "model_metadata.json")

        if not all(os.path.exists(p) for p in [vec_path, svd_path, scaler_path, iso_path]):
            raise FileNotFoundError(f"Model artifacts missing in '{self.models_dir}'. Run model_trainer.py first.")

        self.vectorizer = joblib.load(vec_path)
        self.svd = joblib.load(svd_path)
        self.scaler = joblib.load(scaler_path)
        self.iso_forest = joblib.load(iso_path)

        if os.path.exists(meta_path):
            with open(meta_path, "r", encoding="utf-8") as f:
                self.metadata = json.load(f)

        self.is_loaded = True
        return self

    def predict_batch(self, messages: List[str]) -> Dict[str, Any]:
        """Process a batch of raw SMS messages and calculate drift metrics."""
        if not self.is_loaded:
            self.load_artifacts()

        if not messages:
            return self.drift_detector.analyze_batch(np.array([]), np.array([]), [])

        # 1. Clean text
        cleaned = [self.preprocessor.clean_text(msg) for msg in messages]

        # 2. Vectorize with Char TF-IDF
        tfidf_mat = self.vectorizer.transform(cleaned)

        # 3. Dimensionality reduction with TruncatedSVD
        svd_mat = self.svd.transform(tfidf_mat)

        # 4. Extract statistical domain features
        stat_df = self.preprocessor.extract_batch_features(messages)
        scaled_stat = self.scaler.transform(stat_df.values)

        # 5. Combine features
        combined_features = np.hstack([svd_mat, scaled_stat])

        # 6. Isolation Forest scoring & prediction
        raw_scores = self.iso_forest.score_samples(combined_features)
        predictions = self.iso_forest.predict(combined_features)

        # 7. Compute drift metrics & top anomalies
        results = self.drift_detector.analyze_batch(raw_scores, predictions, messages)
        
        # Attach statistical breakdown to top anomalies
        for item in results["all_results"]:
            idx = item["message_id"] - 1
            item["char_length"] = int(stat_df.iloc[idx]["char_length"])
            item["digit_count"] = int(stat_df.iloc[idx]["digit_count"])
            item["upper_ratio"] = float(stat_df.iloc[idx]["upper_ratio"])
            item["special_char_ratio"] = float(stat_df.iloc[idx]["special_char_ratio"])

        return results
