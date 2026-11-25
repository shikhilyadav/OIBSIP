import React from 'react';
import { 
  Cpu, 
  Award, 
  Layers, 
  Activity, 
  ShieldCheck, 
  Zap, 
  CheckCircle2,
  Sparkles,
  GitBranch
} from 'lucide-react';

export default function ModelIntelligencePage() {
  const models = [
    {
      id: 'naive_bayes',
      name: 'Multinomial Naive Bayes',
      arch: 'TF-IDF Vectorizer + Multinomial Naive Bayes',
      tag: 'Lexical Baseline',
      accuracy: '96.95%',
      precision: '99.15%',
      recall: '77.85%',
      f1: '0.8722',
      latency: '~0.8 ms',
      vocab: '8,713 n-grams',
      params: 'Classical Parameterless',
      desc: 'High precision on standard keyword spam (e.g., "FREE", "WINNER"). However, it experiences extreme recall degradation on modern phrasing variations due to strict token matching.',
      strengths: ['Sub-millisecond latency', 'Ultra-high precision (99.15%)', 'No GPU requirement'],
      weaknesses: ['Vulnerable to vocabulary drift', 'Misses 22.15% in-dist spam']
    },
    {
      id: 'logistic_regression',
      name: 'Logistic Regression',
      arch: 'TF-IDF + L2 Regularized Sigmoid',
      tag: 'Calibrated Classifier',
      accuracy: '96.68%',
      precision: '98.28%',
      recall: '76.51%',
      f1: '0.8604',
      latency: '~0.6 ms',
      vocab: '8,713 n-grams',
      params: '8,713 Coeffs',
      desc: 'Provides smooth, calibrated probability scores. Well-suited for probability ranking and score calibration, though constrained by bag-of-words independence assumptions.',
      strengths: ['Calibrated class probabilities', 'Fast linear inference', 'Interpretable coefficients'],
      weaknesses: ['Ignores word order & syntax', 'Misses 23.49% in-dist spam']
    },
    {
      id: 'bert_tiny',
      name: 'BERT-Tiny Transformer',
      arch: '2-Layer Distilled Transformer (mrm8488)',
      tag: 'Neural Champion',
      accuracy: '98.57%',
      precision: '96.50%',
      recall: '92.62%',
      f1: '0.9452',
      latency: '~2.8 ms',
      vocab: '30,522 WordPiece',
      params: '4.39M Parameters',
      desc: 'Pre-trained bidirectional self-attention network fine-tuned for SMS spam detection. Leverages WordPiece subword tokenization to capture semantic context and resist spelling obfuscations.',
      strengths: ['Contextual self-attention', 'High recall (92.62%)', 'Subword resilience'],
      weaknesses: ['Higher latency than classical', 'Conservative on OOD custom templates']
    }
  ];

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-extrabold text-[#542B38] tracking-tight font-display">
          Model Intelligence & Architectural Registry
        </h2>
        <p className="text-xs text-[#817A76] mt-0.5">
          Comprehensive forensic review of trained classical classifiers, deep transformer networks, and hybrid triage policies.
        </p>
      </div>

      {/* 3 Model Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {models.map((m) => {
          const isChampion = m.id === 'bert_tiny';
          return (
            <div
              key={m.id}
              className={`bg-[#FFFCF8] rounded-3xl p-6 border shadow-soft flex flex-col justify-between transition-all ${
                isChampion ? 'border-[#A83F55] ring-2 ring-[#A83F55]/10' : 'border-[#E4DAD0]'
              }`}
            >
              <div className="space-y-4">
                {/* Header Badge */}
                <div className="flex justify-between items-start">
                  <div>
                    <span className="text-[10px] uppercase font-bold text-[#A83F55] tracking-widest block">
                      {m.tag}
                    </span>
                    <h3 className="text-lg font-extrabold text-[#542B38] font-display mt-0.5">
                      {m.name}
                    </h3>
                  </div>
                  <div className={`w-9 h-9 rounded-xl flex items-center justify-center shrink-0 ${
                    isChampion ? 'bg-[#FDF0F2] text-[#A83F55]' : 'bg-[#F5F0E9] text-[#542B38]'
                  }`}>
                    {isChampion ? <Award className="w-5 h-5" /> : <Cpu className="w-5 h-5" />}
                  </div>
                </div>

                <p className="text-xs text-[#817A76] leading-relaxed">
                  {m.desc}
                </p>

                {/* Metrics Grid */}
                <div className="grid grid-cols-2 gap-2 p-3.5 rounded-2xl bg-[#F5F0E9] border border-[#E4DAD0] text-xs">
                  <div>
                    <span className="text-[10px] text-[#817A76]">Accuracy</span>
                    <div className="font-bold text-[#33302E] font-mono text-sm">{m.accuracy}</div>
                  </div>
                  <div>
                    <span className="text-[10px] text-[#817A76]">Spam Precision</span>
                    <div className="font-bold text-[#2E6B4F] font-mono text-sm">{m.precision}</div>
                  </div>
                  <div>
                    <span className="text-[10px] text-[#817A76]">Spam Recall</span>
                    <div className="font-bold text-[#542B38] font-mono text-sm">{m.recall}</div>
                  </div>
                  <div>
                    <span className="text-[10px] text-[#817A76]">Spam F1-Score</span>
                    <div className="font-bold text-[#A83F55] font-mono text-sm">{m.f1}</div>
                  </div>
                </div>

                {/* Specs */}
                <div className="space-y-1.5 text-[11px] text-[#817A76]">
                  <div className="flex justify-between">
                    <span>Architecture:</span>
                    <span className="font-mono text-[#33302E] font-medium truncate max-w-[150px]">{m.arch.split('+')[0]}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Inference Latency:</span>
                    <span className="font-mono font-bold text-[#542B38]">{m.latency}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Vocabulary / Params:</span>
                    <span className="font-mono text-[#33302E]">{m.params}</span>
                  </div>
                </div>
              </div>

              {/* Strengths / Weaknesses */}
              <div className="pt-4 border-t border-[#E4DAD0] mt-4 space-y-2 text-[11px]">
                <div>
                  <span className="font-bold text-[#2E6B4F] block mb-0.5">Primary Advantages</span>
                  <div className="space-y-0.5 text-[#817A76]">
                    {m.strengths.map((s, i) => (
                      <div key={i} className="flex items-center space-x-1.5">
                        <CheckCircle2 className="w-3 h-3 text-[#2E6B4F] shrink-0" />
                        <span>{s}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Hybrid Triage Specification Banner */}
      <div className="bg-[#FFFCF8] rounded-3xl p-6 lg:p-8 border border-[#E4DAD0] shadow-soft space-y-4">
        <div className="flex items-center space-x-3 border-b border-[#E4DAD0] pb-4">
          <div className="w-10 h-10 rounded-2xl bg-[#542B38] text-white flex items-center justify-center">
            <GitBranch className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-base font-extrabold text-[#542B38] font-display">
              Calibrated Hybrid Triage Engine (Dual-Threshold Abstention)
            </h3>
            <p className="text-xs text-[#817A76]">
              Combines BERT-Tiny semantic embeddings with classical consensus to eliminate false positives.
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-1">
          <div className="p-4 rounded-2xl bg-[#FDF0F2] border border-[#F5D5DC] space-y-1">
            <div className="text-[10px] uppercase font-bold text-[#A83F55] tracking-wider">
              Automated Quarantine
            </div>
            <div className="text-base font-extrabold text-[#A83F55] font-display">
              p_spam ≥ 0.60
            </div>
            <p className="text-[11px] text-[#817A76] leading-relaxed">
              High-confidence spam payload blocked and archived immediately.
            </p>
          </div>

          <div className="p-4 rounded-2xl bg-[#FEF8EE] border border-[#F6E6CE] space-y-1">
            <div className="text-[10px] uppercase font-bold text-[#B87B2E] tracking-wider">
              Human SecOps Review
            </div>
            <div className="text-base font-extrabold text-[#B87B2E] font-display">
              0.10 &lt; p_spam &lt; 0.60
            </div>
            <p className="text-[11px] text-[#817A76] leading-relaxed">
              Abstention band (19.1% of modern OOD traffic, capturing 70.68% spam).
            </p>
          </div>

          <div className="p-4 rounded-2xl bg-[#EFF7F2] border border-[#D1E8DA] space-y-1">
            <div className="text-[10px] uppercase font-bold text-[#2E6B4F] tracking-wider">
              Automated Clearance
            </div>
            <div className="text-base font-extrabold text-[#2E6B4F] font-display">
              p_spam ≤ 0.10
            </div>
            <p className="text-[11px] text-[#817A76] leading-relaxed">
              Guaranteed legitimate communication routed with zero latency.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
