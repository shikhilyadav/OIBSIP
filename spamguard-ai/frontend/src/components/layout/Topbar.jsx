import React, { useState, useEffect } from 'react';
import { ShieldCheck, Activity, Bell, RefreshCw, Cpu } from 'lucide-react';
import { fetchHealth } from '../../api/client';

export default function Topbar() {
  const [health, setHealth] = useState({ status: 'checking', active_models: {} });
  const [isRefreshing, setIsRefreshing] = useState(false);

  const checkStatus = async () => {
    setIsRefreshing(true);
    try {
      const data = await fetchHealth();
      setHealth(data);
    } catch (e) {
      setHealth({ status: 'offline', active_models: {} });
    } finally {
      setIsRefreshing(false);
    }
  };

  useEffect(() => {
    checkStatus();
    const interval = setInterval(checkStatus, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <header className="h-16 bg-cyber-card border-b border-cyber-border px-6 flex items-center justify-between sticky top-0 z-20">
      {/* Title / Status */}
      <div className="flex items-center space-x-4">
        <div className="flex items-center space-x-2">
          <Activity className="w-4 h-4 text-cyber-accent" />
          <span className="text-xs font-mono font-medium text-slate-300">
            SYSTEM STATUS:
          </span>
          <span
            className={`text-xs font-mono font-bold px-2 py-0.5 rounded border ${
              health.status === 'healthy'
                ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
                : health.status === 'checking'
                ? 'bg-amber-500/10 text-amber-400 border-amber-500/30'
                : 'bg-rose-500/10 text-rose-400 border-rose-500/30'
            }`}
          >
            {health.status.toUpperCase()}
          </span>
        </div>

        <div className="hidden md:flex items-center space-x-3 text-xs text-cyber-muted font-mono border-l border-cyber-border pl-4">
          <span className="flex items-center space-x-1">
            <Cpu className="w-3.5 h-3.5 text-cyber-cyan" />
            <span>BERT-Tiny (4.39M params): Active</span>
          </span>
        </div>
      </div>

      {/* Right Controls */}
      <div className="flex items-center space-x-3">
        <button
          onClick={checkStatus}
          disabled={isRefreshing}
          className="p-2 rounded-lg bg-cyber-surface hover:bg-cyber-subtle text-slate-400 hover:text-slate-200 transition-colors border border-cyber-border"
          title="Refresh Backend Health"
        >
          <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin text-cyber-accent' : ''}`} />
        </button>

        <div className="flex items-center space-x-2 px-3 py-1.5 rounded-lg bg-cyber-surface border border-cyber-border text-xs font-mono">
          <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
          <span className="text-slate-300">FastAPI Port 8000</span>
        </div>
      </div>
    </header>
  );
}
