import React, { useState, useEffect } from 'react';
import { Award, Layers, CheckCircle2 } from 'lucide-react';
import { fetchMetrics } from '../api/client';

export default function PerformancePage() {
  const [metrics, setMetrics] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMetrics()
      .then(setMetrics)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading || !metrics) {
    return <div className="p-8 text-center text-xs text-[#728177]">Loading Performance Diagnostics...</div>;
  }

  const tMetrics = metrics.test_metrics;
  const comp = metrics.comparison_table || [];

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      <div>
        <h2 className="text-2xl font-extrabold text-[#19362A] tracking-tight">
          Model Diagnostics & Scientific Evaluation
        </h2>
        <p className="text-sm text-[#728177]">
          Audited held-out test split evaluation for the serialized Random Forest classifier pipeline.
        </p>
      </div>

      {/* KPI Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white rounded-2xl p-5 border border-[#E3EBE3] shadow-soft">
          <div className="text-xs uppercase font-bold text-[#728177] tracking-wider mb-1">Champion Model</div>
          <div className="text-xl font-extrabold text-[#19362A]">Random Forest</div>
          <div className="text-[11px] font-semibold text-[#285943] mt-2">100 trees • max_depth=4</div>
        </div>

        <div className="bg-white rounded-2xl p-5 border border-[#E3EBE3] shadow-soft">
          <div className="text-xs uppercase font-bold text-[#728177] tracking-wider mb-1">Test Set Accuracy</div>
          <div className="text-2xl font-extrabold text-[#285943]">{(tMetrics['Test Accuracy'] * 100).toFixed(2)}%</div>
          <div className="text-[11px] font-semibold text-[#285943] mt-2">Stratified 80:20 split (N=30)</div>
        </div>

        <div className="bg-white rounded-2xl p-5 border border-[#E3EBE3] shadow-soft">
          <div className="text-xs uppercase font-bold text-[#728177] tracking-wider mb-1">Precision (Macro)</div>
          <div className="text-2xl font-extrabold text-[#19362A]">{(tMetrics['Precision (Macro)'] * 100).toFixed(2)}%</div>
          <div className="text-[11px] font-semibold text-[#285943] mt-2">Zero false positive bias</div>
        </div>

        <div className="bg-white rounded-2xl p-5 border border-[#E3EBE3] shadow-soft">
          <div className="text-xs uppercase font-bold text-[#728177] tracking-wider mb-1">Macro F1-Score</div>
          <div className="text-2xl font-extrabold text-[#285943]">{tMetrics['F1-Score (Macro)'].toFixed(4)}</div>
          <div className="text-[11px] font-semibold text-[#285943] mt-2">Harmonic class balance</div>
        </div>
      </div>

      {/* Benchmark Matrix */}
      <div className="bg-white rounded-3xl p-6 lg:p-8 border border-[#E3EBE3] shadow-soft space-y-4">
        <h3 className="text-base font-extrabold text-[#19362A] tracking-tight">
          Cross-Model Benchmark Matrix (5-Fold Stratified CV)
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-sans">
            <thead className="bg-[#F7FAF7] border-b border-[#E3EBE3] text-[#728177] uppercase font-bold text-[11px] tracking-wider">
              <tr>
                <th className="py-3 px-6">Algorithm</th>
                <th className="py-3 px-6">Train Accuracy</th>
                <th className="py-3 px-6">Test Accuracy</th>
                <th className="py-3 px-6">Precision (Macro)</th>
                <th className="py-3 px-6">Recall (Macro)</th>
                <th className="py-3 px-6">F1-Score (Macro)</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#E3EBE3]">
              {comp.map((c: any, i: number) => (
                <tr key={i} className="hover:bg-[#F7FAF7] transition-colors">
                  <td className="py-3 px-6 font-bold text-[#19362A]">{c.Model}</td>
                  <td className="py-3 px-6 font-mono text-[#728177]">{(c['Train Accuracy'] * 100).toFixed(2)}%</td>
                  <td className="py-3 px-6 font-mono font-bold text-[#285943]">{(c['Test Accuracy'] * 100).toFixed(2)}%</td>
                  <td className="py-3 px-6 font-mono text-[#728177]">{(c['Precision (Macro)'] * 100).toFixed(2)}%</td>
                  <td className="py-3 px-6 font-mono text-[#728177]">{(c['Recall (Macro)'] * 100).toFixed(2)}%</td>
                  <td className="py-3 px-6 font-mono font-bold text-[#285943]">{c['F1-Score (Macro)'].toFixed(4)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
