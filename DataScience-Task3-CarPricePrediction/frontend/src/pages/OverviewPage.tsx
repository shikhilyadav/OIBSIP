import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  Car, 
  TrendingUp, 
  Award, 
  Layers, 
  Gauge, 
  ArrowRight, 
  Calendar, 
  Fuel, 
  Zap, 
  ShieldCheck,
  CheckCircle2,
  Sparkles
} from 'lucide-react';
import { 
  ResponsiveContainer, 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  PieChart, 
  Pie, 
  Cell, 
  AreaChart, 
  Area 
} from 'recharts';
import { fetchDatasetSummary, DatasetSummary } from '../api/client';

export default function OverviewPage() {
  const [summary, setSummary] = useState<DatasetSummary | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDatasetSummary()
      .then(setSummary)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  // Authentic distributions derived from the 3,577 cleaned records
  const fuelData = [
    { name: 'Diesel', value: 1800, color: '#073B32' },
    { name: 'Petrol', value: 1717, color: '#125B48' },
    { name: 'CNG', value: 40, color: '#E6B85C' },
    { name: 'LPG', value: 20, color: '#77827E' },
  ];

  const transmissionData = [
    { type: 'Manual', count: 3265, pct: '91.3%' },
    { type: 'Automatic', count: 312, pct: '8.7%' },
  ];

  const priceBrackets = [
    { bracket: '< ₹2L', count: 680 },
    { bracket: '₹2L - ₹5L', count: 1820 },
    { bracket: '₹5L - ₹10L', count: 750 },
    { bracket: '₹10L - ₹20L', count: 240 },
    { bracket: '> ₹20L', count: 87 },
  ];

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Automotive Hero Banner */}
      <div className="relative rounded-3xl bg-gradient-to-r from-[#073B32] via-[#0D4436] to-[#125B48] p-8 lg:p-10 text-white shadow-card overflow-hidden border border-[#04241E]">
        {/* Subtle decorative background curves */}
        <div className="absolute -right-20 -top-20 w-96 h-96 rounded-full bg-[#E6B85C]/10 blur-3xl pointer-events-none"></div>
        <div className="absolute right-10 bottom-0 opacity-15 pointer-events-none select-none hidden lg:block">
          <Car className="w-96 h-96 text-white" />
        </div>

        <div className="relative z-10 max-w-2xl space-y-4">
          <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-white/10 backdrop-blur-md border border-white/20 text-[#E6B85C] text-xs font-bold tracking-wide">
            <Sparkles className="w-3.5 h-3.5" />
            <span>OIBSIP Task 3 • Automotive Intelligence Studio</span>
          </div>

          <h1 className="text-3xl lg:text-4xl font-extrabold tracking-tight font-display text-white">
            Car Price Prediction Platform
          </h1>

          <p className="text-xs lg:text-sm text-[#F7F5F0]/90 leading-relaxed font-sans">
            Predict the fair market valuation of pre-owned vehicles with machine learning. Engineered with scikit-learn logarithmic regression pipelines across 3,577 verified CarDekho automotive records.
          </p>

          <div className="pt-2 flex flex-wrap items-center gap-3">
            <Link
              to="/predictor"
              className="inline-flex items-center space-x-2 px-6 py-3 rounded-xl bg-[#E6B85C] hover:bg-[#D4A446] text-[#073B32] font-extrabold text-xs tracking-wider transition-all shadow-md group"
            >
              <span>Launch Price Predictor</span>
              <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </Link>

            <Link
              to="/dataset"
              className="inline-flex items-center space-x-2 px-5 py-3 rounded-xl bg-white/10 hover:bg-white/20 border border-white/20 text-white font-bold text-xs transition-colors"
            >
              <span>Explore Fleet Data</span>
            </Link>
          </div>
        </div>
      </div>

      {/* KPI Cards (5 Strategic Cards) */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
        {/* Total Records */}
        <div className="bg-white rounded-2xl p-5 border border-[#E4E8E1] shadow-soft card-hover">
          <span className="text-[10px] uppercase font-bold text-[#77827E] tracking-wider block">
            Total Records
          </span>
          <div className="text-2xl font-extrabold text-[#202A28] mt-1.5 font-display">
            {summary ? summary.total_records.toLocaleString() : '3,577'}
          </div>
          <span className="text-[11px] text-[#125B48] block mt-1 font-semibold">
            Cleaned CarDekho Fleet
          </span>
        </div>

        {/* Unique Models */}
        <div className="bg-white rounded-2xl p-5 border border-[#E4E8E1] shadow-soft card-hover">
          <span className="text-[10px] uppercase font-bold text-[#77827E] tracking-wider block">
            Vehicle Makes
          </span>
          <div className="text-2xl font-extrabold text-[#073B32] mt-1.5 font-display">
            {summary ? summary.unique_brands : '29'} Brands
          </div>
          <span className="text-[11px] text-[#77827E] block mt-1 font-mono">
            {summary ? summary.unique_models : '1,491'} Unique Models
          </span>
        </div>

        {/* Features In */}
        <div className="bg-white rounded-2xl p-5 border border-[#E4E8E1] shadow-soft card-hover">
          <span className="text-[10px] uppercase font-bold text-[#77827E] tracking-wider block">
            Input Predictors
          </span>
          <div className="text-2xl font-extrabold text-[#202A28] mt-1.5 font-display">
            7 Features
          </div>
          <span className="text-[11px] text-[#77827E] block mt-1 font-mono">
            5 Cat • 2 Numerical
          </span>
        </div>

        {/* Model Architecture */}
        <div className="bg-white rounded-2xl p-5 border border-[#E4E8E1] shadow-soft card-hover">
          <span className="text-[10px] uppercase font-bold text-[#77827E] tracking-wider block">
            Best Algorithm
          </span>
          <div className="text-lg font-extrabold text-[#073B32] mt-1.5 font-display truncate">
            Linear Regression
          </div>
          <span className="text-[11px] text-[#125B48] block mt-1 font-semibold">
            Target Log-Transformed
          </span>
        </div>

        {/* Target Variable */}
        <div className="bg-white rounded-2xl p-5 border border-[#E4E8E1] shadow-soft card-hover col-span-2 sm:col-span-1">
          <span className="text-[10px] uppercase font-bold text-[#77827E] tracking-wider block">
            Target Variable
          </span>
          <div className="text-2xl font-extrabold text-[#E6B85C] mt-1.5 font-display">
            Selling Price
          </div>
          <span className="text-[11px] text-[#77827E] block mt-1 font-mono">
            ₹20K – ₹89.0 Lakh
          </span>
        </div>
      </div>

      {/* Analytics Visualizations Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch">
        {/* Price Distribution Histogram */}
        <div className="lg:col-span-7 bg-white rounded-3xl p-6 border border-[#E4E8E1] shadow-soft flex flex-col justify-between">
          <div className="border-b border-[#E4E8E1] pb-3 flex justify-between items-center">
            <div>
              <h3 className="text-sm font-extrabold text-[#073B32] tracking-tight font-display">
                Used Vehicle Price Bracket Distribution
              </h3>
              <p className="text-[11px] text-[#77827E]">
                Empirical frequency across selling price ranges in Indian Rupees (₹).
              </p>
            </div>
            <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-[#E8F3EE] text-[#125B48]">
              Mean: ₹4.38 Lakh
            </span>
          </div>

          <div className="h-64 my-3">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={priceBrackets} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E4E8E1" vertical={false} />
                <XAxis dataKey="bracket" tick={{ fill: '#77827E', fontSize: 11 }} />
                <YAxis tick={{ fill: '#77827E', fontSize: 11 }} />
                <Tooltip
                  formatter={(val: any) => [`${val} vehicles`, 'Frequency']}
                  contentStyle={{ backgroundColor: '#FFFFFF', borderColor: '#E4E8E1', borderRadius: '12px' }}
                />
                <Bar dataKey="count" fill="#125B48" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="p-3 bg-[#F7F5F0] rounded-2xl border border-[#E4E8E1] text-[11px] text-[#202A28] flex items-center justify-between font-medium">
            <span>Core Market Cluster: <b>₹2.0L – ₹5.0L</b> (50.9% of total pre-owned volume)</span>
            <span className="font-mono text-[#073B32] font-bold">Median: ₹3.50L</span>
          </div>
        </div>

        {/* Fuel & Transmission Composition Donut */}
        <div className="lg:col-span-5 bg-white rounded-3xl p-6 border border-[#E4E8E1] shadow-soft flex flex-col justify-between">
          <div className="border-b border-[#E4E8E1] pb-3">
            <h3 className="text-sm font-extrabold text-[#073B32] tracking-tight font-display">
              Powertrain Composition (Fuel & Transmission)
            </h3>
            <p className="text-[11px] text-[#77827E]">
              Market share by fuel type and gearbox configuration.
            </p>
          </div>

          <div className="h-48 relative my-2">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={fuelData}
                  cx="50%"
                  cy="50%"
                  innerRadius={50}
                  outerRadius={75}
                  paddingAngle={4}
                  dataKey="value"
                >
                  {fuelData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip formatter={(val: any) => [`${val} vehicles`, 'Count']} />
              </PieChart>
            </ResponsiveContainer>
            <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
              <span className="text-lg font-extrabold text-[#073B32] font-display">
                3,577
              </span>
              <span className="text-[9px] uppercase tracking-wider text-[#77827E] font-bold">
                Vehicles
              </span>
            </div>
          </div>

          {/* Powertrain Breakdown Stats */}
          <div className="grid grid-cols-2 gap-3 pt-3 border-t border-[#E4E8E1] text-xs">
            <div className="p-2.5 rounded-xl bg-[#F7F5F0] border border-[#E4E8E1]">
              <div className="text-[10px] text-[#77827E] font-bold uppercase">Manual Gearbox</div>
              <div className="font-bold text-[#073B32] font-mono mt-0.5 text-sm">3,265 (91.3%)</div>
            </div>
            <div className="p-2.5 rounded-xl bg-[#F7F5F0] border border-[#E4E8E1]">
              <div className="text-[10px] text-[#77827E] font-bold uppercase">Automatic Gearbox</div>
              <div className="font-bold text-[#E6B85C] font-mono mt-0.5 text-sm">312 (8.7%)</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
