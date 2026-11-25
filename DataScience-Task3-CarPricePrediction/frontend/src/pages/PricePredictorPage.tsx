import React, { useState, useEffect } from 'react';
import { 
  Calculator, 
  Car, 
  RotateCcw, 
  Send, 
  Loader2, 
  CheckCircle2, 
  AlertCircle, 
  Clock, 
  Download, 
  History, 
  ShieldCheck,
  Sparkles,
  Info
} from 'lucide-react';
import { 
  predictPrice, 
  fetchDatasetOptions, 
  DatasetOptions, 
  PredictResult 
} from '../api/client';

interface PredictionRecord extends PredictResult {
  id: string;
}

export default function PricePredictorPage() {
  const [options, setOptions] = useState<DatasetOptions | null>(null);
  const [brand, setBrand] = useState('Maruti');
  const [year, setYear] = useState(2017);
  const [kmDriven, setKmDriven] = useState(45000);
  const [fuel, setFuel] = useState('Petrol');
  const [sellerType, setSellerType] = useState('Individual');
  const [transmission, setTransmission] = useState('Manual');
  const [owner, setOwner] = useState('First Owner');

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<PredictResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [history, setHistory] = useState<PredictionRecord[]>([]);

  useEffect(() => {
    fetchDatasetOptions().then(setOptions).catch(console.error);
  }, []);

  const handlePredict = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res = await predictPrice({
        brand,
        year,
        km_driven: kmDriven,
        fuel,
        seller_type: sellerType,
        transmission,
        owner
      });
      setResult(res.data);
      const newRecord: PredictionRecord = {
        ...res.data,
        id: `VAL-${Date.now().toString().slice(-6)}`
      };
      setHistory(prev => [newRecord, ...prev.slice(0, 9)]);
    } catch (err: any) {
      setError(err.message || 'Valuation service unreachable. Please ensure the backend server is running on port 8002.');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setBrand('Maruti');
    setYear(2017);
    setKmDriven(45000);
    setFuel('Petrol');
    setSellerType('Individual');
    setTransmission('Manual');
    setOwner('First Owner');
    setResult(null);
    setError(null);
  };

  const applyPreset = (b: string, y: number, km: number, f: string, t: string, o: string, s: string) => {
    setBrand(b);
    setYear(y);
    setKmDriven(km);
    setFuel(f);
    setTransmission(t);
    setOwner(o);
    setSellerType(s);
    setResult(null);
  };

  const exportHistoryCSV = () => {
    if (!history.length) return;
    const headers = ['ID', 'Brand', 'Year', 'KmDriven', 'Fuel', 'Transmission', 'Owner', 'PredictedPrice', 'FormattedPrice', 'Timestamp'];
    const rows = history.map(h => [
      h.id,
      h.inputs.brand,
      h.inputs.year,
      h.inputs.km_driven,
      h.inputs.fuel,
      h.inputs.transmission,
      h.inputs.owner,
      h.predicted_price,
      `"${h.formatted_price}"`,
      `"${h.timestamp}"`
    ]);
    const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...rows.map(e => e.join(','))].join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `autovalue_predictions_${Date.now()}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-extrabold text-[#073B32] tracking-tight font-display">
          Vehicle Valuation Calculator
        </h2>
        <p className="text-xs text-[#77827E] mt-0.5">
          Enter vehicle specifications to generate fair-market appraisal values using the trained scikit-learn regression pipeline.
        </p>
      </div>

      {/* Main Two-Column Valuation Interface */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Left Column: Input Form */}
        <div className="lg:col-span-7 bg-white rounded-3xl p-6 lg:p-8 border border-[#E4E8E1] shadow-soft space-y-6">
          <div className="border-b border-[#E4E8E1] pb-3 flex justify-between items-center">
            <div>
              <h3 className="text-base font-extrabold text-[#073B32] font-display">
                Vehicle Telemetry Form
              </h3>
              <p className="text-[11px] text-[#77827E]">
                Select make, age, odometer, and mechanical attributes.
              </p>
            </div>
            <div className="w-8 h-8 rounded-xl bg-[#F7F5F0] text-[#073B32] flex items-center justify-center">
              <Calculator className="w-4 h-4" />
            </div>
          </div>

          <form onSubmit={handlePredict} className="space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {/* Brand Selector */}
              <div>
                <label className="text-[11px] uppercase font-bold text-[#77827E] tracking-wider block mb-1">
                  Manufacturer / Brand
                </label>
                <select
                  value={brand}
                  onChange={(e) => setBrand(e.target.value)}
                  className="w-full bg-[#F7F5F0] border border-[#E4E8E1] rounded-xl px-3.5 py-2.5 text-xs text-[#202A28] font-semibold focus:outline-none focus:border-[#125B48] transition-colors cursor-pointer"
                >
                  {options?.brands.map((b) => (
                    <option key={b} value={b}>{b}</option>
                  )) || <option value="Maruti">Maruti</option>}
                </select>
              </div>

              {/* Year Selector */}
              <div>
                <label className="text-[11px] uppercase font-bold text-[#77827E] tracking-wider block mb-1">
                  Manufacturing Year
                </label>
                <select
                  value={year}
                  onChange={(e) => setYear(parseInt(e.target.value))}
                  className="w-full bg-[#F7F5F0] border border-[#E4E8E1] rounded-xl px-3.5 py-2.5 text-xs text-[#202A28] font-semibold focus:outline-none focus:border-[#125B48] transition-colors cursor-pointer"
                >
                  {Array.from({ length: 28 }, (_, i) => 2020 - i).map((y) => (
                    <option key={y} value={y}>{y} ({2020 - y} yrs old)</option>
                  ))}
                </select>
              </div>

              {/* Odometer (Km Driven) */}
              <div>
                <div className="flex justify-between items-center mb-1">
                  <label className="text-[11px] uppercase font-bold text-[#77827E] tracking-wider">
                    Odometer Mileage
                  </label>
                  <span className="font-mono text-xs font-bold text-[#073B32]">
                    {kmDriven.toLocaleString()} km
                  </span>
                </div>
                <input
                  type="number"
                  min={0}
                  max={500000}
                  step={1000}
                  value={kmDriven}
                  onChange={(e) => setKmDriven(Math.max(0, parseInt(e.target.value) || 0))}
                  className="w-full bg-[#F7F5F0] border border-[#E4E8E1] rounded-xl px-3.5 py-2 text-xs text-[#202A28] font-mono font-bold focus:outline-none focus:border-[#125B48]"
                />
              </div>

              {/* Fuel Type */}
              <div>
                <label className="text-[11px] uppercase font-bold text-[#77827E] tracking-wider block mb-1">
                  Fuel Type
                </label>
                <select
                  value={fuel}
                  onChange={(e) => setFuel(e.target.value)}
                  className="w-full bg-[#F7F5F0] border border-[#E4E8E1] rounded-xl px-3.5 py-2.5 text-xs text-[#202A28] font-semibold focus:outline-none focus:border-[#125B48] transition-colors cursor-pointer"
                >
                  {options?.fuels.map((f) => (
                    <option key={f} value={f}>{f}</option>
                  )) || ['Petrol', 'Diesel', 'CNG', 'LPG'].map(f => <option key={f} value={f}>{f}</option>)}
                </select>
              </div>

              {/* Transmission */}
              <div>
                <label className="text-[11px] uppercase font-bold text-[#77827E] tracking-wider block mb-1">
                  Transmission
                </label>
                <select
                  value={transmission}
                  onChange={(e) => setTransmission(e.target.value)}
                  className="w-full bg-[#F7F5F0] border border-[#E4E8E1] rounded-xl px-3.5 py-2.5 text-xs text-[#202A28] font-semibold focus:outline-none focus:border-[#125B48] transition-colors cursor-pointer"
                >
                  <option value="Manual">Manual</option>
                  <option value="Automatic">Automatic</option>
                </select>
              </div>

              {/* Owner Type */}
              <div>
                <label className="text-[11px] uppercase font-bold text-[#77827E] tracking-wider block mb-1">
                  Ownership Title
                </label>
                <select
                  value={owner}
                  onChange={(e) => setOwner(e.target.value)}
                  className="w-full bg-[#F7F5F0] border border-[#E4E8E1] rounded-xl px-3.5 py-2.5 text-xs text-[#202A28] font-semibold focus:outline-none focus:border-[#125B48] transition-colors cursor-pointer"
                >
                  <option value="First Owner">First Owner</option>
                  <option value="Second Owner">Second Owner</option>
                  <option value="Third Owner">Third Owner</option>
                  <option value="Fourth & Above Owner">Fourth & Above Owner</option>
                  <option value="Test Drive Car">Test Drive Car</option>
                </select>
              </div>

              {/* Seller Type */}
              <div className="sm:col-span-2">
                <label className="text-[11px] uppercase font-bold text-[#77827E] tracking-wider block mb-1">
                  Seller Channel
                </label>
                <div className="grid grid-cols-3 gap-2">
                  {['Individual', 'Dealer', 'Trustmark Dealer'].map((st) => (
                    <button
                      key={st}
                      type="button"
                      onClick={() => setSellerType(st)}
                      className={`py-2 px-3 rounded-xl text-xs font-bold transition-all border ${
                        sellerType === st
                          ? 'bg-[#073B32] text-white border-[#073B32] shadow-sm'
                          : 'bg-[#F7F5F0] text-[#77827E] border-[#E4E8E1] hover:bg-[#EFECE3]'
                      }`}
                    >
                      {st}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {/* Quick Presets */}
            <div className="pt-2 border-t border-[#E4E8E1] space-y-1.5">
              <span className="text-[10px] uppercase font-bold text-[#77827E] tracking-wider block">
                Quick Archetype Presets
              </span>
              <div className="grid grid-cols-3 gap-2">
                <button
                  type="button"
                  onClick={() => applyPreset('Maruti', 2018, 30000, 'Petrol', 'Manual', 'First Owner', 'Individual')}
                  className="p-2 rounded-xl bg-[#F7F5F0] hover:bg-[#EFECE3] border border-[#E4E8E1] text-[11px] font-bold text-[#073B32] text-center"
                >
                  🚗 Maruti Swift '18
                </button>
                <button
                  type="button"
                  onClick={() => applyPreset('Toyota', 2016, 75000, 'Diesel', 'Manual', 'First Owner', 'Dealer')}
                  className="p-2 rounded-xl bg-[#F7F5F0] hover:bg-[#EFECE3] border border-[#E4E8E1] text-[11px] font-bold text-[#073B32] text-center"
                >
                  🚙 Toyota Fortuner '16
                </button>
                <button
                  type="button"
                  onClick={() => applyPreset('BMW', 2019, 22000, 'Diesel', 'Automatic', 'First Owner', 'Trustmark Dealer')}
                  className="p-2 rounded-xl bg-[#F7F5F0] hover:bg-[#EFECE3] border border-[#E4E8E1] text-[11px] font-bold text-[#073B32] text-center"
                >
                  🏎️ BMW 3 Series '19
                </button>
              </div>
            </div>

            {/* Actions */}
            <div className="flex items-center space-x-3 pt-3">
              <button
                type="submit"
                disabled={loading}
                className="flex-1 flex items-center justify-center space-x-2 py-3.5 rounded-xl bg-[#E6B85C] hover:bg-[#D4A446] text-[#073B32] font-extrabold text-xs tracking-wider transition-all shadow-md disabled:opacity-50"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>Calculating Fair Valuation...</span>
                  </>
                ) : (
                  <>
                    <Calculator className="w-4 h-4" />
                    <span>Generate Valuation Appraisal</span>
                  </>
                )}
              </button>

              <button
                type="button"
                onClick={handleReset}
                className="px-4 py-3.5 rounded-xl bg-[#F7F5F0] hover:bg-[#EFECE3] border border-[#E4E8E1] text-[#073B32] font-bold text-xs transition-colors"
                title="Reset Form"
              >
                <RotateCcw className="w-4 h-4" />
              </button>
            </div>
          </form>

          {error && (
            <div className="p-3.5 rounded-2xl bg-rose-50 border border-rose-200 text-rose-800 text-xs flex items-center space-x-2">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}
        </div>

        {/* Right Column: Estimated Price Result */}
        <div className="lg:col-span-5 space-y-4">
          {!result && !loading && (
            <div className="h-full min-h-[460px] bg-white rounded-3xl p-8 border border-dashed border-[#E4E8E1] flex flex-col items-center justify-center text-center">
              <div className="w-16 h-16 rounded-3xl bg-[#F7F5F0] flex items-center justify-center text-[#073B32] mb-4">
                <Car className="w-8 h-8 opacity-70" />
              </div>
              <h4 className="text-base font-extrabold text-[#073B32] font-display">
                Ready for Valuation Appraisal
              </h4>
              <p className="text-xs text-[#77827E] max-w-xs mt-1.5 leading-relaxed">
                Configure vehicle specifications on the left and click <b>"Generate Valuation Appraisal"</b> to compute predicted market value.
              </p>
              <div className="mt-6 flex flex-wrap justify-center gap-2 text-[11px] font-semibold text-[#77827E]">
                <span className="px-3 py-1 bg-[#F7F5F0] rounded-full border border-[#E4E8E1]">
                  Linear Regression Pipeline
                </span>
                <span className="px-3 py-1 bg-[#F7F5F0] rounded-full border border-[#E4E8E1]">
                  Non-Negative Guarantee
                </span>
              </div>
            </div>
          )}

          {result && (
            <div className="bg-[#073B32] text-white rounded-3xl p-6 lg:p-8 shadow-card space-y-6 border border-[#04241E] relative overflow-hidden">
              <div className="absolute -right-10 -bottom-10 w-48 h-48 rounded-full bg-[#E6B85C]/10 blur-2xl pointer-events-none"></div>

              {/* Price Hero */}
              <div className="border-b border-white/10 pb-5 text-center">
                <span className="text-[10px] uppercase font-bold tracking-widest text-[#E6B85C] block">
                  Fair Market Value Estimate
                </span>
                <div className="text-4xl font-extrabold tracking-tight text-[#E6B85C] font-display mt-1">
                  {result.formatted_price}
                </div>
                <div className="text-xs text-[#F7F5F0]/80 mt-1 font-mono">
                  Raw Estimate: ₹{result.predicted_price.toLocaleString()} INR
                </div>

                {/* Valuation Confidence Range */}
                <div className="mt-4 p-3 rounded-2xl bg-white/10 backdrop-blur-sm border border-white/10 text-xs">
                  <div className="text-[10px] uppercase text-[#E6B85C] font-bold">Estimated Market Band (± MAE)</div>
                  <div className="font-mono font-bold text-sm mt-0.5 text-white">
                    ₹{(result.lower_bound / 1e5).toFixed(2)}L – ₹{(result.upper_bound / 1e5).toFixed(2)}L
                  </div>
                </div>
              </div>

              {/* Spec Recap */}
              <div className="space-y-2 text-xs">
                <span className="text-[10px] uppercase font-bold text-[#E6B85C] tracking-wider block">
                  Evaluated Specifications
                </span>
                <div className="grid grid-cols-2 gap-2 text-[11px]">
                  <div className="p-2 rounded-xl bg-white/5 border border-white/10">
                    <span className="text-[#F7F5F0]/60 block text-[10px]">Make & Year</span>
                    <span className="font-bold text-white">{result.inputs.brand} ({result.inputs.year})</span>
                  </div>
                  <div className="p-2 rounded-xl bg-white/5 border border-white/10">
                    <span className="text-[#F7F5F0]/60 block text-[10px]">Odometer</span>
                    <span className="font-bold font-mono text-white">{result.inputs.km_driven.toLocaleString()} km</span>
                  </div>
                  <div className="p-2 rounded-xl bg-white/5 border border-white/10">
                    <span className="text-[#F7F5F0]/60 block text-[10px]">Fuel & Gearbox</span>
                    <span className="font-bold text-white">{result.inputs.fuel} • {result.inputs.transmission}</span>
                  </div>
                  <div className="p-2 rounded-xl bg-white/5 border border-white/10">
                    <span className="text-[#F7F5F0]/60 block text-[10px]">Title & Channel</span>
                    <span className="font-bold text-white">{result.inputs.owner}</span>
                  </div>
                </div>
              </div>

              <div className="pt-2 text-[11px] text-[#F7F5F0]/70 flex items-center justify-between font-mono">
                <span>Model: {result.model_used}</span>
                <span>{result.timestamp.split(' ')[1]}</span>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Section 8: Recent Predictions Session Table */}
      {history.length > 0 && (
        <div className="bg-white rounded-3xl p-6 border border-[#E4E8E1] shadow-soft space-y-4">
          <div className="flex justify-between items-center border-b border-[#E4E8E1] pb-3">
            <div>
              <h3 className="text-sm font-extrabold text-[#073B32] font-display flex items-center space-x-2">
                <History className="w-4 h-4 text-[#E6B85C]" />
                <span>Recent Session Appraisals</span>
              </h3>
              <p className="text-[11px] text-[#77827E]">
                Temporary session-level audit trail of valuations generated during this browser session.
              </p>
            </div>
            <button
              onClick={exportHistoryCSV}
              className="flex items-center space-x-1.5 px-3 py-1.5 rounded-xl bg-[#F7F5F0] hover:bg-[#EFECE3] border border-[#E4E8E1] text-xs font-bold text-[#073B32] transition-colors"
            >
              <Download className="w-3.5 h-3.5 text-[#E6B85C]" />
              <span>Export History CSV</span>
            </button>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs font-sans">
              <thead className="bg-[#F7F5F0] text-[#77827E] uppercase font-bold text-[10px] tracking-wider">
                <tr>
                  <th className="py-2.5 px-3 rounded-l-xl">ID</th>
                  <th className="py-2.5 px-3">Vehicle Details</th>
                  <th className="py-2.5 px-3">Mileage</th>
                  <th className="py-2.5 px-3">Fuel / Transmission</th>
                  <th className="py-2.5 px-3">Valuation (INR)</th>
                  <th className="py-2.5 px-3 rounded-r-xl">Timestamp</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#E4E8E1]">
                {history.map((h) => (
                  <tr key={h.id} className="hover:bg-[#F7F5F0]/50 transition-colors">
                    <td className="py-3 px-3 font-mono text-[#77827E] text-[11px]">
                      {h.id}
                    </td>
                    <td className="py-3 px-3 font-bold text-[#202A28]">
                      {h.inputs.brand} ({h.inputs.year})
                    </td>
                    <td className="py-3 px-3 font-mono text-[#77827E]">
                      {h.inputs.km_driven.toLocaleString()} km
                    </td>
                    <td className="py-3 px-3 text-[#202A28]">
                      {h.inputs.fuel} • {h.inputs.transmission}
                    </td>
                    <td className="py-3 px-3 font-bold text-[#073B32] font-mono text-sm">
                      {h.formatted_price}
                    </td>
                    <td className="py-3 px-3 text-[#77827E] font-mono text-[11px]">
                      {h.timestamp}
                    </td>
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
