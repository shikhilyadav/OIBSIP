import React, { useState } from 'react';
import {
  ScanEye,
  RefreshCw,
  Loader2,
  CheckCircle2,
  AlertCircle,
  HelpCircle,
  ArrowRight,
  Sparkles,
  Layers,
  Ruler
} from 'lucide-react';
import { predictSpecimen, PredictionResponse } from '../api/client';

export default function ClassifierPage() {
  const [sepalLength, setSepalLength] = useState<number>(5.8);
  const [sepalWidth, setSepalWidth] = useState<number>(3.0);
  const [petalLength, setPetalLength] = useState<number>(4.3);
  const [petalWidth, setPetalWidth] = useState<number>(1.3);

  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<PredictionResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handlePredict = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await predictSpecimen({
        sepal_length: sepalLength,
        sepal_width: sepalWidth,
        petal_length: petalLength,
        petal_width: petalWidth,
      });
      setResponse(data);
    } catch (err: any) {
      setError(err.message || 'Prediction service unavailable. Please ensure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const applyPreset = (sl: number, sw: number, pl: number, pw: number) => {
    setSepalLength(sl);
    setSepalWidth(sw);
    setPetalLength(pl);
    setPetalWidth(pw);
  };

  const getSpeciesBadge = (speciesName: string) => {
    if (speciesName.toLowerCase().includes('setosa')) {
      return {
        bg: 'bg-[#EAE7F5]',
        text: 'text-[#76649D]',
        border: 'border-[#D6D0E8]',
        emoji: '🌸',
        taxon: 'Iris setosa Pallas ex Link',
        note: 'Distinctive compact petals with wide sepals. Absolute linear separability in petal feature space.'
      };
    }
    if (speciesName.toLowerCase().includes('versicolor')) {
      return {
        bg: 'bg-[#F7EBDD]',
        text: 'text-[#C18E61]',
        border: 'border-[#EBDDCF]',
        emoji: '🌾',
        taxon: 'Iris versicolor L.',
        note: 'Intermediate morphometric dimensions across all four structural axes.'
      };
    }
    return {
      bg: 'bg-[#DFF4E5]',
      text: 'text-[#285943]',
      border: 'border-[#C7E2CE]',
      emoji: '🌺',
      taxon: 'Iris virginica L.',
      note: 'Robust structural scale characterized by elongated petals and high petal width.'
    };
  };

  const speciesInfo = response ? getSpeciesBadge(response.prediction.species) : null;

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-extrabold text-[#19362A] tracking-tight">
          Botanical Specimen Classifier
        </h2>
        <p className="text-sm text-[#728177]">
          Measure. Analyze. Discover. Enter flower measurements to identify the Iris species with machine-calibrated ensemble class probabilities.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Left Column: Morphometric Controls */}
        <div className="lg:col-span-6 bg-white rounded-3xl p-6 lg:p-8 border border-[#E3EBE3] shadow-soft space-y-6">
          <div className="border-b border-[#E3EBE3] pb-4 flex justify-between items-center">
            <div>
              <h3 className="text-base font-extrabold text-[#19362A] tracking-tight">
                Morphometric Measurement Panel
              </h3>
              <p className="text-xs text-[#728177]">
                Bounded within empirical dataset coordinates (4.3–7.9 cm sepal, 1.0–6.9 cm petal).
              </p>
            </div>
            <div className="w-8 h-8 rounded-full bg-[#EFF8F0] flex items-center justify-center text-[#285943]">
              <Ruler className="w-4 h-4" />
            </div>
          </div>

          <div className="space-y-5">
            {/* Sepal Length */}
            <div>
              <div className="flex justify-between items-center text-xs font-bold text-[#19362A] mb-1.5">
                <span className="flex items-center space-x-1.5">
                  <span className="w-2 h-2 rounded-full bg-[#285943]"></span>
                  <span>Sepal Length</span>
                </span>
                <span className="font-mono text-[#285943] text-sm bg-[#EFF8F0] px-2 py-0.5 rounded-lg border border-[#E3EBE3]">
                  {sepalLength.toFixed(1)} cm
                </span>
              </div>
              <input
                type="range"
                min="4.0"
                max="8.0"
                step="0.1"
                value={sepalLength}
                onChange={(e) => setSepalLength(parseFloat(e.target.value))}
                className="w-full accent-[#285943] cursor-pointer"
              />
              <div className="flex justify-between text-[10px] text-[#8BAA91] font-mono mt-0.5">
                <span>Min: 4.0 cm</span>
                <span>Dataset Mean: 5.84 cm</span>
                <span>Max: 8.0 cm</span>
              </div>
            </div>

            {/* Sepal Width */}
            <div>
              <div className="flex justify-between items-center text-xs font-bold text-[#19362A] mb-1.5">
                <span className="flex items-center space-x-1.5">
                  <span className="w-2 h-2 rounded-full bg-[#8BAA91]"></span>
                  <span>Sepal Width</span>
                </span>
                <span className="font-mono text-[#285943] text-sm bg-[#EFF8F0] px-2 py-0.5 rounded-lg border border-[#E3EBE3]">
                  {sepalWidth.toFixed(1)} cm
                </span>
              </div>
              <input
                type="range"
                min="2.0"
                max="4.5"
                step="0.1"
                value={sepalWidth}
                onChange={(e) => setSepalWidth(parseFloat(e.target.value))}
                className="w-full accent-[#285943] cursor-pointer"
              />
              <div className="flex justify-between text-[10px] text-[#8BAA91] font-mono mt-0.5">
                <span>Min: 2.0 cm</span>
                <span>Dataset Mean: 3.05 cm</span>
                <span>Max: 4.5 cm</span>
              </div>
            </div>

            {/* Petal Length */}
            <div>
              <div className="flex justify-between items-center text-xs font-bold text-[#19362A] mb-1.5">
                <span className="flex items-center space-x-1.5">
                  <span className="w-2 h-2 rounded-full bg-[#C18E61]"></span>
                  <span>Petal Length</span>
                </span>
                <span className="font-mono text-[#285943] text-sm bg-[#EFF8F0] px-2 py-0.5 rounded-lg border border-[#E3EBE3]">
                  {petalLength.toFixed(1)} cm
                </span>
              </div>
              <input
                type="range"
                min="1.0"
                max="7.0"
                step="0.1"
                value={petalLength}
                onChange={(e) => setPetalLength(parseFloat(e.target.value))}
                className="w-full accent-[#285943] cursor-pointer"
              />
              <div className="flex justify-between text-[10px] text-[#8BAA91] font-mono mt-0.5">
                <span>Min: 1.0 cm</span>
                <span>Dataset Mean: 3.76 cm</span>
                <span>Max: 7.0 cm</span>
              </div>
            </div>

            {/* Petal Width */}
            <div>
              <div className="flex justify-between items-center text-xs font-bold text-[#19362A] mb-1.5">
                <span className="flex items-center space-x-1.5">
                  <span className="w-2 h-2 rounded-full bg-[#76649D]"></span>
                  <span>Petal Width</span>
                </span>
                <span className="font-mono text-[#285943] text-sm bg-[#EFF8F0] px-2 py-0.5 rounded-lg border border-[#E3EBE3]">
                  {petalWidth.toFixed(1)} cm
                </span>
              </div>
              <input
                type="range"
                min="0.1"
                max="2.6"
                step="0.1"
                value={petalWidth}
                onChange={(e) => setPetalWidth(parseFloat(e.target.value))}
                className="w-full accent-[#285943] cursor-pointer"
              />
              <div className="flex justify-between text-[10px] text-[#8BAA91] font-mono mt-0.5">
                <span>Min: 0.1 cm</span>
                <span>Dataset Mean: 1.20 cm</span>
                <span>Max: 2.6 cm</span>
              </div>
            </div>
          </div>

          {/* Preset Buttons */}
          <div className="border-t border-[#E3EBE3] pt-4 space-y-2">
            <span className="text-[11px] uppercase font-bold text-[#8BAA91] tracking-wider block">
              Morphometric Archetype Presets
            </span>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
              <button
                type="button"
                onClick={() => applyPreset(5.0, 3.4, 1.5, 0.2)}
                className="px-3 py-2 rounded-xl bg-[#F7FAF7] hover:bg-[#EAE7F5] border border-[#E3EBE3] text-xs font-bold text-[#19362A] transition-colors flex items-center justify-center space-x-1"
              >
                <span>🌸</span>
                <span>Setosa</span>
              </button>
              <button
                type="button"
                onClick={() => applyPreset(5.9, 2.8, 4.3, 1.3)}
                className="px-3 py-2 rounded-xl bg-[#F7FAF7] hover:bg-[#F7EBDD] border border-[#E3EBE3] text-xs font-bold text-[#19362A] transition-colors flex items-center justify-center space-x-1"
              >
                <span>🌾</span>
                <span>Versicolor</span>
              </button>
              <button
                type="button"
                onClick={() => applyPreset(6.6, 3.0, 5.6, 2.0)}
                className="px-3 py-2 rounded-xl bg-[#F7FAF7] hover:bg-[#EFF8F0] border border-[#E3EBE3] text-xs font-bold text-[#19362A] transition-colors flex items-center justify-center space-x-1"
              >
                <span>🌺</span>
                <span>Virginica</span>
              </button>
              <button
                type="button"
                onClick={() => applyPreset(5.8, 3.0, 4.3, 1.3)}
                className="px-3 py-2 rounded-xl bg-[#F7FAF7] hover:bg-[#E3EBE3] border border-[#E3EBE3] text-xs font-bold text-[#728177] transition-colors flex items-center justify-center space-x-1"
              >
                <RefreshCw className="w-3.5 h-3.5" />
                <span>Reset</span>
              </button>
            </div>
          </div>

          <button
            onClick={handlePredict}
            disabled={loading}
            className="w-full flex items-center justify-center space-x-2 py-3.5 rounded-xl bg-[#285943] hover:bg-[#173D2D] text-white font-bold text-sm tracking-wide transition-all shadow-md disabled:opacity-60"
          >
            {loading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                <span>Running Pipeline Inference...</span>
              </>
            ) : (
              <>
                <ScanEye className="w-4 h-4" />
                <span>Predict Botanical Species</span>
              </>
            )}
          </button>
        </div>

        {/* Right Column: Prediction Output */}
        <div className="lg:col-span-6 space-y-4">
          {error && (
            <div className="p-5 rounded-2xl bg-rose-50 border border-rose-200 text-rose-700 text-xs flex items-center space-x-3">
              <AlertCircle className="w-5 h-5 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          {!response && !loading && (
            <div className="h-full min-h-[460px] bg-white rounded-3xl p-8 border border-dashed border-[#E3EBE3] flex flex-col items-center justify-center text-center">
              <div className="w-16 h-16 rounded-3xl bg-[#EFF8F0] flex items-center justify-center text-[#285943] mb-4">
                <ScanEye className="w-8 h-8 opacity-80" />
              </div>
              <h4 className="text-base font-extrabold text-[#19362A]">
                Ready for Morphometric Inference
              </h4>
              <p className="text-xs text-[#728177] max-w-sm mt-1.5 leading-relaxed">
                Adjust sliders or click a sample preset on the left, then click "Predict Botanical Species" to query the trained Random Forest classifier.
              </p>
              <div className="mt-6 flex flex-wrap justify-center gap-2 text-[11px] font-semibold text-[#8BAA91]">
                <span className="px-3 py-1 bg-[#F7FAF7] rounded-full border border-[#E3EBE3]">
                  100 Ensemble Trees
                </span>
                <span className="px-3 py-1 bg-[#F7FAF7] rounded-full border border-[#E3EBE3]">
                  4 Dimensional Vector
                </span>
                <span className="px-3 py-1 bg-[#F7FAF7] rounded-full border border-[#E3EBE3]">
                  96.67% Test Accuracy
                </span>
              </div>
            </div>
          )}

          {response && speciesInfo && (
            <div className="bg-white rounded-3xl p-6 lg:p-8 border border-[#E3EBE3] shadow-soft space-y-6">
              {/* Hero Diagnosis Banner */}
              <div className={`p-6 rounded-2xl text-center border relative overflow-hidden ${speciesInfo.bg} ${speciesInfo.border}`}>
                <div className="text-4xl mb-2">{speciesInfo.emoji}</div>
                <span className={`text-[11px] uppercase tracking-widest font-extrabold ${speciesInfo.text}`}>
                  Verified Taxonomic Class
                </span>
                <h3 className={`text-3xl font-extrabold tracking-tight mt-1 mb-1 ${speciesInfo.text}`}>
                  {response.prediction.species}
                </h3>
                <div className="text-xs italic text-[#19362A] opacity-80 mb-3">
                  {speciesInfo.taxon}
                </div>
                <div className="inline-flex items-center space-x-2 bg-white/80 backdrop-blur-sm px-4 py-1.5 rounded-full border border-white/60 shadow-xs">
                  <span className="text-xs font-bold text-[#19362A]">
                    Ensemble Confidence:
                  </span>
                  <span className="text-sm font-extrabold text-[#285943]">
                    {(response.prediction.confidence * 100).toFixed(2)}%
                  </span>
                </div>
                <p className="text-xs text-[#19362A]/80 mt-3 max-w-md mx-auto leading-relaxed">
                  {speciesInfo.note}
                </p>
              </div>

              {/* Class Probability Distribution */}
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-xs font-extrabold text-[#19362A] uppercase tracking-wider">
                    Class Probability Distribution
                  </span>
                  <span className="text-[11px] text-[#728177] font-mono">
                    Vote Fraction
                  </span>
                </div>

                {Object.entries(response.prediction.probabilities).map(([sp, prob]) => {
                  const pct = Math.round(prob * 100);
                  const isWinner = response.prediction.species.toLowerCase().includes(sp.toLowerCase());
                  const barColor = isWinner
                    ? 'bg-[#285943]'
                    : sp.toLowerCase().includes('setosa')
                    ? 'bg-[#76649D]'
                    : sp.toLowerCase().includes('versicolor')
                    ? 'bg-[#C18E61]'
                    : 'bg-[#8BAA91]';

                  return (
                    <div key={sp} className="space-y-1">
                      <div className="flex justify-between text-xs font-semibold">
                        <span className="capitalize text-[#19362A] font-bold flex items-center space-x-1.5">
                          <span>{sp.toLowerCase().includes('setosa') ? '🌸' : sp.toLowerCase().includes('versicolor') ? '🌾' : '🌺'}</span>
                          <span>Iris {sp}</span>
                        </span>
                        <span className={isWinner ? 'text-[#285943] font-bold' : 'text-[#728177]'}>
                          {(prob * 100).toFixed(1)}%
                        </span>
                      </div>
                      <div className="w-full bg-[#EFF8F0] h-2.5 rounded-full overflow-hidden border border-[#E3EBE3]">
                        <div
                          className={`h-full transition-all duration-500 rounded-full ${barColor}`}
                          style={{ width: `${pct}%` }}
                        />
                      </div>
                    </div>
                  );
                })}
              </div>

              {/* Measurement Recap Table */}
              <div className="p-4 rounded-2xl bg-[#F7FAF7] border border-[#E3EBE3] space-y-2">
                <span className="text-[11px] uppercase font-bold text-[#728177] tracking-wider block">
                  Input Telemetry Recap
                </span>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-center text-xs">
                  <div className="bg-white p-2 rounded-xl border border-[#E3EBE3]">
                    <div className="text-[10px] text-[#728177]">Sepal L.</div>
                    <div className="font-bold text-[#19362A] font-mono">{sepalLength.toFixed(1)} cm</div>
                  </div>
                  <div className="bg-white p-2 rounded-xl border border-[#E3EBE3]">
                    <div className="text-[10px] text-[#728177]">Sepal W.</div>
                    <div className="font-bold text-[#19362A] font-mono">{sepalWidth.toFixed(1)} cm</div>
                  </div>
                  <div className="bg-white p-2 rounded-xl border border-[#E3EBE3]">
                    <div className="text-[10px] text-[#728177]">Petal L.</div>
                    <div className="font-bold text-[#19362A] font-mono">{petalLength.toFixed(1)} cm</div>
                  </div>
                  <div className="bg-white p-2 rounded-xl border border-[#E3EBE3]">
                    <div className="text-[10px] text-[#728177]">Petal W.</div>
                    <div className="font-bold text-[#19362A] font-mono">{petalWidth.toFixed(1)} cm</div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
