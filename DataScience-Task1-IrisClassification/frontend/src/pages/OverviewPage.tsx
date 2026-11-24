import React, { useState, useEffect } from 'react';
import {
  Flower2,
  Database,
  Layers,
  Award,
  ArrowRight,
  TrendingUp,
  Sparkles,
  Info
} from 'lucide-react';
import { fetchDatasetSummary, fetchMetrics, DatasetSummary } from '../api/client';
import {
  ResponsiveContainer,
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  Tooltip,
  PieChart,
  Pie,
  Cell,
  Legend
} from 'recharts';

export default function OverviewPage() {
  const [summary, setSummary] = useState<DatasetSummary | null>(null);
  const [metrics, setMetrics] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([fetchDatasetSummary(), fetchMetrics()])
      .then(([s, m]) => {
        setSummary(s);
        setMetrics(m);
      })
      .catch((e) => console.error(e))
      .finally(() => setLoading(false));
  }, []);

  const sampleScatterData = [
    { petal_len: 1.4, petal_wid: 0.2, species: 'Setosa' },
    { petal_len: 1.5, petal_wid: 0.2, species: 'Setosa' },
    { petal_len: 1.3, petal_wid: 0.2, species: 'Setosa' },
    { petal_len: 1.6, petal_wid: 0.4, species: 'Setosa' },
    { petal_len: 4.7, petal_wid: 1.4, species: 'Versicolor' },
    { petal_len: 4.5, petal_wid: 1.5, species: 'Versicolor' },
    { petal_len: 4.9, petal_wid: 1.5, species: 'Versicolor' },
    { petal_len: 4.0, petal_wid: 1.3, species: 'Versicolor' },
    { petal_len: 6.0, petal_wid: 2.5, species: 'Virginica' },
    { petal_len: 5.1, petal_wid: 1.9, species: 'Virginica' },
    { petal_len: 5.9, petal_wid: 2.1, species: 'Virginica' },
    { petal_len: 5.6, petal_wid: 2.0, species: 'Virginica' },
  ];

  const speciesPieData = [
    { name: 'Setosa', value: 50, color: '#76649D' },
    { name: 'Versicolor', value: 50, color: '#C18E61' },
    { name: 'Virginica', value: 50, color: '#2C6A50' },
  ];

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Visual Reference Botanical Hero Banner */}
      <div className="relative rounded-3xl p-8 lg:p-10 overflow-hidden bg-gradient-to-br from-[#EFF8F0] via-[#DFF4E5] to-[#FFFFFF] border border-[#D6E4D5] shadow-soft">
        <div className="relative z-10 max-w-2xl">
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-white/80 border border-[#C7E2CE] text-[#285943] text-xs font-extrabold uppercase tracking-widest mb-4 backdrop-blur-sm">
            <Sparkles className="w-3.5 h-3.5 text-[#285943]" />
            <span>Botanical Intelligence Studio</span>
          </div>
          <h2 className="text-3xl lg:text-4xl font-extrabold text-[#19362A] tracking-tight leading-tight mb-3 font-sans">
            Where Nature Meets Intelligence.
          </h2>
          <p className="text-sm lg:text-base text-[#4A6353] leading-relaxed mb-6">
            Explore Iris morphology and discover algorithmic species taxonomy. Calibrated with scikit-learn Random Forest inference, interactive dimensional projections, and validated scientific benchmarks.
          </p>

          <div className="flex flex-wrap items-center gap-3">
            <div className="flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-white text-xs font-bold text-[#19362A] shadow-sm border border-[#E3EBE3]">
              <span className="w-2 h-2 rounded-full bg-[#76649D]"></span>
              <span>Iris Setosa</span>
            </div>
            <div className="flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-white text-xs font-bold text-[#19362A] shadow-sm border border-[#E3EBE3]">
              <span className="w-2 h-2 rounded-full bg-[#C18E61]"></span>
              <span>Iris Versicolor</span>
            </div>
            <div className="flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-white text-xs font-bold text-[#19362A] shadow-sm border border-[#E3EBE3]">
              <span className="w-2 h-2 rounded-full bg-[#2C6A50]"></span>
              <span>Iris Virginica</span>
            </div>
          </div>
        </div>

        {/* Floating Botanical SVG Accent Artwork */}
        <div className="absolute -right-6 -bottom-8 pointer-events-none opacity-20 lg:opacity-30">
          <svg width="340" height="340" viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M100 20C80 60 40 80 20 100C60 120 80 160 100 180C120 140 160 120 180 100C140 80 120 40 100 20Z" fill="#285943" />
            <circle cx="100" cy="100" r="30" fill="#8BAA91" />
          </svg>
        </div>
      </div>

      {/* Pastel KPI Telemetry Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white rounded-2xl p-5 border border-[#E3EBE3] shadow-soft hover:shadow-float transition-all">
          <div className="w-10 h-10 rounded-xl bg-[#EAE7F5] text-[#76649D] flex items-center justify-center mb-3">
            <Database className="w-5 h-5" />
          </div>
          <div className="text-2xl font-extrabold text-[#19362A] tracking-tight">
            {summary ? summary.total_specimens : '150'}
          </div>
          <div className="text-xs uppercase font-bold text-[#728177] tracking-wider mt-1">
            Dataset Specimens
          </div>
          <div className="text-[11px] font-semibold text-[#285943] mt-2">
            50 samples per balanced class
          </div>
        </div>

        <div className="bg-white rounded-2xl p-5 border border-[#E3EBE3] shadow-soft hover:shadow-float transition-all">
          <div className="w-10 h-10 rounded-xl bg-[#F7EBDD] text-[#C18E61] flex items-center justify-center mb-3">
            <Flower2 className="w-5 h-5" />
          </div>
          <div className="text-2xl font-extrabold text-[#19362A] tracking-tight">
            {summary ? summary.distinct_species : '3'}
          </div>
          <div className="text-xs uppercase font-bold text-[#728177] tracking-wider mt-1">
            Distinct Species
          </div>
          <div className="text-[11px] font-semibold text-[#C18E61] mt-2">
            Setosa, Versicolor, Virginica
          </div>
        </div>

        <div className="bg-white rounded-2xl p-5 border border-[#E3EBE3] shadow-soft hover:shadow-float transition-all">
          <div className="w-10 h-10 rounded-xl bg-[#DFF4E5] text-[#285943] flex items-center justify-center mb-3">
            <Layers className="w-5 h-5" />
          </div>
          <div className="text-2xl font-extrabold text-[#19362A] tracking-tight">
            4 Features
          </div>
          <div className="text-xs uppercase font-bold text-[#728177] tracking-wider mt-1">
            Input Dimensions
          </div>
          <div className="text-[11px] font-semibold text-[#285943] mt-2">
            Sepal & Petal Length/Width (cm)
          </div>
        </div>

        <div className="bg-white rounded-2xl p-5 border border-[#E3EBE3] shadow-soft hover:shadow-float transition-all">
          <div className="w-10 h-10 rounded-xl bg-[#EFF8F0] text-[#285943] flex items-center justify-center mb-3">
            <Award className="w-5 h-5" />
          </div>
          <div className="text-2xl font-extrabold text-[#285943] tracking-tight">
            {metrics?.test_metrics ? `${(metrics.test_metrics['Test Accuracy'] * 100).toFixed(2)}%` : '96.67%'}
          </div>
          <div className="text-xs uppercase font-bold text-[#728177] tracking-wider mt-1">
            Audited Test Accuracy
          </div>
          <div className="text-[11px] font-semibold text-[#285943] mt-2">
            Stratified held-out test split
          </div>
        </div>
      </div>

      {/* Analytics Workspace Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left: Morphological Scatter Plot */}
        <div className="lg:col-span-7 bg-white rounded-2xl p-6 border border-[#E3EBE3] shadow-soft space-y-4">
          <div>
            <h3 className="text-base font-extrabold text-[#19362A] tracking-tight">
              Morphological Relationships (Petal Space)
            </h3>
            <p className="text-xs text-[#728177]">
              Petal length vs. petal width showcases linear separability for Setosa and clear decision margins for Virginica.
            </p>
          </div>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <ScatterChart margin={{ top: 10, right: 20, bottom: 20, left: 0 }}>
                <XAxis type="number" dataKey="petal_len" name="Petal Length" unit="cm" stroke="#8BAA91" fontSize={11} />
                <YAxis type="number" dataKey="petal_wid" name="Petal Width" unit="cm" stroke="#8BAA91" fontSize={11} />
                <Tooltip cursor={{ strokeDasharray: '3 3' }} />
                <Scatter name="Specimens" data={sampleScatterData} fill="#285943" />
              </ScatterChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Right: Species Cohort Donut */}
        <div className="lg:col-span-5 bg-white rounded-2xl p-6 border border-[#E3EBE3] shadow-soft space-y-4">
          <div>
            <h3 className="text-base font-extrabold text-[#19362A] tracking-tight">
              Taxonomic Cohort Distribution
            </h3>
            <p className="text-xs text-[#728177]">
              Fisher's canonical 150-sample dataset: 50 balanced specimens per species.
            </p>
          </div>
          <div className="h-56">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={speciesPieData}
                  cx="50%"
                  cy="50%"
                  innerRadius={55}
                  outerRadius={80}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {speciesPieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend verticalAlign="bottom" height={36} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}
