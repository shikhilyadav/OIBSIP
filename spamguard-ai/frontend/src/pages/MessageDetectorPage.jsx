import React, { useState } from 'react';
import { 
  ScanSearch, 
  Send, 
  RotateCcw, 
  Loader2, 
  ShieldCheck, 
  ShieldAlert, 
  AlertCircle, 
  AlertTriangle,
  Clock, 
  Hash, 
  CheckCircle2, 
  Sparkles,
  Info
} from 'lucide-react';
import { analyzeMessage } from '../api/client';

const SAMPLES = {
  normal: "Hey mate, are we still meeting up for dinner tonight at the downtown bistro around 7:30pm?",
  offer: "URGENT! Your mobile number has won a £2,000 cash reward. Call 09061701461 now to claim your prize. 150p/min 18+ only.",
  prize: "WINNER! As a valued customer, you have been selected for a free £1,000 Tesco gift voucher. Text CLAIM to 87070 immediately."
};

const MODELS = [
  { id: 'hybrid', name: 'SpamShield Hybrid Triage (Recommended)', tag: 'Ensemble + Abstention' },
  { id: 'bert_tiny', name: 'BERT-Tiny Transformer', tag: '4.39M Subword Attention' },
  { id: 'naive_bayes', name: 'Multinomial Naive Bayes', tag: 'TF-IDF Lexical Classifier' },
  { id: 'logistic_regression', name: 'Logistic Regression', tag: 'L2 Calibrated Sigmoid' },
];

