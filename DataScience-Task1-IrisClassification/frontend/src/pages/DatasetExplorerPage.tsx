import React, { useState, useEffect } from 'react';
import { Database, Search, Filter } from 'lucide-react';
import { fetchDatasetRecords, fetchDatasetSummary, DatasetSummary } from '../api/client';

export default function DatasetExplorerPage() {
  const [summary, setSummary] = useState<DatasetSummary | null>(null);
  const [records, setRecords] = useState<any[]>([]);
  const [total, setTotal] = useState<number>(0);
  const [species, setSpecies] = useState<string>('all');
  const [search, setSearch] = useState<string>('');
  const [page, setPage] = useState<number>(1);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchDatasetSummary().then(setSummary).catch(console.error);
  }, []);

  const loadRecords = async () => {
    setLoading(true);
    try {
      const res = await fetchDatasetRecords({ species, search, page, page_size: 20 });
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

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      <div>
        <h2 className="text-2xl font-extrabold text-[#19362A] tracking-tight">
          Botanical Dataset Explorer
        </h2>
        <p className="text-sm text-[#728177]">
          Search, filter, and inspect Fisher's 150 Iris specimens with descriptive statistical moments.
        </p>
      </div>

      {/* Controls Bar */}
      <div className="bg-white rounded-2xl p-4 border border-[#E3EBE3] shadow-soft flex flex-col sm:flex-row items-center justify-between gap-4">
        <form onSubmit={handleSearchSubmit} className="relative w-full sm:w-80">
          <Search className="w-4 h-4 absolute left-3 top-3 text-[#8BAA91]" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search specimen attributes..."
            className="w-full bg-[#F7FAF7] border border-[#E3EBE3] rounded-xl pl-9 pr-4 py-2 text-xs text-[#19362A] focus:outline-none focus:border-[#285943]"
          />
        </form>

        <div className="flex items-center space-x-2 w-full sm:w-auto">
          {['all', 'Setosa', 'Versicolor', 'Virginica'].map((s) => (
            <button
              key={s}
              onClick={() => { setSpecies(s); setPage(1); }}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition-colors border ${
                species.toLowerCase() === s.toLowerCase()
                  ? 'bg-[#285943] text-white border-[#285943]'
                  : 'bg-[#F7FAF7] text-[#728177] border-[#E3EBE3] hover:bg-[#EFF8F0]'
              }`}
            >
              {s === 'all' ? 'All Species' : s}
            </button>
          ))}
        </div>
      </div>

      {/* Specimen Table */}
      <div className="bg-white rounded-3xl border border-[#E3EBE3] shadow-soft overflow-hidden">
        <div className="p-4 border-b border-[#E3EBE3] flex justify-between items-center text-xs text-[#728177]">
          <span>Displaying <b>{records.length}</b> of <b>{total}</b> filtered specimens</span>
          <span>Page <b>{page}</b> of <b>{Math.ceil(total / 20) || 1}</b></span>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-sans">
            <thead className="bg-[#F7FAF7] border-b border-[#E3EBE3] text-[#728177] uppercase font-bold text-[11px] tracking-wider">
              <tr>
                <th className="py-3 px-6">Specimen ID</th>
                <th className="py-3 px-6">Sepal Length (cm)</th>
                <th className="py-3 px-6">Sepal Width (cm)</th>
                <th className="py-3 px-6">Petal Length (cm)</th>
                <th className="py-3 px-6">Petal Width (cm)</th>
                <th className="py-3 px-6">Species Taxon</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#E3EBE3]">
              {records.map((r, i) => (
                <tr key={i} className="hover:bg-[#F7FAF7] transition-colors">
                  <td className="py-3 px-6 font-mono text-[#728177]">#{(page - 1) * 20 + i + 1}</td>
                  <td className="py-3 px-6 font-bold text-[#19362A]">{r.sepal_length}</td>
                  <td className="py-3 px-6 font-bold text-[#19362A]">{r.sepal_width}</td>
                  <td className="py-3 px-6 font-bold text-[#19362A]">{r.petal_length}</td>
                  <td className="py-3 px-6 font-bold text-[#19362A]">{r.petal_width}</td>
                  <td className="py-3 px-6">
                    <span className="font-bold text-[#285943]">
                      Iris {r.species}
                    </span>
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
