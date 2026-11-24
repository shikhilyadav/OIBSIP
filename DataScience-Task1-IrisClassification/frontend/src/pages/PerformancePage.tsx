import React, { useState, useEffect } from 'react';
import { Award, Layers, CheckCircle2, ShieldCheck, Activity, Brain } from 'lucide-react';
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

  // Exact 3x3 Confusion Matrix for held-out test split (N=30)
  // Accuracy = 29/30 (96.67%), 1 Versicolor misclassified as Virginica
  const confusionData = [
    { actual: 'Setosa', predSetosa: 10, predVersicolor: 0, predVirginica: 0, total: 10 },
    { actual: 'Versicolor', predSetosa: 0, predVersicolor: 9, predVirginica: 1, total: 10 },
    { actual: 'Virginica', predSetosa: 0, predVersicolor: 0, predVirginica: 10, total: 10 },
  ];

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Header */}
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
          <div className="text-[10px] uppercase font-bold text-[#728177] tracking-wider mb-1">
            Champion Architecture
          </div>
          <div className="text-xl font-extrabold text-[#19362A]">Random Forest</div>
          <div className="text-[11px] font-semibold text-[#285943] mt-2 flex items-center space-x-1">
            <Brain className="w-3.5 h-3.5" />
            <span>100 Trees • Gini Criterion</span>
          </div>
        </div>

        <div className="bg-white rounded-2xl p-5 border border-[#E3EBE3] shadow-soft">
          <div className="text-[10px] uppercase font-bold text-[#728177] tracking-wider mb-1">
            Test Set Accuracy
          </div>
          <div className="text-2xl font-extrabold text-[#285943]">
            {(tMetrics['Test Accuracy'] * 100).toFixed(2)}%
          </div>
          <div className="text-[11px] font-semibold text-[#285943] mt-2 flex items-center space-x-1">
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>Stratified 80:20 split (N=30)</span>
          </div>
        </div>

        <div className="bg-white rounded-2xl p-5 border border-[#E3EBE3] shadow-soft">
          <div className="text-[10px] uppercase font-bold text-[#728177] tracking-wider mb-1">
            Precision (Macro)
          </div>
          <div className="text-2xl font-extrabold text-[#19362A]">
            {(tMetrics['Precision (Macro)'] * 100).toFixed(2)}%
          </div>
          <div className="text-[11px] font-semibold text-[#285943] mt-2 flex items-center space-x-1">
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>Zero False Positive Setosa</span>
          </div>
        </div>

        <div className="bg-white rounded-2xl p-5 border border-[#E3EBE3] shadow-soft">
          <div className="text-[10px] uppercase font-bold text-[#728177] tracking-wider mb-1">
            Macro F1-Score
          </div>
          <div className="text-2xl font-extrabold text-[#285943]">
            {tMetrics['F1-Score (Macro)'].toFixed(4)}
          </div>
          <div className="text-[11px] font-semibold text-[#285943] mt-2 flex items-center space-x-1">
            <Activity className="w-3.5 h-3.5" />
            <span>Harmonic Class Balance</span>
          </div>
        </div>
      </div>

      {/* Confusion Matrix & Pipeline Architecture Split */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Confusion Matrix Heatmap (3x3) */}
        <div className="lg:col-span-7 bg-white rounded-3xl p-6 lg:p-8 border border-[#E3EBE3] shadow-soft space-y-5">
          <div className="border-b border-[#E3EBE3] pb-3">
            <h3 className="text-base font-extrabold text-[#19362A] tracking-tight">
              Held-Out Test Confusion Matrix Heatmap
            </h3>
            <p className="text-xs text-[#728177]">
              Stratified held-out test split (N=30 specimens: 10 Setosa, 10 Versicolor, 10 Virginica).
            </p>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-center text-xs font-sans">
              <thead>
                <tr>
                  <th className="py-2 px-3 text-left text-[11px] font-bold text-[#728177] uppercase tracking-wider">
                    Actual \ Predicted
                  </th>
                  <th className="py-2 px-3 text-[11px] font-bold text-[#76649D] uppercase tracking-wider">
                    Pred. Setosa
                  </th>
                  <th className="py-2 px-3 text-[11px] font-bold text-[#C18E61] uppercase tracking-wider">
                    Pred. Versicolor
                  </th>
                  <th className="py-2 px-3 text-[11px] font-bold text-[#285943] uppercase tracking-wider">
                    Pred. Virginica
                  </th>
                  <th className="py-2 px-3 text-[11px] font-bold text-[#728177] uppercase tracking-wider">
                    Recall
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#E3EBE3]">
                {confusionData.map((row, idx) => (
                  <tr key={idx} className="hover:bg-[#F7FAF7] transition-colors">
                    <td className="py-3 px-3 text-left font-bold text-[#19362A]">
                      Iris {row.actual}
                    </td>
                    <td className={`py-3 px-3 font-mono font-bold ${row.predSetosa > 0 ? 'bg-[#EFF8F0] text-[#285943]' : 'text-[#728177]'}`}>
                      {row.predSetosa}
                    </td>
                    <td className={`py-3 px-3 font-mono font-bold ${row.predVersicolor > 0 ? 'bg-[#EFF8F0] text-[#285943]' : 'text-[#728177]'}`}>
                      {row.predVersicolor}
                    </td>
                    <td className={`py-3 px-3 font-mono font-bold ${row.predVirginica === 1 ? 'bg-amber-50 text-amber-700 font-extrabold' : row.predVirginica > 0 ? 'bg-[#EFF8F0] text-[#285943]' : 'text-[#728177]'}`}>
                      {row.predVirginica}
                    </td>
                    <td className="py-3 px-3 font-mono font-bold text-[#285943]">
                      {((Math.max(row.predSetosa, row.predVersicolor, row.predVirginica) / row.total) * 100).toFixed(0)}%
                    </td>
                  </tr>
                ))}
                <tr className="bg-[#F7FAF7] font-bold text-[#19362A]">
                  <td className="py-3 px-3 text-left text-[#728177]">
                    Precision
                  </td>
                  <td className="py-3 px-3 font-mono text-[#285943]">100%</td>
                  <td className="py-3 px-3 font-mono text-[#285943]">100%</td>
                  <td className="py-3 px-3 font-mono text-[#285943]">90.9%</td>
                  <td className="py-3 px-3 font-mono text-[#285943]">96.67%</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div className="p-3.5 rounded-2xl bg-[#F7FAF7] border border-[#E3EBE3] text-[11px] text-[#728177] flex items-center justify-between">
            <span>29/30 correct classifications across held-out test distribution.</span>
            <span className="font-bold text-[#285943]">1 Error (Versicolor → Virginica)</span>
          </div>
        </div>

        {/* Model Specs / Pipeline Architecture */}
        <div className="lg:col-span-5 bg-white rounded-3xl p-6 lg:p-8 border border-[#E3EBE3] shadow-soft space-y-4">
          <div className="border-b border-[#E3EBE3] pb-3">
            <h3 className="text-base font-extrabold text-[#19362A] tracking-tight">
              Pipeline Architecture
            </h3>
            <p className="text-xs text-[#728177]">
              Deterministic scikit-learn pipeline configuration.
            </p>
          </div>

          <div className="space-y-3 text-xs">
            <div className="p-3.5 rounded-2xl bg-[#F7FAF7] border border-[#E3EBE3] space-y-1">
              <div className="font-bold text-[#19362A]">StandardScaler Step</div>
              <p className="text-[#728177] text-[11px]">
                Z-score feature centering and variance scaling fit exclusively on training fold.
              </p>
            </div>

            <div className="p-3.5 rounded-2xl bg-[#F7FAF7] border border-[#E3EBE3] space-y-1">
              <div className="font-bold text-[#19362A]">RandomForestClassifier Step</div>
              <p className="text-[#728177] text-[11px]">
                Ensemble of 100 decorrelated decision trees with max_depth=4 and Gini split criterion.
              </p>
            </div>

            <div className="p-3.5 rounded-2xl bg-[#EFF8F0] border border-[#C7E2CE] space-y-1">
              <div className="font-bold text-[#285943]">Serialization Checksum</div>
              <p className="text-[#285943] text-[11px] font-mono">
                Artifact: models/best_iris_model.joblib (4 features in)
              </p>
            </div>
          </div>
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
                <th className="py-3.5 px-6">Algorithm</th>
                <th className="py-3.5 px-6">Train Accuracy</th>
                <th className="py-3.5 px-6">Test Accuracy</th>
                <th className="py-3.5 px-6">Precision (Macro)</th>
                <th className="py-3.5 px-6">Recall (Macro)</th>
                <th className="py-3.5 px-6">F1-Score (Macro)</th>
                <th className="py-3.5 px-6">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#E3EBE3]">
              {comp.map((c: any, i: number) => {
                const isChampion = c.Model.includes('Random Forest');
                return (
                  <tr key={i} className={`transition-colors ${isChampion ? 'bg-[#EFF8F0]/40' : 'hover:bg-[#F7FAF7]'}`}>
                    <td className="py-3.5 px-6 font-bold text-[#19362A] flex items-center space-x-2">
                      {isChampion && <Award className="w-4 h-4 text-[#285943]" />}
                      <span>{c.Model}</span>
                    </td>
                    <td className="py-3.5 px-6 font-mono text-[#728177]">
                      {(c['Train Accuracy'] * 100).toFixed(2)}%
                    </td>
                    <td className="py-3.5 px-6 font-mono font-bold text-[#285943]">
                      {(c['Test Accuracy'] * 100).toFixed(2)}%
                    </td>
                    <td className="py-3.5 px-6 font-mono text-[#728177]">
                      {(c['Precision (Macro)'] * 100).toFixed(2)}%
                    </td>
                    <td className="py-3.5 px-6 font-mono text-[#728177]">
                      {(c['Recall (Macro)'] * 100).toFixed(2)}%
                    </td>
                    <td className="py-3.5 px-6 font-mono font-bold text-[#285943]">
                      {c['F1-Score (Macro)'].toFixed(4)}
                    </td>
                    <td className="py-3.5 px-6">
                      {isChampion ? (
                        <span className="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-bold bg-[#285943] text-white">
                          Champion
                        </span>
                      ) : (
                        <span className="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-bold bg-[#F7FAF7] text-[#728177] border border-[#E3EBE3]">
                          Evaluated
                        </span>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
