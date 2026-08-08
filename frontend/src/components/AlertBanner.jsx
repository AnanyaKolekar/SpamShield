/**
 * frontend/src/components/AlertBanner.jsx
 * 
 * Clean, human-made alert status banner.
 */

import React from 'react';
import { AlertTriangle, CheckCircle2, ShieldAlert } from 'lucide-react';

const AlertBanner = ({ driftScore, threshold = 0.35, driftStatus }) => {
  const isHighDrift = driftScore >= threshold || driftStatus === 'HIGH DRIFT DETECTED';

  return (
    <div
      className={`rounded-xl p-4 border transition-all ${
        isHighDrift
          ? 'bg-red-950/40 border-red-800/80 text-red-200'
          : 'bg-emerald-950/30 border-emerald-800/60 text-emerald-200'
      }`}
    >
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="flex items-center space-x-3">
          <div
            className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-lg ${
              isHighDrift ? 'bg-red-900/60 text-red-400' : 'bg-emerald-900/60 text-emerald-400'
            }`}
          >
            {isHighDrift ? (
              <ShieldAlert className="h-5 w-5" />
            ) : (
              <CheckCircle2 className="h-5 w-5" />
            )}
          </div>

          <div>
            <div className="flex items-center space-x-2">
              <h2 className="text-base font-bold tracking-tight">
                {isHighDrift ? 'HIGH DRIFT DETECTED' : 'NORMAL TRAFFIC'}
              </h2>
              <span
                className={`rounded-md px-2 py-0.5 text-xs font-semibold ${
                  isHighDrift ? 'bg-red-900/50 text-red-300' : 'bg-emerald-900/50 text-emerald-300'
                }`}
              >
                Threshold: {(threshold * 100).toFixed(0)}%
              </span>
            </div>
            <p className="text-xs text-slate-300 mt-0.5">
              {isHighDrift
                ? 'Incoming SMS traffic patterns deviate significantly from baseline normal behavior. Possible spam campaign shift detected.'
                : 'SMS message distributions are consistent with normal historical traffic.'}
            </p>
          </div>
        </div>

        <div className="text-right shrink-0">
          <span className="text-[11px] font-medium text-slate-400 block">Current Drift Score</span>
          <span className="text-2xl font-black font-mono">
            {(driftScore * 100).toFixed(1)}%
          </span>
        </div>
      </div>
    </div>
  );
};

export default AlertBanner;
