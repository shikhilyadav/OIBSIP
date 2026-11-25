import React, { useState, useEffect } from 'react';
import { NavLink } from 'react-router-dom';
import { 
  Gauge, 
  Calculator, 
  Database, 
  Cpu, 
  BarChart2, 
  BookOpen, 
  Car, 
  Sparkles
} from 'lucide-react';
import { fetchHealth } from '../../api/client';

const navItems = [
  { name: 'Overview', path: '/', icon: Gauge },
  { name: 'Price Predictor', path: '/predictor', icon: Calculator, badge: 'Valuation' },
  { name: 'Data Explorer', path: '/dataset', icon: Database },
  { name: 'Model Intelligence', path: '/models', icon: Cpu },
  { name: 'Evaluation', path: '/evaluation', icon: BarChart2 },
  { name: 'Documentation', path: '/documentation', icon: BookOpen },
];

export default function Sidebar() {
  const [health, setHealth] = useState<any>(null);

  useEffect(() => {
    fetchHealth().then(setHealth).catch(() => setHealth({ status: 'offline' }));
  }, []);

  const isOnline = health?.status === 'healthy';

  return (
    <aside className="w-64 bg-[#063B32] text-white flex flex-col shrink-0 h-screen sticky top-0 select-none border-r border-[#032620] z-30 relative overflow-hidden">
      {/* Subtle automotive road curve vector background */}
      <svg 
        className="absolute inset-0 w-full h-full pointer-events-none opacity-5 z-0" 
        xmlns="http://www.w3.org/2000/svg" 
        viewBox="0 0 256 900" 
        fill="none" 
        stroke="currentColor"
      >
        <path d="M-50,150 Q100,280 40,480 T180,750" strokeWidth="2" strokeDasharray="6 6" />
        <path d="M50,100 Q200,250 140,450 T280,720" strokeWidth="1.5" />
        <circle cx="128" cy="800" r="160" strokeWidth="1" />
      </svg>

      {/* Top Branding Header */}
      <div className="p-5 border-b border-white/10 flex items-center space-x-3 relative z-10">
        <div className="w-10 h-10 rounded-2xl bg-[#E8B956] text-[#063B32] flex items-center justify-center shadow-lg shadow-[#032620]/40 shrink-0">
          <Car className="w-5 h-5 stroke-[2.2]" />
        </div>
        <div className="min-w-0">
          <div className="flex items-center space-x-1.5">
            <span className="font-extrabold text-base tracking-tight font-display text-white">
              AutoValue
            </span>
            <span className="text-[10px] font-black px-1.5 py-0.5 rounded bg-[#E8B956] text-[#063B32] tracking-wider uppercase">
              AI
            </span>
          </div>
          <p className="text-[11px] text-[#B8D1C7] font-medium tracking-tight truncate">
            Car Price Prediction
          </p>
        </div>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 px-3 py-4 space-y-1.5 overflow-y-auto relative z-10">
        <div className="text-[10px] font-bold uppercase text-[#B8D1C7]/70 px-3 mb-2 tracking-widest">
          Automotive Intelligence
        </div>
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-semibold transition-all duration-200 group ${
                  isActive
                    ? 'bg-[#17634D] text-[#E8B956] shadow-md border-l-4 border-[#E8B956] font-bold'
                    : 'text-[#B8D1C7] hover:bg-white/5 hover:text-white'
                }`
              }
            >
              <div className="flex items-center space-x-3">
                <Icon className="w-4 h-4 shrink-0 text-white group-hover:scale-105 transition-transform" />
                <span>{item.name}</span>
              </div>
              {item.badge && (
                <span className="text-[9px] font-extrabold px-1.5 py-0.5 rounded-full bg-[#E8B956] text-[#063B32] tracking-wider uppercase">
                  {item.badge}
                </span>
              )}
            </NavLink>
          );
        })}
      </nav>

      {/* Dedicated Bottom OIBSIP Task 3 Card */}
      <div className="p-4 m-3 rounded-2xl bg-[#032620]/90 border border-white/10 space-y-2 relative z-10 shadow-lg">
        <div className="flex items-center justify-between">
          <span className="text-[10px] uppercase font-black tracking-widest text-[#E8B956]">
            OIBSIP — TASK 3
          </span>
          <span className="flex h-2 w-2 relative">
            <span className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${isOnline ? 'bg-emerald-400' : 'bg-amber-400'}`}></span>
            <span className={`relative inline-flex rounded-full h-2 w-2 ${isOnline ? 'bg-emerald-500' : 'bg-amber-500'}`}></span>
          </span>
        </div>
        <div className="text-xs font-bold text-white leading-tight">
          Car Price Prediction
        </div>
        <div className="text-[10px] text-[#B8D1C7] leading-tight">
          Machine Learning • Regression Pipeline
        </div>
        <div className="inline-flex items-center space-x-1.5 px-2.5 py-1 rounded-lg bg-[#17634D] text-[#E8B956] text-[10px] font-mono font-bold w-full justify-center">
          <Sparkles className="w-3 h-3 shrink-0" />
          <span>Champion R² = 0.7120</span>
        </div>
      </div>
    </aside>
  );
}
