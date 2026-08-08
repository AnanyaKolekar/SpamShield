"""
tests/test_ml_pipeline.py

Why this file exists:
Unit tests validating text cleaning, feature extraction, TF-IDF vectorization, TruncatedSVD, Isolation Forest scoring, and drift metric calculations.
"""

import pytest
import numpy as np
from ml.preprocessor import SMSPreprocessor
from ml.feature_engineering import SMSFeaturePipeline
from ml.drift_detector import SMSDriftDetector
from ml.inference import SMSInferencePipeline


def test_preprocessor_text_clean():
    """Verify minimal lowercasing preserving obfuscation characters."""
    raw = "  fr33 cl1ck h3r3 NOW $$$!  "
    cleaned = SMSPreprocessor.clean_text(raw)
    assert cleaned == "fr33 cl1ck h3r3 now $$$!"


def test_preprocessor_extract_single_features():
    """Verify statistical domain feature calculations."""
    text = "W1N $500 NOW!"
    features = SMSPreprocessor.extract_single_features(text)
    assert features["char_length"] == 13.0
    assert features["digit_count"] == 4.0
    assert features["upper_ratio"] > 0.3
    assert features["special_char_ratio"] > 0.1


def test_feature_pipeline_fit_transform():
    """Verify Char TF-IDF (3,5) and TruncatedSVD dimensionality reduction."""
    messages = [
        "Hey how are you doing today?",
        "Are we meeting for lunch at 1pm?",
        "fr33 cl1ck h3r3 to w1n $$$ cash prize!",
        "URGENT! Call 08001234567 FREE win prize"
    ]
    pipeline = SMSFeaturePipeline(ngram_range=(3, 5), max_features=500, n_components=10, random_state=42)
    matrix = pipeline.fit_transform(messages)
    
    assert matrix.shape[0] == 4
    assert matrix.shape[1] > 4


def test_drift_detector_analyze_batch():
    """Verify per-message anomaly scoring and daily drift calculation."""
    detector = SMSDriftDetector(drift_threshold=0.35)
    raw_scores = np.array([-0.7, -0.6, -0.3, -0.2])
    predictions = np.array([-1, -1, 1, 1])
    messages = ["Spam 1", "Spam 2", "Normal 1", "Normal 2"]

    results = detector.analyze_batch(raw_scores, predictions, messages)
    assert results["total_messages"] == 4
    assert results["anomaly_count"] == 2
    assert results["anomaly_percentage"] == 50.0
    assert results["drift_score"] > 0.35
    assert results["drift_status"] == "HIGH DRIFT DETECTED"


def test_inference_pipeline_execution():
    """Verify end-to-end inference execution using saved model artifacts."""
    inference = SMSInferencePipeline(models_dir="models", drift_threshold=0.35)
    inference.load_artifacts()
    
    sample = ["Hello friend, hope you are well.", "fr33 cl1ck h3r3 to w1n $$$ cash!"]
    results = inference.predict_batch(sample)
    assert results["total_messages"] == 2
    assert "drift_score" in results
    assert "top_anomalies" in results
