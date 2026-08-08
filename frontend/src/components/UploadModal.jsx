/**
 * frontend/src/components/UploadModal.jsx
 * 
 * Why this file exists:
 * Modal component allowing users to drag-and-drop or select CSV files for batch SMS scoring.
 */

import React, { useState } from 'react';
import { X, UploadCloud, FileText, CheckCircle2, AlertCircle } from 'lucide-react';
import { uploadBatchCSV } from '../services/api';

const UploadModal = ({ isOpen, onClose, onUploadSuccess }) => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [isDragOver, setIsDragOver] = useState(false);

  if (!isOpen) return null;

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setError('');
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
      setError('');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a CSV file to upload.');
      return;
    }

    setLoading(true);
    setError('');
    try {
      const result = await uploadBatchCSV(file);
      setLoading(false);
      setFile(null);
      onUploadSuccess(result);
      onClose();
    } catch (err) {
      setLoading(false);
      setError(err.response?.data?.detail || 'Failed to upload CSV file. Please check CSV formatting.');
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 p-4 backdrop-blur-sm animate-fadeIn">
      <div className="w-full max-w-md rounded-2xl border border-slate-800 bg-slate-900 p-6 shadow-2xl">
        {/* Modal Header */}
        <div className="flex items-center justify-between border-b border-slate-800 pb-4">
          <div className="flex items-center space-x-2">
            <UploadCloud className="h-5 w-5 text-cyan-400" />
            <h3 className="text-lg font-bold text-slate-100">Upload SMS Batch CSV</h3>
          </div>
          <button
            onClick={onClose}
            className="rounded-lg p-1 text-slate-400 hover:bg-slate-800 hover:text-slate-200"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Modal Body */}
        <form onSubmit={handleSubmit} className="mt-4 space-y-4">
          <div
            onDragOver={(e) => {
              e.preventDefault();
              setIsDragOver(true);
            }}
            onDragLeave={() => setIsDragOver(false)}
            onDrop={handleDrop}
            className={`flex flex-col items-center justify-center rounded-xl border-2 border-dashed p-6 transition-all ${
              isDragOver
                ? 'border-cyan-400 bg-cyan-500/10'
                : 'border-slate-700 bg-slate-950/50 hover:border-slate-600'
            }`}
          >
            <FileText className="h-10 w-10 text-cyan-400 mb-2" />
            <p className="text-sm font-semibold text-slate-200">
              {file ? file.name : 'Drag & drop SMS batch CSV file here'}
            </p>
            <p className="text-xs text-slate-400 mt-1">
              File format: <code className="text-cyan-400 font-mono">label,message</code> or text column
            </p>
            <label className="mt-3 inline-flex cursor-pointer items-center rounded-lg bg-slate-800 px-3.5 py-1.5 text-xs font-semibold text-cyan-400 hover:bg-slate-700 border border-slate-700">
              <span>Browse File</span>
              <input type="file" accept=".csv" onChange={handleFileChange} className="hidden" />
            </label>
          </div>

          {error && (
            <div className="flex items-center space-x-2 rounded-lg bg-red-500/10 border border-red-500/30 p-3 text-xs text-red-400">
              <AlertCircle className="h-4 w-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          {/* Modal Actions */}
          <div className="flex items-center justify-end space-x-3 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="rounded-lg px-4 py-2 text-xs font-semibold text-slate-400 hover:bg-slate-800 hover:text-slate-200"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading || !file}
              className="flex items-center space-x-2 rounded-lg bg-gradient-to-r from-cyan-500 to-teal-500 px-4 py-2 text-xs font-bold text-slate-950 shadow-md hover:brightness-110 disabled:opacity-50"
            >
              {loading ? 'Analyzing Batch...' : 'Start Batch Analysis'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default UploadModal;
