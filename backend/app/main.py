"""
backend/app/main.py

Why this file exists:
Main entrypoint for the FastAPI backend web server.
- Configures CORS middleware
- Initializes database tables
- Loads fitted ML inference pipeline on startup
- Seeds initial drift dataset if database is empty
- Registers API router endpoints under /api/v1
"""

import os
import logging
import pandas as pd
from datetime import date, timedelta
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.core.config import settings
from backend.app.db.database import create_tables, SessionLocal
from ml.inference import SMSInferencePipeline
from backend.app.services.drift_service import DriftService
from backend.app import api

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("sms_shield")


def seed_initial_demo_data(drift_service: DriftService):
    """Seed 30 days of historical drift records if database has fewer than 10 records."""
    db = SessionLocal()
    try:
        from backend.app.db.models import DailyDrift
        count = db.query(DailyDrift).count()
        if count < 10:
            logger.info("Seeding 30 days of historical drift metrics...")
            # Clear incomplete seed records
            db.query(DailyDrift).delete()
            db.commit()

            data_file = os.path.join(settings.DATA_DIR, "raw", "sms_dataset.csv")
            if os.path.exists(data_file):
                df = pd.read_csv(data_file)
                base_date = date.today() - timedelta(days=29)
                chunk_size = max(len(df) // 30, 50)

                for i in range(30):
                    start_idx = (i * chunk_size) % (len(df) - chunk_size)
                    sub_df = df.iloc[start_idx : start_idx + chunk_size]
                    
                    batch_date = base_date + timedelta(days=i)
                    ml_res = drift_service.pipeline.predict_batch(sub_df['message'].tolist())
                    
                    # On day 28 & 29, simulate elevated campaign drift for realistic timeline variance
                    if i in [27, 28]:
                        ml_res["drift_score"] = round(0.42 + (i - 27) * 0.05, 4)
                        ml_res["drift_status"] = "HIGH DRIFT DETECTED"
                    
                    import json
                    daily_rec = DailyDrift(
                        date=batch_date,
                        total_messages=ml_res["total_messages"],
                        anomaly_count=ml_res["anomaly_count"],
                        anomaly_percentage=ml_res["anomaly_percentage"],
                        avg_anomaly_score=ml_res["avg_anomaly_score"],
                        drift_score=ml_res["drift_score"],
                        drift_status=ml_res["drift_status"],
                        top_anomalies_json=json.dumps(ml_res["top_anomalies"])
                    )
                    db.add(daily_rec)
                db.commit()
                logger.info("Successfully seeded 30 days of historical drift data!")
    except Exception as e:
        logger.warning(f"Seed data generation skipped: {e}")
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown."""
    logger.info("Starting SMS Shield FastAPI service...")
    
    # 1. Ensure DB tables exist
    create_tables()

    # 2. Load ML inference engine
    try:
        inference_pipeline = SMSInferencePipeline(
            models_dir=settings.MODELS_DIR,
            drift_threshold=settings.DRIFT_THRESHOLD
        )
        inference_pipeline.load_artifacts()
        drift_service = DriftService(inference_pipeline)
        api.endpoints.drift_service_instance = drift_service
        logger.info("ML Inference pipeline successfully loaded into memory!")
        
        # 3. Seed data if needed
        seed_initial_demo_data(drift_service)
    except Exception as e:
        logger.error(f"Failed to load ML inference pipeline: {e}")

    yield

    logger.info("Shutting down SMS Shield FastAPI service...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(api.endpoints.router, prefix=settings.API_V1_STR)


@app.get("/")
def root():
    return {
        "title": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs_url": "/docs",
        "api_v1": f"{settings.API_V1_STR}"
    }
