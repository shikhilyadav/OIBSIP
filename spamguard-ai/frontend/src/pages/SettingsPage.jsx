import React, { useState, useEffect } from 'react';
import { Settings, Shield, Server, RefreshCw } from 'lucide-react';
import { fetchHealth } from '../api/client';

export default function SettingsPage() {
  const [health, setHealth] = useState(null);
  const [loading, setLoading] = useState(false);

  const checkStatus = async () => {
    setLoading(true);
    try {
      const data = await fetchHealth();
      setHealth(data);
    } catch (e) {
      setHealth({ status: 'offline', version: 'unknown', models_ready: false });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    checkStatus();
  }, []);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="border-b border-cyber-border pb-4">
        <h1 className="text-2xl font-bold font-mono text-white tracking-tight flex items-center gap-2">
          <Settings className="w-6 h-6 text-cyber-accent" />
          System Configuration & Settings
        </h1>
        <p className="text-sm text-cyber-muted mt-1">
          Ensemble thresholds, runtime connectivity, and privacy policy safeguards.
        </p>
      </div>

      {/* Backend Connectivity Status */}
      <div className="bg-cyber-card border border-cyber-border rounded-xl p-5 space-y-4">
        <div className="flex items-center justify-between border-b border-cyber-border pb-3">
          <div className="flex items-center gap-2 font-mono font-bold text-white text-sm">
            <Server className="w-4 h-4 text-cyber-cyan" />
            <span>FastAPI Inference Backend</span>
          </div>
          <button
            onClick={checkStatus}
            disabled={loading}
            className="flex items-center gap-1.5 px-3 py-1 rounded-lg bg-cyber-surface border border-cyber-border text-xs font-mono text-slate-300 hover:text-white"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin text-cyber-accent' : ''}`} />
            <span>Check Connectivity</span>
          </button>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs font-mono">
          <div className="p-3 rounded-lg bg-cyber-surface border border-cyber-border">
            <span className="text-cyber-muted block mb-1">Status</span>
            <span className={health?.status === 'healthy' ? 'text-cyber-accent font-bold' : 'text-amber-400 font-bold'}>
              {health?.status ? health.status.toUpperCase() : 'CHECKING...'}
            </span>
          </div>
          <div className="p-3 rounded-lg bg-cyber-surface border border-cyber-border">
            <span className="text-cyber-muted block mb-1">Backend Version</span>
            <span className="text-white font-bold">{health?.version || '2.0.0'}</span>
          </div>
          <div className="p-3 rounded-lg bg-cyber-surface border border-cyber-border">
            <span className="text-cyber-muted block mb-1">Models In Memory</span>
            <span className="text-cyber-cyan font-bold">{health?.models_ready ? 'ALL READY' : 'LOADING'}</span>
          </div>
        </div>
      </div>

      {/* Production Triage Policy Guardrails */}
      <div className="bg-cyber-card border border-cyber-border rounded-xl p-5 space-y-4">
        <div className="flex items-center gap-2 font-mono font-bold text-white text-sm border-b border-cyber-border pb-3">
          <Shield className="w-4 h-4 text-cyber-accent" />
          <span>Audited Triage Policy Parameters (Immutable)</span>
        </div>
        <p className="text-xs text-cyber-muted font-sans">
          To maintain audited mathematical rigor and prevent unverified drift, the hybrid classification thresholds are strictly locked to their experimentally validated values:
        </p>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs font-mono">
          <div className="p-3 rounded-lg bg-cyber-surface border border-cyber-border">
            <span className="text-cyber-muted block mb-1">Spam Acceptance Threshold (θ_spam)</span>
            <span className="text-cyber-danger font-bold text-base">0.60 (Enforced)</span>
            <p className="text-[11px] text-cyber-muted font-sans mt-1">
              Messages with composite probability ≥ 0.60 are automatically classified as SPAM and quarantined.
            </p>
          </div>
          <div className="p-3 rounded-lg bg-cyber-surface border border-cyber-border">
            <span className="text-cyber-muted block mb-1">Ham Clearance Threshold (θ_ham)</span>
            <span className="text-cyber-accent font-bold text-base">0.10 (Enforced)</span>
            <p className="text-[11px] text-cyber-muted font-sans mt-1">
              Messages with composite probability ≤ 0.10 are cleared automatically as legitimate HAM.
            </p>
          </div>
        </div>
      </div>

      {/* Data Retention & Privacy Disclaimer */}
      <div className="bg-cyber-card border border-cyber-border rounded-xl p-5 space-y-2">
        <h3 className="font-mono font-bold text-slate-300 text-xs uppercase tracking-wider">
          Forensic Privacy Safeguard
        </h3>
        <p className="text-xs text-cyber-muted font-sans leading-relaxed">
          SpamGuard AI operates in zero-retention mode. Analyzed message payloads are evaluated strictly in transient memory. Scan history records are kept in session RAM and are cleared upon restarting the backend or pressing "Clear Session History".
        </p>
      </div>
    </div>
  );
}
