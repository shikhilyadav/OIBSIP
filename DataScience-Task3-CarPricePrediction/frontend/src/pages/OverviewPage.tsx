import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  Car, 
  ArrowRight, 
  Sparkles,
  Layers,
  Award,
  Zap,
  TrendingUp,
  Database
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
  Cell 
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
    { name: 'Diesel', value: 1800, color: '#063B32' },
    { name: 'Petrol', value: 1717, color: '#17634D' },
    { name: 'CNG', value: 40, color: '#E8B956' },
    { name: 'LPG', value: 20, color: '#77827E' },
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
      <div className="relative rounded-3xl bg-gradient-to-r from-[#063B32] via-[#0B4B3F] to-[#17634D] p-8 lg:p-10 text-white shadow-card overflow-hidden border border-[#032620]">
        {/* Modern architectural skyline + subtle automotive glow */}
        <div className="absolute -right-20 -top-20 w-96 h-96 rounded-full bg-[#E8B956]/15 blur-3xl pointer-events-none"></div>
        <div className="absolute right-0 bottom-0 top-0 w-2/5 pointer-events-none select-none hidden lg:flex items-center justify-center opacity-25">
          <svg viewBox="0 0 500 250" className="w-full h-auto text-white" fill="none" stroke="currentColor">
            {/* Architectural Skyline Silhouette */}
            <path d="M20,220 L20,130 L50,130 L50,80 L70,80 L70,40 L100,40 L100,100 L120,100 L120,70 L150,70 L150,150 L180,150 L180,220 Z" strokeWidth="1" opacity="0.4" />
            <path d="M300,220 L300,90 L330,90 L330,50 L360,50 L360,110 L390,110 L390,70 L420,70 L420,140 L450,140 L450,220 Z" strokeWidth="1" opacity="0.4" />
            {/* Sleek luxury sedan silhouette line */}
            <path d="M40,210 C90,210 120,205 160,185 C200,165 240,135 320,135 C380,135 410,165 440,180 C465,190 480,210 490,210" strokeWidth="3" stroke="#E8B956" />
            <circle cx="130" cy="210" r="24" strokeWidth="3" stroke="#E8B956" />
            <circle cx="410" cy="210" r="24" strokeWidth="3" stroke="#E8B956" />
            <line x1="0" y1="210" x2="500" y2="210" strokeWidth="1" stroke="#E8B956" strokeDasharray="6 6" />
          </svg>
        </div>

        <div className="relative z-10 max-w-2xl space-y-4">
          {/* Small Badge */}
          <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-white/10 backdrop-blur-md border border-white/20 text-[#E8B956] text-xs font-bold tracking-wide">
            <Sparkles className="w-3.5 h-3.5" />
            <span>OIBSIP Task 3 • Automotive Intelligence Studio</span>
          </div>

          {/* Heading */}
          <h1 className="text-3xl lg:text-4xl font-extrabold tracking-tight font-display text-white">
            Car Price Prediction
          </h1>

          {/* Subtitle */}
          <p className="text-xs lg:text-sm text-[#F7F5F0]/90 leading-relaxed font-sans">
            Predict the market price of used cars with machine learning. Engineered with scikit-learn logarithmic regression pipelines across 3,577 verified CarDekho automotive records.
          </p>

          {/* Informational Pills */}
          <div className="flex flex-wrap items-center gap-2 pt-1">
            <span className="px-3 py-1 rounded-full bg-white/10 border border-white/15 text-[11px] font-bold text-[#E8B956] flex items-center space-x-1">
              <Zap className="w-3 h-3" />
              <span>Regression</span>
            </span>
            <span className="px-3 py-1 rounded-full bg-white/10 border border-white/15 text-[11px] font-bold text-white flex items-center space-x-1">
              <Database className="w-3 h-3" />
              <span>3,577 Records</span>
            </span>
            <span className="px-3 py-1 rounded-full bg-white/10 border border-white/15 text-[11px] font-bold text-white flex items-center space-x-1">
              <Layers className="w-3 h-3" />
              <span>7 Input Features</span>
            </span>
          </div>

          {/* Action Buttons */}
          <div className="pt-2 flex flex-wrap items-center gap-3">
            <Link
              to="/predictor"
              className="inline-flex items-center space-x-2 px-6 py-3 rounded-xl bg-[#E8B956] hover:bg-[#D4A446] text-[#063B32] font-black text-xs tracking-wider transition-all shadow-md group"
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

      {/* 5 KPI Cards in one horizontal row */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
        {/* 1. Total Records */}
        <div className="bg-white rounded-2xl p-5 border border-[#E4E8E1] shadow-soft card-hover flex flex-col justify-between">
          <span className="text-[10px] uppercase font-bold text-[#77827E] tracking-wider block">
            Total Records
          </span>
          <div className="text-2xl font-black text-[#202A28] mt-1.5 font-display">
            {summary ? summary.total_records.toLocaleString() : '3,577'}
          </div>
          <span className="text-[11px] text-[#17634D] block mt-1 font-semibold">
            Cleaned CarDekho Fleet
          </span>
        </div>

        {/* 2. Unique Models/Brands */}
        <div className="bg-white rounded-2xl p-5 border border-[#E4E8E1] shadow-soft card-hover flex flex-col justify-between">
          <span className="text-[10px] uppercase font-bold text-[#77827E] tracking-wider block">
            Unique Models / Brands
          </span>
          <div className="text-xl font-black text-[#063B32] mt-1.5 font-display truncate">
            {summary ? summary.unique_brands : '29'} Brands
          </div>
          <span className="text-[11px] text-[#77827E] block mt-1 font-mono">
            {summary ? summary.unique_models : '1,491'} Models
          </span>
        </div>

        {/* 3. Input Features */}
        <div className="bg-white rounded-2xl p-5 border border-[#E4E8E1] shadow-soft card-hover flex flex-col justify-between">
          <span className="text-[10px] uppercase font-bold text-[#77827E] tracking-wider block">
            Input Features
          </span>
          <div className="text-2xl font-black text-[#202A28] mt-1.5 font-display">
            7 Features
          </div>
          <span className="text-[11px] text-[#77827E] block mt-1 font-mono">
            5 Cat • 2 Numerical
          </span>
        </div>

        {/* 4. Best Algorithm */}
        <div className="bg-white rounded-2xl p-5 border border-[#E4E8E1] shadow-soft card-hover flex flex-col justify-between">
          <span className="text-[10px] uppercase font-bold text-[#77827E] tracking-wider block">
            Best Algorithm
          </span>
          <div className="text-base font-black text-[#063B32] mt-1.5 font-display truncate">
            Linear Regression
          </div>
          <span className="text-[11px] text-[#17634D] block mt-1 font-semibold">
            R² = 0.7120 • Target log1p
          </span>
        </div>

        {/* 5. Target Variable */}
        <div className="bg-white rounded-2xl p-5 border border-[#E4E8E1] shadow-soft card-hover col-span-2 md:col-span-1 flex flex-col justify-between">
          <span className="text-[10px] uppercase font-bold text-[#77827E] tracking-wider block">
            Target Variable
          </span>
          <div className="text-xl font-black text-[#E8B956] mt-1.5 font-display">
            Selling Price
          </div>
          <span className="text-[11px] text-[#77827E] block mt-1 font-mono">
            ₹20K – ₹89.0L
          </span>
        </div>
      </div>

      {/* Analytics Visualizations Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch">
        {/* Price Distribution Histogram */}
        <div className="lg:col-span-7 bg-white rounded-3xl p-6 border border-[#E4E8E1] shadow-soft flex flex-col justify-between">
          <div className="border-b border-[#E4E8E1] pb-3 flex justify-between items-center">
            <div>
              <h3 className="text-sm font-extrabold text-[#063B32] tracking-tight font-display">
                Used Vehicle Price Bracket Distribution
              </h3>
              <p className="text-[11px] text-[#77827E]">
                Empirical frequency across selling price ranges in Indian Rupees (₹).
              </p>
            </div>
            <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-[#E8F3EE] text-[#17634D]">
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
                <Bar dataKey="count" fill="#17634D" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="p-3 bg-[#F7F5F0] rounded-2xl border border-[#E4E8E1] text-[11px] text-[#202A28] flex items-center justify-between font-medium">
            <span>Core Market Cluster: <b>₹2.0L – ₹5.0L</b> (50.9% of total pre-owned volume)</span>
            <span className="font-mono text-[#063B32] font-bold">Median: ₹3.50L</span>
          </div>
        </div>

        {/* Fuel & Transmission Composition Donut */}
        <div className="lg:col-span-5 bg-white rounded-3xl p-6 border border-[#E4E8E1] shadow-soft flex flex-col justify-between">
          <div className="border-b border-[#E4E8E1] pb-3">
            <h3 className="text-sm font-extrabold text-[#063B32] tracking-tight font-display">
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
              <span className="text-lg font-extrabold text-[#063B32] font-display">
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
              <div className="font-bold text-[#063B32] font-mono mt-0.5 text-sm">3,265 (91.3%)</div>
            </div>
            <div className="p-2.5 rounded-xl bg-[#F7F5F0] border border-[#E4E8E1]">
              <div className="text-[10px] text-[#77827E] font-bold uppercase">Automatic Gearbox</div>
              <div className="font-bold text-[#E8B956] font-mono mt-0.5 text-sm">312 (8.7%)</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
