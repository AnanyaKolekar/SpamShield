## API Endpoints – SMS SHIELD Drift Monitoring System

### Base URL  
`/api/v1`

---

## Authentication APIs (Optional – Role Based Login)

| Method | Endpoint | Role | Description | Request Body | Response |
|--------|---------|------|------------|-------------|---------|
| POST | `/auth/register` | Admin/Viewer | Register new user | name, email, password | JWT token + role |
| POST | `/auth/login` | Admin/Viewer | User login | email, password | JWT token + role |
| GET | `/auth/me` | Admin/Viewer | Get logged-in profile | — | User profile data |

---

## Data Input / Scoring APIs

| Method | Endpoint | Role | Description | Request Body | Response |
|--------|---------|------|------------|-------------|---------|
| POST | `/score` | Admin | Upload SMS batch & run ML pipeline | CSV file / SMS batch JSON | Drift score + anomaly stats |
| POST | `/score/demo` | Admin | Run scoring on demo dataset | — | Drift result summary |

---

## ML / Drift Processing APIs

| Method | Endpoint | Role | Description | Request Body | Response |
|--------|---------|------|------------|-------------|---------|
| POST | `/ml/pipeline` | Internal | Execute preprocessing + feature engineering + inference | SMS batch JSON | Message-level anomaly scores |
| GET | `/ml/modelInfo` | Admin | Get model metadata | — | Model name, PCA config, Isolation Forest params |
| GET | `/ml/health` | Admin | Check pipeline health status | — | Service status + latency |

---

## Drift Dashboard APIs

| Method | Endpoint | Role | Description | Request Body | Response |
|--------|---------|------|------------|-------------|---------|
| GET | `/drift` | Admin/Viewer | Get drift trend data | range=day/week/month | Drift score timeline |
| GET | `/drift/summary` | Admin/Viewer | Get latest drift summary | — | Global drift score + anomaly % |
| GET | `/anomalies/{date}` | Admin/Viewer | Get top anomalous messages | — | Message list + risk score |
| GET | `/anomalies/stats` | Admin/Viewer | Aggregated anomaly statistics | — | Daily anomaly counts |

---

## History / Admin APIs

| Method | Endpoint | Role | Description | Request Body | Response |
|--------|---------|------|------------|-------------|---------|
| GET | `/history` | Admin | List historical analysis runs | range, status | Batch run list |
| GET | `/history/{run_id}` | Admin | Get run details | — | Drift metrics + logs |
| DELETE | `/history/{run_id}` | Admin | Remove run record | — | Success message |

---

## Batch Upload APIs

| Method | Endpoint | Role | Description | Request Body | Response |
|--------|---------|------|------------|-------------|---------|
| POST | `/batch/upload` | Admin | Upload CSV for batch scoring | CSV file | Batch ID + processing status |
| GET | `/batch/{batch_id}` | Admin | Check batch processing status | — | Status + drift result |

---

## Analytics APIs

| Method | Endpoint | Role | Description | Request Body | Response |
|--------|---------|------|------------|-------------|---------|
| GET | `/analytics/trend` | Admin/Viewer | Drift trend analytics | range | Trend dataset |
| GET | `/analytics/distribution` | Admin | Drift distribution analysis | — | Histogram data |
| GET | `/analytics/export` | Admin | Export drift analytics CSV | — | CSV file |
