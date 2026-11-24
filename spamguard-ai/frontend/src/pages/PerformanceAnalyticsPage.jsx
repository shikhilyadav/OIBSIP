import React, { useState, useEffect } from 'react';
import { BarChart3, AlertOctagon, CheckCircle2, Users, ShieldAlert } from 'lucide-react';
import { fetchBenchmarkMetrics, fetchAnalytics } from '../api/client';
import { 
  ResponsiveContainer, 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  Tooltip, 
  Legend 
} from 'recharts';

export default function PerformanceAnalyticsPage() {
  const [benchmark, setBenchmark] = useState(null);
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([fetchBenchmarkMetrics(), fetchAnalytics()])
      .then(([bench, ana]) => {
        setBenchmark(bench);
        setAnalytics(ana);
      })
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  if (loading || !benchmark || !analytics) {
    return (
      <div className="flex items-center justify-center h-64 text-cyber-muted font-mono text-sm">
        Loading Audited Historical Benchmarks...
      </div>
    );
  }

  const { audited_hybrid_metrics } = benchmark;
  const { confusion_matrices, metrics_comparison } = analytics;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="border-b border-cyber-border pb-4">
        <h1 className="text-2xl font-bold font-mono text-white tracking-tight flex items-center gap-2">
          <BarChart3 className="w-6 h-6 text-cyber-accent" />
          Forensic Performance Analytics & Audited Benchmarks
        </h1>
        <p className="text-sm text-cyber-muted mt-1">
          Authentic metrics derived from Task 5 independent audit ($N=1,000$ modern unseen SMS test set).
        </p>
      </div>

      {/* Comparison Chart */}
      <div className="bg-cyber-card border border-cyber-border rounded-xl p-5">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-4">
          <div>
            <h2 className="text-sm font-semibold font-mono text-white uppercase tracking-wider">
              Out-of-Distribution Benchmark Comparison (%)
            </h2>
            <p className="text-xs text-cyber-muted">Evaluated on Task 5 independent test set (500 Ham / 500 Spam)</p>
          </div>
        </div>
        <div className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={metrics_comparison}>
              <XAxis dataKey="metric" stroke="#475569" tick={{ fill: '#8A99AD', fontSize: 12 }} />
              <YAxis stroke="#475569" tick={{ fill: '#8A99AD', fontSize: 12 }} domain={[0, 100]} />
              <Tooltip contentStyle={{ backgroundColor: '#0D1422', borderColor: '#1E2D44', borderRadius: '8px' }} />
              <Legend wrapperStyle={{ paddingTop: '10px' }} />
              <Bar dataKey="Naive Bayes" fill="#FFB800" radius={[4, 4, 0, 0]} />
              <Bar dataKey="BERT-Tiny" fill="#00D9F5" radius={[4, 4, 0, 0]} />
              <Bar dataKey="Hybrid Automated" fill="#00F5A0" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Audited Confusion Matrices 3-Column Grid */}
      <div className="space-y-3">
        <div className="text-xs font-mono font-semibold text-slate-300 uppercase tracking-wider">
          Audited Confusion Matrices ($N=1,000$ Samples)
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Naive Bayes */}
          <div className="bg-cyber-card border border-cyber-border rounded-xl p-4 space-y-3">
            <div className="flex items-center justify-between border-b border-cyber-border pb-2">
              <span className="font-mono font-bold text-xs text-white">Multinomial Naive Bayes</span>
              <span className="text-[10px] font-mono text-amber-400">Acc: 53.50%</span>
            </div>
            <div className="grid grid-cols-2 gap-2 text-center font-mono text-xs">
              <div className="p-2 rounded bg-cyber-surface border border-cyber-border">
                <span className="text-[10px] text-cyber-muted block">True Negative</span>
                <span className="text-emerald-400 font-bold text-base">499</span>
              </div>
              <div className="p-2 rounded bg-cyber-surface border border-rose-500/20">
                <span className="text-[10px] text-cyber-muted block">False Positive</span>
                <span className="text-cyber-danger font-bold text-base">1</span>
              </div>
              <div className="p-2 rounded bg-cyber-surface border border-rose-500/40">
                <span className="text-[10px] text-cyber-danger font-bold block">False Negative</span>
                <span className="text-cyber-danger font-bold text-base">464</span>
              </div>
              <div className="p-2 rounded bg-cyber-surface border border-cyber-border">
                <span className="text-[10px] text-cyber-muted block">True Positive</span>
                <span className="text-cyber-cyan font-bold text-base">36</span>
              </div>
            </div>
            <p className="text-[11px] text-cyber-muted leading-tight font-sans">
              464 false negatives caused by vocabulary shift on modern phishing templates.
            </p>
          </div>

          {/* BERT-Tiny */}
          <div className="bg-cyber-card border border-cyber-border rounded-xl p-4 space-y-3">
            <div className="flex items-center justify-between border-b border-cyber-border pb-2">
              <span className="font-mono font-bold text-xs text-white">BERT-Tiny Pretrained</span>
              <span className="text-[10px] font-mono text-cyan-400">Acc: 87.10%</span>
            </div>
            <div className="grid grid-cols-2 gap-2 text-center font-mono text-xs">
              <div className="p-2 rounded bg-cyber-surface border border-cyber-border">
                <span className="text-[10px] text-cyber-muted block">True Negative</span>
                <span className="text-emerald-400 font-bold text-base">488</span>
              </div>
              <div className="p-2 rounded bg-cyber-surface border border-rose-500/20">
                <span className="text-[10px] text-cyber-muted block">False Positive</span>
                <span className="text-cyber-danger font-bold text-base">12</span>
              </div>
              <div className="p-2 rounded bg-cyber-surface border border-rose-500/40">
                <span className="text-[10px] text-cyber-danger font-bold block">False Negative</span>
                <span className="text-cyber-danger font-bold text-base">117</span>
              </div>
              <div className="p-2 rounded bg-cyber-surface border border-cyber-border">
                <span className="text-[10px] text-cyber-muted block">True Positive</span>
                <span className="text-cyber-cyan font-bold text-base">383</span>
              </div>
            </div>
            <p className="text-[11px] text-cyber-muted leading-tight font-sans">
              117 false negatives due to low confidence on ambiguous promotional SMS.
            </p>
          </div>

          {/* Hybrid Automated */}
          <div className="bg-cyber-card border border-emerald-500/30 rounded-xl p-4 space-y-3 glow-accent">
            <div className="flex items-center justify-between border-b border-cyber-border pb-2">
              <span className="font-mono font-bold text-xs text-cyber-accent">Hybrid Triage Layer</span>
              <span className="text-[10px] font-mono text-emerald-400 font-bold">Sel. Acc: 96.66%</span>
            </div>
            <div className="grid grid-cols-2 gap-2 text-center font-mono text-xs">
              <div className="p-2 rounded bg-cyber-surface border border-emerald-500/30">
                <span className="text-[10px] text-cyber-muted block">True Negative</span>
                <span className="text-emerald-400 font-bold text-base">432</span>
              </div>
              <div className="p-2 rounded bg-cyber-surface border border-cyber-border">
                <span className="text-[10px] text-cyber-muted block">False Positive</span>
                <span className="text-slate-300 font-bold text-base">12</span>
              </div>
              <div className="p-2 rounded bg-cyber-surface border border-cyber-border">
                <span className="text-[10px] text-cyber-muted block">False Negative</span>
                <span className="text-slate-300 font-bold text-base">15</span>
              </div>
              <div className="p-2 rounded bg-cyber-surface border border-emerald-500/30">
                <span className="text-[10px] text-cyber-muted block">True Positive</span>
                <span className="text-cyber-accent font-bold text-base">350</span>
              </div>
            </div>
            <p className="text-[11px] text-cyber-muted leading-tight font-sans">
              Automated decisions on 809 messages (80.9% coverage); 191 ambiguous routed to review.
            </p>
          </div>
        </div>
      </div>

      {/* Review Queue Composition Audit Card */}
      <div className="bg-cyber-card border border-amber-500/30 rounded-xl p-5 space-y-3">
        <div className="flex items-center gap-2">
          <Users className="w-5 h-5 text-amber-400" />
          <h3 className="text-sm font-bold font-mono text-white">
            Human-in-the-Loop Review Queue Composition ($N=191$ Messages)
          </h3>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs font-mono">
          <div className="p-3 rounded-lg bg-cyber-surface border border-cyber-border">
            <span className="text-cyber-muted block mb-1">Spam In Review Queue</span>
            <span className="text-cyber-danger font-bold text-base">
              {audited_hybrid_metrics.review_queue_composition.spam_count} messages (70.68%)
            </span>
          </div>
          <div className="p-3 rounded-lg bg-cyber-surface border border-cyber-border">
            <span className="text-cyber-muted block mb-1">Ham In Review Queue</span>
            <span className="text-cyber-accent font-bold text-base">
              {audited_hybrid_metrics.review_queue_composition.ham_count} messages (29.32%)
            </span>
          </div>
          <div className="p-3 rounded-lg bg-cyber-surface border border-cyber-border">
            <span className="text-cyber-muted block mb-1">Audited Coverage Rate</span>
            <span className="text-cyber-cyan font-bold text-base">
              {audited_hybrid_metrics.coverage_percentage}% Automated
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
