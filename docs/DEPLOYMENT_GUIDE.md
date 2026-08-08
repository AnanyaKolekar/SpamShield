# SMS Shield - Production Deployment Guide (Vercel & Render)

This guide provides step-by-step instructions for deploying the **SMS Shield** application:
- **Backend (FastAPI + ML Engine):** Deployed on **Render**
- **Frontend (React + Vite + Tailwind):** Deployed on **Vercel**

---

## 1. Local Development Setup

### Backend Setup
```bash
# 1. Open project directory
cd /path/to/SpamShield

# 2. Activate virtual environment & install requirements
source venv/bin/activate
pip install -r requirements.txt

# 3. Train ML baseline model (if retrained)
PYTHONPATH=. python ml/model_trainer.py

# 4. Start FastAPI server on port 8000
PYTHONPATH=. uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```
- **Backend API Docs:** `http://localhost:8000/docs`

### Frontend Setup
```bash
# In a separate terminal
cd frontend
npm install
npm run dev
```
- **Dashboard UI:** `http://localhost:3000`

---

## 2. Deploying Backend to Render

### Option A: Automatic Blueprint Deployment (`render.yaml`)
1. Push your repository to GitHub.
2. Go to [Render Dashboard](https://dashboard.render.com/) and click **New** -> **Blueprint**.
3. Connect your GitHub repository. Render will automatically detect `render.yaml` and configure the Python 3.12 service.
4. Click **Apply**.

### Option B: Manual Web Service Setup on Render
1. Go to [Render Dashboard](https://dashboard.render.com/) -> **New Web Service**.
2. Connect your GitHub repository.
3. Configure settings:
   - **Name:** `sms-shield-backend`
   - **Environment:** `Python 3`
   - **Region:** Choose nearest (e.g., Oregon or Frankfurt)
   - **Branch:** `main`
   - **Build Command:** `pip install --upgrade pip && pip install -r requirements.txt`
   - **Start Command:** `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
4. Environment Variables:
   - `PYTHONPATH` = `.`
   - `DRIFT_THRESHOLD` = `0.35`
   - `DATABASE_URL` = (Optional PostgreSQL URL or default to SQLite)
5. Click **Create Web Service**.
6. Copy your live Render URL (e.g. `https://sms-shield-backend.onrender.com`).

---

## 3. Deploying Frontend to Vercel

1. Go to [Vercel Dashboard](https://vercel.com/dashboard) -> **Add New Project**.
2. Import your GitHub repository.
3. Select the **`frontend`** directory as the **Root Directory**.
4. Framework Preset: **Vite**
5. Build Settings:
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
6. Verify `frontend/vercel.json` contains your Render backend destination URL:
   ```json
   {
     "rewrites": [
       {
         "source": "/api/v1/:path*",
         "destination": "https://YOUR-RENDER-BACKEND.onrender.com/api/v1/:path*"
       }
     ]
   }
   ```
7. Click **Deploy**.

---

## 4. Verification

Once deployed:
1. Open your Vercel URL (e.g. `https://sms-shield.vercel.app`).
2. Test loading Dashboard KPIs, clicking **"Last 7 Days"** / **"Last 30 Days"**, and running **"Simulate Campaign"**.
