import React, { useState, useEffect } from 'react';
import { 
  Database, 
  Search, 
  ChevronLeft, 
  ChevronRight, 
  Download, 
  ShieldCheck, 
  ShieldAlert, 
  Filter,
  Loader2
} from 'lucide-react';
import { fetchDatasetRecords, fetchDatasetSummary } from '../api/client';

export default function DatasetExplorerPage() {
  const [summary, setSummary] = useState(null);
  const [records, setRecords] = useState([]);
  const [total, setTotal] = useState(0);
  const [totalPages, setTotalPages] = useState(1);
  const [labelFilter, setLabelFilter] = useState('all');
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(false);

  const PAGE_SIZE = 15;

  useEffect(() => {
    fetchDatasetSummary().then(setSummary).catch(console.error);
  }, []);

  const loadRecords = async () => {
    setLoading(true);
    try {
      const res = await fetchDatasetRecords({
        label: labelFilter,
        search,
        page,
        page_size: PAGE_SIZE
      });
      setRecords(res.records);
      setTotal(res.total);
      setTotalPages(res.total_pages);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadRecords();
  }, [labelFilter, page]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    setPage(1);
    loadRecords();
  };

  const handleDownloadCSV = () => {
    if (!records.length) return;
    const headers = ['SpecimenID', 'Label', 'CharLength', 'WordCount', 'Message'];
    const rows = records.map(r => [
      r.id,
      r.label.toUpperCase(),
      r.char_length,
      r.word_count,
      `"${r.message.replace(/"/g, '""')}"`
    ]);
    const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...rows.map(e => e.join(','))].join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `uci_sms_dataset_page_${page}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-extrabold text-[#542B38] tracking-tight font-display">
          UCI SMS Dataset Explorer
        </h2>
        <p className="text-xs text-[#817A76] mt-0.5">
          Audit, filter, and inspect all 5,572 authentic historical SMS specimens from the training corpus.
        </p>
      </div>

      {/* Dataset Telemetry Cards */}
      {summary && (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <div className="bg-[#FFFCF8] rounded-2xl p-4 border border-[#E4DAD0] shadow-soft">
            <span className="text-[10px] uppercase font-bold text-[#817A76] tracking-wider block">
              Total Observations
            </span>
            <span className="text-2xl font-extrabold text-[#33302E] font-display">
              {summary.total_messages.toLocaleString()}
            </span>
            <span className="text-[11px] text-[#2E6B4F] block mt-0.5 font-semibold">
              0.00% Missing Attributes
            </span>
          </div>

          <div className="bg-[#FFFCF8] rounded-2xl p-4 border border-[#E4DAD0] shadow-soft">
            <span className="text-[10px] uppercase font-bold text-[#817A76] tracking-wider block">
              Ham Distribution
            </span>
            <span className="text-2xl font-extrabold text-[#2E6B4F] font-display">
              {summary.ham_count.toLocaleString()}
            </span>
            <span className="text-[11px] text-[#2E6B4F] block mt-0.5 font-mono">
              {summary.ham_percentage}% of corpus
            </span>
          </div>

          <div className="bg-[#FFFCF8] rounded-2xl p-4 border border-[#E4DAD0] shadow-soft">
            <span className="text-[10px] uppercase font-bold text-[#817A76] tracking-wider block">
              Spam Distribution
            </span>
            <span className="text-2xl font-extrabold text-[#A83F55] font-display">
              {summary.spam_count.toLocaleString()}
            </span>
            <span className="text-[11px] text-[#A83F55] block mt-0.5 font-mono">
              {summary.spam_percentage}% of corpus
            </span>
          </div>

          <div className="bg-[#FFFCF8] rounded-2xl p-4 border border-[#E4DAD0] shadow-soft">
            <span className="text-[10px] uppercase font-bold text-[#817A76] tracking-wider block">
              Mean Message Length
            </span>
            <span className="text-2xl font-extrabold text-[#542B38] font-display">
              {summary.avg_char_length} <span className="text-xs text-[#817A76] font-normal">chars</span>
            </span>
            <span className="text-[11px] text-[#817A76] block mt-0.5 font-mono">
              ~{summary.avg_word_count} words/msg
            </span>
          </div>
        </div>
      )}

      {/* Controls Bar */}
      <div className="bg-[#FFFCF8] rounded-2xl p-4 border border-[#E4DAD0] shadow-soft flex flex-col md:flex-row items-center justify-between gap-4">
        {/* Search */}
        <form onSubmit={handleSearchSubmit} className="relative w-full md:w-80">
          <Search className="w-4 h-4 absolute left-3 top-3 text-[#817A76]" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search keywords in messages..."
            className="w-full bg-[#F5F0E9] border border-[#E4DAD0] rounded-xl pl-9 pr-4 py-2 text-xs text-[#33302E] placeholder-[#817A76] focus:outline-none focus:border-[#A83F55]"
          />
        </form>

        {/* Filter Pills & Export */}
        <div className="flex flex-wrap items-center gap-2 w-full md:w-auto justify-between md:justify-end">
          <div className="flex items-center space-x-1.5">
            {['all', 'ham', 'spam'].map((l) => (
              <button
                key={l}
                onClick={() => { setLabelFilter(l); setPage(1); }}
                className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-colors border capitalize ${
                  labelFilter === l
                    ? 'bg-[#542B38] text-white border-[#542B38]'
                    : 'bg-[#F5F0E9] text-[#817A76] border-[#E4DAD0] hover:bg-[#EAE1D7]'
                }`}
              >
                {l === 'all' ? 'All Messages' : l}
              </button>
            ))}
          </div>

          <button
            onClick={handleDownloadCSV}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-xl bg-[#F5F0E9] hover:bg-[#EAE1D7] border border-[#E4DAD0] text-xs font-bold text-[#542B38] transition-colors"
          >
            <Download className="w-3.5 h-3.5 text-[#A83F55]" />
            <span>Export CSV</span>
          </button>
        </div>
      </div>

      {/* Table */}
      <div className="bg-[#FFFCF8] rounded-3xl border border-[#E4DAD0] shadow-soft overflow-hidden">
        <div className="p-4 border-b border-[#E4DAD0] flex justify-between items-center text-xs text-[#817A76]">
          <span>Displaying <b>{records.length}</b> of <b>{total}</b> filtered messages</span>
          <span>Page <b>{page}</b> of <b>{totalPages}</b></span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-[#F5F0E9] border-b border-[#E4DAD0] text-[#817A76] uppercase font-bold text-[10px] tracking-wider">
              <tr>
                <th className="py-3 px-6">ID</th>
                <th className="py-3 px-6">Ground Truth</th>
                <th className="py-3 px-6">Message Body</th>
                <th className="py-3 px-6 text-right">Length</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#E4DAD0]">
              {loading ? (
                <tr>
                  <td colSpan={4} className="py-12 text-center text-xs text-[#817A76]">
                    <Loader2 className="w-5 h-5 animate-spin mx-auto text-[#A83F55] mb-2" />
                    <span>Loading authentic dataset records...</span>
                  </td>
                </tr>
              ) : records.length === 0 ? (
                <tr>
                  <td colSpan={4} className="py-12 text-center text-xs text-[#817A76]">
                    No messages matched the search criteria.
                  </td>
                </tr>
              ) : (
                records.map((r) => {
                  const isSpam = r.label === 'spam';
                  return (
                    <tr key={r.id} className="hover:bg-[#F5F0E9]/50 transition-colors">
                      <td className="py-3.5 px-6 font-mono text-[#817A76] text-[11px]">
                        #{r.id}
                      </td>
                      <td className="py-3.5 px-6">
                        <span
                          className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-[10px] font-bold border uppercase tracking-wider ${
                            isSpam
                              ? 'bg-[#FDF0F2] text-[#A83F55] border-[#F5D5DC]'
                              : 'bg-[#EFF7F2] text-[#2E6B4F] border-[#D1E8DA]'
                          }`}
                        >
                          {r.label}
                        </span>
                      </td>
                      <td className="py-3.5 px-6 font-sans text-[#33302E] leading-relaxed max-w-xl">
                        {r.message}
                      </td>
                      <td className="py-3.5 px-6 font-mono text-[#817A76] text-right whitespace-nowrap text-[11px]">
                        {r.char_length} chars ({r.word_count}w)
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination Bar */}
        <div className="p-4 border-t border-[#E4DAD0] flex items-center justify-between">
          <div className="text-xs text-[#817A76]">
            Showing {(page - 1) * PAGE_SIZE + 1} to {Math.min(page * PAGE_SIZE, total)} of {total} results
          </div>
          <div className="flex items-center space-x-2">
            <button
              onClick={() => setPage(p => Math.max(1, p - 1))}
              disabled={page === 1}
              className="p-2 rounded-xl border border-[#E4DAD0] bg-white text-[#33302E] hover:bg-[#F5F0E9] disabled:opacity-40 transition-colors"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <span className="text-xs font-bold text-[#542B38] px-2 font-mono">
              {page} / {totalPages}
            </span>
            <button
              onClick={() => setPage(p => Math.min(totalPages, p + 1))}
              disabled={page === totalPages}
              className="p-2 rounded-xl border border-[#E4DAD0] bg-white text-[#33302E] hover:bg-[#F5F0E9] disabled:opacity-40 transition-colors"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
