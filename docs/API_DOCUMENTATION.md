# SMS Shield - REST API Documentation

Base URL: `http://localhost:8000/api/v1`

---

## 1. Data Ingestion & Scoring APIs

### POST `/api/v1/ingest`
**Description:** Upload a daily SMS message batch via CSV file upload or JSON payload. Runs ML inference pipeline, computes per-message anomaly scores, aggregates daily drift score, and persists records into PostgreSQL/SQLite database tables.

**Headers:**
- `Content-Type: multipart/form-data` (for CSV upload) or `application/json` (for JSON payload)

**Request Payload (JSON):**
```json
{
  "batch_name": "Daily SMS Traffic Batch",
  "messages": [
    { "message": "Hey John, meeting at 3pm today?", "label": "ham" },
    { "message": "fr33 cl1ck h3r3 to w1n $$$ cash prize!", "label": "spam" }
  ]
}
```

**Response (200 OK):**
```json
{
  "batch_id": "batch_a1b2c3d4e5f6",
  "batch_name": "Daily SMS Traffic Batch",
  "total_messages": 2,
  "anomaly_count": 1,
  "anomaly_percentage": 50.0,
  "avg_anomaly_score": 0.4512,
  "drift_score": 0.4756,
  "drift_status": "HIGH DRIFT DETECTED",
  "created_at": "2026-08-08T23:00:00.000Z",
  "top_anomalies": [
    {
      "message_id": 2,
      "message": "fr33 cl1ck h3r3 to w1n $$$ cash prize!",
      "anomaly_score": 0.8613,
      "is_anomaly": true,
      "char_length": 38,
      "digit_count": 6,
      "upper_ratio": 0.0,
      "special_char_ratio": 0.105
    }
  ]
}
```

---

### POST `/api/v1/analyze`
**Description:** Trigger drift analysis on a raw array of messages provided in JSON.

---

### POST `/api/v1/score/demo`
**Description:** Inject and score a pre-packaged synthetic SMS batch simulating an emerging campaign shift. Useful for UI demonstrations.

---

## 2. Monitoring & Analytics APIs

### GET `/api/v1/dashboard`
**Description:** Returns full monitoring dashboard metrics: KPI cards, daily drift history, top suspicious messages, and alert status banner.

**Response (200 OK):**
```json
{
  "total_messages_analyzed": 5574,
  "total_anomalies_detected": 284,
  "latest_drift_score": 0.4215,
  "latest_drift_status": "HIGH DRIFT DETECTED",
  "overall_anomaly_percentage": 5.09,
  "drift_threshold": 0.35,
  "daily_trend": [ ... ],
  "top_suspicious_messages": [ ... ]
}
```

---

### GET `/api/v1/drift`
**Query Parameters:**
- `limit` (integer, optional, default: 30): Number of daily history records to return.

---

### GET `/api/v1/anomalies`
**Query Parameters:**
- `limit` (integer, optional, default: 50): Number of top anomalous messages to return.

---

## 3. Machine Learning Model APIs

### GET `/api/v1/ml/model-info`
**Description:** Returns active baseline model metadata, TF-IDF vectorizer parameters, TruncatedSVD components, Isolation Forest settings, and technical justification for SVD vs PCA.

---

### GET `/api/v1/health`
**Description:** Service health check endpoint.
