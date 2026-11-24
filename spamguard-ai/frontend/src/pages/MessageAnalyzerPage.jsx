import React, { useState } from 'react';
import { 
  ScanSearch, 
  ShieldCheck, 
  ShieldAlert, 
  AlertCircle, 
  Sparkles, 
  Terminal, 
  Send,
  Loader2,
  Copy,
  Check
} from 'lucide-react';
import { analyzeMessage } from '../api/client';
import ModelScoreCard from '../components/common/ModelScoreCard';
import ThreatSignalsView from '../components/common/ThreatSignalsView';
import { DecisionBadge, RiskBadge } from '../components/common/Cards';

const sampleMessages = [
  {
    label: "🚨 Urgent Phish / Shortcode",
    text: "URGENT! Your mobile account is suspended due to billing error. To verify and prevent cancellation, reply YES to 86021 or call 08712400600 now."
  },
  {
    label: "🎁 Prize / Lottery Bait",
    text: "WINNER!! You have won a £1,000 cash prize or a free holiday! Text CLAIM to 87077 or call 09061701461 to collect your prize. Valid 24h."
  },
  {
    label: "💬 Legitimate Clean SMS",
    text: "Hey, are you still free for dinner tonight around 7:30? Let me know and I will book the table."
  },
  {
    label: "⚠️ Ambiguous Promo / Review Queue",
    text: "Your daily news subscription digest is ready. Review your preferences online or reply STOP to unsubscribe."
  }
];

