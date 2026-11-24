import React, { useState, useEffect } from 'react';
import { Cpu, CheckCircle2, AlertTriangle, Layers, Zap } from 'lucide-react';
import { fetchModels } from '../api/client';

export default function ModelIntelligencePage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchModels()
      .then(setData)
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  if (loading || !data) {
    return (
      <div className="flex items-center justify-center h-64 text-cyber-muted font-mono text-sm">
        Loading Model Architecture Registry...
      </div>
    );
  }

  const { models, hybrid_triage_config } = data;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="border-b border-cyber-border pb-4">
        <h1 className="text-2xl font-bold font-mono text-white tracking-tight flex items-center gap-2">
          <Cpu className="w-6 h-6 text-cyber-cyan" />
          Model Intelligence & Architecture Registry
        </h1>
        <p className="text-sm text-cyber-muted mt-1">
          Technical specifications, parameter distributions, in-distribution vs out-of-distribution generalization.
        </p>
      </div>

      {/* Hybrid Triage Enforced Architecture Card */}
      <div className="bg-cyber-card border border-emerald-500/30 rounded-xl p-5 glow-accent space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center">
              <Layers className="w-5 h-5 text-cyber-accent" />
            </div>
            <div>
              <h2 className="text-base font-bold font-mono text-white">
                {hybrid_triage_config.engine_name}
              </h2>
              <p className="text-xs text-cyber-muted font-sans">
                Dual-Threshold Abstention Routing (Enforced Production Policy)
              </p>
            </div>
          </div>
          <span className="px-3 py-1 rounded-full text-xs font-mono font-bold bg-emerald-500/15 text-cyber-accent border border-emerald-500/30">
            ENFORCED PRODUCTION POLICY
          </span>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-3 border-t border-cyber-border font-mono text-xs">
          <div className="p-3 rounded-lg bg-cyber-surface border border-cyber-border">
            <span className="text-cyber-muted block mb-1">Spam Cutoff (θ_spam)</span>
            <span className="text-cyber-danger font-bold text-sm">≥ {hybrid_triage_config.theta_spam.toFixed(2)}</span>
          </div>
          <div className="p-3 rounded-lg bg-cyber-surface border border-cyber-border">
            <span className="text-cyber-muted block mb-1">Ham Cutoff (θ_ham)</span>
            <span className="text-cyber-accent font-bold text-sm">≤ {hybrid_triage_config.theta_ham.toFixed(2)}</span>
          </div>
          <div className="p-3 rounded-lg bg-cyber-surface border border-cyber-border">
            <span className="text-cyber-muted block mb-1">Automated Coverage</span>
            <span className="text-white font-bold text-sm">{hybrid_triage_config.triage_coverage_pct}%</span>
          </div>
          <div className="p-3 rounded-lg bg-cyber-surface border border-cyber-border">
            <span className="text-cyber-muted block mb-1">Selective Accuracy</span>
            <span className="text-cyber-cyan font-bold text-sm">{hybrid_triage_config.selective_accuracy_pct}%</span>
          </div>
        </div>
      </div>

      {/* Model Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {models.map((m) => (
          <div key={m.id} className="bg-cyber-card border border-cyber-border rounded-xl p-5 space-y-4 hover:border-cyber-subtle transition-all">
            <div className="flex items-start justify-between">
              <div>
                <h3 className="text-base font-bold font-mono text-white">
                  {m.name}
                </h3>
                <span className="text-xs font-mono text-cyber-cyan">
                  {m.parameter_count}
                </span>
              </div>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-cyber-surface border border-cyber-border text-slate-300">
                {m.status.toUpperCase()}
              </span>
            </div>

            <p className="text-xs text-cyber-muted font-sans leading-relaxed">
              {m.description}
            </p>

            <div className="bg-cyber-surface rounded-lg p-3 border border-cyber-border/80 space-y-2">
              <div className="text-[11px] font-mono uppercase text-slate-400 font-semibold mb-1">
                Forensic Generalization Profile
              </div>
              <div className="grid grid-cols-2 gap-2 text-xs font-mono">
                <div>
                  <span className="text-cyber-muted block text-[10px]">In-Distribution Acc (UCI):</span>
                  <span className="text-slate-200 font-bold">{(m.in_distribution_accuracy * 100).toFixed(2)}%</span>
                </div>
                <div>
                  <span className="text-cyber-muted block text-[10px]">OOD Independent Acc (Task 5):</span>
                  <span className={`font-bold ${m.out_of_distribution_accuracy < 0.6 ? 'text-cyber-danger' : 'text-cyber-accent'}`}>
                    {m.out_of_distribution_accuracy ? `${(m.out_of_distribution_accuracy * 100).toFixed(2)}%` : 'N/A'}
                  </span>
                </div>
                <div>
                  <span className="text-cyber-muted block text-[10px]">In-Distribution Recall:</span>
                  <span className="text-slate-200 font-bold">{(m.in_distribution_recall * 100).toFixed(2)}%</span>
                </div>
                <div>
                  <span className="text-cyber-muted block text-[10px]">OOD Independent Recall:</span>
                  <span className={`font-bold ${m.out_of_distribution_recall < 0.2 ? 'text-cyber-danger' : 'text-cyber-accent'}`}>
                    {m.out_of_distribution_recall ? `${(m.out_of_distribution_recall * 100).toFixed(2)}%` : 'N/A'}
                  </span>
                </div>
              </div>
            </div>

            <div className="flex items-center justify-between text-xs font-mono text-cyber-muted pt-2 border-t border-cyber-border">
              <span className="flex items-center gap-1">
                <Zap className="w-3.5 h-3.5 text-amber-400" />
                <span>Latency: {m.latency_per_sample_ms} ms</span>
              </span>
              <span className="text-slate-400">Target: Binary SMS</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
