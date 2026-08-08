/**
 * frontend/src/pages/DashboardPage.jsx
 * 
 * Clean, human-made monitoring dashboard.
 * Fixed 7 Days, 30 Days, All Time date filtering logic.
 */

import React from 'react';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend
} from 'recharts';
import { Activity, AlertTriangle, ShieldCheck, TrendingUp, Calendar, MessageSquare } from 'lucide-react';
import AlertBanner from '../components/AlertBanner';
import DriftGauge from '../components/DriftGauge';

const DashboardPage = ({ data, dateFilter, setDateFilter }) => {
  if (!data) return <div className="p-8 text-center text-slate-400">Loading Dashboard...</div>;

  const {
    total_messages_analyzed = 0,
    total_anomalies_detected = 0,
    latest_drift_score = 0.0,
    latest_drift_status = 'NORMAL TRAFFIC',
    overall_anomaly_percentage = 0.0,
    drift_threshold = 0.35,
    daily_trend = [],
    top_suspicious_messages = []
  } = data;

  // Filter trend records based on active date range picker
  const getFilteredTrend = () => {
    if (!daily_trend || daily_trend.length === 0) return [];
    if (dateFilter === '7d') return daily_trend.slice(-7);
    if (dateFilter === '30d') return daily_trend.slice(-30);
    return daily_trend;
  };

  const filteredTrend = getFilteredTrend();

  return (
    <div className="space-y-6">
      {/* Status Alert Banner */}
      <AlertBanner
        driftScore={latest_drift_score}
        threshold={drift_threshold}
        driftStatus={latest_drift_status}
      />

      {/* Date Filter Bar */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 rounded-xl border border-slate-800 bg-slate-900 p-3">
        <div className="flex items-center space-x-2 text-xs font-semibold text-slate-300">
          <Calendar className="h-4 w-4 text-cyan-400" />
          <span>Monitoring Timeframe:</span>
        </div>
        <div className="flex items-center space-x-1.5 bg-slate-950 p-1 rounded-lg border border-slate-800">
          {[
            { id: '7d', label: 'Last 7 Days' },
            { id: '30d', label: 'Last 30 Days' },
            { id: 'all', label: 'All Time' },
          ].map((item) => (
            <button
              key={item.id}
              onClick={() => setDateFilter(item.id)}
              className={`px-3 py-1 text-xs font-semibold rounded transition-all ${
                dateFilter === item.id
                  ? 'bg-cyan-500 text-slate-950 font-bold'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              {item.label}
            </button>
          ))}
        </div>
      </div>

      {/* Key Metric Cards */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {/* Card 1: Total Messages */}
        <div className="rounded-xl border border-slate-800 bg-slate-900 p-4">
          <div className="flex items-center justify-between text-xs font-semibold text-slate-400">
            <span>Total Messages Scored</span>
            <MessageSquare className="h-4 w-4 text-cyan-400" />
          </div>
          <div className="mt-2">
            <span className="text-2xl font-bold font-mono text-slate-100">
              {total_messages_analyzed.toLocaleString()}
            </span>
            <p className="text-xs text-slate-400 mt-0.5">Historical traffic total</p>
          </div>
        </div>

        {/* Card 2: Total Anomalies */}
        <div className="rounded-xl border border-slate-800 bg-slate-900 p-4">
          <div className="flex items-center justify-between text-xs font-semibold text-slate-400">
            <span>Anomalies Flagged</span>
            <AlertTriangle className="h-4 w-4 text-amber-400" />
          </div>
          <div className="mt-2">
            <span className="text-2xl font-bold font-mono text-amber-400">
              {total_anomalies_detected.toLocaleString()}
            </span>
            <p className="text-xs text-slate-400 mt-0.5">{overall_anomaly_percentage}% anomaly rate</p>
          </div>
        </div>

        {/* Card 3: Latest Drift Score */}
        <div className="rounded-xl border border-slate-800 bg-slate-900 p-4">
          <div className="flex items-center justify-between text-xs font-semibold text-slate-400">
            <span>Latest Drift Score</span>
            <TrendingUp className="h-4 w-4 text-purple-400" />
          </div>
          <div className="mt-2">
            <span className={`text-2xl font-bold font-mono ${latest_drift_score >= drift_threshold ? 'text-red-400' : 'text-emerald-400'}`}>
              {(latest_drift_score * 100).toFixed(1)}%
            </span>
            <p className="text-xs text-slate-400 mt-0.5">Threshold: {(drift_threshold * 100).toFixed(0)}%</p>
          </div>
        </div>

        {/* Card 4: Model Status */}
        <div className="rounded-xl border border-slate-800 bg-slate-900 p-4">
          <div className="flex items-center justify-between text-xs font-semibold text-slate-400">
            <span>ML Anomaly Engine</span>
            <ShieldCheck className="h-4 w-4 text-emerald-400" />
          </div>
          <div className="mt-2">
            <span className="text-base font-bold text-slate-100 block">
              Isolation Forest
            </span>
            <p className="text-xs text-emerald-400 mt-0.5">Unsupervised Active</p>
          </div>
        </div>
      </div>

      {/* Main Charts Row */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        {/* Daily Drift Line Chart */}
        <div className="lg:col-span-2 rounded-xl border border-slate-800 bg-slate-900 p-5">
          <div className="flex items-center justify-between pb-3 border-b border-slate-800">
            <div>
              <h3 className="text-sm font-bold text-slate-100">Daily Drift Trend</h3>
              <p className="text-xs text-slate-400">Distribution shift percentage ({filteredTrend.length} days showing)</p>
            </div>
            <span className="text-xs font-mono text-cyan-400 bg-slate-950 px-2 py-1 rounded border border-slate-800">
              {dateFilter.toUpperCase()} View
            </span>
          </div>

          <div className="h-64 mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={filteredTrend} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="date" stroke="#64748b" fontSize={11} />
                <YAxis stroke="#64748b" fontSize={11} domain={[0, 1]} tickFormatter={(val) => `${(val * 100).toFixed(0)}%`} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#090d16', borderColor: '#334155', borderRadius: '8px', fontSize: '12px' }}
                  formatter={(val) => [`${(val * 100).toFixed(1)}%`, 'Drift Score']}
                />
                <Legend wrapperStyle={{ fontSize: '12px', paddingTop: '8px' }} />
                <Line
                  type="monotone"
                  dataKey="drift_score"
                  name="Drift Score"
                  stroke="#06b6d4"
                  strokeWidth={2.5}
                  dot={{ r: 3, fill: '#06b6d4' }}
                  activeDot={{ r: 6 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Drift Gauge */}
        <div className="rounded-xl border border-slate-800 bg-slate-900 p-5 flex flex-col justify-between">
          <div className="pb-3 border-b border-slate-800">
            <h3 className="text-sm font-bold text-slate-100">Drift Gauge</h3>
            <p className="text-xs text-slate-400">Current traffic anomaly level</p>
          </div>

          <DriftGauge score={latest_drift_score} threshold={drift_threshold} />

          <div className="rounded-lg bg-slate-950 p-2.5 text-center border border-slate-800">
            <span className="text-xs text-slate-400 block">System Recommendation:</span>
            <span className={`text-xs font-bold ${latest_drift_score >= drift_threshold ? 'text-red-400' : 'text-emerald-400'}`}>
              {latest_drift_score >= drift_threshold ? 'ALERT: Emerging Spam Campaign' : 'Baseline Normal Traffic'}
            </span>
          </div>
        </div>
      </div>

      {/* Anomaly Bar Chart & Top Suspicious Table */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Daily Anomaly Count Bar Chart */}
        <div className="rounded-xl border border-slate-800 bg-slate-900 p-5">
          <div className="flex items-center justify-between pb-3 border-b border-slate-800">
            <div>
              <h3 className="text-sm font-bold text-slate-100">Daily Anomaly Count</h3>
              <p className="text-xs text-slate-400">Anomalous messages detected per day</p>
            </div>
          </div>

          <div className="h-64 mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={filteredTrend} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="date" stroke="#64748b" fontSize={11} />
                <YAxis stroke="#64748b" fontSize={11} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#090d16', borderColor: '#334155', borderRadius: '8px', fontSize: '12px' }}
                />
                <Bar dataKey="anomaly_count" name="Anomalies" fill="#f59e0b" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Top Suspicious Messages */}
        <div className="rounded-xl border border-slate-800 bg-slate-900 p-5">
          <div className="flex items-center justify-between pb-3 border-b border-slate-800">
            <div>
              <h3 className="text-sm font-bold text-slate-100">Top Suspicious Messages</h3>
              <p className="text-xs text-slate-400">Recent high-scoring distribution anomalies</p>
            </div>
          </div>

          <div className="mt-4 space-y-2.5 max-h-64 overflow-y-auto pr-1">
            {top_suspicious_messages.length === 0 ? (
              <p className="text-xs text-slate-400 text-center py-8">No anomalous messages detected.</p>
            ) : (
              top_suspicious_messages.slice(0, 5).map((msg, idx) => (
                <div
                  key={msg.message_id || idx}
                  className="p-3 rounded-lg bg-slate-950 border border-slate-800"
                >
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-xs font-medium text-slate-400">Msg #{msg.message_id}</span>
                    <span className="rounded bg-red-950 text-red-400 border border-red-800 px-2 py-0.5 text-xs font-mono font-bold">
                      Score: {(msg.anomaly_score * 100).toFixed(1)}%
                    </span>
                  </div>
                  <p className="text-xs text-slate-200 font-mono bg-slate-900 p-2 rounded border border-slate-800">
                    "{msg.message}"
                  </p>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
