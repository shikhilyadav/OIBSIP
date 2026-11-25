import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { 
  Search, 
  Bell, 
  RefreshCw, 
  Activity, 
  User, 
  ShieldCheck 
} from 'lucide-react';
import { fetchHealth } from '../../api/client';

const pageTitles = {
  '/': 'Overview',
  '/detector': 'Message Detector',
  '/batch': 'Batch Analysis',
  '/models': 'Model Intelligence',
  '/dataset': 'Dataset Explorer',
  '/validation': 'Validation Lab',
  '/documentation': 'Documentation',
};

export default function Topbar() {
  const location = useLocation();
  const [health, setHealth] = useState({ status: 'checking' });
  const [isRefreshing, setIsRefreshing] = useState(false);

  const activeTitle = pageTitles[location.pathname] || 'Studio Workspace';

  const checkStatus = async () => {
    setIsRefreshing(true);
    try {
      const data = await fetchHealth();
      setHealth(data);
    } catch (e) {
      setHealth({ status: 'offline' });
    } finally {
      setIsRefreshing(false);
    }
  };

  useEffect(() => {
    checkStatus();
  }, []);

  const isOnline = health.status === 'healthy';

  return (
    <header className="h-16 bg-[#FFFCF8] border-b border-[#E4DAD0] px-6 lg:px-8 flex items-center justify-between sticky top-0 z-20 shadow-soft">
      {/* Breadcrumb Workspace */}
      <div className="flex items-center space-x-2 text-xs">
        <span className="font-semibold text-[#817A76]">Studio Workspace</span>
        <span className="text-[#D5BDA4]">/</span>
        <span className="font-extrabold text-[#542B38] text-sm tracking-tight font-display">
          {activeTitle}
        </span>
      </div>

      {/* Center/Search */}
      <div className="hidden md:flex items-center relative w-72 lg:w-96">
        <Search className="w-4 h-4 absolute left-3 text-[#817A76] pointer-events-none" />
        <input
          type="text"
          placeholder="Search threat indicators, model benchmarks..."
          className="w-full bg-[#F5F0E9] border border-[#E4DAD0] rounded-xl pl-9 pr-4 py-1.5 text-xs text-[#33302E] placeholder-[#817A76] focus:outline-none focus:border-[#A83F55] transition-colors"
        />
      </div>

      {/* Right Controls */}
      <div className="flex items-center space-x-3">
        {/* Backend Status Pill */}
        <div className="flex items-center space-x-2 px-3 py-1.5 rounded-xl bg-[#F5F0E9] border border-[#E4DAD0] text-xs font-mono">
          <span className={`w-2 h-2 rounded-full ${isOnline ? 'bg-emerald-500' : 'bg-rose-500'}`}></span>
          <span className="text-[#33302E] font-bold text-[11px]">
            {isOnline ? 'FastAPI :8000' : 'Offline'}
          </span>
        </div>

        {/* Refresh health */}
        <button
          onClick={checkStatus}
          disabled={isRefreshing}
          className="p-2 rounded-xl bg-[#F5F0E9] hover:bg-[#EAE1D7] border border-[#E4DAD0] text-[#542B38] transition-colors"
          title="Refresh Backend Health"
        >
          <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin text-[#A83F55]' : ''}`} />
        </button>

        {/* Notification Bell */}
        <button 
          className="p-2 rounded-xl bg-[#F5F0E9] hover:bg-[#EAE1D7] border border-[#E4DAD0] text-[#542B38] relative transition-colors"
          title="Notifications"
        >
          <Bell className="w-4 h-4" />
          <span className="w-2 h-2 rounded-full bg-[#A83F55] absolute top-1.5 right-1.5"></span>
        </button>

        {/* User Avatar */}
        <div className="w-8 h-8 rounded-xl bg-[#542B38] text-white flex items-center justify-center font-bold text-xs shadow-sm">
          <span>SA</span>
        </div>
      </div>
    </header>
  );
}
