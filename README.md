# SMS Shield – SMS Spam Drift Monitoring & Emerging Campaign Detection

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg)](https://react.dev/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.4-F7931E.svg)](https://scikit-learn.org/)
[![Vercel](https://img.shields.io/badge/Vercel-Deployed-black.svg)](https://vercel.com/)
[![Render](https://img.shields.io/badge/Render-Deployed-46E3B7.svg)](https://render.com/)

> **Unsupervised SMS drift monitoring system that detects emerging spam campaigns by identifying distribution shifts in incoming SMS traffic using Character N-Gram TF-IDF, TruncatedSVD, Isolation Forest anomaly detection, PostgreSQL/SQLite persistence, and a React + Tailwind CSS dashboard.**

---

## 🎯 Key Objectives & Core ML Design

Traditional spam classifiers fail when attackers obfuscate text (e.g. `fr33`, `cl1ck`, `$$$`, `W1N`, `FREE!!!`) or launch zero-day emerging campaigns that differ from historical training sets.

**SMS Shield solves this by focusing on distribution drift monitoring rather than supervised classification:**

1. **NO Supervised Classifiers**: No Naive Bayes, Logistic Regression, Random Forest, or BERT deep learning models are used.
2. **Unsupervised Anomaly Detection**: `IsolationForest` is trained **strictly on baseline normal (ham) traffic**. Spam messages are used only for drift evaluation.
3. **Character N-Gram TF-IDF (3-5)**: Captures character-level subword obfuscations and punctuation patterns.
4. **TruncatedSVD over PCA**: Prefers `TruncatedSVD` (n_components=100) to project sparse 5,000-dimensional TF-IDF matrices without dense mean-centering (preserving sparsity and memory efficiency).
5. **Daily Drift Score & Alerting**:
   $$\text{Drift Score} = (\text{Percentage of Anomalous Messages} \times 0.5) + (\text{Average Anomaly Score} \times 0.5)$$
   Displays **`HIGH DRIFT DETECTED`** alert banner if drift score exceeds the threshold (default `35%`), otherwise **`NORMAL TRAFFIC`**.

---

## 🏗️ Architecture Flow

```text
Raw SMS Batch
     │
     ▼
Minimal Preprocessing (Lowercase & Feature Extraction: Length, Digits, Upper Ratio, Special Chars)
     │
     ▼
Character N-Gram TF-IDF Vectorizer (analyzer="char", ngram_range=(3,5), max_features=5000)
     │
     ▼
TruncatedSVD Dimensionality Reduction (n_components=100)
     │
     ▼
Isolation Forest Anomaly Detector (Trained strictly on Baseline Ham Traffic)
     │
     ▼
Drift Score & Anomaly Calculation Engine
     │
     ▼
PostgreSQL / SQLite Storage + FastAPI REST Endpoints (/ingest, /analyze, /drift, /anomalies, /dashboard)
     │
     ▼
React + Tailwind CSS + Recharts Monitoring Dashboard
```

---

## 📁 Project Structure

```text
sms-shield/
├── backend/
│   └── app/
│       ├── api/               # FastAPI endpoints (/ingest, /analyze, /drift, /anomalies, /dashboard, /ml/model-info)
│       ├── core/              # Config settings, CORS, Pydantic settings
│       ├── db/                # SQLAlchemy database engine, session handler, ORM models
│       ├── schemas/           # Pydantic request & response schemas
│       ├── services/          # Business logic & drift aggregation service
│       └── main.py            # FastAPI application entrypoint & startup hooks
├── frontend/
│   ├── src/
│   │   ├── components/        # Navbar, AlertBanner, DriftGauge, UploadModal
│   │   ├── pages/             # DashboardPage, AnomaliesPage, HistoryPage, ModelInfoPage
│   │   ├── services/          # Axios API connector
│   │   ├── App.jsx            # Main React container
│   │   └── index.css          # Design system & Tailwind directives
│   ├── package.json           # React dependencies (Vite, Tailwind, Recharts, Lucide)
│   ├── vercel.json            # Vercel SPA routing & API proxy rewrite
│   └── vite.config.js         # Vite build settings & API proxy
├── ml/
│   ├── preprocessor.py        # Text cleaner & statistical feature extractor
│   ├── feature_engineering.py # Char TF-IDF (3,5) + TruncatedSVD pipeline
│   ├── model_trainer.py       # Isolation Forest trainer (fitted strictly on ham baseline)
│   ├── drift_detector.py      # Normalized anomaly score & drift metric engine
│   ├── inference.py          # Production inference pipeline loading joblib artifacts
│   └── eda_runner.py          # Automated EDA generator producing matplotlib/seaborn figures
├── data/
│   ├── raw/                   # Raw SMS Spam Collection dataset (sms_dataset.csv)
│   └── processed/             # Feature engineered datasets
├── models/                    # Trained .joblib model artifacts & model_metadata.json
├── database/
│   ├── schema.sql             # PostgreSQL DDL schema definition
│   └── init.sql               # Database initialization script
├── docs/
│   ├── API_DOCUMENTATION.md   # OpenAPI REST endpoint specifications
│   ├── DEPLOYMENT_GUIDE.md    # Production deployment manual for Render & Vercel
│   ├── TESTING_GUIDE.md       # Pytest & build verification guide
│   └── SMS_Shield_EDA.ipynb   # Executed Jupyter EDA notebook
├── tests/
│   ├── test_ml_pipeline.py    # Pytest unit tests for ML pipeline
│   └── test_api.py            # Pytest integration tests for FastAPI APIs
├── render.yaml                # Render Blueprint deployment configuration
├── requirements.txt           # Python backend dependencies
└── README.md                  # Project documentation
```

---

## 🚀 Quick Start (Local Run)

```bash
# 1. Activate Python virtual environment
source venv/bin/activate
pip install -r requirements.txt

# 2. Train baseline model on ham traffic (if retrained)
PYTHONPATH=. python ml/model_trainer.py

# 3. Launch FastAPI backend server (Port 8000)
PYTHONPATH=. uvicorn backend.app.main:app --reload --port 8000

# 4. Launch React frontend (In a separate terminal tab, Port 3000)
cd frontend
npm run dev
```

- **React Dashboard:** `http://localhost:3000`
- **FastAPI OpenAPI Docs:** `http://localhost:8000/docs`

---

## ☁️ Cloud Deployment (Render & Vercel)

### Backend Deployment on Render
1. Connect your repository on [Render](https://render.com/).
2. Select **Blueprint** to use `render.yaml` automatically, or create a **Web Service**.
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`

### Frontend Deployment on Vercel
1. Import repository on [Vercel](https://vercel.com/).
2. Set Root Directory to `frontend`.
3. Vercel automatically detects `frontend/vercel.json` for routing & API proxies.

---

## 🧪 Testing

Execute automated pytest unit and integration tests:

```bash
PYTHONPATH=. pytest tests/ -v
```

---

## 📜 License

Distributed under the MIT License.
