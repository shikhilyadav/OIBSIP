import React from 'react';
import { ShieldCheck, AlertTriangle, ExternalLink } from 'lucide-react';

export default function ThreatSignalsView({ signals }) {
  if (!signals || signals.length === 0) {
    return (
      <div className="p-4 rounded-lg bg-cyber-surface/50 border border-cyber-border text-center">
        <ShieldCheck className="w-5 h-5 text-cyber-accent mx-auto mb-1" />
        <p className="text-xs text-slate-300 font-medium">No Structural Threat Patterns Detected</p>
        <p className="text-[11px] text-cyber-muted">Message contains no blacklisted shortcodes, urgent callback traps, or masked URLs.</p>
      </div>
    );
  }

  const severityStyles = {
    critical: 'border-red-500/40 bg-red-950/20 text-red-300',
    high: 'border-rose-500/30 bg-rose-950/20 text-rose-300',
    medium: 'border-amber-500/30 bg-amber-950/20 text-amber-300',
    low: 'border-blue-500/30 bg-blue-950/20 text-blue-300'
  };

  return (
    <div className="space-y-2">
      {signals.map((sig, idx) => (
        <div
          key={idx}
          className={`p-3 rounded-lg border text-xs ${
            severityStyles[sig.severity.toLowerCase()] || severityStyles.medium
          }`}
        >
          <div className="flex items-center justify-between mb-1">
            <span className="font-mono font-bold uppercase tracking-wider text-[11px]">
              {sig.signal_type}
            </span>
            <span className="font-mono font-bold text-[10px] px-1.5 py-0.5 rounded bg-black/40 border border-current">
              {sig.severity.toUpperCase()}
            </span>
          </div>
          <div className="font-mono text-slate-200 bg-black/30 px-2 py-1 rounded my-1 text-[11px] break-all">
            Match: "{sig.indicator}"
          </div>
          <p className="text-slate-300 text-[11px]">{sig.description}</p>
        </div>
      ))}
    </div>
  );
}
