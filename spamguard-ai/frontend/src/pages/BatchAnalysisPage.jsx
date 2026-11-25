import React, { useState } from 'react';
import { 
  UploadCloud, 
  FileText, 
  Play, 
  Download, 
  CheckCircle2, 
  AlertCircle, 
  Loader2, 
  ShieldAlert, 
  ShieldCheck,
  HelpCircle
} from 'lucide-react';
import { analyzeBatch } from '../api/client';

export default function BatchAnalysisPage() {
  const [file, setFile] = useState(null);
  const [parsedRows, setParsedRows] = useState([]);
  const [model, setModel] = useState('hybrid');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (!selectedFile) return;

    if (!selectedFile.name.endsWith('.csv') && !selectedFile.name.endsWith('.txt')) {
      setError('Please upload a valid CSV or TXT file.');
      return;
    }

    setFile(selectedFile);
    setError(null);
    setResults(null);

    const reader = new FileReader();
    reader.onload = (event) => {
      const text = event.target.result;
      const lines = text.split(/\r?\n/).filter(line => line.trim().length > 0);
      
      // Auto-detect header or raw lines
      const rows = [];
      const isHeader = lines[0]?.toLowerCase().includes('text') || lines[0]?.toLowerCase().includes('message') || lines[0]?.toLowerCase().includes('sms') || lines[0]?.toLowerCase().includes('v2');
      const startIdx = isHeader ? 1 : 0;

      for (let i = startIdx; i < Math.min(lines.length, 100); i++) {
        let msg = lines[i];
        // If CSV format, take the second column if available or clean quotes
        if (msg.includes(',')) {
          const parts = msg.split(',');
          msg = parts.length > 1 ? parts.slice(1).join(',') : parts[0];
        }
        msg = msg.replace(/^["']|["']$/g, '').trim();
        if (msg) rows.push(msg);
      }
      setParsedRows(rows);
    };
    reader.readAsText(selectedFile);
  };

  const handleStartAnalysis = async () => {
    if (!parsedRows.length) {
      setError('No valid messages found in the uploaded file.');
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const res = await analyzeBatch(parsedRows, model);
      setResults(res);
    } catch (err) {
      setError(err.message || 'Batch analysis failed.');
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadCSV = () => {
    if (!results || !results.results.length) return;
    const headers = ['Index', 'Message', 'Prediction', 'Confidence', 'ModelUsed', 'LatencyMs', 'RequiresReview'];
    const csvRows = results.results.map(r => [
      r.index,
      `"${r.message.replace(/"/g, '""')}"`,
      r.prediction,
      r.confidence,
      `"${r.model_used}"`,
      r.latency_ms,
      r.requires_review
    ]);
    const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...csvRows.map(e => e.join(','))].join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `spamshield_batch_results_${model}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-extrabold text-[#542B38] tracking-tight font-display">
          Batch Message Threat Inspection
        </h2>
        <p className="text-xs text-[#817A76] mt-0.5">
          Upload bulk message logs for high-throughput inference and export classified datasets with model confidence scores.
        </p>
      </div>

      {/* Upload and Controls Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Left Column: Upload Box */}
        <div className="lg:col-span-6 bg-[#FFFCF8] rounded-3xl p-6 lg:p-8 border border-[#E4DAD0] shadow-soft space-y-5">
          <div className="border-b border-[#E4DAD0] pb-3">
            <h3 className="text-base font-extrabold text-[#542B38] tracking-tight font-display">
              Upload Batch Dataset
            </h3>
            <p className="text-[11px] text-[#817A76]">
              Upload a .csv or .txt file containing messages (up to 100 per run).
            </p>
          </div>

          {/* Drag & Drop Area */}
          <label className="border-2 border-dashed border-[#D5BDA4] hover:border-[#A83F55] rounded-3xl p-8 flex flex-col items-center justify-center cursor-pointer bg-[#F5F0E9]/50 hover:bg-[#F5F0E9] transition-all group">
            <div className="w-12 h-12 rounded-2xl bg-white border border-[#E4DAD0] flex items-center justify-center text-[#542B38] group-hover:scale-105 transition-transform mb-3 shadow-xs">
              <UploadCloud className="w-6 h-6 text-[#A83F55]" />
            </div>
            <span className="text-xs font-bold text-[#542B38]">
              {file ? file.name : 'Choose file or drag & drop here'}
            </span>
            <span className="text-[10px] text-[#817A76] mt-1">
              Supports CSV (with text/message column) or newline-separated TXT
            </span>
            <input
              type="file"
              accept=".csv,.txt"
              onChange={handleFileChange}
              className="hidden"
            />
          </label>

          {/* Model Selector */}
          <div className="space-y-1.5">
            <label className="text-[11px] uppercase font-bold text-[#817A76] tracking-wider block">
              Inference Architecture
            </label>
            <select
              value={model}
              onChange={(e) => setModel(e.target.value)}
              className="w-full bg-[#F5F0E9] border border-[#E4DAD0] rounded-xl px-3.5 py-2.5 text-xs text-[#33302E] font-medium focus:outline-none focus:border-[#A83F55] transition-colors cursor-pointer"
            >
              <option value="hybrid">SpamShield Hybrid Triage (Calibrated Abstention)</option>
              <option value="bert_tiny">BERT-Tiny Transformer (Subword Attention)</option>
              <option value="naive_bayes">Multinomial Naive Bayes (TF-IDF)</option>
              <option value="logistic_regression">Logistic Regression (L2 Sigmoid)</option>
            </select>
          </div>

          {/* Action Button */}
          <button
            onClick={handleStartAnalysis}
            disabled={loading || !parsedRows.length}
            className="w-full flex items-center justify-center space-x-2 py-3.5 rounded-xl bg-[#A83F55] hover:bg-[#8E3346] text-white font-bold text-xs tracking-wide transition-all shadow-md disabled:opacity-50"
          >
            {loading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                <span>Processing Batch Pipeline...</span>
              </>
            ) : (
              <>
                <Play className="w-4 h-4 fill-current" />
                <span>Start Batch Analysis ({parsedRows.length} messages)</span>
              </>
            )}
          </button>

          {error && (
            <div className="p-3.5 rounded-2xl bg-rose-50 border border-rose-200 text-rose-800 text-xs flex items-center space-x-2">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}
        </div>

        {/* Right Column: Preview & Summary */}
        <div className="lg:col-span-6 space-y-5">
          {/* File Preview */}
          <div className="bg-[#FFFCF8] rounded-3xl p-6 border border-[#E4DAD0] shadow-soft space-y-3">
            <div className="flex justify-between items-center border-b border-[#E4DAD0] pb-3">
              <h4 className="text-sm font-extrabold text-[#542B38] font-display">
                Dataset Ingestion Preview
              </h4>
              <span className="text-[10px] font-mono text-[#817A76]">
                {parsedRows.length} rows loaded
              </span>
            </div>

            {parsedRows.length === 0 ? (
              <div className="py-12 text-center text-xs text-[#817A76] italic">
                Upload a file to preview parsed messages.
              </div>
            ) : (
              <div className="max-h-52 overflow-y-auto divide-y divide-[#E4DAD0] text-xs">
                {parsedRows.slice(0, 5).map((row, idx) => (
                  <div key={idx} className="py-2.5 flex items-start space-x-2">
                    <span className="font-mono text-[#817A76] text-[10px] shrink-0 mt-0.5">#{idx + 1}</span>
                    <span className="text-[#33302E] truncate font-sans">{row}</span>
                  </div>
                ))}
                {parsedRows.length > 5 && (
                  <div className="pt-2 text-center text-[10px] text-[#817A76] italic">
                    + {parsedRows.length - 5} more records ready for inference...
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Results Summary & Export */}
          {results && (
            <div className="bg-[#FFFCF8] rounded-3xl p-6 border border-[#E4DAD0] shadow-soft space-y-4">
              <div className="flex justify-between items-center border-b border-[#E4DAD0] pb-3">
                <div>
                  <h4 className="text-sm font-extrabold text-[#542B38] font-display">
                    Batch Classification Summary
                  </h4>
                  <p className="text-[11px] text-[#817A76]">
                    Processed {results.total_processed} items via {results.model_used}.
                  </p>
                </div>
                <button
                  onClick={handleDownloadCSV}
                  className="flex items-center space-x-1.5 px-3 py-1.5 rounded-xl bg-[#A83F55] hover:bg-[#8E3346] text-white text-xs font-bold transition-colors shadow-sm"
                >
                  <Download className="w-3.5 h-3.5" />
                  <span>Download CSV</span>
                </button>
              </div>

              <div className="grid grid-cols-3 gap-3 text-center">
                <div className="p-3 bg-[#EFF7F2] rounded-2xl border border-[#D1E8DA]">
                  <div className="text-[10px] uppercase font-bold text-[#2E6B4F]">Ham Cleared</div>
                  <div className="text-xl font-extrabold text-[#2E6B4F] font-mono mt-1">
                    {results.ham_count}
                  </div>
                </div>
                <div className="p-3 bg-[#FDF0F2] rounded-2xl border border-[#F5D5DC]">
                  <div className="text-[10px] uppercase font-bold text-[#A83F55]">Spam Flagged</div>
                  <div className="text-xl font-extrabold text-[#A83F55] font-mono mt-1">
                    {results.spam_count}
                  </div>
                </div>
                <div className="p-3 bg-[#FEF8EE] rounded-2xl border border-[#F6E6CE]">
                  <div className="text-[10px] uppercase font-bold text-[#B87B2E]">Review Queue</div>
                  <div className="text-xl font-extrabold text-[#B87B2E] font-mono mt-1">
                    {results.review_count}
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
