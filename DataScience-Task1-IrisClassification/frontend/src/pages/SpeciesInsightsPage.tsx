import React, { useState, useEffect } from 'react';
import { Flower2, Sparkles } from 'lucide-react';
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

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      <div>
        <h2 className="text-2xl font-extrabold text-[#19362A] tracking-tight">
          Species Morphology & Insights
        </h2>
        <p className="text-sm text-[#728177]">
          Comparative botanical profiles, structural dimension boundaries, and morphological moments.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Setosa Profile Card */}
        <div className="bg-white rounded-3xl p-6 border-t-4 border-[#76649D] border border-[#E3EBE3] shadow-soft space-y-4">
          <div className="flex justify-between items-start">
            <div>
              <span className="text-[10px] uppercase font-bold text-[#76649D] tracking-widest block">
                Taxonomic Class
              </span>
              <h3 className="text-xl font-extrabold text-[#19362A]">Iris Setosa</h3>
            </div>
            <div className="w-8 h-8 rounded-full bg-[#EAE7F5] flex items-center justify-center text-[#76649D]">
              🌸
            </div>
          </div>
          <p className="text-xs text-[#728177] leading-relaxed">
            {setosa.profile.description}
          </p>
          <div className="p-4 rounded-2xl bg-[#F7FAF7] border border-[#E3EBE3] space-y-2 text-xs font-semibold text-[#19362A]">
            <div className="flex justify-between">
              <span className="text-[#728177]">Mean Sepal Length</span>
              <span className="font-bold">{setosa.means.sepal_length} cm</span>
            </div>
            <div className="flex justify-between">
              <span className="text-[#728177]">Mean Sepal Width</span>
              <span className="font-bold">{setosa.means.sepal_width} cm (Broadest)</span>
            </div>
            <div className="flex justify-between">
              <span className="text-[#728177]">Mean Petal Length</span>
              <span className="font-bold">{setosa.means.petal_length} cm (Shortest)</span>
            </div>
            <div className="flex justify-between">
              <span className="text-[#728177]">Mean Petal Width</span>
              <span className="font-bold">{setosa.means.petal_width} cm</span>
            </div>
          </div>
        </div>

        {/* Versicolor Profile Card */}
        <div className="bg-white rounded-3xl p-6 border-t-4 border-[#C18E61] border border-[#E3EBE3] shadow-soft space-y-4">
          <div className="flex justify-between items-start">
            <div>
              <span className="text-[10px] uppercase font-bold text-[#C18E61] tracking-widest block">
                Taxonomic Class
              </span>
              <h3 className="text-xl font-extrabold text-[#19362A]">Iris Versicolor</h3>
            </div>
            <div className="w-8 h-8 rounded-full bg-[#F7EBDD] flex items-center justify-center text-[#C18E61]">
              🌾
            </div>
          </div>
          <p className="text-xs text-[#728177] leading-relaxed">
            {versicolor.profile.description}
          </p>
          <div className="p-4 rounded-2xl bg-[#F7FAF7] border border-[#E3EBE3] space-y-2 text-xs font-semibold text-[#19362A]">
            <div className="flex justify-between">
              <span className="text-[#728177]">Mean Sepal Length</span>
              <span className="font-bold">{versicolor.means.sepal_length} cm</span>
            </div>
            <div className="flex justify-between">
              <span className="text-[#728177]">Mean Sepal Width</span>
              <span className="font-bold">{versicolor.means.sepal_width} cm</span>
            </div>
            <div className="flex justify-between">
              <span className="text-[#728177]">Mean Petal Length</span>
              <span className="font-bold">{versicolor.means.petal_length} cm</span>
            </div>
            <div className="flex justify-between">
              <span className="text-[#728177]">Mean Petal Width</span>
              <span className="font-bold">{versicolor.means.petal_width} cm</span>
            </div>
          </div>
        </div>

        {/* Virginica Profile Card */}
        <div className="bg-white rounded-3xl p-6 border-t-4 border-[#285943] border border-[#E3EBE3] shadow-soft space-y-4">
          <div className="flex justify-between items-start">
            <div>
              <span className="text-[10px] uppercase font-bold text-[#285943] tracking-widest block">
                Taxonomic Class
              </span>
              <h3 className="text-xl font-extrabold text-[#19362A]">Iris Virginica</h3>
            </div>
            <div className="w-8 h-8 rounded-full bg-[#EFF8F0] flex items-center justify-center text-[#285943]">
              🌺
            </div>
          </div>
          <p className="text-xs text-[#728177] leading-relaxed">
            {virginica.profile.description}
          </p>
          <div className="p-4 rounded-2xl bg-[#F7FAF7] border border-[#E3EBE3] space-y-2 text-xs font-semibold text-[#19362A]">
            <div className="flex justify-between">
              <span className="text-[#728177]">Mean Sepal Length</span>
              <span className="font-bold">{virginica.means.sepal_length} cm (Longest)</span>
            </div>
            <div className="flex justify-between">
              <span className="text-[#728177]">Mean Sepal Width</span>
              <span className="font-bold">{virginica.means.sepal_width} cm</span>
            </div>
            <div className="flex justify-between">
              <span className="text-[#728177]">Mean Petal Length</span>
              <span className="font-bold">{virginica.means.petal_length} cm (Longest)</span>
            </div>
            <div className="flex justify-between">
              <span className="text-[#728177]">Mean Petal Width</span>
              <span className="font-bold">{virginica.means.petal_width} cm (Widest)</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
