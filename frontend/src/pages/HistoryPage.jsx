/**
 * frontend/src/pages/HistoryPage.jsx
 * 
 * Why this file exists:
 * Displays historical audit log of daily drift analysis runs and batch scoring records.
 */

import React from 'react';
import { History, Download, Calendar, CheckCircle2, ShieldAlert } from 'lucide-react';

const HistoryPage = ({ history = [] }) => {
  const exportCSV = () => {
    if (!history || history.length === 0) return;
    const headers = ['ID', 'Date', 'Total Messages', 'Anomaly Count', 'Anomaly %', 'Avg Anomaly Score', 'Drift Score', 'Status'];
    const rows = history.map((r) => [
      r.id,
      r.date,
      r.total_messages,
      r.anomaly_count,
      r.anomaly_percentage,
      r.avg_anomaly_score,
      r.drift_score,
      r.drift_status
    ]);
    const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...rows.map((e) => e.join(','))].join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `sms_shield_drift_history_${new Date().toISOString().slice(0, 10)}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 glass-panel p-5 rounded-2xl border border-slate-800">
        <div>
          <div className="flex items-center space-x-2">
            <History className="h-6 w-6 text-cyan-400" />
            <h2 className="text-xl font-black text-slate-100">Historical Batch Analysis Runs</h2>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Audit log of daily message batches, drift scores, anomaly percentages, and alerts.
          </p>
        </div>

        <button
          onClick={exportCSV}
          className="flex items-center space-x-2 rounded-xl bg-slate-900 px-4 py-2 text-xs font-bold text-cyan-400 border border-cyan-500/30 hover:bg-cyan-500/10 transition-all"
        >
          <Download className="h-4 w-4" />
          <span>Export Analytics CSV</span>
        </button>
      </div>

      {/* History Table */}
      <div className="glass-panel rounded-2xl border border-slate-800 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-slate-900/90 text-slate-400 font-semibold uppercase tracking-wider border-b border-slate-800">
              <tr>
                <th className="px-4 py-3.5">Run Date</th>
                <th className="px-4 py-3.5 text-center">Total Messages</th>
                <th className="px-4 py-3.5 text-center">Anomaly Count</th>
                <th className="px-4 py-3.5 text-center">Anomaly %</th>
                <th className="px-4 py-3.5 text-center">Avg Anomaly Score</th>
                <th className="px-4 py-3.5 text-center">Drift Score</th>
                <th className="px-4 py-3.5 text-center">Alert Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 font-mono">
              {history.length === 0 ? (
                <tr>
                  <td colSpan={7} className="px-4 py-12 text-center text-slate-500">
                    No historical analysis runs recorded yet. Upload a batch to create historical logs.
                  </td>
                </tr>
              ) : (
                history.map((run, idx) => {
                  const isHigh = run.drift_status === 'HIGH DRIFT DETECTED' || run.drift_score >= 0.35;
                  return (
                    <tr key={run.id || idx} className="hover:bg-slate-800/40 transition-colors">
                      <td className="px-4 py-3 font-semibold text-slate-200 flex items-center space-x-2">
                        <Calendar className="h-4 w-4 text-cyan-400" />
                        <span>{run.date}</span>
                      </td>
                      <td className="px-4 py-3 text-center text-slate-300">{run.total_messages.toLocaleString()}</td>
                      <td className="px-4 py-3 text-center text-amber-400 font-bold">{run.anomaly_count}</td>
                      <td className="px-4 py-3 text-center text-slate-300">{run.anomaly_percentage}%</td>
                      <td className="px-4 py-3 text-center text-slate-400">{(run.avg_anomaly_score * 100).toFixed(1)}%</td>
                      <td className="px-4 py-3 text-center font-bold">
                        <span className={isHigh ? 'text-red-400' : 'text-emerald-400'}>
                          {(run.drift_score * 100).toFixed(1)}%
                        </span>
                      </td>
                      <td className="px-4 py-3 text-center">
                        <span
                          className={`inline-flex items-center space-x-1.5 rounded-full px-2.5 py-1 text-xs font-bold ${
                            isHigh
                              ? 'bg-red-500/20 text-red-400 border border-red-500/40'
                              : 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/40'
                          }`}
                        >
                          {isHigh ? <ShieldAlert className="h-3.5 w-3.5" /> : <CheckCircle2 className="h-3.5 w-3.5" />}
                          <span>{isHigh ? 'HIGH DRIFT DETECTED' : 'NORMAL TRAFFIC'}</span>
                        </span>
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default HistoryPage;
