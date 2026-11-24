import React, { useState, useEffect } from 'react';
import { Database, Search, ChevronLeft, ChevronRight, Download, Filter } from 'lucide-react';
import { fetchDatasetRecords, fetchDatasetSummary, DatasetSummary } from '../api/client';

export default function DatasetExplorerPage() {
  const [summary, setSummary] = useState<DatasetSummary | null>(null);
  const [records, setRecords] = useState<any[]>([]);
  const [total, setTotal] = useState<number>(0);
  const [species, setSpecies] = useState<string>('all');
  const [search, setSearch] = useState<string>('');
  const [page, setPage] = useState<number>(1);
  const [loading, setLoading] = useState(false);

  const PAGE_SIZE = 15;

  useEffect(() => {
    fetchDatasetSummary().then(setSummary).catch(console.error);
  }, []);

  const loadRecords = async () => {
    setLoading(true);
    try {
      const res = await fetchDatasetRecords({ species, search, page, page_size: PAGE_SIZE });
      setRecords(res.records);
      setTotal(res.total);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadRecords();
  }, [species, page]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setPage(1);
    loadRecords();
  };

  const totalPages = Math.ceil(total / PAGE_SIZE) || 1;

  const downloadCSV = () => {
    if (!records.length) return;
    const headers = ['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm', 'Species'];
    const rows = records.map((r) => [r.sepal_length, r.sepal_width, r.petal_length, r.petal_width, `Iris-${r.species}`]);
    const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...rows.map(e => e.join(','))].join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `iris_specimens_page_${page}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const getSpeciesBadge = (sp: string) => {
    if (sp.toLowerCase().includes('setosa')) {
      return 'bg-[#EAE7F5] text-[#76649D] border-[#D6D0E8]';
    }
    if (sp.toLowerCase().includes('versicolor')) {
      return 'bg-[#F7EBDD] text-[#C18E61] border-[#EBDDCF]';
    }
    return 'bg-[#EFF8F0] text-[#285943] border-[#C7E2CE]';
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-extrabold text-[#19362A] tracking-tight">
          Botanical Dataset Explorer
        </h2>
        <p className="text-sm text-[#728177]">
          Search, filter, and inspect Fisher's 150 Iris specimens with descriptive statistical moments.
        </p>
      </div>

      {/* Dataset Summary Telemetry */}
      {summary && (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <div className="bg-white rounded-2xl p-4 border border-[#E3EBE3] shadow-soft">
            <span className="text-[10px] uppercase font-bold text-[#728177] tracking-wider block">
              Total Observations
            </span>
            <span className="text-2xl font-extrabold text-[#19362A]">
              {summary.total_specimens}
            </span>
            <span className="text-[11px] text-[#285943] block mt-0.5 font-semibold">
              3 Equal 50-specimen cohorts
            </span>
          </div>

          <div className="bg-white rounded-2xl p-4 border border-[#E3EBE3] shadow-soft">
            <span className="text-[10px] uppercase font-bold text-[#728177] tracking-wider block">
              Sepal Length Bounds
            </span>
            <span className="text-2xl font-extrabold text-[#19362A]">
              4.3 – 7.9 <span className="text-xs text-[#728177] font-normal">cm</span>
            </span>
            <span className="text-[11px] text-[#728177] block mt-0.5 font-mono">
              Mean: 5.84 cm
            </span>
          </div>

          <div className="bg-white rounded-2xl p-4 border border-[#E3EBE3] shadow-soft">
            <span className="text-[10px] uppercase font-bold text-[#728177] tracking-wider block">
              Petal Length Bounds
            </span>
            <span className="text-2xl font-extrabold text-[#19362A]">
              1.0 – 6.9 <span className="text-xs text-[#728177] font-normal">cm</span>
            </span>
            <span className="text-[11px] text-[#728177] block mt-0.5 font-mono">
              Mean: 3.76 cm
            </span>
          </div>

          <div className="bg-white rounded-2xl p-4 border border-[#E3EBE3] shadow-soft">
            <span className="text-[10px] uppercase font-bold text-[#728177] tracking-wider block">
              Missing Values
            </span>
            <span className="text-2xl font-extrabold text-[#285943]">
              0.00%
            </span>
            <span className="text-[11px] text-[#285943] block mt-0.5 font-semibold">
              100% Complete telemetry
            </span>
          </div>
        </div>
      )}

      {/* Controls Bar */}
      <div className="bg-white rounded-2xl p-4 border border-[#E3EBE3] shadow-soft flex flex-col md:flex-row items-center justify-between gap-4">
        {/* Search */}
        <form onSubmit={handleSearchSubmit} className="relative w-full md:w-80">
          <Search className="w-4 h-4 absolute left-3 top-3 text-[#8BAA91]" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search specimen attributes..."
            className="w-full bg-[#F7FAF7] border border-[#E3EBE3] rounded-xl pl-9 pr-4 py-2 text-xs text-[#19362A] focus:outline-none focus:border-[#285943]"
          />
        </form>

        {/* Filter Pills & Export */}
        <div className="flex flex-wrap items-center gap-2 w-full md:w-auto justify-between md:justify-end">
          <div className="flex items-center space-x-1.5">
            {['all', 'Setosa', 'Versicolor', 'Virginica'].map((s) => (
              <button
                key={s}
                onClick={() => { setSpecies(s); setPage(1); }}
                className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-colors border ${
                  species.toLowerCase() === s.toLowerCase()
                    ? 'bg-[#285943] text-white border-[#285943]'
                    : 'bg-[#F7FAF7] text-[#728177] border-[#E3EBE3] hover:bg-[#EFF8F0]'
                }`}
              >
                {s === 'all' ? 'All Species' : s}
              </button>
            ))}
          </div>

          <button
            onClick={downloadCSV}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-xl bg-[#F7FAF7] hover:bg-[#EFF8F0] border border-[#E3EBE3] text-xs font-bold text-[#19362A] transition-colors"
          >
            <Download className="w-3.5 h-3.5 text-[#285943]" />
            <span>Export CSV</span>
          </button>
        </div>
      </div>

      {/* Specimen Table */}
      <div className="bg-white rounded-3xl border border-[#E3EBE3] shadow-soft overflow-hidden">
        <div className="p-4 border-b border-[#E3EBE3] flex justify-between items-center text-xs text-[#728177]">
          <span>Displaying <b>{records.length}</b> of <b>{total}</b> filtered specimens</span>
          <span>Page <b>{page}</b> of <b>{totalPages}</b></span>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-sans">
            <thead className="bg-[#F7FAF7] border-b border-[#E3EBE3] text-[#728177] uppercase font-bold text-[11px] tracking-wider">
              <tr>
                <th className="py-3.5 px-6">Specimen ID</th>
                <th className="py-3.5 px-6">Sepal Length</th>
                <th className="py-3.5 px-6">Sepal Width</th>
                <th className="py-3.5 px-6">Petal Length</th>
                <th className="py-3.5 px-6">Petal Width</th>
                <th className="py-3.5 px-6">Taxonomic Class</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#E3EBE3]">
              {loading ? (
                <tr>
                  <td colSpan={6} className="py-8 text-center text-xs text-[#728177]">
                    Loading specimens...
                  </td>
                </tr>
              ) : records.length === 0 ? (
                <tr>
                  <td colSpan={6} className="py-8 text-center text-xs text-[#728177]">
                    No matching botanical specimens found.
                  </td>
                </tr>
              ) : (
                records.map((r, i) => (
                  <tr key={i} className="hover:bg-[#F7FAF7] transition-colors">
                    <td className="py-3.5 px-6 font-mono text-[#728177]">
                      #{(page - 1) * PAGE_SIZE + i + 1}
                    </td>
                    <td className="py-3.5 px-6 font-bold text-[#19362A] font-mono">
                      {r.sepal_length.toFixed(1)} cm
                    </td>
                    <td className="py-3.5 px-6 font-bold text-[#19362A] font-mono">
                      {r.sepal_width.toFixed(1)} cm
                    </td>
                    <td className="py-3.5 px-6 font-bold text-[#19362A] font-mono">
                      {r.petal_length.toFixed(1)} cm
                    </td>
                    <td className="py-3.5 px-6 font-bold text-[#19362A] font-mono">
                      {r.petal_width.toFixed(1)} cm
                    </td>
                    <td className="py-3.5 px-6">
                      <span className={`inline-flex items-center px-2.5 py-1 rounded-full text-[11px] font-bold border ${getSpeciesBadge(r.species)}`}>
                        Iris {r.species}
                      </span>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination Bar */}
        <div className="p-4 border-t border-[#E3EBE3] flex items-center justify-between">
          <div className="text-xs text-[#728177]">
            Showing {(page - 1) * PAGE_SIZE + 1} to {Math.min(page * PAGE_SIZE, total)} of {total} results
          </div>
          <div className="flex items-center space-x-2">
            <button
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={page === 1}
              className="p-2 rounded-xl border border-[#E3EBE3] bg-white text-[#19362A] hover:bg-[#EFF8F0] disabled:opacity-40 transition-colors"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <span className="text-xs font-bold text-[#19362A] px-2 font-mono">
              {page} / {totalPages}
            </span>
            <button
              onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
              disabled={page === totalPages}
              className="p-2 rounded-xl border border-[#E3EBE3] bg-white text-[#19362A] hover:bg-[#EFF8F0] disabled:opacity-40 transition-colors"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
