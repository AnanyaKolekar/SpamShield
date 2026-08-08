/**
 * frontend/src/services/api.js
 * 
 * Why this file exists:
 * Provides API communication layer connecting React components to FastAPI endpoints.
 */

import axios from 'axios';

const API_BASE = '/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

export const fetchDashboardData = async () => {
  try {
    const res = await apiClient.get('/dashboard');
    return res.data;
  } catch (err) {
    console.warn('Backend unavailable, using fallback mock data for frontend rendering:', err);
    return getFallbackDashboardData();
  }
};

export const fetchDriftHistory = async (limit = 30) => {
  try {
    const res = await apiClient.get(`/drift?limit=${limit}`);
    return res.data;
  } catch (err) {
    return getFallbackDriftHistory();
  }
};

export const fetchAnomalies = async (limit = 50) => {
  try {
    const res = await apiClient.get(`/anomalies?limit=${limit}`);
    return res.data;
  } catch (err) {
    return getFallbackAnomalies();
  }
};

export const fetchModelInfo = async () => {
  try {
    const res = await apiClient.get('/ml/model-info');
    return res.data;
  } catch (err) {
    return getFallbackModelInfo();
  }
};

export const runDemoScore = async () => {
  const res = await apiClient.post('/score/demo');
  return res.data;
};

export const uploadBatchCSV = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  const res = await apiClient.post('/ingest', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return res.data;
};

// Fallback Mock Generators
function getFallbackDashboardData() {
  return {
    total_messages_analyzed: 5574,
    total_anomalies_detected: 284,
    latest_drift_score: 0.4215,
    latest_drift_status: 'HIGH DRIFT DETECTED',
    overall_anomaly_percentage: 5.09,
    drift_threshold: 0.35,
    daily_trend: getFallbackDriftHistory(),
    top_suspicious_messages: getFallbackAnomalies().slice(0, 5),
  };
}

function getFallbackDriftHistory() {
  const result = [];
  const today = new Date();
  for (let i = 29; i >= 0; i--) {
    const d = new Date(today);
    d.setDate(d.getDate() - i);
    const dateStr = d.toISOString().slice(0, 10);
    const isSpamSpike = i === 1 || i === 2;
    result.push({
      id: 30 - i,
      date: dateStr,
      total_messages: 1100 + (i % 7) * 40,
      anomaly_count: isSpamSpike ? 145 : 35 + (i % 5) * 6,
      anomaly_percentage: isSpamSpike ? 12.8 : 3.2 + (i % 4) * 0.5,
      avg_anomaly_score: isSpamSpike ? 0.72 : 0.28 + (i % 3) * 0.03,
      drift_score: isSpamSpike ? 0.4215 : 0.18 + (i % 6) * 0.025,
      drift_status: isSpamSpike ? 'HIGH DRIFT DETECTED' : 'NORMAL TRAFFIC',
    });
  }
  return result;
}

function getFallbackAnomalies() {
  return [
    {
      message_id: 101,
      message: 'fr33 cl1ck h3r3 to w1n $$$ cash prize now!!! Call 0800999888 FREE gift',
      anomaly_score: 0.8924,
      is_anomaly: true,
      char_length: 76,
      digit_count: 14,
      upper_ratio: 0.18,
      special_char_ratio: 0.12,
    },
    {
      message_id: 102,
      message: 'URGENT! Your bank account 4829 has been locked. Click http://bank-update-verify.com',
      anomaly_score: 0.8412,
      is_anomaly: true,
      char_length: 88,
      digit_count: 8,
      upper_ratio: 0.12,
      special_char_ratio: 0.09,
    },
    {
      message_id: 103,
      message: 'W1NN3R! Claim $5000000 instant cash payout reply CLAIM to 88044',
      anomaly_score: 0.8105,
      is_anomaly: true,
      char_length: 64,
      digit_count: 12,
      upper_ratio: 0.25,
      special_char_ratio: 0.05,
    },
  ];
}
