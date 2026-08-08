# SMS Shield - Testing & Quality Assurance Guide

This document outlines the test suite for validating ML algorithms, FastAPI endpoints, and database models.

---

## 1. Running Automated Pytest Suite

```bash
# Activate virtual environment
source venv/bin/activate

# Execute pytest suite with PYTHONPATH set
PYTHONPATH=. pytest tests/ -v
```

---

## 2. Test Coverage Summary

- `tests/test_ml_pipeline.py`:
  - `test_preprocessor_text_clean`: Verifies minimal text cleaning while retaining obfuscations (`fr33`, `cl1ck`, `$$$`).
  - `test_preprocessor_extract_single_features`: Validates digit count, uppercase letter ratio, and special character ratio calculations.
  - `test_feature_pipeline_fit_transform`: Validates Char N-Gram TF-IDF `(3,5)` vectorization and TruncatedSVD dimensionality reduction.
  - `test_drift_detector_analyze_batch`: Validates Isolation Forest score normalization and daily drift score calculation.
  - `test_inference_pipeline_execution`: Validates production inference execution using fitted `.joblib` model artifacts.

- `tests/test_api.py`:
  - `test_api_health`: Tests `/api/v1/health` endpoint.
  - `test_api_dashboard`: Tests `/api/v1/dashboard` metrics aggregation.
  - `test_api_model_info`: Tests `/api/v1/ml/model-info` metadata.
  - `test_api_score_demo`: Tests synthetic emerging campaign drift scoring.
  - `test_api_ingest_json`: Tests batch JSON ingestion.

---

## 3. Validating Frontend React Build

```bash
cd frontend
npm run build
```
Verify zero build errors or broken dependencies.
