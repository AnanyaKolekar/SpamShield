-- database/schema.sql
-- SMS Shield: SMS Spam Drift Monitoring & Emerging Campaign Detection
-- PostgreSQL Database DDL Schema

CREATE TABLE IF NOT EXISTS batch_runs (
    id VARCHAR(64) PRIMARY KEY,
    batch_name VARCHAR(255) NOT NULL,
    total_messages INTEGER NOT NULL DEFAULT 0,
    anomaly_count INTEGER NOT NULL DEFAULT 0,
    anomaly_percentage DOUBLE PRECISION NOT NULL DEFAULT 0.0,
    avg_anomaly_score DOUBLE PRECISION NOT NULL DEFAULT 0.0,
    drift_score DOUBLE PRECISION NOT NULL DEFAULT 0.0,
    drift_status VARCHAR(50) NOT NULL DEFAULT 'NORMAL TRAFFIC',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sms_messages (
    id SERIAL PRIMARY KEY,
    batch_id VARCHAR(64) REFERENCES batch_runs(id) ON DELETE CASCADE,
    label VARCHAR(20) DEFAULT 'unknown',
    message TEXT NOT NULL,
    char_length INTEGER NOT NULL DEFAULT 0,
    digit_count INTEGER NOT NULL DEFAULT 0,
    upper_ratio DOUBLE PRECISION NOT NULL DEFAULT 0.0,
    special_char_ratio DOUBLE PRECISION NOT NULL DEFAULT 0.0,
    anomaly_score DOUBLE PRECISION NOT NULL DEFAULT 0.0,
    is_anomaly BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS daily_drift (
    id SERIAL PRIMARY KEY,
    date DATE UNIQUE NOT NULL,
    total_messages INTEGER NOT NULL DEFAULT 0,
    anomaly_count INTEGER NOT NULL DEFAULT 0,
    anomaly_percentage DOUBLE PRECISION NOT NULL DEFAULT 0.0,
    avg_anomaly_score DOUBLE PRECISION NOT NULL DEFAULT 0.0,
    drift_score DOUBLE PRECISION NOT NULL DEFAULT 0.0,
    drift_status VARCHAR(50) NOT NULL DEFAULT 'NORMAL TRAFFIC',
    top_anomalies_json TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS baseline_models (
    id SERIAL PRIMARY KEY,
    model_name VARCHAR(100) NOT NULL,
    ngram_min INTEGER NOT NULL DEFAULT 3,
    ngram_max INTEGER NOT NULL DEFAULT 5,
    max_features INTEGER NOT NULL DEFAULT 5000,
    svd_components INTEGER NOT NULL DEFAULT 100,
    contamination DOUBLE PRECISION NOT NULL DEFAULT 0.05,
    ham_train_count INTEGER NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for efficient querying
CREATE INDEX IF NOT EXISTS idx_sms_messages_batch_id ON sms_messages(batch_id);
CREATE INDEX IF NOT EXISTS idx_sms_messages_is_anomaly ON sms_messages(is_anomaly);
CREATE INDEX IF NOT EXISTS idx_daily_drift_date ON daily_drift(date);