export default function MessageAnalyzerPage() {
  const [inputText, setInputText] = useState('');
  const [modelPref, setModelPref] = useState('hybrid');
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [copied, setCopied] = useState(false);

  const handleAnalyze = async () => {
    if (!inputText.trim()) return;
    setAnalyzing(true);
    setError(null);
    try {
      const data = await analyzeMessage(inputText, modelPref, true);
      setResult(data);
    } catch (err) {
      setError(err.message || 'Inspection failed');
    } finally {
      setAnalyzing(false);
    }
  };

  const loadSample = (sample) => {
    setInputText(sample.text);
    setResult(null);
    setError(null);
  };

  const copyCleanTokens = () => {
    if (!result?.preprocessed_tokens) return;
    navigator.clipboard.writeText(result.preprocessed_tokens);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="border-b border-cyber-border pb-4">
        <h1 className="text-2xl font-bold font-mono text-white tracking-tight flex items-center gap-2">
          <ScanSearch className="w-6 h-6 text-cyber-accent" />
          Message Security Analyzer
        </h1>
        <p className="text-sm text-cyber-muted mt-1">
          Deep-packet NLP payload inspection, multi-model scoring, and audited hybrid triage routing.
        </p>
      </div>

      {/* Main 2-Column Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Input Panel */}
        <div className="lg:col-span-5 space-y-4">
          <div className="bg-cyber-card border border-cyber-border rounded-xl p-5 space-y-4">
            <div className="flex items-center justify-between">
              <label className="text-xs font-mono uppercase font-bold text-slate-300">
                Raw Message Payload
              </label>
              <div className="text-[11px] font-mono text-cyber-muted">
                {inputText.length} chars | {inputText.trim() ? inputText.trim().split(/\s+/).length : 0} words
              </div>
            </div>

            <textarea
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Paste raw SMS, email excerpt, or suspicious notification payload here..."
              rows={7}
              className="w-full bg-cyber-surface border border-cyber-border rounded-lg p-3 text-sm text-slate-100 placeholder:text-slate-500 font-mono focus:outline-none focus:border-cyber-accent focus:ring-1 focus:ring-cyber-accent transition-all resize-none"
            />

            {/* Model Selector & Action */}
            <div className="flex flex-col sm:flex-row items-center justify-between gap-3 pt-2 border-t border-cyber-border">
              <div className="w-full sm:w-auto">
                <select
                  value={modelPref}
                  onChange={(e) => setModelPref(e.target.value)}
                  className="w-full sm:w-auto bg-cyber-surface border border-cyber-border text-xs font-mono text-slate-200 rounded-lg px-3 py-2 focus:outline-none focus:border-cyber-cyan"
                >
                  <option value="hybrid">Ensemble: Hybrid Triage (Default)</option>
                  <option value="bert_tiny">Single: BERT-Tiny (Transformer)</option>
                  <option value="naive_bayes">Single: Multinomial Naive Bayes</option>
                  <option value="logistic_regression">Single: Logistic Regression</option>
                </select>
              </div>

              <button
                onClick={handleAnalyze}
                disabled={analyzing || !inputText.trim()}
                className="w-full sm:w-auto flex items-center justify-center gap-2 px-5 py-2 rounded-lg bg-cyber-accent text-slate-900 font-mono font-bold text-xs uppercase tracking-wider hover:bg-emerald-400 disabled:opacity-50 disabled:cursor-not-allowed transition-all glow-accent"
              >
                {analyzing ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>Analyzing...</span>
                  </>
                ) : (
                  <>
                    <Send className="w-4 h-4" />
                    <span>Scan Payload</span>
                  </>
                )}
              </button>
            </div>
          </div>

          {/* Preset Attack Samples */}
          <div className="bg-cyber-card border border-cyber-border rounded-xl p-5 space-y-3">
            <div className="flex items-center gap-1.5 text-xs font-mono font-semibold text-slate-300">
              <Sparkles className="w-4 h-4 text-cyber-accent" />
              <span>Load Realistic Forensic Test Payloads</span>
            </div>
            <div className="space-y-2">
              {sampleMessages.map((sample, idx) => (
                <button
                  key={idx}
                  onClick={() => loadSample(sample)}
                  className="w-full text-left p-2.5 rounded-lg bg-cyber-surface hover:bg-cyber-subtle border border-cyber-border text-xs transition-colors"
                >
                  <div className="font-semibold text-slate-200 font-mono text-[11px] mb-1">
                    {sample.label}
                  </div>
                  <p className="text-cyber-muted line-clamp-1 text-[11px] font-sans">
                    {sample.text}
                  </p>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Right Column: Analysis Results */}
        <div className="lg:col-span-7 space-y-4">
          {error && (
            <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs font-mono flex items-center gap-2">
              <AlertCircle className="w-4 h-4 shrink-0 text-cyber-danger" />
              <span>{error}</span>
            </div>
          )}

          {!result && !analyzing && (
            <div className="h-full min-h-[420px] bg-cyber-card border border-dashed border-cyber-border rounded-xl flex flex-col items-center justify-center p-8 text-center">
              <ScanSearch className="w-12 h-12 text-slate-600 mb-3" />
              <h3 className="text-base font-semibold font-mono text-slate-300">Awaiting Payload Submission</h3>
              <p className="text-xs text-cyber-muted max-w-sm mt-1">
                Enter text or select a forensic sample on the left. The engine will evaluate multi-model probabilities and structural threat heuristics.
              </p>
            </div>
          )}

          {analyzing && (
            <div className="h-full min-h-[420px] bg-cyber-card border border-cyber-border rounded-xl flex flex-col items-center justify-center p-8 text-center">
              <Loader2 className="w-10 h-10 animate-spin text-cyber-accent mb-3" />
              <h3 className="text-sm font-semibold font-mono text-slate-200">Executing NLP Inference Pipeline...</h3>
              <p className="text-xs text-cyber-muted mt-1 font-mono">
                Extracting regex patterns → Subword tokenization → Softmax calibrated scoring
              </p>
            </div>
          )}

          {result && (
            <div className="space-y-4">
              {/* Verdict Header Card */}
              <div className="bg-cyber-card border border-cyber-border rounded-xl p-5 space-y-4">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-cyber-border pb-3">
                  <div>
                    <span className="text-[11px] font-mono text-cyber-muted uppercase tracking-wider">
                      Hybrid Triage Verdict
                    </span>
                    <div className="flex items-center gap-2 mt-1">
                      <DecisionBadge decision={result.hybrid_decision} />
                      <RiskBadge level={result.risk_level} />
                    </div>
                  </div>
                  <div className="text-right sm:text-right">
                    <span className="text-[11px] font-mono text-cyber-muted uppercase tracking-wider">
                      Composite Risk Score
                    </span>
                    <div className="text-2xl font-bold font-mono text-white">
                      {(result.risk_score * 100).toFixed(1)}%
                    </div>
                  </div>
                </div>

                {/* Explanation */}
                <div className="p-3 rounded-lg bg-cyber-surface border border-cyber-border text-xs text-slate-300 font-sans">
                  <span className="font-mono font-bold text-cyber-accent mr-1">Security Directive:</span>
                  {result.explanation}
                </div>
              </div>

              {/* Multi-Model Breakdown Grid */}
              <div className="space-y-2">
                <div className="text-xs font-mono font-semibold text-slate-300 uppercase tracking-wider">
                  Model Ensemble Comparison
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                  {Object.entries(result.model_predictions).map(([key, score]) => (
                    <ModelScoreCard key={key} modelKey={key} scoreData={score} />
                  ))}
                </div>
              </div>

              {/* Structural Threat Signals */}
              <div className="space-y-2">
                <div className="text-xs font-mono font-semibold text-slate-300 uppercase tracking-wider">
                  Extracted Threat Heuristics ({result.threat_signals.length})
                </div>
                <ThreatSignalsView signals={result.threat_signals} />
              </div>

              {/* Preprocessed Tokens View */}
              <div className="bg-cyber-card border border-cyber-border rounded-xl p-4 space-y-2">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-1.5 text-xs font-mono text-slate-300">
                    <Terminal className="w-3.5 h-3.5 text-cyber-cyan" />
                    <span>Normalized Token Stream (Task 4 Pipeline)</span>
                  </div>
                  <button
                    onClick={copyCleanTokens}
                    className="flex items-center gap-1 text-[11px] font-mono text-cyber-muted hover:text-slate-200 transition-colors"
                  >
                    {copied ? <Check className="w-3 h-3 text-cyber-accent" /> : <Copy className="w-3 h-3" />}
                    <span>{copied ? 'Copied' : 'Copy'}</span>
                  </button>
                </div>
                <div className="p-2.5 rounded bg-black/40 font-mono text-xs text-emerald-400 break-words border border-cyber-border">
                  {result.preprocessed_tokens || '(no residual tokens after stopword/symbol stripping)'}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
