import React, { useState, useEffect } from 'react';
import { 
  ShieldCheck, 
  ShieldAlert, 
  Inbox, 
  Percent, 
  BarChart3, 
  PieChart as PieIcon, 
  Activity, 
  Award,
  AlertTriangle
} from 'lucide-react';
import { 
  PieChart, 
  Pie, 
  Cell, 
  ResponsiveContainer, 
  Tooltip as RechartsTooltip,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Legend
} from 'recharts';
import { fetchBenchmarkMetrics, fetchDatasetSummary } from '../api/client';

export default function OverviewPage() {
  const [metrics, setMetrics] = useState(null);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [matrixSplit, setMatrixSplit] = useState('in_distribution'); // 'in_distribution' | 'independent'

  useEffect(() => {
    Promise.all([
      fetchBenchmarkMetrics().catch(() => null),
      fetchDatasetSummary().catch(() => null)
    ]).then(([m, s]) => {
      setMetrics(m);
      setSummary(s);
    }).finally(() => setLoading(false));
  }, []);

  const total = summary?.total_messages || 5572;
  const ham = summary?.ham_count || 4825;
  const spam = summary?.spam_count || 747;
  const spamPct = summary?.spam_percentage || 13.41;

  const distributionData = [
    { name: 'Ham (Legitimate)', value: ham, color: '#2E6B4F' },
    { name: 'Spam (Threats)', value: spam, color: '#A83F55' },
  ];

  // Model comparison bar data
  const comparisonData = [
    { model: 'Naive Bayes', Accuracy: 96.95, Precision: 99.15, Recall: 77.85, F1: 87.22 },
    { model: 'Logistic Regression', Accuracy: 96.68, Precision: 98.28, Recall: 76.51, F1: 86.04 },
    { model: 'BERT-Tiny', Accuracy: 98.57, Precision: 96.50, Recall: 92.62, F1: 94.52 },
  ];

  // Confusion matrix datasets
  const inDistCM = {
    title: 'UCI SMS Collection Test Split (N = 1,115)',
    tn: 961, fp: 5, fn: 11, tp: 138,
    acc: '98.57%', prec: '96.50%', rec: '92.62%'
  };

  const indepCM = {
    title: 'Task 5 Modern Independent Test (N = 1,000)',
    tn: 495, fp: 5, fn: 117, tp: 383,
    acc: '87.10%', prec: '98.71%', rec: '76.60%'
  };

  const activeCM = matrixSplit === 'in_distribution' ? inDistCM : indepCM;

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Page Header */}
      <div>
        <h2 className="text-2xl font-extrabold text-[#542B38] tracking-tight font-display">
          Executive Threat Intelligence Dashboard
        </h2>
        <p className="text-xs text-[#817A76] mt-0.5">
          Real-time SMS traffic classification, multi-model consensus metrics, and audited threat telemetry.
        </p>
      </div>

      {/* KPI Cards (4 Cards) */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Total Messages */}
        <div className="bg-[#FFFCF8] rounded-2xl p-5 border border-[#E4DAD0] shadow-soft card-hover">
          <div className="flex items-center justify-between">
            <span className="text-[10px] uppercase font-bold text-[#817A76] tracking-wider">
              Total Monitored
            </span>
            <div className="w-8 h-8 rounded-xl bg-[#F5F0E9] text-[#542B38] flex items-center justify-center">
              <Inbox className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-extrabold text-[#33302E] mt-2 font-display">
            {total.toLocaleString()}
          </div>
          <div className="text-[11px] text-[#817A76] mt-1 font-medium">
            100% Corpus Integrity
          </div>
        </div>

        {/* Ham Messages */}
        <div className="bg-[#FFFCF8] rounded-2xl p-5 border border-[#E4DAD0] shadow-soft card-hover">
          <div className="flex items-center justify-between">
            <span className="text-[10px] uppercase font-bold text-[#817A76] tracking-wider">
              Legitimate (Ham)
            </span>
            <div className="w-8 h-8 rounded-xl bg-[#EFF7F2] text-[#2E6B4F] flex items-center justify-center">
              <ShieldCheck className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-extrabold text-[#2E6B4F] mt-2 font-display">
            {ham.toLocaleString()}
          </div>
          <div className="text-[11px] text-[#2E6B4F] mt-1 font-medium">
            {(100 - spamPct).toFixed(2)}% Baseline Clearance
          </div>
        </div>

        {/* Spam Messages */}
        <div className="bg-[#FFFCF8] rounded-2xl p-5 border border-[#E4DAD0] shadow-soft card-hover">
          <div className="flex items-center justify-between">
            <span className="text-[10px] uppercase font-bold text-[#817A76] tracking-wider">
              Flagged Threats (Spam)
            </span>
            <div className="w-8 h-8 rounded-xl bg-[#FDF0F2] text-[#A83F55] flex items-center justify-center">
              <ShieldAlert className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-extrabold text-[#A83F55] mt-2 font-display">
            {spam.toLocaleString()}
          </div>
          <div className="text-[11px] text-[#A83F55] mt-1 font-medium">
            Quarantine & Threat Extraction
          </div>
        </div>

        {/* Spam Ratio */}
        <div className="bg-[#FFFCF8] rounded-2xl p-5 border border-[#E4DAD0] shadow-soft card-hover">
          <div className="flex items-center justify-between">
            <span className="text-[10px] uppercase font-bold text-[#817A76] tracking-wider">
              Spam Concentration
            </span>
            <div className="w-8 h-8 rounded-xl bg-[#F5F0E9] text-[#542B38] flex items-center justify-center">
              <Percent className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-extrabold text-[#542B38] mt-2 font-display">
            {spamPct}%
          </div>
          <div className="text-[11px] text-[#817A76] mt-1 font-medium">
            Balanced SMS Natural Prior
          </div>
        </div>
      </div>

      {/* Analytics Row: Donut Chart & Model Performance Comparison */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch">
        {/* Spam vs Ham Donut */}
        <div className="lg:col-span-5 bg-[#FFFCF8] rounded-3xl p-6 border border-[#E4DAD0] shadow-soft flex flex-col justify-between">
          <div className="border-b border-[#E4DAD0] pb-3">
            <h3 className="text-sm font-extrabold text-[#542B38] tracking-tight flex items-center space-x-2">
              <PieIcon className="w-4 h-4 text-[#A83F55]" />
              <span>Corpus Distribution (Spam vs. Ham)</span>
            </h3>
            <p className="text-[11px] text-[#817A76]">
              Canonical 5,572 SMS sample distribution from UCI dataset.
            </p>
          </div>

          <div className="h-56 relative my-2">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={distributionData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={85}
                  paddingAngle={4}
                  dataKey="value"
                >
                  {distributionData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <RechartsTooltip 
                  formatter={(val) => [`${val.toLocaleString()} msgs (${((val/total)*100).toFixed(1)}%)`, 'Count']}
                />
              </PieChart>
            </ResponsiveContainer>
            <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
              <span className="text-xl font-extrabold text-[#542B38] font-display">
                {total.toLocaleString()}
              </span>
              <span className="text-[10px] uppercase tracking-wider text-[#817A76] font-bold">
                Total Msgs
              </span>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3 pt-3 border-t border-[#E4DAD0] text-xs">
            <div className="flex items-center space-x-2">
              <span className="w-3 h-3 rounded-full bg-[#2E6B4F]"></span>
              <div>
                <div className="font-bold text-[#33302E]">Ham ({ham.toLocaleString()})</div>
                <div className="text-[10px] text-[#817A76]">86.59% Clearance</div>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <span className="w-3 h-3 rounded-full bg-[#A83F55]"></span>
              <div>
                <div className="font-bold text-[#33302E]">Spam ({spam.toLocaleString()})</div>
                <div className="text-[10px] text-[#817A76]">13.41% Quarantine</div>
              </div>
            </div>
          </div>
        </div>

        {/* Model Performance Comparison Bar Chart */}
        <div className="lg:col-span-7 bg-[#FFFCF8] rounded-3xl p-6 border border-[#E4DAD0] shadow-soft flex flex-col justify-between">
          <div className="border-b border-[#E4DAD0] pb-3 flex justify-between items-center">
            <div>
              <h3 className="text-sm font-extrabold text-[#542B38] tracking-tight flex items-center space-x-2">
                <BarChart3 className="w-4 h-4 text-[#A83F55]" />
                <span>Audited Model Evaluation (In-Distribution)</span>
              </h3>
              <p className="text-[11px] text-[#817A76]">
                Benchmark comparison across Accuracy, Precision, Recall, and F1.
              </p>
            </div>
            <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-[#D5BDA4]/30 text-[#542B38]">
              Stratified 80:20 Split
            </span>
          </div>

          <div className="h-64 my-2">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={comparisonData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E4DAD0" vertical={false} />
                <XAxis dataKey="model" tick={{ fill: '#817A76', fontSize: 11 }} />
                <YAxis domain={[70, 100]} tick={{ fill: '#817A76', fontSize: 11 }} />
                <RechartsTooltip 
                  formatter={(val) => [`${val}%`, '']}
                  contentStyle={{ backgroundColor: '#FFFCF8', borderColor: '#E4DAD0', borderRadius: '12px' }}
                />
                <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '8px' }} />
                <Bar dataKey="Accuracy" fill="#542B38" radius={[4, 4, 0, 0]} />
                <Bar dataKey="Precision" fill="#A83F55" radius={[4, 4, 0, 0]} />
                <Bar dataKey="Recall" fill="#D5BDA4" radius={[4, 4, 0, 0]} />
                <Bar dataKey="F1" fill="#A56F73" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="p-2.5 rounded-xl bg-[#F5F0E9] text-[11px] text-[#542B38] flex items-center justify-between font-medium">
            <span>Champion Classifier: <b>BERT-Tiny Transformer</b></span>
            <span className="font-mono font-bold text-[#A83F55]">98.57% Accuracy • 0.9452 F1</span>
          </div>
        </div>
      </div>

      {/* Confusion Matrix & Model Performance Summary Table */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* BERT-Tiny Confusion Matrix */}
        <div className="lg:col-span-5 bg-[#FFFCF8] rounded-3xl p-6 border border-[#E4DAD0] shadow-soft space-y-4">
          <div className="border-b border-[#E4DAD0] pb-3 flex justify-between items-center">
            <div>
              <h3 className="text-sm font-extrabold text-[#542B38] tracking-tight">
                BERT-Tiny Confusion Matrix Heatmap
              </h3>
              <p className="text-[11px] text-[#817A76]">
                Audited diagnostic error matrix.
              </p>
            </div>
            <div className="flex bg-[#F5F0E9] p-0.5 rounded-xl border border-[#E4DAD0]">
              <button
                onClick={() => setMatrixSplit('in_distribution')}
                className={`px-2 py-1 rounded-lg text-[10px] font-bold transition-colors ${
                  matrixSplit === 'in_distribution' ? 'bg-[#542B38] text-white' : 'text-[#817A76]'
                }`}
              >
                In-Dist (UCI)
              </button>
              <button
                onClick={() => setMatrixSplit('independent')}
                className={`px-2 py-1 rounded-lg text-[10px] font-bold transition-colors ${
                  matrixSplit === 'independent' ? 'bg-[#542B38] text-white' : 'text-[#817A76]'
                }`}
              >
                Task 5 (Modern)
              </button>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-center text-xs">
              <thead>
                <tr>
                  <th className="py-2 px-3 text-left text-[10px] font-bold text-[#817A76] uppercase">
                    Actual \ Predicted
                  </th>
                  <th className="py-2 px-3 text-[10px] font-bold text-[#2E6B4F] uppercase bg-[#EFF7F2]/60 rounded-t-lg">
                    Pred. Ham
                  </th>
                  <th className="py-2 px-3 text-[10px] font-bold text-[#A83F55] uppercase bg-[#FDF0F2]/60 rounded-t-lg">
                    Pred. Spam
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#E4DAD0]">
                <tr>
                  <td className="py-3 px-3 text-left font-bold text-[#33302E]">
                    Actual Ham
                  </td>
                  <td className="py-3 px-3 font-mono font-bold text-[#2E6B4F] bg-[#EFF7F2]/40 text-sm">
                    {activeCM.tn} <span className="text-[10px] font-normal block text-[#817A76]">True Negative</span>
                  </td>
                  <td className="py-3 px-3 font-mono font-bold text-[#A83F55] bg-[#FDF0F2]/40 text-sm">
                    {activeCM.fp} <span className="text-[10px] font-normal block text-[#817A76]">False Positive</span>
                  </td>
                </tr>
                <tr>
                  <td className="py-3 px-3 text-left font-bold text-[#33302E]">
                    Actual Spam
                  </td>
                  <td className="py-3 px-3 font-mono font-bold text-[#A83F55] bg-[#FDF0F2]/40 text-sm">
                    {activeCM.fn} <span className="text-[10px] font-normal block text-[#817A76]">False Negative</span>
                  </td>
                  <td className="py-3 px-3 font-mono font-bold text-[#2E6B4F] bg-[#EFF7F2]/40 text-sm">
                    {activeCM.tp} <span className="text-[10px] font-normal block text-[#817A76]">True Positive</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <div className="grid grid-cols-3 gap-2 pt-2 text-center text-xs">
            <div className="p-2 bg-[#F5F0E9] rounded-xl border border-[#E4DAD0]">
              <div className="text-[10px] text-[#817A76]">Accuracy</div>
              <div className="font-bold text-[#542B38] font-mono">{activeCM.acc}</div>
            </div>
            <div className="p-2 bg-[#F5F0E9] rounded-xl border border-[#E4DAD0]">
              <div className="text-[10px] text-[#817A76]">Precision</div>
              <div className="font-bold text-[#542B38] font-mono">{activeCM.prec}</div>
            </div>
            <div className="p-2 bg-[#F5F0E9] rounded-xl border border-[#E4DAD0]">
              <div className="text-[10px] text-[#817A76]">Recall</div>
              <div className="font-bold text-[#542B38] font-mono">{activeCM.rec}</div>
            </div>
          </div>
        </div>

        {/* Model Performance Summary Table */}
        <div className="lg:col-span-7 bg-[#FFFCF8] rounded-3xl p-6 border border-[#E4DAD0] shadow-soft space-y-4">
          <div className="border-b border-[#E4DAD0] pb-3">
            <h3 className="text-sm font-extrabold text-[#542B38] tracking-tight">
              Reported Model Performance Summary Table
            </h3>
            <p className="text-[11px] text-[#817A76]">
              Historical audited results from Task 4 & Task 5 research pipelines.
            </p>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-[#F5F0E9] text-[#817A76] uppercase font-bold text-[10px] tracking-wider">
                <tr>
                  <th className="py-2.5 px-3 rounded-l-xl">Model Architecture</th>
                  <th className="py-2.5 px-3">Accuracy</th>
                  <th className="py-2.5 px-3">Spam Prec.</th>
                  <th className="py-2.5 px-3">Spam Rec.</th>
                  <th className="py-2.5 px-3">Spam F1</th>
                  <th className="py-2.5 px-3 rounded-r-xl">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#E4DAD0]">
                <tr className="hover:bg-[#F5F0E9]/50 transition-colors">
                  <td className="py-3 px-3 font-bold text-[#33302E]">
                    Multinomial Naive Bayes
                  </td>
                  <td className="py-3 px-3 font-mono">96.95%</td>
                  <td className="py-3 px-3 font-mono font-bold text-[#2E6B4F]">99.15%</td>
                  <td className="py-3 px-3 font-mono text-[#817A76]">77.85%</td>
                  <td className="py-3 px-3 font-mono">0.8722</td>
                  <td className="py-3 px-3">
                    <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-[#EAE1D7] text-[#542B38]">
                      Baseline
                    </span>
                  </td>
                </tr>
                <tr className="hover:bg-[#F5F0E9]/50 transition-colors">
                  <td className="py-3 px-3 font-bold text-[#33302E]">
                    Logistic Regression
                  </td>
                  <td className="py-3 px-3 font-mono">96.68%</td>
                  <td className="py-3 px-3 font-mono font-bold text-[#2E6B4F]">98.28%</td>
                  <td className="py-3 px-3 font-mono text-[#817A76]">76.51%</td>
                  <td className="py-3 px-3 font-mono">0.8604</td>
                  <td className="py-3 px-3">
                    <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-[#EAE1D7] text-[#542B38]">
                      Calibrated
                    </span>
                  </td>
                </tr>
                <tr className="bg-[#EFF7F2]/40 font-semibold">
                  <td className="py-3 px-3 font-bold text-[#542B38] flex items-center space-x-1.5">
                    <Award className="w-3.5 h-3.5 text-[#A83F55]" />
                    <span>BERT-Tiny Transformer</span>
                  </td>
                  <td className="py-3 px-3 font-mono font-bold text-[#2E6B4F]">98.57%</td>
                  <td className="py-3 px-3 font-mono">96.50%</td>
                  <td className="py-3 px-3 font-mono font-bold text-[#2E6B4F]">92.62%</td>
                  <td className="py-3 px-3 font-mono font-bold text-[#542B38]">0.9452</td>
                  <td className="py-3 px-3">
                    <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-[#A83F55] text-white">
                      Champion
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <div className="p-3.5 rounded-2xl bg-[#F5F0E9] border border-[#E4DAD0] text-[11px] text-[#542B38] leading-relaxed">
            <b>Audited Finding:</b> Classical models exhibit high precision (&gt;98%) on in-distribution data, but BERT-Tiny offers superior recall (+15% higher) due to subword tokenization handling vocabulary variations.
          </div>
        </div>
      </div>
    </div>
  );
}
