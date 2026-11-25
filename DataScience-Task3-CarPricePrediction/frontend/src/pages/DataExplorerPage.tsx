import React, { useState, useEffect } from 'react';
import { 
  Database, 
  Search, 
  ChevronLeft, 
  ChevronRight, 
  Download, 
  Filter, 
  Car, 
  Loader2 
} from 'lucide-react';
import { 
  fetchDatasetRecords, 
  fetchDatasetSummary, 
  fetchDatasetOptions, 
  DatasetSummary, 
  DatasetOptions, 
  CarRecord 
} from '../api/client';

export default function DataExplorerPage() {
  const [summary, setSummary] = useState<DatasetSummary | null>(null);
  const [options, setOptions] = useState<DatasetOptions | null>(null);
  const [records, setRecords] = useState<CarRecord[]>([]);
  const [total, setTotal] = useState(0);
  const [totalPages, setTotalPages] = useState(1);
  const [brand, setBrand] = useState('all');
  const [fuel, setFuel] = useState('all');
  const [transmission, setTransmission] = useState('all');
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(false);

  const PAGE_SIZE = 15;

  useEffect(() => {
    fetchDatasetSummary().then(setSummary).catch(console.error);
    fetchDatasetOptions().then(setOptions).catch(console.error);
  }, []);

  const loadRecords = async () => {
    setLoading(true);
    try {
      const res = await fetchDatasetRecords({
        brand,
        fuel,
        transmission,
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
  }, [brand, fuel, transmission, page]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setPage(1);
    loadRecords();
  };

  const downloadCSV = () => {
    if (!records.length) return;
    const headers = ['VehicleName', 'Brand', 'Year', 'SellingPrice', 'KmDriven', 'Fuel', 'SellerType', 'Transmission', 'Owner'];
    const rows = records.map(r => [
      `"${r.name.replace(/"/g, '""')}"`,
      r.brand,
      r.year,
      r.selling_price,
      r.km_driven,
      r.fuel,
      r.seller_type,
      r.transmission,
      `"${r.owner}"`
    ]);
    const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...rows.map(e => e.join(','))].join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `cardekho_fleet_page_${page}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-extrabold text-[#073B32] tracking-tight font-display">
          Fleet Dataset Explorer
        </h2>
        <p className="text-xs text-[#77827E] mt-0.5">
          Query, filter, and inspect all 3,577 verified CarDekho automotive records with descriptive statistics.
        </p>
      </div>

      {/* Dataset Summary Telemetry */}
      {summary && (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <div className="bg-white rounded-2xl p-4 border border-[#E4E8E1] shadow-soft">
            <span className="text-[10px] uppercase font-bold text-[#77827E] tracking-wider block">
              Fleet Corpus Size
            </span>
            <div className="text-2xl font-extrabold text-[#202A28] font-display">
              {summary.total_records.toLocaleString()}
            </div>
            <span className="text-[11px] text-[#125B48] block mt-0.5 font-semibold">
              0.00% Missing Values
            </span>
          </div>

          <div className="bg-white rounded-2xl p-4 border border-[#E4E8E1] shadow-soft">
            <span className="text-[10px] uppercase font-bold text-[#77827E] tracking-wider block">
              Mean Selling Price
            </span>
            <div className="text-2xl font-extrabold text-[#073B32] font-display">
              ₹{(summary.average_price / 1e5).toFixed(2)} Lakh
            </div>
            <span className="text-[11px] text-[#77827E] block mt-0.5 font-mono">
              Median: ₹{(summary.median_price / 1e5).toFixed(2)}L
            </span>
          </div>

          <div className="bg-white rounded-2xl p-4 border border-[#E4E8E1] shadow-soft">
            <span className="text-[10px] uppercase font-bold text-[#77827E] tracking-wider block">
              Mean Fleet Odometer
            </span>
            <div className="text-2xl font-extrabold text-[#202A28] font-display">
              {summary.average_km.toLocaleString()} km
            </div>
            <span className="text-[11px] text-[#77827E] block mt-0.5 font-mono">
              Mean Age: {summary.average_age} yrs
            </span>
          </div>

          <div className="bg-white rounded-2xl p-4 border border-[#E4E8E1] shadow-soft">
            <span className="text-[10px] uppercase font-bold text-[#77827E] tracking-wider block">
              Valuation Bounds
            </span>
            <div className="text-2xl font-extrabold text-[#E6B85C] font-display">
              ₹20K – ₹89.0L
            </div>
            <span className="text-[11px] text-[#77827E] block mt-0.5 font-mono">
              {summary.unique_brands} Brands Represented
            </span>
          </div>
        </div>
      )}

      {/* Filter and Search Bar */}
      <div className="bg-white rounded-2xl p-4 border border-[#E4E8E1] shadow-soft flex flex-col md:flex-row items-center justify-between gap-4">
        {/* Search */}
        <form onSubmit={handleSearchSubmit} className="relative w-full md:w-80">
          <Search className="w-4 h-4 absolute left-3 top-3 text-[#77827E]" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search vehicle model, trim..."
            className="w-full bg-[#F7F5F0] border border-[#E4E8E1] rounded-xl pl-9 pr-4 py-2 text-xs text-[#202A28] placeholder-[#77827E] focus:outline-none focus:border-[#125B48]"
          />
        </form>

        {/* Dropdowns & Export */}
        <div className="flex flex-wrap items-center gap-2 w-full md:w-auto justify-between md:justify-end">
          {/* Brand */}
          <select
            value={brand}
            onChange={(e) => { setBrand(e.target.value); setPage(1); }}
            className="bg-[#F7F5F0] border border-[#E4E8E1] rounded-xl px-3 py-1.5 text-xs text-[#202A28] font-semibold focus:outline-none focus:border-[#125B48] cursor-pointer"
          >
            <option value="all">All Brands</option>
            {options?.brands.map(b => <option key={b} value={b}>{b}</option>)}
          </select>

          {/* Fuel */}
          <select
            value={fuel}
            onChange={(e) => { setFuel(e.target.value); setPage(1); }}
            className="bg-[#F7F5F0] border border-[#E4E8E1] rounded-xl px-3 py-1.5 text-xs text-[#202A28] font-semibold focus:outline-none focus:border-[#125B48] cursor-pointer"
          >
            <option value="all">All Fuels</option>
            {options?.fuels.map(f => <option key={f} value={f}>{f}</option>)}
          </select>

          {/* Transmission */}
          <select
            value={transmission}
            onChange={(e) => { setTransmission(e.target.value); setPage(1); }}
            className="bg-[#F7F5F0] border border-[#E4E8E1] rounded-xl px-3 py-1.5 text-xs text-[#202A28] font-semibold focus:outline-none focus:border-[#125B48] cursor-pointer"
          >
            <option value="all">All Gearboxes</option>
            <option value="Manual">Manual</option>
            <option value="Automatic">Automatic</option>
          </select>

          <button
            onClick={downloadCSV}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-xl bg-[#F7F5F0] hover:bg-[#EFECE3] border border-[#E4E8E1] text-xs font-bold text-[#073B32] transition-colors"
          >
            <Download className="w-3.5 h-3.5 text-[#E6B85C]" />
            <span>Export CSV</span>
          </button>
        </div>
      </div>

      {/* Fleet Records Table */}
      <div className="bg-white rounded-3xl border border-[#E4E8E1] shadow-soft overflow-hidden">
        <div className="p-4 border-b border-[#E4E8E1] flex justify-between items-center text-xs text-[#77827E]">
          <span>Displaying <b>{records.length}</b> of <b>{total}</b> filtered records</span>
          <span>Page <b>{page}</b> of <b>{totalPages}</b></span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-sans">
            <thead className="bg-[#F7F5F0] border-b border-[#E4E8E1] text-[#77827E] uppercase font-bold text-[10px] tracking-wider">
              <tr>
                <th className="py-3 px-6">Vehicle Make & Model</th>
                <th className="py-3 px-6">Year / Age</th>
                <th className="py-3 px-6">Odometer</th>
                <th className="py-3 px-6">Fuel / Gearbox</th>
                <th className="py-3 px-6">Owner Title</th>
                <th className="py-3 px-6 text-right">Selling Price</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#E4E8E1]">
              {loading ? (
                <tr>
                  <td colSpan={6} className="py-12 text-center text-xs text-[#77827E]">
                    <Loader2 className="w-5 h-5 animate-spin mx-auto text-[#073B32] mb-2" />
                    <span>Loading authentic fleet records...</span>
                  </td>
                </tr>
              ) : records.length === 0 ? (
                <tr>
                  <td colSpan={6} className="py-12 text-center text-xs text-[#77827E]">
                    No vehicles matched the search criteria.
                  </td>
                </tr>
              ) : (
                records.map((r, i) => (
                  <tr key={i} className="hover:bg-[#F7F5F0]/50 transition-colors">
                    <td className="py-3.5 px-6 font-bold text-[#202A28]">
                      {r.name}
                    </td>
                    <td className="py-3.5 px-6 font-mono text-[#77827E]">
                      {r.year} <span className="text-[10px]">({r.car_age} yrs)</span>
                    </td>
                    <td className="py-3.5 px-6 font-mono text-[#202A28]">
                      {r.km_driven.toLocaleString()} km
                    </td>
                    <td className="py-3.5 px-6">
                      <span className="text-[#073B32] font-semibold">{r.fuel}</span> • <span className="text-[#77827E]">{r.transmission}</span>
                    </td>
                    <td className="py-3.5 px-6 text-[#77827E]">
                      {r.owner}
                    </td>
                    <td className="py-3.5 px-6 text-right font-bold text-[#073B32] font-mono text-sm">
                      {r.formatted_price}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination Bar */}
        <div className="p-4 border-t border-[#E4E8E1] flex items-center justify-between">
          <div className="text-xs text-[#77827E]">
            Showing {(page - 1) * PAGE_SIZE + 1} to {Math.min(page * PAGE_SIZE, total)} of {total} records
          </div>
          <div className="flex items-center space-x-2">
            <button
              onClick={() => setPage(p => Math.max(1, p - 1))}
              disabled={page === 1}
              className="p-2 rounded-xl border border-[#E4E8E1] bg-white text-[#202A28] hover:bg-[#F7F5F0] disabled:opacity-40 transition-colors"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <span className="text-xs font-bold text-[#073B32] px-2 font-mono">
              {page} / {totalPages}
            </span>
            <button
              onClick={() => setPage(p => Math.min(totalPages, p + 1))}
              disabled={page === totalPages}
              className="p-2 rounded-xl border border-[#E4E8E1] bg-white text-[#202A28] hover:bg-[#F7F5F0] disabled:opacity-40 transition-colors"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
