"""
tests/test_api.py

Why this file exists:
Integration tests for FastAPI REST API endpoints using TestClient context manager.
"""

import pytest
from fastapi.testclient import TestClient
from backend.app.main import app


def test_api_health():
    """Test health check endpoint."""
    with TestClient(app) as client:
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


def test_api_dashboard():
    """Test dashboard data endpoint."""
    with TestClient(app) as client:
        response = client.get("/api/v1/dashboard")
        assert response.status_code == 200
        data = response.json()
        assert "total_messages_analyzed" in data
        assert "latest_drift_score" in data
        assert "latest_drift_status" in data


def test_api_model_info():
    """Test model metadata info endpoint."""
    with TestClient(app) as client:
        response = client.get("/api/v1/ml/model-info")
        assert response.status_code == 200
        data = response.json()
        assert data["model_name"] == "SMS-Shield-IsolationForest-SVD"
        assert "justification_svd_vs_pca" in data


def test_api_score_demo():
    """Test synthetic demo campaign scoring endpoint."""
    with TestClient(app) as client:
        response = client.post("/api/v1/score/demo")
        assert response.status_code == 200
        data = response.json()
        assert "drift_score" in data
        assert "drift_status" in data
        assert len(data["top_anomalies"]) > 0


def test_api_ingest_json():
    """Test message batch JSON ingestion endpoint."""
    with TestClient(app) as client:
        payload = {
            "batch_name": "Test Ingest Batch",
            "messages": [
                {"message": "Hello, see you tomorrow.", "label": "ham"},
                {"message": "fr33 cl1ck NOW to win $$$ cash!", "label": "spam"}
            ]
        }
        response = client.post("/api/v1/ingest", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["total_messages"] == 2
        assert "batch_id" in data
