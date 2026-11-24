import React, { useState } from 'react';
import {
  ScanEye,
  Sparkles,
  RefreshCw,
  Send,
  Loader2,
  CheckCircle2,
  AlertCircle
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

  const speciesColor = response?.prediction.species.includes('Setosa')
    ? { bg: 'bg-[#EAE7F5]', text: 'text-[#76649D]', border: 'border-[#D6D0E8]' }
    : response?.prediction.species.includes('Versicolor')
    ? { bg: 'bg-[#F7EBDD]', text: 'text-[#C18E61]', border: 'border-[#EBDDCF]' }
    : { bg: 'bg-[#DFF4E5]', text: 'text-[#285943]', border: 'border-[#C7E2CE]' };

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      <div>
        <h2 className="text-2xl font-extrabold text-[#19362A] tracking-tight">
          Botanical Specimen Classifier
        </h2>
        <p className="text-sm text-[#728177]">
          Measure. Analyze. Discover. Enter flower measurements to identify the Iris species with machine-calibrated Softmax confidence.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Measurement Controls */}
        <div className="lg:col-span-6 bg-white rounded-3xl p-6 lg:p-8 border border-[#E3EBE3] shadow-soft space-y-6">
          <div className="border-b border-[#E3EBE3] pb-4">
            <h3 className="text-base font-extrabold text-[#19362A] tracking-tight">
              Morphometric Measurement Panel
            </h3>
            <p className="text-xs text-[#728177]">
              Bounded within empirical dataset coordinates (4.3–7.9 cm sepal, 1.0–6.9 cm petal).
            </p>
          </div>

          <div className="space-y-4">
            <div>
              <div className="flex justify-between text-xs font-bold text-[#19362A] mb-1">
                <span>Sepal Length (cm)</span>
                <span className="font-mono text-[#285943] text-sm">{sepalLength.toFixed(1)} cm</span>
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
            </div>

            <div>
              <div className="flex justify-between text-xs font-bold text-[#19362A] mb-1">
                <span>Sepal Width (cm)</span>
                <span className="font-mono text-[#285943] text-sm">{sepalWidth.toFixed(1)} cm</span>
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
            </div>

            <div>
              <div className="flex justify-between text-xs font-bold text-[#19362A] mb-1">
                <span>Petal Length (cm)</span>
                <span className="font-mono text-[#285943] text-sm">{petalLength.toFixed(1)} cm</span>
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
            </div>

            <div>
              <div className="flex justify-between text-xs font-bold text-[#19362A] mb-1">
                <span>Petal Width (cm)</span>
                <span className="font-mono text-[#285943] text-sm">{petalWidth.toFixed(1)} cm</span>
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
            </div>
          </div>

          {/* Quick Presets */}
          <div className="border-t border-[#E3EBE3] pt-4 space-y-2">
            <span className="text-[11px] uppercase font-bold text-[#8BAA91] tracking-wider block">
              Botanical Sample Presets
            </span>
            <div className="grid grid-cols-4 gap-2">
              <button
                onClick={() => applyPreset(5.0, 3.4, 1.5, 0.2)}
                className="px-2 py-2 rounded-xl bg-[#F7FAF7] hover:bg-[#EAE7F5] border border-[#E3EBE3] text-xs font-bold text-[#19362A] transition-colors"
              >
                Setosa
              </button>
              <button
                onClick={() => applyPreset(5.9, 2.8, 4.3, 1.3)}
                className="px-2 py-2 rounded-xl bg-[#F7FAF7] hover:bg-[#F7EBDD] border border-[#E3EBE3] text-xs font-bold text-[#19362A] transition-colors"
              >
                Versicolor
              </button>
              <button
                onClick={() => applyPreset(6.6, 3.0, 5.6, 2.0)}
                className="px-2 py-2 rounded-xl bg-[#F7FAF7] hover:bg-[#EFF8F0] border border-[#E3EBE3] text-xs font-bold text-[#19362A] transition-colors"
              >
                Virginica
              </button>
              <button
                onClick={() => applyPreset(5.8, 3.0, 4.3, 1.3)}
                className="px-2 py-2 rounded-xl bg-[#F7FAF7] hover:bg-[#E3EBE3] border border-[#E3EBE3] text-xs font-bold text-[#728177] transition-colors"
              >
                Reset
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
            <div className="h-full min-h-[400px] bg-white rounded-3xl p-8 border border-dashed border-[#E3EBE3] flex flex-col items-center justify-center text-center">
              <ScanEye className="w-12 h-12 text-[#8BAA91] mb-3 opacity-60" />
              <h4 className="text-base font-extrabold text-[#19362A]">
                Ready for Morphometric Inference
              </h4>
              <p className="text-xs text-[#728177] max-w-sm mt-1">
                Adjust sliders or click a sample preset on the left, then click "Predict Botanical Species".
              </p>
            </div>
          )}

          {response && (
            <div className="bg-white rounded-3xl p-6 lg:p-8 border border-[#E3EBE3] shadow-soft space-y-6">
              {/* Hero Diagnosis Badge */}
              <div className={`p-6 rounded-2xl text-center border ${speciesColor.bg} ${speciesColor.border}`}>
                <span className={`text-[11px] uppercase tracking-widest font-extrabold ${speciesColor.text}`}>
                  Verified Taxonomic Class
                </span>
                <h3 className={`text-3xl font-extrabold tracking-tight mt-1 mb-2 ${speciesColor.text}`}>
                  {response.prediction.species}
                </h3>
                <div className="text-xs font-bold text-[#19362A]">
                  Model Confidence: {(response.prediction.confidence * 100).toFixed(2)}%
                </div>
              </div>

              {/* Class Probability Distribution */}
              <div className="space-y-3">
                <span className="text-xs font-extrabold text-[#19362A] uppercase tracking-wider block">
                  Probability Distribution
                </span>

                {Object.entries(response.prediction.probabilities).map(([sp, prob]) => {
                  const pct = Math.round(prob * 100);
                  const isWinner = response.prediction.species.toLowerCase().includes(sp);
                  return (
                    <div key={sp} className="space-y-1">
                      <div className="flex justify-between text-xs font-semibold">
                        <span className="capitalize text-[#19362A] font-bold">Iris {sp}</span>
                        <span className={isWinner ? 'text-[#285943] font-bold' : 'text-[#728177]'}>
                          {(prob * 100).toFixed(1)}%
                        </span>
                      </div>
                      <div className="w-full bg-[#EFF8F0] h-2.5 rounded-full overflow-hidden border border-[#E3EBE3]">
                        <div
                          className={`h-full transition-all duration-500 rounded-full ${
                            isWinner ? 'bg-[#285943]' : 'bg-[#8BAA91]'
                          }`}
                          style={{ width: `${pct}%` }}
                        />
                      </div>
                    </div>
                  );
                })}
              </div>

              {/* Measurement Recap Pill */}
              <div className="p-3.5 rounded-xl bg-[#F7FAF7] border border-[#E3EBE3] text-xs text-[#19362A] flex justify-between font-mono">
                <span>Sepal: {sepalLength} × {sepalWidth} cm</span>
                <span>Petal: {petalLength} × {petalWidth} cm</span>
                <span>Ratio: {(petalLength / petalWidth).toFixed(2)}</span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
