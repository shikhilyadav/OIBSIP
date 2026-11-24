import React, { useState, useEffect } from 'react';
import { Flower2, Sparkles, BarChart2, Layers, CheckCircle2 } from 'lucide-react';
import { fetchSpeciesInsights, SpeciesInsightItem } from '../api/client';

export default function SpeciesInsightsPage() {
  const [insights, setInsights] = useState<Record<string, SpeciesInsightItem> | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSpeciesInsights()
      .then((res) => setInsights(res.insights))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading || !insights) {
    return <div className="p-8 text-center text-xs text-[#728177]">Loading Species Morphology Insights...</div>;
  }

  const setosa = insights['Setosa'];
  const versicolor = insights['Versicolor'];
  const virginica = insights['Virginica'];

  const speciesList = [
    { key: 'Setosa', data: setosa, icon: '🌸', color: '#76649D', bg: '#EAE7F5', border: '#D6D0E8' },
    { key: 'Versicolor', data: versicolor, icon: '🌾', color: '#C18E61', bg: '#F7EBDD', border: '#EBDDCF' },
    { key: 'Virginica', data: virginica, icon: '🌺', color: '#285943', bg: '#EFF8F0', border: '#C7E2CE' },
  ];

  const features = [
    { label: 'Sepal Length', key: 'sepal_length', maxVal: 8.0, unit: 'cm' },
    { label: 'Sepal Width', key: 'sepal_width', maxVal: 4.5, unit: 'cm' },
    { label: 'Petal Length', key: 'petal_length', maxVal: 7.0, unit: 'cm' },
    { label: 'Petal Width', key: 'petal_width', maxVal: 2.6, unit: 'cm' },
  ];

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-extrabold text-[#19362A] tracking-tight">
          Species Morphology & Taxonomic Insights
        </h2>
        <p className="text-sm text-[#728177]">
          Comparative botanical profiles, structural dimension boundaries, and morphological moments.
        </p>
      </div>

      {/* 3 Taxonomic Profile Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {speciesList.map(({ key, data, icon, color, bg, border }) => (
          <div
            key={key}
            className="bg-white rounded-3xl p-6 border border-[#E3EBE3] shadow-soft space-y-4 relative overflow-hidden"
            style={{ borderTop: `4px solid ${color}` }}
          >
            <div className="flex justify-between items-start">
              <div>
                <span
                  className="text-[10px] uppercase font-bold tracking-widest block"
                  style={{ color }}
                >
                  {data.profile.tagline || 'Taxonomic Cohort'}
                </span>
                <h3 className="text-xl font-extrabold text-[#19362A] mt-0.5">
                  Iris {key}
                </h3>
              </div>
              <div
                className="w-10 h-10 rounded-2xl flex items-center justify-center text-lg border"
                style={{ backgroundColor: bg, borderColor: border }}
              >
                {icon}
              </div>
            </div>

            <p className="text-xs text-[#728177] leading-relaxed">
              {data.profile.description}
            </p>

            <div className="p-3.5 rounded-2xl bg-[#F7FAF7] border border-[#E3EBE3] space-y-2 text-xs">
              <div className="flex justify-between">
                <span className="text-[#728177]">Mean Sepal Length</span>
                <span className="font-bold text-[#19362A] font-mono">{data.means.sepal_length} cm</span>
              </div>
              <div className="flex justify-between">
                <span className="text-[#728177]">Mean Sepal Width</span>
                <span className="font-bold text-[#19362A] font-mono">{data.means.sepal_width} cm</span>
              </div>
              <div className="flex justify-between">
                <span className="text-[#728177]">Mean Petal Length</span>
                <span className="font-bold text-[#19362A] font-mono">{data.means.petal_length} cm</span>
              </div>
              <div className="flex justify-between">
                <span className="text-[#728177]">Mean Petal Width</span>
                <span className="font-bold text-[#19362A] font-mono">{data.means.petal_width} cm</span>
              </div>
            </div>

            <div className="pt-1 text-[11px] text-[#728177] flex items-center space-x-1.5 font-medium">
              <span className="w-1.5 h-1.5 rounded-full" style={{ backgroundColor: color }}></span>
              <span>Sample Cohort: <b>{data.count} specimens</b> (33.3% of corpus)</span>
            </div>
          </div>
        ))}
      </div>

      {/* Morphometric Comparison Matrix */}
      <div className="bg-white rounded-3xl p-6 lg:p-8 border border-[#E3EBE3] shadow-soft space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-[#E3EBE3] pb-4">
          <div>
            <h3 className="text-base font-extrabold text-[#19362A] tracking-tight">
              Cross-Taxa Morphometric Scale Comparison
            </h3>
            <p className="text-xs text-[#728177]">
              Empirical mean structural dimensions normalized across maximum biological boundaries.
            </p>
          </div>
          <div className="flex items-center space-x-3 text-xs font-semibold">
            <span className="flex items-center space-x-1 text-[#76649D]">
              <span className="w-2.5 h-2.5 rounded-full bg-[#76649D]"></span>
              <span>Setosa</span>
            </span>
            <span className="flex items-center space-x-1 text-[#C18E61]">
              <span className="w-2.5 h-2.5 rounded-full bg-[#C18E61]"></span>
              <span>Versicolor</span>
            </span>
            <span className="flex items-center space-x-1 text-[#285943]">
              <span className="w-2.5 h-2.5 rounded-full bg-[#285943]"></span>
              <span>Virginica</span>
            </span>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {features.map((f) => (
            <div key={f.key} className="p-4 rounded-2xl bg-[#F7FAF7] border border-[#E3EBE3] space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-xs font-bold text-[#19362A]">{f.label}</span>
                <span className="text-[10px] text-[#728177] font-mono">Max: {f.maxVal} {f.unit}</span>
              </div>

              {speciesList.map(({ key, data, color }) => {
                const val = (data.means as any)[f.key];
                const pct = Math.round((val / f.maxVal) * 100);
                return (
                  <div key={key} className="space-y-1">
                    <div className="flex justify-between text-[11px] font-semibold">
                      <span className="text-[#728177]">Iris {key}</span>
                      <span className="font-mono text-[#19362A] font-bold">{val} {f.unit}</span>
                    </div>
                    <div className="w-full bg-white h-2 rounded-full overflow-hidden border border-[#E3EBE3]">
                      <div
                        className="h-full rounded-full transition-all duration-500"
                        style={{ width: `${pct}%`, backgroundColor: color }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          ))}
        </div>
      </div>

      {/* Key Botanical Takeaways */}
      <div className="bg-[#EFF8F0] rounded-3xl p-6 border border-[#C7E2CE] flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="flex items-center space-x-4">
          <div className="w-12 h-12 rounded-2xl bg-[#285943] text-white flex items-center justify-center shrink-0">
            <Sparkles className="w-6 h-6" />
          </div>
          <div>
            <h4 className="text-sm font-extrabold text-[#19362A]">
              Taxonomic Separability Diagnostic
            </h4>
            <p className="text-xs text-[#285943] mt-0.5 max-w-2xl leading-relaxed">
              Iris Setosa displays strict linear separability in petal dimensions (petal length &lt; 2 cm, petal width &lt; 0.6 cm). Versicolor and Virginica share adjacent morphometric boundaries with minimal overlap, reliably resolved by our 100-tree Random Forest ensemble.
            </p>
          </div>
        </div>
        <div className="shrink-0 text-right">
          <span className="text-[10px] uppercase font-bold text-[#285943] tracking-widest block">
            Linear Separability
          </span>
          <span className="text-xl font-extrabold text-[#19362A]">
            100% Setosa
          </span>
        </div>
      </div>
    </div>
  );
}
