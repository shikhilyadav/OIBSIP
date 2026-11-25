import React, { useState, useEffect } from 'react';
import { 
  Cpu, 
  BarChart2, 
  TrendingUp, 
  TrendingDown, 
  CheckCircle2, 
  Layers, 
  Sparkles,
  Info
} from 'lucide-react';
import { 
  ResponsiveContainer, 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Cell 
} from 'recharts';
import { fetchFeatureImportance, fetchModelInfo, FeatureImportanceItem } from '../api/client';

export default function ModelIntelligencePage() {
  const [importance, setImportance] = useState<FeatureImportanceItem[]>([]);
  const [modelInfo, setModelInfo] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetchFeatureImportance().catch(() => []),
      fetchModelInfo().catch(() => null)
    ]).then(([fi, mi]) => {
      setImportance(fi);
      setModelInfo(mi);
    }).finally(() => setLoading(false));
  }, []);

  const top10 = importance.slice(0, 10);

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-extrabold text-[#073B32] tracking-tight font-display">
          Model Intelligence & Feature Coefficients
        </h2>
        <p className="text-xs text-[#77827E] mt-0.5">
          Audited feature impact analysis and coefficient weights from the scikit-learn regression pipeline.
        </p>
      </div>

      {/* Model Spec Card */}
      <div className="bg-white rounded-3xl p-6 lg:p-8 border border-[#E4E8E1] shadow-soft space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-[#E4E8E1] pb-4">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-2xl bg-[#073B32] text-[#E6B85C] flex items-center justify-center">
              <Cpu className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-extrabold text-[#073B32] font-display">
                Transformed Target Linear Regression Pipeline
              </h3>
              <p className="text-xs text-[#77827E]">
                Target Log1p transform ensures strictly non-negative prices and corrects exponential depreciation curves.
              </p>
            </div>
          </div>
          <span className="text-xs font-bold px-3 py-1 rounded-full bg-[#E8F3EE] text-[#125B48] font-mono">
            R² = 0.7120 on Test Set
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs pt-1">
          <div className="p-3.5 rounded-2xl bg-[#F7F5F0] border border-[#E4E8E1] space-y-1">
            <span className="text-[10px] uppercase font-bold text-[#77827E]">Numerical Preprocessing</span>
            <div className="font-bold text-[#073B32]">StandardScaler (Z-Score)</div>
            <p className="text-[11px] text-[#77827E]">Applied to car_age and km_driven.</p>
          </div>
          <div className="p-3.5 rounded-2xl bg-[#F7F5F0] border border-[#E4E8E1] space-y-1">
            <span className="text-[10px] uppercase font-bold text-[#77827E]">Categorical Encoding</span>
            <div className="font-bold text-[#073B32]">OneHotEncoder (handle_unknown='ignore')</div>
            <p className="text-[11px] text-[#77827E]">One-hot encodings across brand, fuel, transmission, seller, owner.</p>
          </div>
          <div className="p-3.5 rounded-2xl bg-[#F7F5F0] border border-[#E4E8E1] space-y-1">
            <span className="text-[10px] uppercase font-bold text-[#77827E]">Target Transformation</span>
            <div className="font-bold text-[#073B32]">np.log1p / np.expm1</div>
            <p className="text-[11px] text-[#77827E]">Corrects right-skewed pricing and prevents negative valuations.</p>
          </div>
        </div>
      </div>

      {/* Feature Importance Bar Chart */}
      <div className="bg-white rounded-3xl p-6 lg:p-8 border border-[#E4E8E1] shadow-soft space-y-4">
        <div className="border-b border-[#E4E8E1] pb-3 flex justify-between items-center">
          <div>
            <h3 className="text-base font-extrabold text-[#073B32] font-display">
              Top 10 Strongest Price-Influencing Coefficients
            </h3>
            <p className="text-xs text-[#77827E]">
              Positive weights increase valuation; negative weights reflect market depreciation or economy tiering.
            </p>
          </div>
          <div className="flex items-center space-x-3 text-xs">
            <span className="flex items-center space-x-1 text-[#125B48]">
              <span className="w-2.5 h-2.5 rounded-full bg-[#125B48]"></span>
              <span>Value Premium (+)</span>
            </span>
            <span className="flex items-center space-x-1 text-rose-700">
              <span className="w-2.5 h-2.5 rounded-full bg-rose-600"></span>
              <span>Depreciation Factor (-)</span>
            </span>
          </div>
        </div>

        <div className="h-72 my-2">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={top10}
              layout="vertical"
              margin={{ top: 5, right: 30, left: 80, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="#E4E8E1" horizontal={false} />
              <XAxis type="number" tick={{ fill: '#77827E', fontSize: 11 }} />
              <YAxis 
                type="category" 
                dataKey="display_name" 
                tick={{ fill: '#202A28', fontSize: 11 }}
                width={120}
              />
              <Tooltip 
                formatter={(val: any) => [`${val}`, 'Coefficient Weight']}
                contentStyle={{ backgroundColor: '#FFFFFF', borderColor: '#E4E8E1', borderRadius: '12px' }}
              />
              <Bar dataKey="coefficient" radius={[4, 4, 4, 4]}>
                {top10.map((entry, index) => (
                  <Cell 
                    key={`cell-${index}`} 
                    fill={entry.direction === 'positive' ? '#125B48' : '#BE123C'} 
                  />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Analytical Findings Callout */}
        <div className="p-4 rounded-2xl bg-[#F7F5F0] border border-[#E4E8E1] space-y-2 text-xs leading-relaxed text-[#202A28]">
          <div className="font-bold text-[#073B32] flex items-center space-x-1.5">
            <Sparkles className="w-4 h-4 text-[#E6B85C]" />
            <span>Key Econometric Observations:</span>
          </div>
          <ul className="list-disc pl-5 space-y-1 text-[#77827E]">
            <li><b>Luxury Brand Equity:</b> Land Rover (+1.320), Jaguar (+1.155), Mercedes-Benz (+0.838), and BMW (+0.694) exhibit the highest positive multipliers in the Indian secondary car market.</li>
            <li><b>Car Age Depreciation:</b> Age (-0.475) is by far the single strongest numerical depreciator, overshadowing pure kilometer usage (-0.035).</li>
            <li><b>Powertrain Premium:</b> Diesel (+0.370) command a significant valuation premium over Petrol (-0.051) and alternative fuels.</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
