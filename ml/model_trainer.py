"""
ml/model_trainer.py

Why this file exists:
This module trains the Isolation Forest anomaly detection model strictly on baseline (ham / normal) SMS traffic.
- Ensures NO supervised classifiers or word embeddings are used.
- Saves trained model artifacts (char_tfidf_vectorizer, truncated_svd, scaler, isolation_forest, metadata) into models/
"""

import os
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from ml.feature_engineering import SMSFeaturePipeline


class SMSModelTrainer:
    """Trains Isolation Forest strictly on normal (ham) SMS messages and exports model artifacts."""

    def __init__(
        self,
        models_dir: str = "models",
        contamination: float = 0.05,
        n_estimators: int = 150,
        random_state: int = 42
    ):
        self.models_dir = models_dir
        self.contamination = contamination
        self.n_estimators = n_estimators
        self.random_state = random_state
        os.makedirs(self.models_dir, exist_ok=True)

    def train_baseline(self, data_path: str = "data/raw/sms_dataset.csv"):
        """Train pipeline strictly on normal (ham) traffic."""
        print(f"Loading data from {data_path}...")
        df = pd.read_csv(data_path)

        # Filter strictly for ham (baseline normal traffic)
        ham_df = df[df['label'] == 'ham'].reset_index(drop=True)
        spam_df = df[df['label'] == 'spam'].reset_index(drop=True)

        print(f"Baseline Normal (Ham) Messages: {len(ham_df)}")
        print(f"Holdout Spam Messages (for evaluation): {len(spam_df)}")

        # Fit feature pipeline on baseline normal messages
        feature_pipeline = SMSFeaturePipeline(
            ngram_range=(3, 5),
            max_features=5000,
            n_components=100,
            random_state=self.random_state
        )
        print("Fitting Character TF-IDF & TruncatedSVD on baseline ham traffic...")
        X_ham = feature_pipeline.fit_transform(ham_df['message'].tolist())

        # Fit Isolation Forest strictly on baseline normal features
        print("Training Isolation Forest anomaly detector on normal traffic...")
        iso_forest = IsolationForest(
            n_estimators=self.n_estimators,
            contamination=self.contamination,
            random_state=self.random_state,
            n_jobs=-1
        )
        iso_forest.fit(X_ham)

        # Evaluate decision scores on Ham vs Spam to verify anomaly separation
        ham_scores = iso_forest.score_samples(X_ham)
        X_spam = feature_pipeline.transform(spam_df['message'].tolist())
        spam_scores = iso_forest.score_samples(X_spam)

        print("\n--- Model Evaluation Summary ---")
        print(f"Ham Baseline Mean Decision Score (higher = normal): {np.mean(ham_scores):.4f}")
        print(f"Spam Evaluation Mean Decision Score (lower = anomalous): {np.mean(spam_scores):.4f}")
        print(f"Separation Gap: {np.mean(ham_scores) - np.mean(spam_scores):.4f}")

        # Save artifacts
        joblib.dump(feature_pipeline.vectorizer, os.path.join(self.models_dir, "char_tfidf_vectorizer.joblib"))
        joblib.dump(feature_pipeline.svd, os.path.join(self.models_dir, "truncated_svd.joblib"))
        joblib.dump(feature_pipeline.scaler, os.path.join(self.models_dir, "feature_scaler.joblib"))
        joblib.dump(iso_forest, os.path.join(self.models_dir, "isolation_forest.joblib"))

        # Save model metadata
        metadata = {
            "model_name": "SMS-Shield-IsolationForest-SVD",
            "ngram_range": [3, 5],
            "max_features": 5000,
            "svd_n_components": 100,
            "n_estimators": self.n_estimators,
            "contamination": self.contamination,
            "train_samples_count": len(ham_df),
            "ham_mean_score": float(np.mean(ham_scores)),
            "spam_mean_score": float(np.mean(spam_scores)),
            "baseline_threshold": float(np.percentile(ham_scores, 5))
        }

        with open(os.path.join(self.models_dir, "model_metadata.json"), "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)

        print(f"\nAll baseline model artifacts successfully saved to '{self.models_dir}/'!")
        return metadata


if __name__ == "__main__":
    trainer = SMSModelTrainer()
    trainer.train_baseline()
