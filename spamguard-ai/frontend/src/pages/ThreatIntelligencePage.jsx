import React, { useState, useEffect } from 'react';
import { Terminal, Shield, AlertTriangle, ExternalLink } from 'lucide-react';
import { fetchThreatIntel } from '../api/client';

export default function ThreatIntelligencePage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchThreatIntel()
      .then(setData)
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  if (loading || !data) {
    return (
      <div className="flex items-center justify-center h-64 text-cyber-muted font-mono text-sm">
        Loading Threat Intelligence Catalog...
      </div>
    );
  }

  const { threat_catalog, mitre_alignment } = data;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="border-b border-cyber-border pb-4">
        <h1 className="text-2xl font-bold font-mono text-white tracking-tight flex items-center gap-2">
          <Terminal className="w-6 h-6 text-cyber-accent" />
          Threat Intelligence & Pattern Signatures
        </h1>
        <p className="text-sm text-cyber-muted mt-1">
          Heuristic rules, structural regex signatures, and MITRE ATT&CK messaging vector mapping.
        </p>
      </div>

      {/* MITRE Alignment Banner */}
      <div className="bg-cyber-card border border-cyber-border rounded-xl p-5 space-y-3">
        <div className="flex items-center gap-2 text-xs font-mono font-bold text-slate-300 uppercase tracking-wider">
          <Shield className="w-4 h-4 text-cyber-cyan" />
          <span>MITRE ATT&CK Framework Mapping (Messaging Vectors)</span>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
          {mitre_alignment.map((item, idx) => (
            <div key={idx} className="p-3 rounded-lg bg-cyber-surface border border-cyber-border text-xs font-mono">
              <span className="text-cyber-cyan font-bold block mb-0.5">{item.technique_id}</span>
              <span className="text-white font-medium block">{item.name}</span>
              <span className="text-cyber-muted text-[10px] block mt-1">Tactic: {item.tactic}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Threat Rules Catalog */}
      <div className="space-y-3">
        <div className="text-xs font-mono font-semibold text-slate-300 uppercase tracking-wider">
          Active Structural Threat Indicators ({threat_catalog.length})
        </div>
        <div className="space-y-3">
          {threat_catalog.map((rule) => (
            <div key={rule.id} className="bg-cyber-card border border-cyber-border rounded-xl p-5 space-y-3 hover:border-cyber-subtle transition-all">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                <div className="flex items-center gap-2">
                  <span className="font-mono font-bold text-cyber-cyan text-xs">
                    [{rule.id}]
                  </span>
                  <h3 className="font-mono font-bold text-white text-sm">
                    {rule.name}
                  </h3>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-cyber-surface border border-cyber-border text-slate-300">
                    {rule.category}
                  </span>
                  <span
                    className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded border ${
                      rule.severity === 'CRITICAL'
                        ? 'bg-rose-500/10 text-rose-400 border-rose-500/30'
                        : 'bg-amber-500/10 text-amber-400 border-amber-500/30'
                    }`}
                  >
                    {rule.severity}
                  </span>
                </div>
              </div>

              {/* Regex */}
              <div className="p-2.5 rounded bg-black/40 font-mono text-xs text-amber-300 border border-cyber-border break-all">
                Pattern: {rule.pattern}
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs font-sans">
                <div className="p-2.5 rounded bg-cyber-surface border border-cyber-border/80">
                  <span className="font-mono font-bold text-slate-300 block mb-1 text-[11px]">
                    Exploitation Mechanism:
                  </span>
                  <p className="text-cyber-muted leading-relaxed">{rule.mechanism}</p>
                </div>
                <div className="p-2.5 rounded bg-cyber-surface border border-cyber-border/80">
                  <span className="font-mono font-bold text-cyber-accent block mb-1 text-[11px]">
                    Mitigation Policy:
                  </span>
                  <p className="text-cyber-muted leading-relaxed">{rule.remediation}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
