# SMS Shield – SMS Spam Drift Monitoring & Emerging Campaign Detection

A lightweight drift detection app for SMS traffic.

## Live demo

- https://spam-shield-git-main-ananyas-projects-64c5647f.vercel.app/

## What it does

- Ingests SMS batches via FastAPI
- Builds character n-gram TF-IDF features
- Reduces dimensions with TruncatedSVD
- Detects anomalies with IsolationForest trained on normal SMS
- Stores drift metrics in a database
- Shows results in a React + Tailwind dashboard

## Project structure

- `backend/` – FastAPI backend, database, ML service
- `frontend/` – React dashboard, API proxy, Vercel routing
- `ml/` – preprocessing, feature pipeline, model training, inference
- `models/` – saved model artifacts
- `database/` – schema and init scripts
- `tests/` – backend and ML tests
- `render.yaml` – Render blueprint for backend
- `frontend/vercel.json` – Vercel frontend routing

## Run locally

```bash
cd /home/mystiqueen/Desktop/Disk-D/Projects/SpamSheild
source venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. python ml/model_trainer.py
PYTHONPATH=. uvicorn backend.app.main:app --reload --port 8000
```

In another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`.

## Deploy notes

### Backend on Render
- Uses `render.yaml` from repo root
- Build command: `pip install --upgrade pip && pip install -r requirements.txt`
- Start command: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
- Uses `DATABASE_URL` if available, otherwise falls back to SQLite

### Frontend on Vercel
- Root directory: `frontend`
- Build command: `npm run build`
- Output directory: `dist`
- `frontend/vercel.json` rewrites `/api/v1/*` to the backend URL

## Test

```bash
PYTHONPATH=. pytest tests/ -v
```

## License

MIT
