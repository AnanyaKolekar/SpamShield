/**
 * frontend/src/App.jsx
 * 
 * Why this file exists:
 * Main root application container managing active tabs, API data loading, date filter states,
 * campaign demo triggers, and upload modal triggers.
 */

import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import DashboardPage from './pages/DashboardPage';
import AnomaliesPage from './pages/AnomaliesPage';
import HistoryPage from './pages/HistoryPage';
import ModelInfoPage from './pages/ModelInfoPage';
import UploadModal from './components/UploadModal';
import {
  fetchDashboardData,
  fetchDriftHistory,
  fetchAnomalies,
  fetchModelInfo,
  runDemoScore
} from './services/api';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [dateFilter, setDateFilter] = useState('7d');
  const [isUploadOpen, setIsUploadOpen] = useState(false);
  const [isRunningDemo, setIsRunningDemo] = useState(false);
  const [loading, setLoading] = useState(true);

  // API State
  const [dashboardData, setDashboardData] = useState(null);
  const [history, setHistory] = useState([]);
  const [anomalies, setAnomalies] = useState([]);
  const [modelInfo, setModelInfo] = useState(null);

  const loadAllData = async () => {
    setLoading(true);
    try {
      const [dash, hist, anom, info] = await Promise.all([
        fetchDashboardData(),
        fetchDriftHistory(),
        fetchAnomalies(),
        fetchModelInfo()
      ]);
      setDashboardData(dash);
      setHistory(hist);
      setAnomalies(anom);
      setModelInfo(info);
    } catch (err) {
      console.error('Error fetching API data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAllData();
  }, []);

  const handleRunDemo = async () => {
    setIsRunningDemo(true);
    try {
      await runDemoScore();
      await loadAllData();
      setActiveTab('dashboard');
    } catch (err) {
      console.error('Failed to run demo campaign score:', err);
    } finally {
      setIsRunningDemo(false);
    }
  };

  const handleUploadSuccess = async () => {
    await loadAllData();
    setActiveTab('dashboard');
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-cyan-500 selection:text-slate-950">
      {/* Top Header Navbar */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        onOpenUpload={() => setIsUploadOpen(true)}
        onRunDemo={handleRunDemo}
        isRunningDemo={isRunningDemo}
      />

      {/* Main Content Area */}
      <main className="flex-1 mx-auto w-full max-w-7xl px-4 py-6 sm:px-6">
        {loading ? (
          <div className="flex flex-col items-center justify-center py-20">
            <div className="h-10 w-10 animate-spin rounded-full border-4 border-slate-800 border-t-cyan-400"></div>
            <p className="mt-4 text-xs font-semibold text-slate-400">Loading SMS Shield Intelligence System...</p>
          </div>
        ) : (
          <>
            {activeTab === 'dashboard' && (
              <DashboardPage
                data={dashboardData}
                dateFilter={dateFilter}
                setDateFilter={setDateFilter}
                onRunDemo={handleRunDemo}
              />
            )}

            {activeTab === 'anomalies' && (
              <AnomaliesPage anomalies={anomalies.length > 0 ? anomalies : (dashboardData?.top_suspicious_messages || [])} />
            )}

            {activeTab === 'history' && (
              <HistoryPage history={history.length > 0 ? history : (dashboardData?.daily_trend || [])} />
            )}

            {activeTab === 'model' && (
              <ModelInfoPage modelInfo={modelInfo} />
            )}
          </>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-900 bg-slate-950 py-4 text-center text-xs text-slate-500">
        <div className="mx-auto max-w-7xl px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
          <span>SMS Shield v1.0.0 &bull; Unsupervised SMS Drift & Emerging Campaign Detection</span>
          <span className="text-slate-600">Built with React, FastAPI, TruncatedSVD & Isolation Forest</span>
        </div>
      </footer>

      {/* Batch CSV Upload Modal */}
      <UploadModal
        isOpen={isUploadOpen}
        onClose={() => setIsUploadOpen(false)}
        onUploadSuccess={handleUploadSuccess}
      />
    </div>
  );
}

export default App;
