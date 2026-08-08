/**
 * frontend/src/pages/ModelInfoPage.jsx
 * 
 * Why this file exists:
 * Displays active baseline ML model specifications, hyperparameter configurations, and technical justification for TruncatedSVD vs PCA.
 */

import React from 'react';
import { Cpu, Layers, Database, ShieldCheck, HelpCircle, CheckCircle2, Sliders } from 'lucide-react';

const ModelInfoPage = ({ modelInfo }) => {
  const info = modelInfo || {
    model_name: 'SMS-Shield-IsolationForest-SVD',
    pipeline_type: 'Unsupervised Anomaly & Distribution Drift Monitoring Pipeline',
    vectorizer: { analyzer: 'char', ngram_range: [3, 5], max_features: 5000 },
    svd: { n_components: 100, algorithm: 'TruncatedSVD' },
    isolation_forest: { n_estimators: 150, contamination: 0.05 },
    baseline_ham_samples: 4827,
    drift_threshold: 0.35,
    justification_svd_vs_pca:
      'TruncatedSVD is preferred over standard PCA because character N-Gram TF-IDF produces high-dimensional sparse matrices. Standard PCA requires explicit mean-centering, converting sparse matrices into dense matrices ($O(N \\cdot D)$ memory), destroying sparsity. TruncatedSVD operates directly on sparse matrices.',
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="glass-panel p-5 rounded-2xl border border-slate-800 flex items-center space-x-3">
        <div className="p-3 rounded-xl bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
          <Cpu className="h-6 w-6 stroke-[2.5]" />
        </div>
        <div>
          <h2 className="text-xl font-black text-slate-100">{info.model_name}</h2>
          <p className="text-xs text-cyan-400 font-semibold">{info.pipeline_type}</p>
        </div>
      </div>

      {/* Grid of Architecture Cards */}
      <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
        {/* Card 1: Feature Vectorizer */}
        <div className="glass-panel p-5 rounded-2xl border border-slate-800">
          <div className="flex items-center space-x-2 pb-3 border-b border-slate-800">
            <Layers className="h-5 w-5 text-cyan-400" />
            <h3 className="text-sm font-bold text-slate-100">1. Character N-Gram TF-IDF Vectorizer</h3>
          </div>
          <div className="mt-4 space-y-2 text-xs font-mono">
            <div className="flex justify-between py-1 border-b border-slate-800/40">
              <span className="text-slate-400">Analyzer:</span>
              <span className="text-cyan-400 font-bold">{info.vectorizer?.analyzer || 'char'}</span>
            </div>
            <div className="flex justify-between py-1 border-b border-slate-800/40">
              <span className="text-slate-400">N-Gram Range:</span>
              <span className="text-slate-200">({info.vectorizer?.ngram_range?.join(', ') || '3, 5'})</span>
            </div>
            <div className="flex justify-between py-1">
              <span className="text-slate-400">Max Vocabulary Features:</span>
              <span className="text-slate-200">{info.vectorizer?.max_features || 5000}</span>
            </div>
          </div>
          <p className="text-[11px] text-slate-400 mt-3 italic">
            Captures character-level subword obfuscations such as "fr33", "cl1ck", "$$$", "W1N", "FREE!!!".
          </p>
        </div>

        {/* Card 2: TruncatedSVD */}
        <div className="glass-panel p-5 rounded-2xl border border-slate-800">
          <div className="flex items-center space-x-2 pb-3 border-b border-slate-800">
            <Sliders className="h-5 w-5 text-teal-400" />
            <h3 className="text-sm font-bold text-slate-100">2. TruncatedSVD Dimensionality Reduction</h3>
          </div>
          <div className="mt-4 space-y-2 text-xs font-mono">
            <div className="flex justify-between py-1 border-b border-slate-800/40">
              <span className="text-slate-400">Target Components:</span>
              <span className="text-teal-400 font-bold">{info.svd?.n_components || 100}</span>
            </div>
            <div className="flex justify-between py-1 border-b border-slate-800/40">
              <span className="text-slate-400">Algorithm:</span>
              <span className="text-slate-200">{info.svd?.algorithm || 'TruncatedSVD (Randomized)'}</span>
            </div>
            <div className="flex justify-between py-1">
              <span className="text-slate-400">Matrix Matrix Format:</span>
              <span className="text-slate-200">SciPy CSR Sparse Compatible</span>
            </div>
          </div>
          <p className="text-[11px] text-slate-400 mt-3 italic">
            Reduces 5,000-dimensional sparse TF-IDF vectors into a 100-dimensional dense subspace without dense centering.
          </p>
        </div>

        {/* Card 3: Isolation Forest */}
        <div className="glass-panel p-5 rounded-2xl border border-slate-800">
          <div className="flex items-center space-x-2 pb-3 border-b border-slate-800">
            <ShieldCheck className="h-5 w-5 text-emerald-400" />
            <h3 className="text-sm font-bold text-slate-100">3. Isolation Forest Anomaly Detector</h3>
          </div>
          <div className="mt-4 space-y-2 text-xs font-mono">
            <div className="flex justify-between py-1 border-b border-slate-800/40">
              <span className="text-slate-400">Estimators Count:</span>
              <span className="text-emerald-400 font-bold">{info.isolation_forest?.n_estimators || 150}</span>
            </div>
            <div className="flex justify-between py-1 border-b border-slate-800/40">
              <span className="text-slate-400">Baseline Contamination:</span>
              <span className="text-slate-200">{info.isolation_forest?.contamination || 0.05}</span>
            </div>
            <div className="flex justify-between py-1">
              <span className="text-slate-400">Baseline Ham Train Count:</span>
              <span className="text-slate-200">{info.baseline_ham_samples || 4827}</span>
            </div>
          </div>
          <p className="text-[11px] text-slate-400 mt-3 italic">
            Trained strictly on historical baseline normal (ham) traffic. Detects novel distribution shifts without supervision.
          </p>
        </div>

        {/* Card 4: SVD vs PCA Justification */}
        <div className="glass-panel p-5 rounded-2xl border border-slate-800 bg-slate-900/80">
          <div className="flex items-center space-x-2 pb-3 border-b border-slate-800">
            <HelpCircle className="h-5 w-5 text-purple-400" />
            <h3 className="text-sm font-bold text-purple-300">Technical Justification: TruncatedSVD vs PCA</h3>
          </div>
          <p className="text-xs text-slate-300 mt-3 leading-relaxed">
            {info.justification_svd_vs_pca}
          </p>
          <div className="mt-4 rounded-xl bg-slate-950 p-3 border border-slate-800 flex items-center space-x-2 text-xs text-emerald-400">
            <CheckCircle2 className="h-4 w-4 shrink-0" />
            <span>TruncatedSVD eliminates dense memory overhead while preserving TF-IDF feature information.</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ModelInfoPage;
