# SMS Shield - Production Deployment Guide (Vercel & Render)

This guide shows how to run the project locally and where the live deployment is hosted.

## Live deployment

- **Backend:** https://sms-shield-backend.onrender.com
- **Frontend:** https://vercel.com/ananyas-projects-64c5647f/spam-shield/13opnmSRoGcYwbuN3gC31MyM52JZ

---

## 1. Local Development Setup

### Backend
```bash
cd /home/mystiqueen/Desktop/Disk-D/Projects/SpamSheild
source venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. python ml/model_trainer.py
PYTHONPATH=. uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```
- **Backend Docs:** http://localhost:8000/docs

### Frontend
```bash
cd frontend
npm install
npm run dev
```
- **UI:** http://localhost:3000

---

## 2. Deploy Backend to Render

### Recommended: Blueprint deploy
1. Push the repo to GitHub.
2. On Render, click **New → Blueprint**.
3. Select your repo and branch.
4. Render should detect `render.yaml` automatically.
5. Apply the Blueprint.

### If manual setup is needed
1. On Render, click **New Web Service**.
2. Connect your GitHub repo.
3. Configure:
   - **Name:** `sms-shield-backend`
   - **Environment:** `Python 3`
   - **Branch:** `main`
   - **Build command:** `pip install --upgrade pip && pip install -r requirements.txt`
   - **Start command:** `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
4. Add env vars if needed:
   - `PYTHONPATH` = `.`
   - `DRIFT_THRESHOLD` = `0.35`
   - `DATABASE_URL` = your PostgreSQL URL (if using Postgres)

---

## 3. Deploy Frontend to Vercel

1. On Vercel, click **Add New Project**.
2. Import the GitHub repo.
3. Set the root directory to `frontend`.
4. Choose **Vite** as the framework.
5. Use:
   - **Build command:** `npm run build`
   - **Output directory:** `dist`
6. Ensure `frontend/vercel.json` rewrites `/api/v1/*` to the Render backend.
7. Deploy.

---

## 4. Verify

- Visit the Vercel frontend URL.
- Confirm the app loads and dashboard data appears.
- Confirm network calls to `/api/v1/...` are routed to `https://sms-shield-backend.onrender.com/api/v1/...`.
