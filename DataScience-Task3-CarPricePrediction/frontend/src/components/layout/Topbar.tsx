import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { 
  Search, 
  Bell, 
  RefreshCw, 
  Car, 
  Activity, 
  ShieldCheck 
} from 'lucide-react';
import { fetchHealth } from '../../api/client';

const pageTitles: Record<string, string> = {
  '/': 'Cockpit Overview',
  '/predictor': 'Vehicle Valuation Calculator',
  '/dataset': 'Fleet Dataset Explorer',
  '/models': 'Model Intelligence & Feature Impact',
  '/evaluation': 'Scientific Model Diagnostics',
  '/documentation': 'Platform Documentation',
};

export default function Topbar() {
  const location = useLocation();
  const [health, setHealth] = useState({ status: 'checking', algorithm: 'Linear Regression' });
  const [isRefreshing, setIsRefreshing] = useState(false);

  const activeTitle = pageTitles[location.pathname] || 'Studio Workspace';

  const checkStatus = async () => {
    setIsRefreshing(true);
    try {
      const data = await fetchHealth();
      setHealth(data);
    } catch (e) {
      setHealth({ status: 'offline', algorithm: 'Offline' });
    } finally {
      setIsRefreshing(false);
    }
  };

  useEffect(() => {
    checkStatus();
  }, []);

  const isOnline = health.status === 'healthy';

  return (
    <header className="h-16 bg-[#FFFFFF] border-b border-[#E4E8E1] px-6 lg:px-8 flex items-center justify-between sticky top-0 z-20 shadow-soft">
      {/* Breadcrumb Workspace */}
      <div className="flex items-center space-x-2 text-xs">
        <span className="font-semibold text-[#77827E]">Studio Workspace</span>
        <span className="text-[#E6B85C]">/</span>
        <span className="font-extrabold text-[#073B32] text-sm tracking-tight font-display">
          {activeTitle}
        </span>
      </div>

      {/* Center Search Input */}
      <div className="hidden md:flex items-center relative w-72 lg:w-96">
        <Search className="w-4 h-4 absolute left-3 text-[#77827E] pointer-events-none" />
        <input
          type="text"
          placeholder="Search car makes, models, or market insights..."
          className="w-full bg-[#F7F5F0] border border-[#E4E8E1] rounded-xl pl-9 pr-4 py-1.5 text-xs text-[#202A28] placeholder-[#77827E] focus:outline-none focus:border-[#125B48] transition-colors"
        />
      </div>

      {/* Right Controls */}
      <div className="flex items-center space-x-3">
        {/* Backend Status Pill */}
        <div className="flex items-center space-x-2 px-3 py-1.5 rounded-xl bg-[#F7F5F0] border border-[#E4E8E1] text-xs font-mono">
          <span className={`w-2 h-2 rounded-full ${isOnline ? 'bg-emerald-500' : 'bg-rose-500'}`}></span>
          <span className="text-[#202A28] font-bold text-[11px]">
            {isOnline ? 'FastAPI :8002' : 'Offline'}
          </span>
        </div>

        {/* Refresh health */}
        <button
          onClick={checkStatus}
          disabled={isRefreshing}
          className="p-2 rounded-xl bg-[#F7F5F0] hover:bg-[#EFECE3] border border-[#E4E8E1] text-[#073B32] transition-colors"
          title="Refresh Backend Health"
        >
          <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin text-[#E6B85C]' : ''}`} />
        </button>

        {/* Notification Bell */}
        <button 
          className="p-2 rounded-xl bg-[#F7F5F0] hover:bg-[#EFECE3] border border-[#E4E8E1] text-[#073B32] relative transition-colors"
          title="Notifications"
        >
          <Bell className="w-4 h-4" />
          <span className="w-2 h-2 rounded-full bg-[#E6B85C] absolute top-1.5 right-1.5"></span>
        </button>

        {/* User Avatar */}
        <div className="w-8 h-8 rounded-xl bg-[#073B32] text-[#E6B85C] flex items-center justify-center font-bold text-xs shadow-sm">
          <span>AV</span>
        </div>
      </div>
    </header>
  );
}
