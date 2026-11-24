import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { Activity, RefreshCw, Sparkles, CheckCircle2 } from 'lucide-react';
import { checkHealth, HealthResponse } from '../../api/client';

export default function Topbar() {
  const location = useLocation();
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [isChecking, setIsChecking] = useState(false);

  const routeNames: Record<string, string> = {
    '/': 'Overview & Botanical Dashboard',
    '/classifier': 'Botanical Specimen Classifier',
    '/dataset': 'Botanical Dataset Explorer',
    '/insights': 'Species Morphology & Insights',
    '/performance': 'Model Diagnostics & Scientific Evaluation',
  };

  const currentTitle = routeNames[location.pathname] || 'IrisAI Studio';

  const verifyHealth = async () => {
    setIsChecking(true);
    try {
      const data = await checkHealth();
      setHealth(data);
    } catch {
      setHealth({
        status: 'offline',
        model_loaded: false,
        dataset_loaded: false,
        version: '2.0.0',
        model_name: 'Unavailable'
      });
    } finally {
      setIsChecking(false);
    }
  };

  useEffect(() => {
    verifyHealth();
    const interval = setInterval(verifyHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <header className="h-16 bg-white border-b border-[#E3EBE3] px-6 lg:px-8 flex items-center justify-between sticky top-0 z-20 shadow-sm">
      {/* Breadcrumb & Page Title */}
      <div className="flex items-center space-x-3">
        <span className="text-xs font-bold text-[#8BAA91] tracking-wider uppercase">
          Studio Workspace
        </span>
        <span className="text-[#E3EBE3]">/</span>
        <h1 className="text-sm font-bold text-[#19362A] tracking-tight">
          {currentTitle}
        </h1>
      </div>

      {/* Right Controls */}
      <div className="flex items-center space-x-3">
        <div className="flex items-center space-x-2 px-3 py-1.5 rounded-full bg-[#EFF8F0] border border-[#DFF4E5] text-xs font-medium text-[#285943]">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#5C9A72] opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-[#285943]"></span>
          </span>
          <span className="font-bold">
            {health?.status === 'healthy' ? 'FastAPI Active' : 'Connecting Backend...'}
          </span>
        </div>

        <button
          onClick={verifyHealth}
          disabled={isChecking}
          title="Refresh Backend Connectivity"
          className="p-2 rounded-xl bg-white hover:bg-[#F7FAF7] border border-[#E3EBE3] text-[#728177] hover:text-[#19362A] transition-colors"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${isChecking ? 'animate-spin text-[#285943]' : ''}`} />
        </button>
      </div>
    </header>
  );
}
