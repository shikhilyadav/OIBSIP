import React, { useState, useEffect } from 'react';
import { 
  BarChart2, 
  Award, 
  Activity, 
  TrendingUp, 
  ShieldCheck, 
  Layers,
  Sparkles
} from 'lucide-react';
import { fetchMetrics } from '../api/client';

export default function EvaluationPage() {
  const [metrics, setMetrics] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMetrics()
      .then(setMetrics)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const comparison = metrics?.model_comparison || {
    "Linear Regression": {
      "cv_r2_mean": 0.6981, "cv_r2_std": 0.072, "cv_mae": 136928.51, "cv_rmse": 269369.81,
      "test_r2": 0.712, "test_mae": 144221.02, "test_rmse": 304581.55
    },
    "Ridge Regression": {
      "cv_r2_mean": 0.6955, "cv_r2_std": 0.0901, "cv_mae": 138146.05, "cv_rmse": 271406.44,
      "test_r2": 0.6884, "test_mae": 145432.24, "test_rmse": 316840.94
    },
    "Random Forest": {
      "cv_r2_mean": 0.6685, "cv_r2_std": 0.1198, "cv_mae": 140985.25, "cv_rmse": 282629.68,
      "test_r2": 0.6275, "test_mae": 144999.64, "test_rmse": 346417.04
    },
    "Gradient Boosting": {
      "cv_r2_mean": 0.6822, "cv_r2_std": 0.0996, "cv_mae": 136753.1, "cv_rmse": 276497.09,
      "test_r2": 0.5437, "test_mae": 148130.59, "test_rmse": 383371.75
    }
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-extrabold text-[#073B32] tracking-tight font-display">
          Scientific Valuation Model Evaluation
        </h2>
        <p className="text-xs text-[#77827E] mt-0.5">
          Audited 5-Fold Stratified Cross-Validation and held-out test split evaluation for the CarDekho regression models.
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white rounded-2xl p-5 border border-[#E4E8E1] shadow-soft">
          <span className="text-[10px] uppercase font-bold text-[#77827E] tracking-wider block mb-1">
            Champion Model
          </span>
          <div className="text-xl font-extrabold text-[#073B32] font-display">
            Linear Regression
          </div>
          <div className="text-[11px] font-semibold text-[#125B48] mt-2">
            Target Log-Transformed
          </div>
        </div>

        <div className="bg-white rounded-2xl p-5 border border-[#E4E8E1] shadow-soft">
          <span className="text-[10px] uppercase font-bold text-[#77827E] tracking-wider block mb-1">
            Test R² Score
          </span>
          <div className="text-2xl font-extrabold text-[#125B48] font-display">
            0.7120 (71.2%)
          </div>
          <div className="text-[11px] font-semibold text-[#77827E] mt-2 font-mono">
            5-Fold CV Mean: 0.6981
          </div>
        </div>

        <div className="bg-white rounded-2xl p-5 border border-[#E4E8E1] shadow-soft">
          <span className="text-[10px] uppercase font-bold text-[#77827E] tracking-wider block mb-1">
            Test MAE (Mean Error)
          </span>
          <div className="text-2xl font-extrabold text-[#202A28] font-display">
            ₹1.44 Lakh
          </div>
          <div className="text-[11px] font-semibold text-[#77827E] mt-2 font-mono">
            ₹144,221.02 INR
          </div>
        </div>

        <div className="bg-white rounded-2xl p-5 border border-[#E4E8E1] shadow-soft">
          <span className="text-[10px] uppercase font-bold text-[#77827E] tracking-wider block mb-1">
            Test RMSE
          </span>
          <div className="text-2xl font-extrabold text-[#E6B85C] font-display">
            ₹3.05 Lakh
          </div>
          <div className="text-[11px] font-semibold text-[#77827E] mt-2 font-mono">
            ₹304,581.55 INR
          </div>
        </div>
      </div>

      {/* Model Benchmark Matrix */}
      <div className="bg-white rounded-3xl p-6 lg:p-8 border border-[#E4E8E1] shadow-soft space-y-4">
        <div className="border-b border-[#E4E8E1] pb-3">
          <h3 className="text-base font-extrabold text-[#073B32] font-display">
            Cross-Model Regression Benchmark Matrix
          </h3>
          <p className="text-xs text-[#77827E]">
            Comparison across 5-Fold Cross Validation and 20% hold-out test set (716 test vehicles).
          </p>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-sans">
            <thead className="bg-[#F7F5F0] text-[#77827E] uppercase font-bold text-[10px] tracking-wider">
              <tr>
                <th className="py-3 px-4 rounded-l-xl">Algorithm</th>
                <th className="py-3 px-4">CV Mean R²</th>
                <th className="py-3 px-4">Test R²</th>
                <th className="py-3 px-4">Test MAE (INR)</th>
                <th className="py-3 px-4">Test RMSE (INR)</th>
                <th className="py-3 px-4 rounded-r-xl">Outcome</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#E4E8E1]">
              {Object.entries(comparison).map(([mName, data]: [string, any], idx) => {
                const isChampion = mName === 'Linear Regression';
                return (
                  <tr key={idx} className={`transition-colors ${isChampion ? 'bg-[#E8F3EE]/50' : 'hover:bg-[#F7F5F0]/50'}`}>
                    <td className="py-3.5 px-4 font-bold text-[#202A28] flex items-center space-x-2">
                      {isChampion && <Award className="w-4 h-4 text-[#E6B85C]" />}
                      <span>{mName}</span>
                    </td>
                    <td className="py-3.5 px-4 font-mono text-[#77827E]">
                      {data.cv_r2_mean.toFixed(4)}
                    </td>
                    <td className="py-3.5 px-4 font-mono font-bold text-[#125B48]">
                      {data.test_r2.toFixed(4)}
                    </td>
                    <td className="py-3.5 px-4 font-mono text-[#202A28]">
                      ₹{Math.round(data.test_mae).toLocaleString()}
                    </td>
                    <td className="py-3.5 px-4 font-mono text-[#77827E]">
                      ₹{Math.round(data.test_rmse).toLocaleString()}
                    </td>
                    <td className="py-3.5 px-4">
                      {isChampion ? (
                        <span className="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-bold bg-[#073B32] text-[#E6B85C]">
                          Champion
                        </span>
                      ) : (
                        <span className="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-bold bg-[#F7F5F0] text-[#77827E] border border-[#E4E8E1]">
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

        <div className="p-4 rounded-2xl bg-[#F7F5F0] border border-[#E4E8E1] text-xs leading-relaxed text-[#202A28]">
          <b>Why Linear Regression Outperformed Ensembles:</b> In pre-owned car pricing, vehicle values follow a smooth, continuous exponential decay curve (P = P₀ · e^-λt). Log-transformed target regression models this physical reality natively, whereas decision-tree ensembles partition feature space into piecewise constant steps and struggle to extrapolate on high-mileage or luxury edge cases.
        </div>
      </div>
    </div>
  );
}
