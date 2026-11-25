import React from 'react';
import { 
  BookOpen, 
  Terminal, 
  Cpu, 
  Car, 
  Layers, 
  CheckCircle2, 
  Code2, 
  ExternalLink 
} from 'lucide-react';

export default function DocumentationPage() {
  const endpoints = [
    { method: 'POST', path: '/api/predict', desc: 'Computes real-time fair-market appraisal value and valuation bounds for a vehicle spec.' },
    { method: 'POST', path: '/api/predict/batch', desc: 'Processes batch vehicle lists (up to 100 items) for fleet valuation appraisal.' },
    { method: 'GET', path: '/api/dataset/summary', desc: 'Returns descriptive statistical moments and price distributions for the 3,577 records.' },
    { method: 'GET', path: '/api/dataset/records', desc: 'Paginated, filterable, and searchable access to cleaned CarDekho fleet records.' },
    { method: 'GET', path: '/api/dataset/options', desc: 'Returns categorical options for makes, fuels, transmissions, and owner titles.' },
    { method: 'GET', path: '/api/models/feature-importance', desc: 'Returns regression coefficients and sorted feature impact weights.' },
    { method: 'GET', path: '/api/metrics', desc: 'Returns cross-model evaluation benchmarks (CV R², MAE, RMSE).' },
    { method: 'GET', path: '/api/health', desc: 'Reports system operational status and pipeline loading state.' },
  ];

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-extrabold text-[#073B32] tracking-tight font-display">
          AutoValue AI Technical Documentation
        </h2>
        <p className="text-xs text-[#77827E] mt-0.5">
          Engineering architecture, econometric feature formulations, REST API contracts, and usage instructions.
        </p>
      </div>

      {/* Architecture Overview */}
      <div className="bg-white rounded-3xl p-6 lg:p-8 border border-[#E4E8E1] shadow-soft space-y-4">
        <div className="border-b border-[#E4E8E1] pb-3">
          <h3 className="text-base font-extrabold text-[#073B32] font-display">
            Pipeline Architecture & Data Transformation Flow
          </h3>
          <p className="text-xs text-[#77827E]">
            End-to-end regression pipeline from raw inputs to INR pricing.
          </p>
        </div>

        <div className="p-4 bg-[#F7F5F0] rounded-2xl border border-[#E4E8E1] font-mono text-[11px] text-[#202A28] overflow-x-auto leading-relaxed">
{`User Inputs: [brand, year, km_driven, fuel, seller_type, transmission, owner]
       │
       ├──► Feature Engineering: car_age = max(0, 2020 - year)
       │
       ├──► ColumnTransformer Preprocessing:
       │    ├── Numerical: StandardScaler([car_age, km_driven])
       │    └── Categorical: OneHotEncoder([brand, fuel, seller_type, transmission, owner])
       │
       ▼
TransformedTargetRegressor (LinearRegression)
       │
       ├── Training Fit: Fit on log1p(selling_price)
       └── Inference Prediction: expm1(predicted_log_price)
       │
       ▼
Non-Negative Bounds Enforcer: max(₹20,000, prediction)
       │
       ▼
Formatted Output: Indian Rupee notation (e.g. ₹3.86 Lakh) + Confidence Band (± MAE)`}
        </div>
      </div>

      {/* REST Endpoints Reference */}
      <div className="bg-white rounded-3xl p-6 lg:p-8 border border-[#E4E8E1] shadow-soft space-y-4">
        <div className="border-b border-[#E4E8E1] pb-3 flex justify-between items-center">
          <div>
            <h3 className="text-base font-extrabold text-[#073B32] font-display flex items-center space-x-2">
              <Code2 className="w-5 h-5 text-[#E6B85C]" />
              <span>FastAPI REST Endpoints</span>
            </h3>
            <p className="text-xs text-[#77827E]">
              Available on local port <code>http://127.0.0.1:8002</code>.
            </p>
          </div>
          <a
            href="http://127.0.0.1:8002/docs"
            target="_blank"
            rel="noreferrer"
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-xl bg-[#F7F5F0] hover:bg-[#EFECE3] border border-[#E4E8E1] text-xs font-bold text-[#073B32] transition-colors"
          >
            <span>Swagger UI Docs</span>
            <ExternalLink className="w-3.5 h-3.5" />
          </a>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-sans">
            <thead className="bg-[#F7F5F0] text-[#77827E] uppercase font-bold text-[10px] tracking-wider">
              <tr>
                <th className="py-2.5 px-4 rounded-l-xl">HTTP Method</th>
                <th className="py-2.5 px-4">Endpoint Path</th>
                <th className="py-2.5 px-4 rounded-r-xl">Functional Description</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#E4E8E1]">
              {endpoints.map((ep, i) => (
                <tr key={i} className="hover:bg-[#F7F5F0]/50 transition-colors">
                  <td className="py-3 px-4 font-mono font-bold">
                    <span className={`px-2 py-0.5 rounded text-[10px] ${
                      ep.method === 'POST' ? 'bg-[#E6B85C] text-[#073B32]' : 'bg-[#073B32] text-white'
                    }`}>
                      {ep.method}
                    </span>
                  </td>
                  <td className="py-3 px-4 font-mono font-bold text-[#202A28]">
                    {ep.path}
                  </td>
                  <td className="py-3 px-4 text-[#77827E]">
                    {ep.desc}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
