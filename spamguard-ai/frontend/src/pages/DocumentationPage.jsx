import React from 'react';
import { 
  BookOpen, 
  Terminal, 
  Cpu, 
  ShieldCheck, 
  Layers, 
  ExternalLink,
  Code2
} from 'lucide-react';

export default function DocumentationPage() {
  const endpoints = [
    { method: 'POST', path: '/api/analyze', desc: 'Runs live single-message deep packet inspection through all 3 models + Hybrid Engine.' },
    { method: 'POST', path: '/api/analyze/batch', desc: 'Processes batch message lists (up to 200 items) and returns itemized predictions and counts.' },
    { method: 'GET', path: '/api/dataset/summary', desc: 'Returns descriptive statistical moments of the authentic 5,572-message UCI dataset.' },
    { method: 'GET', path: '/api/dataset/records', desc: 'Paginated, filterable, and searchable access to original dataset records.' },
    { method: 'GET', path: '/api/models', desc: 'Returns metadata, architecture details, and availability status for all inference engines.' },
    { method: 'GET', path: '/api/metrics/benchmark', desc: 'Returns authentic Task 4 and Task 5 audited evaluation metrics and confusion matrices.' },
    { method: 'GET', path: '/api/health', desc: 'Reports system operational status and loaded model states.' },
  ];

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-extrabold text-[#542B38] tracking-tight font-display">
          System Architecture & Technical Documentation
        </h2>
        <p className="text-xs text-[#817A76] mt-0.5">
          Engineering specifications, mathematical triage formulations, REST API contracts, and research citations.
        </p>
      </div>

      {/* System Flow Card */}
      <div className="bg-[#FFFCF8] rounded-3xl p-6 lg:p-8 border border-[#E4DAD0] shadow-soft space-y-4">
        <div className="border-b border-[#E4DAD0] pb-3">
          <h3 className="text-base font-extrabold text-[#542B38] font-display">
            Inference Pipeline Architecture
          </h3>
          <p className="text-xs text-[#817A76]">
            Parallel lexical and transformer analysis with human-in-the-loop triage routing.
          </p>
        </div>

        <div className="p-4 bg-[#F5F0E9] rounded-2xl border border-[#E4DAD0] font-mono text-[11px] text-[#33302E] overflow-x-auto leading-relaxed">
{`Incoming SMS Message
       │
       ├──► Structural Threat Engine (Regex heuristics: dial codes, urgency, prize lures)
       │
       ├──► Multinomial Naive Bayes (TF-IDF 8,713 n-grams, sub-millisecond lexical scoring)
       ├──► Logistic Regression (L2 regularized calibrated posterior probabilities)
       └──► BERT-Tiny Transformer (2-Layer Distilled self-attention, 30,522 WordPiece tokens)
       │
       ▼
Calibrated Hybrid Triage Engine (Dual-Threshold Abstention Policy)
       │
       ├─► [ p_spam ≥ 0.60 ] ────► Automated SPAM Quarantine (Selective Acc: 96.66%)
       ├─► [ 0.10 < p < 0.60 ] ──► Human SecOps Review Queue (Captures 70.68% spam)
       └─► [ p_spam ≤ 0.10 ] ────► Automated HAM Clearance (Zero latency)`}
        </div>
      </div>

      {/* Triage Policy Formulation */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-[#FFFCF8] rounded-3xl p-6 border border-[#E4DAD0] shadow-soft space-y-3">
          <h4 className="text-sm font-extrabold text-[#542B38] font-display">
            Dual-Threshold Abstention Formula
          </h4>
          <p className="text-xs text-[#817A76] leading-relaxed">
            Standard classifiers enforce a binary cut-off at 0.50. Under distribution shift, spammers alter vocabulary, causing high false negative rates. SpamShield AI implements cost-sensitive abstention:
          </p>
          <div className="p-3 bg-[#F5F0E9] rounded-xl border border-[#E4DAD0] font-mono text-xs text-[#542B38]">
            Decision(x) = SPAM if P(y=1|x) ≥ 0.60<br/>
            Decision(x) = REVIEW if 0.10 &lt; P(y=1|x) &lt; 0.60<br/>
            Decision(x) = HAM if P(y=1|x) ≤ 0.10
          </div>
        </div>

        <div className="bg-[#FFFCF8] rounded-3xl p-6 border border-[#E4DAD0] shadow-soft space-y-3">
          <h4 className="text-sm font-extrabold text-[#542B38] font-display">
            Privacy & Compliance Standards
          </h4>
          <p className="text-xs text-[#817A76] leading-relaxed">
            SpamShield AI adheres strictly to enterprise privacy standards:
          </p>
          <ul className="text-xs text-[#817A76] space-y-1.5 list-disc pl-4">
            <li><b>Zero-Persistence Raw Ingestion:</b> SMS payloads are tokenized in transient memory.</li>
            <li><b>Local CPU Inference:</b> BERT-Tiny runs locally without external third-party API dependencies.</li>
            <li><b>Audit Invariance:</b> Historical benchmark datasets and model weights are cryptographically verified.</li>
          </ul>
        </div>
      </div>

      {/* REST API Reference Table */}
      <div className="bg-[#FFFCF8] rounded-3xl p-6 lg:p-8 border border-[#E4DAD0] shadow-soft space-y-4">
        <div className="border-b border-[#E4DAD0] pb-3 flex justify-between items-center">
          <div>
            <h3 className="text-base font-extrabold text-[#542B38] font-display flex items-center space-x-2">
              <Code2 className="w-5 h-5 text-[#A83F55]" />
              <span>FastAPI REST Endpoints Reference</span>
            </h3>
            <p className="text-xs text-[#817A76]">
              All endpoints available at base URL <code>http://127.0.0.1:8000</code>.
            </p>
          </div>
          <a
            href="http://127.0.0.1:8000/docs"
            target="_blank"
            rel="noreferrer"
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-xl bg-[#F5F0E9] hover:bg-[#EAE1D7] border border-[#E4DAD0] text-xs font-bold text-[#542B38] transition-colors"
          >
            <span>Swagger Docs</span>
            <ExternalLink className="w-3.5 h-3.5" />
          </a>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-sans">
            <thead className="bg-[#F5F0E9] text-[#817A76] uppercase font-bold text-[10px] tracking-wider">
              <tr>
                <th className="py-2.5 px-4 rounded-l-xl">HTTP Method</th>
                <th className="py-2.5 px-4">Endpoint Path</th>
                <th className="py-2.5 px-4 rounded-r-xl">Functional Description</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#E4DAD0]">
              {endpoints.map((ep, i) => (
                <tr key={i} className="hover:bg-[#F5F0E9]/50 transition-colors">
                  <td className="py-3 px-4 font-mono font-bold">
                    <span className={`px-2 py-0.5 rounded text-[10px] ${
                      ep.method === 'POST' ? 'bg-[#A83F55] text-white' : 'bg-[#542B38] text-white'
                    }`}>
                      {ep.method}
                    </span>
                  </td>
                  <td className="py-3 px-4 font-mono font-bold text-[#33302E]">
                    {ep.path}
                  </td>
                  <td className="py-3 px-4 text-[#817A76]">
                    {ep.desc}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
