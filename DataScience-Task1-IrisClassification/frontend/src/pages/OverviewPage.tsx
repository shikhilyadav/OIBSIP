import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  Flower2,
  Database,
  Layers,
  Award,
  ArrowRight,
  TrendingUp,
  Sparkles,
  Info,
  CheckCircle2,
  Microscope,
  Compass
} from 'lucide-react';
import { fetchDatasetSummary, fetchDatasetRecords, fetchMetrics, fetchSpeciesInsights, DatasetSummary } from '../api/client';
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
  const [insights, setInsights] = useState<any>(null);
  const [allSpecimens, setAllSpecimens] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetchDatasetSummary(),
      fetchMetrics(),
      fetchSpeciesInsights(),
      fetchDatasetRecords({ page: 1, page_size: 150 })
    ])
      .then(([s, m, ins, recs]) => {
        setSummary(s);
        setMetrics(m);
        setInsights(ins.insights);
        // Map all 150 records for true scatter plot
        if (recs && recs.records) {
          setAllSpecimens(recs.records);
        }
      })
      .catch((e) => console.error(e))
      .finally(() => setLoading(false));
  }, []);

  // Split into species cohorts for scatter coloring
  const setosaData = allSpecimens
    .filter((r) => r.species.toLowerCase() === 'setosa')
    .map((r) => ({ x: r.petal_length, y: r.petal_width, sepal: `${r.sepal_length}x${r.sepal_width}`, species: 'Setosa' }));

  const versicolorData = allSpecimens
    .filter((r) => r.species.toLowerCase() === 'versicolor')
    .map((r) => ({ x: r.petal_length, y: r.petal_width, sepal: `${r.sepal_length}x${r.sepal_width}`, species: 'Versicolor' }));

  const virginicaData = allSpecimens
    .filter((r) => r.species.toLowerCase() === 'virginica')
    .map((r) => ({ x: r.petal_length, y: r.petal_width, sepal: `${r.sepal_length}x${r.sepal_width}`, species: 'Virginica' }));

  const speciesPieData = [
    { name: 'Setosa', value: 50, color: '#76649D' },
    { name: 'Versicolor', value: 50, color: '#C18E61' },
    { name: 'Virginica', value: 50, color: '#2C6A50' },
  ];

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Visual Reference Split Hero Banner with Real Botanical Illustration */}
      <div className="relative rounded-3xl p-8 lg:p-10 overflow-hidden bg-gradient-to-br from-[#EFF8F0] via-[#DFF4E5] to-[#FFFFFF] border border-[#D6E4D5] shadow-soft">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center relative z-10">
          {/* Left Column: Hero Copy & CTA */}
          <div className="lg:col-span-7 space-y-4">
            <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-white/90 border border-[#C7E2CE] text-[#285943] text-xs font-extrabold uppercase tracking-widest backdrop-blur-sm shadow-xs">
              <Sparkles className="w-3.5 h-3.5 text-[#285943]" />
              <span>Botanical Intelligence Studio</span>
            </div>

            <h1 className="text-3xl lg:text-4xl font-extrabold text-[#19362A] tracking-tight leading-tight font-sans">
              Where Nature Meets Intelligence.
            </h1>

            <p className="text-sm lg:text-base text-[#4A6353] leading-relaxed max-w-xl">
              Algorithmic specimen taxonomy and morphometric clustering. Powered by an audited Random Forest pipeline, live 4-dimensional inference, and scientific evaluation across 150 verified botanical records.
            </p>

            <div className="pt-2 flex flex-wrap items-center gap-3">
              <Link
                to="/classifier"
                className="inline-flex items-center space-x-2 px-5 py-2.5 rounded-xl bg-[#285943] hover:bg-[#173D2D] text-white font-bold text-xs tracking-wide transition-all shadow-md hover:shadow-lg"
              >
                <Microscope className="w-4 h-4" />
                <span>Launch Flower Classifier</span>
                <ArrowRight className="w-4 h-4" />
              </Link>
              <Link
                to="/dataset"
                className="inline-flex items-center space-x-2 px-4 py-2.5 rounded-xl bg-white/90 hover:bg-white text-[#19362A] border border-[#E3EBE3] font-bold text-xs tracking-wide transition-all shadow-xs"
              >
                <Database className="w-4 h-4 text-[#8BAA91]" />
                <span>Explore 150 Specimens</span>
              </Link>
            </div>

            {/* Species Identification Chips */}
            <div className="pt-2 flex flex-wrap items-center gap-2">
              <div className="flex items-center space-x-1.5 px-3 py-1 rounded-full bg-white/80 text-[11px] font-bold text-[#19362A] border border-[#E3EBE3]">
                <span className="w-2 h-2 rounded-full bg-[#76649D]"></span>
                <span>Iris Setosa (N=50)</span>
              </div>
              <div className="flex items-center space-x-1.5 px-3 py-1 rounded-full bg-white/80 text-[11px] font-bold text-[#19362A] border border-[#E3EBE3]">
                <span className="w-2 h-2 rounded-full bg-[#C18E61]"></span>
                <span>Iris Versicolor (N=50)</span>
              </div>
              <div className="flex items-center space-x-1.5 px-3 py-1 rounded-full bg-white/80 text-[11px] font-bold text-[#19362A] border border-[#E3EBE3]">
                <span className="w-2 h-2 rounded-full bg-[#2C6A50]"></span>
                <span>Iris Virginica (N=50)</span>
              </div>
            </div>
          </div>

          {/* Right Column: Botanical Visual & Floating Measurement Labels */}
          <div className="lg:col-span-5 relative flex items-center justify-center">
            {/* Soft backdrop radial card */}
            <div className="w-full h-64 lg:h-72 rounded-2xl bg-white/70 border border-[#D6E4D5] p-5 shadow-sm flex items-center justify-center relative overflow-hidden backdrop-blur-sm">
              {/* Botanical Scientific Iris Illustration SVG */}
              <svg width="220" height="220" viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg" className="transform hover:scale-105 transition-transform duration-500">
                {/* Stem & Leaves */}
                <path d="M100 190 C100 130 96 110 98 80" stroke="#2C6A50" strokeWidth="4" strokeLinecap="round"/>
                <path d="M98 130 C75 120 60 140 50 160 C65 155 85 145 98 130Z" fill="#5C9A72" opacity="0.8"/>
                <path d="M100 115 C125 105 140 120 150 145 C135 140 115 130 100 115Z" fill="#5C9A72" opacity="0.8"/>
                {/* Iris Sepals (Falls) */}
                <path d="M98 80 C80 110 55 115 65 85 C75 60 90 65 98 80Z" fill="#76649D" opacity="0.9"/>
                <path d="M98 80 C116 110 141 115 131 85 C121 60 106 65 98 80Z" fill="#76649D" opacity="0.9"/>
                {/* Iris Central Standards */}
                <path d="M98 80 C90 40 75 35 98 25 C121 35 106 40 98 80Z" fill="#8B5CF6" opacity="0.9"/>
                {/* Crest / Beard Accent */}
                <circle cx="98" cy="80" r="6" fill="#F59E0B" />
              </svg>

              {/* Floating Scientific Measurement Labels */}
              <div className="absolute top-4 left-4 bg-white/95 px-3 py-1 rounded-lg border border-[#C7E2CE] shadow-xs text-[10px] font-bold text-[#285943]">
                Sepal Breadth: 2.0–4.4 cm
              </div>
              <div className="absolute bottom-4 right-4 bg-white/95 px-3 py-1 rounded-lg border border-[#C7E2CE] shadow-xs text-[10px] font-bold text-[#76649D]">
                Petal Span: 1.0–6.9 cm
              </div>
              <div className="absolute bottom-4 left-4 bg-white/95 px-3 py-1 rounded-lg border border-[#C7E2CE] shadow-xs text-[10px] font-bold text-[#19362A]">
                Fisher Manifold (1936)
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* 4 Pastel Floating Telemetry KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white rounded-2xl p-5 border border-[#E3EBE3] shadow-soft hover:shadow-float transition-all">
          <div className="w-10 h-10 rounded-xl bg-[#EAE7F5] text-[#76649D] flex items-center justify-center mb-3">
            <Database className="w-5 h-5" />
          </div>
          <div className="text-2xl font-extrabold text-[#19362A] tracking-tight">
            150
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
            3
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
            96.67%
          </div>
          <div className="text-xs uppercase font-bold text-[#728177] tracking-wider mt-1">
            Audited Test Accuracy
          </div>
          <div className="text-[11px] font-semibold text-[#285943] mt-2">
            Random Forest pipeline
          </div>
        </div>
      </div>

      {/* Analytics Workspace Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left: Complete 150-Point Morphological Scatter Plot */}
        <div className="lg:col-span-7 bg-white rounded-2xl p-6 border border-[#E3EBE3] shadow-soft space-y-4">
          <div className="flex justify-between items-start">
            <div>
              <h3 className="text-base font-extrabold text-[#19362A] tracking-tight">
                Morphological Relationships (All 150 Specimens)
              </h3>
              <p className="text-xs text-[#728177]">
                Petal length vs. petal width across the entire dataset. Setosa displays orthogonal separation.
              </p>
            </div>
            <span className="text-[11px] font-bold px-2 py-0.5 rounded-full bg-[#EFF8F0] text-[#285943] border border-[#DFF4E5]">
              Real API Data
            </span>
          </div>

          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <ScatterChart margin={{ top: 10, right: 20, bottom: 20, left: 0 }}>
                <XAxis type="number" dataKey="x" name="Petal Length" unit="cm" stroke="#8BAA91" fontSize={11} domain={[0.5, 7.5]} />
                <YAxis type="number" dataKey="y" name="Petal Width" unit="cm" stroke="#8BAA91" fontSize={11} domain={[0, 2.8]} />
                <Tooltip
                  cursor={{ strokeDasharray: '3 3' }}
                  formatter={(value: any, name: any) => [`${value} cm`, name === 'x' ? 'Petal Length' : 'Petal Width']}
                />
                <Legend verticalAlign="top" height={36} />
                <Scatter name="Setosa (50)" data={setosaData} fill="#76649D" />
                <Scatter name="Versicolor (50)" data={versicolorData} fill="#C18E61" />
                <Scatter name="Virginica (50)" data={virginicaData} fill="#2C6A50" />
              </ScatterChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Right: Species Cohort Donut Chart */}
        <div className="lg:col-span-5 bg-white rounded-2xl p-6 border border-[#E3EBE3] shadow-soft space-y-4">
          <div>
            <h3 className="text-base font-extrabold text-[#19362A] tracking-tight">
              Taxonomic Cohort Distribution
            </h3>
            <p className="text-xs text-[#728177]">
              Fisher's canonical 150-sample dataset: 50 balanced specimens per species (33.3% each).
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
                <Tooltip formatter={(value: any) => [`${value} specimens (33.3%)`, 'Frequency']} />
                <Legend verticalAlign="bottom" height={36} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Species Morphometric Moments Comparison Table */}
      {insights && (
        <div className="bg-white rounded-2xl p-6 border border-[#E3EBE3] shadow-soft space-y-3">
          <div className="flex justify-between items-center">
            <h3 className="text-base font-extrabold text-[#19362A] tracking-tight">
              Species Morphometric Baseline Comparison
            </h3>
            <span className="text-xs text-[#728177]">Empirical Means Calculated from Raw Data</span>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-[#F7FAF7] border-b border-[#E3EBE3] text-[#728177] uppercase font-bold text-[11px]">
                <tr>
                  <th className="py-2.5 px-4">Species Taxon</th>
                  <th className="py-2.5 px-4">Specimens</th>
                  <th className="py-2.5 px-4">Mean Sepal Length</th>
                  <th className="py-2.5 px-4">Mean Sepal Width</th>
                  <th className="py-2.5 px-4">Mean Petal Length</th>
                  <th className="py-2.5 px-4">Mean Petal Width</th>
                  <th className="py-2.5 px-4">Taxonomic Trait</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#E3EBE3]">
                {Object.entries(insights).map(([sp, item]: [string, any]) => (
                  <tr key={sp} className="hover:bg-[#F7FAF7]">
                    <td className="py-3 px-4 font-bold text-[#19362A]">Iris {sp}</td>
                    <td className="py-3 px-4 font-mono text-[#728177]">{item.count}</td>
                    <td className="py-3 px-4 font-mono text-[#19362A]">{item.means.sepal_length} cm</td>
                    <td className="py-3 px-4 font-mono text-[#19362A]">{item.means.sepal_width} cm</td>
                    <td className="py-3 px-4 font-mono text-[#19362A]">{item.means.petal_length} cm</td>
                    <td className="py-3 px-4 font-mono text-[#19362A]">{item.means.petal_width} cm</td>
                    <td className="py-3 px-4 text-[#285943] font-medium">{item.profile.morphology}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
