# Feature Breakdown — SMS SHIELD Drift Monitoring System

---

## 1 Web Dashboard (Admin / Viewer)

**Goal:** Monitor drift levels, anomaly trends, and overall system analytics.

### Implementation
- React + Tailwind dashboard UI
- Drift trend charts
- Anomaly distribution charts
- Date-based filtering (day / week / month)
- Individual batch/run analytics view
- CSV batch upload interface
- Top anomalous message viewer

### APIs
- `/drift`
- `/drift/summary`
- `/anomalies/{date}`
- `/history`
- `/analytics/*`

---

## 2 Authentication Module (Optional)

**Goal:** Secure access to dashboard and APIs.

### Implementation
- Login (JWT based)
- Registration
- Role-based access (Admin / Viewer)
- Session validation

### APIs
- `/auth/register`
- `/auth/login`
- `/auth/me`

---

## 3 Data Input / Upload Module

**Goal:** Allow users to upload datasets or ingest daily batches for drift analysis.

### Implementation
- CSV upload UI
- Daily batch ingestion option
- Demo dataset scoring
- Upload progress and validation
- Error handling for invalid format

### APIs
- `/score`
- `/score/demo`
- `/batch/upload`
- `/batch/{batch_id}`

---

## 4 ML Pipeline Module (Core Engine)

**Goal:** Process SMS data and compute drift metrics.

### Implementation
- Text cleaning & normalization
- Character n-gram vectorization
- PCA dimensionality reduction
- Isolation Forest anomaly scoring
- Daily aggregation
- Drift score computation

### Internal APIs
- `/ml/pipeline`
- `/ml/modelInfo`
- `/ml/health`

---

## 5 Drift Monitoring Dashboard

**Goal:** Visualize ML output clearly for monitoring.

### Implementation
- Drift timeline chart
- Anomaly count visualization
- Global drift score card
- Date filters
- Message-level drill-down

### APIs
- `/drift`
- `/anomalies/{date}`
- `/analytics/trend`

---

## 6 History & Run Tracking Module

**Goal:** Track and inspect previous analysis runs.

### Implementation
- History table of batch runs
- Run status tracking
- Run detail view
- Delete old records

### APIs
- `/history`
- `/history/{run_id}`
- `DELETE /history/{run_id}`

---

## 7 Analytics Module

**Goal:** Provide deeper insights and reporting.

### Implementation
- Trend analytics
- Drift distribution analysis
- Aggregated metrics
- Export analytics CSV

### APIs
- `/analytics/trend`
- `/analytics/distribution`
- `/analytics/export`

---

## 8 Backend API Layer

**Goal:** Serve frontend and orchestrate ML processing.

### Implementation
- FastAPI REST APIs
- Pipeline triggering
- Secure request handling
- Validation & error responses

---

## 9 Database Layer

**Goal:** Persist all monitoring and analytics data.

### Storage Entities
- Users
- Batch runs
- Drift metrics
- Anomaly messages
- Analytics summaries

---

##  End-to-End Feature Flow

```text
Upload Data
   ↓
Backend API
   ↓
ML Pipeline Processing
   ↓
Drift Score Computation
   ↓
Store in Database
   ↓
Dashboard Visualization