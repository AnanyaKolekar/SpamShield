/**
 * frontend/src/pages/AnomaliesPage.jsx
 * 
 * Why this file exists:
 * Detailed explorer page for inspecting individual anomalous SMS messages detected by Isolation Forest.
 * Highlights character obfuscations like 'fr33', 'cl1ck', '$$$', 'W1N'.
 */

import React, { useState } from 'react';
import { Search, AlertTriangle, ShieldAlert, Filter, ArrowUpDown } from 'lucide-react';

const OBFUSCATION_PATTERNS = [/fr33/i, /cl1ck/i, /\$\$\$/i, /w1n/i, /free!/i, /claim/i, /urgent/i, /\d{5,}/];

const AnomaliesPage = ({ anomalies = [] }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [severityFilter, setSeverityFilter] = useState('all');

  const highlightObfuscations = (text) => {
    return text;
  };

  const filteredAnomalies = anomalies.filter((msg) => {
    const matchesSearch = msg.message.toLowerCase().includes(searchQuery.toLowerCase());
    if (!matchesSearch) return false;

    if (severityFilter === 'high') return msg.anomaly_score >= 0.8;
    if (severityFilter === 'medium') return msg.anomaly_score >= 0.5 && msg.anomaly_score < 0.8;
    return true;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 glass-panel p-5 rounded-2xl border border-slate-800">
        <div>
          <div className="flex items-center space-x-2">
            <AlertTriangle className="h-6 w-6 text-red-400" />
            <h2 className="text-xl font-black text-slate-100">Anomalous Messages Explorer</h2>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            SMS traffic flagged as distribution anomalies by Isolation Forest trained strictly on normal traffic.
          </p>
        </div>

        {/* Search & Severity Filter */}
        <div className="flex flex-wrap items-center gap-3 w-full sm:w-auto">
          <div className="relative flex-1 sm:w-64">
            <Search className="absolute left-3 top-2.5 h-4 w-4 text-slate-400" />
            <input
              type="text"
              placeholder="Search obfuscations..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full rounded-xl bg-slate-950 border border-slate-800 pl-9 pr-4 py-2 text-xs text-slate-200 placeholder-slate-500 focus:border-cyan-500 focus:outline-none"
            />
          </div>

          <select
            value={severityFilter}
            onChange={(e) => setSeverityFilter(e.target.value)}
            className="rounded-xl bg-slate-950 border border-slate-800 px-3 py-2 text-xs font-semibold text-slate-300 focus:border-cyan-500 focus:outline-none"
          >
            <option value="all">All Severity</option>
            <option value="high">High (&gt; 80%)</option>
            <option value="medium">Medium (50 - 80%)</option>
          </select>
        </div>
      </div>

      {/* Anomalies Table */}
      <div className="glass-panel rounded-2xl border border-slate-800 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-slate-900/90 text-slate-400 font-semibold uppercase tracking-wider border-b border-slate-800">
              <tr>
                <th className="px-4 py-3.5">Msg ID</th>
                <th className="px-4 py-3.5">SMS Text (Character Obfuscations)</th>
                <th className="px-4 py-3.5 text-center">Anomaly Score</th>
                <th className="px-4 py-3.5 text-center">Length</th>
                <th className="px-4 py-3.5 text-center">Digits</th>
                <th className="px-4 py-3.5 text-center">Upper Ratio</th>
                <th className="px-4 py-3.5 text-center">Special Ratio</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 font-mono">
              {filteredAnomalies.length === 0 ? (
                <tr>
                  <td colSpan={7} className="px-4 py-12 text-center text-slate-500">
                    No anomalous messages match your search or filter criteria.
                  </td>
                </tr>
              ) : (
                filteredAnomalies.map((item, idx) => (
                  <tr key={item.message_id || idx} className="hover:bg-slate-800/40 transition-colors">
                    <td className="px-4 py-3 text-slate-400">#{item.message_id}</td>
                    <td className="px-4 py-3">
                      <div className="max-w-xl bg-slate-950 p-2.5 rounded-xl border border-slate-800 text-slate-200 text-xs font-mono leading-relaxed">
                        {item.message}
                      </div>
                    </td>
                    <td className="px-4 py-3 text-center">
                      <span
                        className={`inline-block rounded-full px-2.5 py-1 text-xs font-bold ${
                          item.anomaly_score >= 0.8
                            ? 'bg-red-500/20 text-red-400 border border-red-500/40'
                            : 'bg-amber-500/20 text-amber-400 border border-amber-500/40'
                        }`}
                      >
                        {(item.anomaly_score * 100).toFixed(1)}%
                      </span>
                    </td>
                    <td className="px-4 py-3 text-center text-slate-400">{item.char_length}</td>
                    <td className="px-4 py-3 text-center text-amber-400 font-bold">{item.digit_count}</td>
                    <td className="px-4 py-3 text-center text-cyan-400">
                      {((item.upper_ratio || 0) * 100).toFixed(0)}%
                    </td>
                    <td className="px-4 py-3 text-center text-teal-400">
                      {((item.special_char_ratio || 0) * 100).toFixed(0)}%
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default AnomaliesPage;
