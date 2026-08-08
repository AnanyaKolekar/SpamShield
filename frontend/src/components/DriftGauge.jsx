/**
 * frontend/src/components/DriftGauge.jsx
 * 
 * Why this file exists:
 * Semi-circular radial gauge component visualizing the current drift score relative to the threshold.
 */

import React from 'react';

const DriftGauge = ({ score = 0.0, threshold = 0.35 }) => {
  const percentage = Math.min(Math.max(score * 100, 0), 100);
  const thresholdPct = Math.min(Math.max(threshold * 100, 0), 100);

  // Angle calculations for semi-circle arc (-90deg to +90deg)
  const scoreAngle = (percentage / 100) * 180 - 90;
  const thresholdAngle = (thresholdPct / 100) * 180 - 90;

  // Gauge color based on threshold
  const isHigh = score >= threshold;
  const strokeColor = isHigh ? '#ef4444' : score > 0.2 ? '#f59e0b' : '#10b981';

  return (
    <div className="flex flex-col items-center justify-center relative p-2">
      <svg className="w-48 h-28 overflow-visible" viewBox="0 0 200 110">
        {/* Background Arc */}
        <path
          d="M 20 100 A 80 80 0 0 1 180 100"
          fill="none"
          stroke="#1e293b"
          strokeWidth="16"
          strokeLinecap="round"
        />

        {/* Active Score Arc */}
        <path
          d="M 20 100 A 80 80 0 0 1 180 100"
          fill="none"
          stroke={strokeColor}
          strokeWidth="16"
          strokeLinecap="round"
          strokeDasharray="251.2"
          strokeDashoffset={251.2 - (percentage / 100) * 251.2}
          className="transition-all duration-1000 ease-out"
        />

        {/* Threshold Marker Line */}
        <g transform={`rotate(${thresholdAngle} 100 100)`}>
          <line x1="100" y1="15" x2="100" y2="30" stroke="#f43f5e" strokeWidth="4" strokeLinecap="round" />
        </g>

        {/* Center Pivot Indicator */}
        <circle cx="100" cy="100" r="8" fill="#334155" />
        
        {/* Needle */}
        <g transform={`rotate(${scoreAngle} 100 100)`} className="transition-transform duration-700 ease-out">
          <polygon points="97,100 103,100 100,28" fill="#f8fafc" />
        </g>
      </svg>

      {/* Numerical Overlay */}
      <div className="text-center -mt-4">
        <span className="text-3xl font-black font-mono tracking-tight" style={{ color: strokeColor }}>
          {percentage.toFixed(1)}%
        </span>
        <div className="flex items-center justify-center space-x-1 text-xs text-slate-400 mt-0.5">
          <span>Threshold:</span>
          <span className="font-semibold text-slate-200">{(threshold * 100).toFixed(0)}%</span>
        </div>
      </div>
    </div>
  );
};

export default DriftGauge;
