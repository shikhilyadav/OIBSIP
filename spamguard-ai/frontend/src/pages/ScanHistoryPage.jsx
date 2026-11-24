import React, { useState, useEffect } from 'react';
import { History, Search, Trash2, ShieldAlert, ShieldCheck, HelpCircle, RefreshCw } from 'lucide-react';
import { fetchHistory, clearHistory } from '../api/client';
import { DecisionBadge, RiskBadge } from '../components/common/Cards';

export default function ScanHistoryPage() {
  const [data, setData] = useState({ items: [], total_records: 0 });
  const [filter, setFilter] = useState('ALL');
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(false);
  const [selectedItem, setSelectedItem] = useState(null);

  const loadData = async () => {
    setLoading(true);
    try {
      const res = await fetchHistory({ filter, search, limit: 50 });
      setData(res);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [filter]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    loadData();
  };

  const handleClear = async () => {
    if (window.confirm('Clear in-memory session history?')) {
      await clearHistory();
      loadData();
      setSelectedItem(null);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-cyber-border pb-4">
        <div>
          <h1 className="text-2xl font-bold font-mono text-white tracking-tight flex items-center gap-2">
            <History className="w-6 h-6 text-cyber-accent" />
            Security Scan History & Audit Trail
          </h1>
          <p className="text-sm text-cyber-muted mt-1">
            In-memory forensic audit log of all inspected messages in current browser session.
          </p>
        </div>
        <button
          onClick={handleClear}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-cyber-surface hover:bg-rose-500/10 text-slate-300 hover:text-cyber-danger border border-cyber-border hover:border-rose-500/30 text-xs font-mono transition-colors"
        >
          <Trash2 className="w-3.5 h-3.5" />
          <span>Clear Session History</span>
        </button>
      </div>

      {/* Controls: Search & Filter */}
      <div className="bg-cyber-card border border-cyber-border rounded-xl p-4 flex flex-col sm:flex-row items-center justify-between gap-3">
        <form onSubmit={handleSearchSubmit} className="relative w-full sm:w-80">
          <Search className="w-4 h-4 absolute left-3 top-2.5 text-slate-400" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search payload keywords..."
            className="w-full bg-cyber-surface border border-cyber-border rounded-lg pl-9 pr-3 py-1.5 text-xs font-mono text-white placeholder:text-slate-500 focus:outline-none focus:border-cyber-accent"
          />
        </form>

        <div className="flex items-center gap-2 w-full sm:w-auto">
          <span className="text-xs font-mono text-cyber-muted hidden sm:inline">Filter:</span>
          {['ALL', 'SPAM', 'HAM', 'SUSPICIOUS'].map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`px-3 py-1 rounded-lg text-xs font-mono font-medium transition-colors border ${
                filter === f
                  ? 'bg-cyber-accent text-slate-900 border-cyber-accent font-bold'
                  : 'bg-cyber-surface text-slate-300 border-cyber-border hover:bg-cyber-subtle'
              }`}
            >
              {f}
            </button>
          ))}
          <button
            onClick={loadData}
            className="p-1.5 rounded-lg bg-cyber-surface hover:bg-cyber-subtle border border-cyber-border text-slate-400"
            title="Refresh"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin text-cyber-accent' : ''}`} />
          </button>
        </div>
      </div>

      {/* History Table */}
      <div className="bg-cyber-card border border-cyber-border rounded-xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-cyber-surface border-b border-cyber-border text-cyber-muted uppercase tracking-wider text-[11px]">
              <tr>
                <th className="py-3 px-4">Timestamp (UTC)</th>
                <th className="py-3 px-4">Payload Excerpt</th>
                <th className="py-3 px-4">Triage Verdict</th>
                <th className="py-3 px-4">Risk Level</th>
                <th className="py-3 px-4">Risk Score</th>
                <th className="py-3 px-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-cyber-border/60">
              {data.items.length === 0 ? (
                <tr>
                  <td colSpan={6} className="py-8 text-center text-cyber-muted font-sans">
                    No scan records found matching active filter.
                  </td>
                </tr>
              ) : (
                data.items.map((item) => (
                  <tr key={item.id} className="hover:bg-cyber-surface/40 transition-colors">
                    <td className="py-3 px-4 text-slate-400 whitespace-nowrap text-[11px]">
                      {item.timestamp}
                    </td>
                    <td className="py-3 px-4 text-slate-200 max-w-xs truncate font-sans">
                      {item.message_preview}
                    </td>
                    <td className="py-3 px-4 whitespace-nowrap">
                      <DecisionBadge decision={item.decision} />
                    </td>
                    <td className="py-3 px-4 whitespace-nowrap">
                      <RiskBadge level={item.risk_level} />
                    </td>
                    <td className="py-3 px-4 font-bold text-white whitespace-nowrap">
                      {(item.risk_score * 100).toFixed(1)}%
                    </td>
                    <td className="py-3 px-4 text-right whitespace-nowrap">
                      <button
                        onClick={() => setSelectedItem(item)}
                        className="text-cyber-cyan hover:underline text-[11px]"
                      >
                        Inspect
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Detail Modal / Drawer */}
      {selectedItem && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50">
          <div className="bg-cyber-card border border-cyber-border rounded-xl p-6 max-w-lg w-full space-y-4 glow-accent">
            <div className="flex items-center justify-between border-b border-cyber-border pb-3">
              <span className="font-mono font-bold text-sm text-white">Scan Record Details ({selectedItem.id})</span>
              <button
                onClick={() => setSelectedItem(null)}
                className="text-cyber-muted hover:text-white font-mono text-sm"
              >
                ✕
              </button>
            </div>
            <div className="space-y-3 text-xs">
              <div>
                <span className="font-mono text-cyber-muted block mb-1">Full Message:</span>
                <p className="p-3 rounded bg-cyber-surface border border-cyber-border text-slate-200 font-sans leading-relaxed">
                  {selectedItem.full_message}
                </p>
              </div>
              <div className="grid grid-cols-2 gap-2 font-mono">
                <div>
                  <span className="text-cyber-muted block">Decision:</span>
                  <span className="text-white font-bold">{selectedItem.decision}</span>
                </div>
                <div>
                  <span className="text-cyber-muted block">Composite Score:</span>
                  <span className="text-white font-bold">{(selectedItem.risk_score * 100).toFixed(1)}%</span>
                </div>
                <div>
                  <span className="text-cyber-muted block">Requires Review:</span>
                  <span className={selectedItem.requires_review ? 'text-amber-400 font-bold' : 'text-slate-300'}>
                    {selectedItem.requires_review ? 'YES' : 'NO'}
                  </span>
                </div>
                <div>
                  <span className="text-cyber-muted block">Model Used:</span>
                  <span className="text-slate-300">{selectedItem.model_used}</span>
                </div>
              </div>
            </div>
            <div className="pt-2 text-right">
              <button
                onClick={() => setSelectedItem(null)}
                className="px-4 py-1.5 rounded-lg bg-cyber-surface hover:bg-cyber-subtle border border-cyber-border text-xs font-mono text-slate-200"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
