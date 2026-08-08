/**
 * frontend/src/components/Navbar.jsx
 * 
 * Clean, human-made header navigation.
 */

import React from 'react';
import { Shield, Activity, AlertTriangle, Cpu, Upload, Zap } from 'lucide-react';

const Navbar = ({ activeTab, setActiveTab, onOpenUpload, onRunDemo, isRunningDemo }) => {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: Activity },
    { id: 'anomalies', label: 'Anomalies', icon: AlertTriangle },
    { id: 'history', label: 'History', icon: Shield },
    { id: 'model', label: 'Model Info', icon: Cpu },
  ];

  return (
    <header className="border-b border-slate-800 bg-slate-900">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 sm:px-6">
        {/* Brand */}
        <div className="flex items-center space-x-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-cyan-500 text-slate-950 font-bold">
            <Shield className="h-5 w-5 stroke-[2.5]" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="text-lg font-bold text-slate-100 tracking-tight">
                SMS Shield
              </span>
              <span className="rounded bg-slate-800 px-2 py-0.5 text-[11px] font-medium text-cyan-400 border border-slate-700">
                Drift Monitor
              </span>
            </div>
            <p className="text-xs text-slate-400 hidden sm:block">Unsupervised Spam Drift & Campaign Detection</p>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="hidden md:flex items-center space-x-1 rounded-lg bg-slate-950 p-1 border border-slate-800">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`flex items-center space-x-2 rounded-md px-3.5 py-1.5 text-xs font-semibold transition-all ${
                  isActive
                    ? 'bg-cyan-500 text-slate-950 font-bold'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'
                }`}
              >
                <Icon className="h-3.5 w-3.5" />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>

        {/* Action Buttons */}
        <div className="flex items-center space-x-2.5">
          <button
            onClick={onRunDemo}
            disabled={isRunningDemo}
            className="flex items-center space-x-1.5 rounded-lg border border-amber-500/40 bg-amber-500/10 px-3 py-1.5 text-xs font-semibold text-amber-400 hover:bg-amber-500/20 transition-all disabled:opacity-50"
            title="Simulate incoming spam campaign drift"
          >
            <Zap className="h-3.5 w-3.5 text-amber-400" />
            <span className="hidden sm:inline">{isRunningDemo ? 'Analyzing...' : 'Simulate Campaign'}</span>
          </button>

          <button
            onClick={onOpenUpload}
            className="flex items-center space-x-1.5 rounded-lg bg-cyan-500 px-3.5 py-1.5 text-xs font-bold text-slate-950 hover:bg-cyan-400 transition-all"
          >
            <Upload className="h-3.5 w-3.5 stroke-[2.5]" />
            <span>Upload Batch</span>
          </button>
        </div>
      </div>

      {/* Mobile Nav */}
      <div className="flex md:hidden border-t border-slate-800 bg-slate-950 px-2 py-1 justify-around">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`flex flex-col items-center py-1.5 px-3 text-xs font-medium ${
                isActive ? 'text-cyan-400 font-bold' : 'text-slate-400'
              }`}
            >
              <Icon className="h-4 w-4 mb-0.5" />
              <span>{item.label}</span>
            </button>
          );
        })}
      </div>
    </header>
  );
};

export default Navbar;