export default function MessageDetectorPage() {
  const [message, setMessage] = useState('');
  const [selectedModel, setSelectedModel] = useState('hybrid');
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);

  const handleAnalyze = async () => {
    if (!message.trim()) {
      setError('Please enter or select a message to analyze.');
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const data = await analyzeMessage(message.trim(), selectedModel);
      setResponse(data);
    } catch (err) {
      setError(err.message || 'Analysis service unreachable. Ensure FastAPI backend is running on port 8000.');
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setMessage('');
    setResponse(null);
    setError(null);
  };

  const applySample = (text) => {
    setMessage(text);
    // Crucial rule: do not show prediction until user clicks Analyze Message!
    setResponse(null);
    setError(null);
  };

  // Derive active model prediction details from response
  let activeScore = null;
  let isSpam = false;
  let confidenceVal = 0;
  let latencyMs = 0;

  if (response) {
    if (selectedModel === 'naive_bayes') {
      activeScore = response.model_predictions.naive_bayes;
      isSpam = activeScore.predicted_label === 'SPAM';
      confidenceVal = isSpam ? activeScore.spam_probability : activeScore.ham_confidence;
      latencyMs = activeScore.latency_ms;
    } else if (selectedModel === 'logistic_regression') {
      activeScore = response.model_predictions.logistic_regression;
      isSpam = activeScore.predicted_label === 'SPAM';
      confidenceVal = isSpam ? activeScore.spam_probability : activeScore.ham_confidence;
      latencyMs = activeScore.latency_ms;
    } else if (selectedModel === 'bert_tiny') {
      activeScore = response.model_predictions.bert_tiny;
      isSpam = activeScore.predicted_label === 'SPAM';
      confidenceVal = isSpam ? activeScore.spam_probability : activeScore.ham_confidence;
      latencyMs = activeScore.latency_ms;
    } else {
      // Hybrid
      isSpam = response.hybrid_decision === 'SPAM';
      confidenceVal = isSpam ? response.risk_score : (1.0 - response.risk_score);
      latencyMs = response.model_predictions.naive_bayes.latency_ms + 
                  response.model_predictions.logistic_regression.latency_ms + 
                  response.model_predictions.bert_tiny.latency_ms;
    }
  }

  const charCount = message.length;
  const wordCount = message.trim() ? message.trim().split(/\s+/).length : 0;

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Page Header */}
      <div>
        <h2 className="text-2xl font-extrabold text-[#542B38] tracking-tight font-display">
          Deep Message Inspection & Threat Detection
        </h2>
        <p className="text-xs text-[#817A76] mt-0.5">
          Evaluate SMS and messaging payloads against classical lexical models, distilled BERT transformers, or calibrated hybrid triage.
        </p>
      </div>

      {/* Main Two-Column Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Left Panel: Enter Message */}
        <div className="lg:col-span-6 bg-[#FFFCF8] rounded-3xl p-6 lg:p-8 border border-[#E4DAD0] shadow-soft space-y-5">
          <div className="border-b border-[#E4DAD0] pb-3 flex justify-between items-center">
            <div>
              <h3 className="text-base font-extrabold text-[#542B38] tracking-tight font-display">
                Enter Message Payload
              </h3>
              <p className="text-[11px] text-[#817A76]">
                Paste raw SMS text or select forensic test payloads.
              </p>
            </div>
            <div className="w-8 h-8 rounded-xl bg-[#F5F0E9] text-[#542B38] flex items-center justify-center">
              <ScanSearch className="w-4 h-4" />
            </div>
          </div>

          {/* Model Selection Dropdown */}
          <div>
            <label className="text-[11px] uppercase font-bold text-[#817A76] tracking-wider block mb-1.5">
              Select Inference Model Architecture
            </label>
            <select
              value={selectedModel}
              onChange={(e) => setSelectedModel(e.target.value)}
              className="w-full bg-[#F5F0E9] border border-[#E4DAD0] rounded-xl px-3.5 py-2.5 text-xs text-[#33302E] font-medium focus:outline-none focus:border-[#A83F55] transition-colors cursor-pointer"
            >
              {MODELS.map((m) => (
                <option key={m.id} value={m.id}>
                  {m.name} ({m.tag})
                </option>
              ))}
            </select>
          </div>

          {/* BERT-Tiny Limitation Alert */}
          {selectedModel === 'bert_tiny' && (
            <div className="p-3.5 rounded-2xl bg-amber-50 border border-amber-200 text-amber-900 text-xs flex items-start space-x-2.5">
              <AlertTriangle className="w-4 h-4 text-amber-700 shrink-0 mt-0.5" />
              <div className="space-y-0.5">
                <span className="font-bold">Audited BERT-Tiny Validation Note:</span>
                <p className="text-[11px] text-amber-800 leading-relaxed">
                  In independent validation trials, custom synthetic test templates without explicit historical spam keywords were classified as HAM. This architectural characteristic is preserved accurately.
                </p>
              </div>
            </div>
          )}

          {/* Textarea */}
          <div className="space-y-1.5">
            <div className="flex justify-between items-center text-[11px] text-[#817A76]">
              <span className="font-semibold">SMS Message Body</span>
              <span className="font-mono">
                {charCount} chars • {wordCount} words
              </span>
            </div>
            <textarea
              rows={6}
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Type or paste SMS payload here for deep packet inspection..."
              className="w-full bg-[#F5F0E9] border border-[#E4DAD0] rounded-2xl p-4 text-xs text-[#33302E] placeholder-[#817A76] focus:outline-none focus:border-[#A83F55] focus:bg-white transition-all resize-none font-sans leading-relaxed"
            />
          </div>

          {/* Forensic Sample Buttons */}
          <div className="space-y-2">
            <span className="text-[10px] uppercase font-bold text-[#817A76] tracking-wider block">
              Forensic Test Samples (Click to Populate)
            </span>
            <div className="grid grid-cols-3 gap-2">
              <button
                type="button"
                onClick={() => applySample(SAMPLES.normal)}
                className="px-2.5 py-2 rounded-xl bg-[#F5F0E9] hover:bg-[#EFF7F2] border border-[#E4DAD0] hover:border-[#D1E8DA] text-xs font-semibold text-[#2E6B4F] transition-all text-center truncate"
              >
                Normal SMS
              </button>
              <button
                type="button"
                onClick={() => applySample(SAMPLES.offer)}
                className="px-2.5 py-2 rounded-xl bg-[#F5F0E9] hover:bg-[#FDF0F2] border border-[#E4DAD0] hover:border-[#F5D5DC] text-xs font-semibold text-[#A83F55] transition-all text-center truncate"
              >
                Spam Offer
              </button>
              <button
                type="button"
                onClick={() => applySample(SAMPLES.prize)}
                className="px-2.5 py-2 rounded-xl bg-[#F5F0E9] hover:bg-[#FDF0F2] border border-[#E4DAD0] hover:border-[#F5D5DC] text-xs font-semibold text-[#A83F55] transition-all text-center truncate"
              >
                Prize SMS
              </button>
            </div>
          </div>

          {/* Actions */}
          <div className="flex items-center space-x-3 pt-2">
            <button
              onClick={handleAnalyze}
              disabled={loading || !message.trim()}
              className="flex-1 flex items-center justify-center space-x-2 py-3.5 rounded-xl bg-[#A83F55] hover:bg-[#8E3346] text-white font-bold text-xs tracking-wide transition-all shadow-md disabled:opacity-50"
            >
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Running Inference Engine...</span>
                </>
              ) : (
                <>
                  <Send className="w-4 h-4" />
                  <span>Analyze Message</span>
                </>
              )}
            </button>

            <button
              onClick={handleClear}
              type="button"
              className="px-4 py-3.5 rounded-xl bg-[#F5F0E9] hover:bg-[#EAE1D7] border border-[#E4DAD0] text-[#542B38] font-bold text-xs transition-colors"
              title="Clear text"
            >
              <RotateCcw className="w-4 h-4" />
            </button>
          </div>

          {error && (
            <div className="p-3.5 rounded-2xl bg-rose-50 border border-rose-200 text-rose-800 text-xs flex items-center space-x-2">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}
        </div>

        {/* Right Panel: Prediction Results */}
        <div className="lg:col-span-6 space-y-4">
          {!response && !loading && (
            <div className="h-full min-h-[460px] bg-[#FFFCF8] rounded-3xl p-8 border border-dashed border-[#E4DAD0] flex flex-col items-center justify-center text-center">
              <div className="w-16 h-16 rounded-3xl bg-[#F5F0E9] flex items-center justify-center text-[#542B38] mb-4">
                <ScanSearch className="w-8 h-8 opacity-70" />
              </div>
              <h4 className="text-base font-extrabold text-[#542B38] font-display">
                Ready for Security Analysis
              </h4>
              <p className="text-xs text-[#817A76] max-w-sm mt-1.5 leading-relaxed">
                Enter an SMS message or click a test sample on the left, then click <b>"Analyze Message"</b> to query the selected classifier.
              </p>
              <div className="mt-6 flex flex-wrap justify-center gap-2 text-[11px] font-semibold text-[#817A76]">
                <span className="px-3 py-1 bg-[#F5F0E9] rounded-full border border-[#E4DAD0]">
                  Multi-Model Scoring
                </span>
                <span className="px-3 py-1 bg-[#F5F0E9] rounded-full border border-[#E4DAD0]">
                  Heuristic Threat Detection
                </span>
                <span className="px-3 py-1 bg-[#F5F0E9] rounded-full border border-[#E4DAD0]">
                  Sub-5ms CPU Latency
                </span>
              </div>
            </div>
          )}

          {response && (
            <div className="bg-[#FFFCF8] rounded-3xl p-6 lg:p-8 border border-[#E4DAD0] shadow-soft space-y-5">
              {/* Prediction Result Badge */}
              <div
                className={`p-6 rounded-2xl text-center border relative overflow-hidden transition-all ${
                  isSpam
                    ? 'bg-[#FDF0F2] border-[#F5D5DC] text-[#A83F55]'
                    : 'bg-[#EFF7F2] border-[#D1E8DA] text-[#2E6B4F]'
                }`}
              >
                <div className="text-4xl mb-2">
                  {isSpam ? '🚨' : '🛡️'}
                </div>
                <span className="text-[10px] uppercase tracking-widest font-extrabold block">
                  Classification Outcome
                </span>
                <h3 className="text-3xl font-extrabold tracking-tight mt-0.5 mb-1 font-display">
                  {isSpam ? 'SPAM DETECTED' : 'LEGITIMATE (HAM)'}
                </h3>
                <div className="text-xs font-bold text-[#33302E] mt-2 inline-flex items-center space-x-2 bg-white/80 px-3.5 py-1.5 rounded-full border border-white/60">
                  <span>Confidence Score:</span>
                  <span className="font-mono text-sm font-extrabold">
                    {(confidenceVal * 100).toFixed(2)}%
                  </span>
                </div>

                {response.requires_review && (
                  <div className="mt-3 p-2 rounded-xl bg-amber-50 border border-amber-200 text-amber-900 text-xs font-semibold">
                    ⚠️ Hybrid Abstention Triggered: Routed to Human SecOps Review Queue.
                  </div>
                )}
              </div>

              {/* Class Probability Distribution */}
              <div className="space-y-3">
                <div className="flex justify-between items-center text-xs">
                  <span className="font-extrabold text-[#542B38] uppercase tracking-wider text-[11px]">
                    Class Probability Distribution
                  </span>
                  <span className="font-mono text-[10px] text-[#817A76]">
                    Model Vote
                  </span>
                </div>

                {/* Spam probability bar */}
                <div className="space-y-1">
                  <div className="flex justify-between text-xs font-semibold">
                    <span className="text-[#A83F55] font-bold">Spam Probability</span>
                    <span className="font-mono font-bold text-[#A83F55]">
                      {isSpam ? (confidenceVal * 100).toFixed(1) : ((1 - confidenceVal) * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="w-full bg-[#F5F0E9] h-2.5 rounded-full overflow-hidden border border-[#E4DAD0]">
                    <div
                      className="h-full rounded-full bg-[#A83F55] transition-all duration-500"
                      style={{
                        width: `${isSpam ? (confidenceVal * 100) : ((1 - confidenceVal) * 100)}%`
                      }}
                    />
                  </div>
                </div>

                {/* Ham probability bar */}
                <div className="space-y-1">
                  <div className="flex justify-between text-xs font-semibold">
                    <span className="text-[#2E6B4F] font-bold">Ham Probability</span>
                    <span className="font-mono font-bold text-[#2E6B4F]">
                      {!isSpam ? (confidenceVal * 100).toFixed(1) : ((1 - confidenceVal) * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="w-full bg-[#F5F0E9] h-2.5 rounded-full overflow-hidden border border-[#E4DAD0]">
                    <div
                      className="h-full rounded-full bg-[#2E6B4F] transition-all duration-500"
                      style={{
                        width: `${!isSpam ? (confidenceVal * 100) : ((1 - confidenceVal) * 100)}%`
                      }}
                    />
                  </div>
                </div>
              </div>

              {/* Metadata Telemetry Recap */}
              <div className="grid grid-cols-3 gap-2 text-center text-xs pt-1">
                <div className="p-2.5 bg-[#F5F0E9] rounded-xl border border-[#E4DAD0]">
                  <div className="text-[10px] text-[#817A76]">Active Model</div>
                  <div className="font-bold text-[#542B38] text-[11px] truncate">
                    {MODELS.find(m => m.id === selectedModel)?.name.split(' ')[0] || 'Hybrid'}
                  </div>
                </div>
                <div className="p-2.5 bg-[#F5F0E9] rounded-xl border border-[#E4DAD0]">
                  <div className="text-[10px] text-[#817A76]">Inference Latency</div>
                  <div className="font-bold text-[#33302E] font-mono text-[11px]">
                    {latencyMs.toFixed(2)} ms
                  </div>
                </div>
                <div className="p-2.5 bg-[#F5F0E9] rounded-xl border border-[#E4DAD0]">
                  <div className="text-[10px] text-[#817A76]">Message Length</div>
                  <div className="font-bold text-[#33302E] font-mono text-[11px]">
                    {response.char_count} chars
                  </div>
                </div>
              </div>

              {/* Heuristic Threat Signals (Rule-Based Analysis) */}
              <div className="pt-2 border-t border-[#E4DAD0] space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-[11px] uppercase font-bold text-[#542B38] tracking-wider">
                    Rule-Based Threat Extraction
                  </span>
                  <span className="text-[10px] text-[#817A76] italic">
                    Regex & Pattern Matching
                  </span>
                </div>

                {response.threat_signals && response.threat_signals.length > 0 ? (
                  <div className="space-y-1.5">
                    {response.threat_signals.map((sig, idx) => (
                      <div
                        key={idx}
                        className="p-2.5 rounded-xl bg-[#FDF0F2] border border-[#F5D5DC] text-xs flex items-start space-x-2"
                      >
                        <ShieldAlert className="w-4 h-4 text-[#A83F55] shrink-0 mt-0.5" />
                        <div>
                          <span className="font-bold text-[#A83F55]">{sig.indicator}: </span>
                          <span className="text-[#33302E]">{sig.description}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="p-2.5 rounded-xl bg-[#EFF7F2] border border-[#D1E8DA] text-xs text-[#2E6B4F] flex items-center space-x-2">
                    <CheckCircle2 className="w-4 h-4 shrink-0" />
                    <span>No structural threat signals (toll dialing, urgency traps, obfuscated URLs) detected.</span>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
