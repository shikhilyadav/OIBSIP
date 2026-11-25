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
  ShieldCheck, 
  Sparkles,
  Zap
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
    <aside className="w-64 bg-[#073B32] text-white flex flex-col shrink-0 h-screen sticky top-0 select-none border-r border-[#04241E] z-30">
      {/* Brand Header */}
      <div className="p-5 border-b border-white/10 flex items-center space-x-3">
        <div className="w-10 h-10 rounded-2xl bg-[#E6B85C] text-[#073B32] flex items-center justify-center shadow-md shrink-0">
          <Car className="w-5 h-5 stroke-[2.2]" />
        </div>
        <div className="min-w-0">
          <div className="flex items-center space-x-1.5">
            <span className="font-extrabold text-base tracking-tight font-display text-white">
              AutoValue
            </span>
            <span className="text-[10px] font-extrabold px-1.5 py-0.5 rounded bg-[#E6B85C] text-[#073B32] tracking-wider">
              AI
            </span>
          </div>
          <p className="text-[11px] text-[#E6B85C]/90 font-medium tracking-tight truncate">
            Car Price Prediction Platform
          </p>
        </div>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
        <div className="text-[10px] font-bold uppercase text-[#E6B85C]/70 px-3 mb-2 tracking-widest">
          Automotive Intelligence
        </div>
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-semibold transition-all duration-200 ${
                  isActive
                    ? 'bg-[#125B48] text-[#E6B85C] shadow-md border-l-4 border-[#E6B85C] font-bold'
                    : 'text-[#F7F5F0]/80 hover:bg-white/5 hover:text-white'
                }`
              }
            >
              <div className="flex items-center space-x-3">
                <Icon className="w-4 h-4 shrink-0 opacity-90" />
                <span>{item.name}</span>
              </div>
              {item.badge && (
                <span className="text-[9px] font-bold px-1.5 py-0.5 rounded-full bg-[#E6B85C] text-[#073B32] tracking-wider uppercase">
                  {item.badge}
                </span>
              )}
            </NavLink>
          );
        })}
      </nav>

      {/* Bottom Task Badge */}
      <div className="p-4 m-3 rounded-2xl bg-[#04241E]/80 border border-white/10 space-y-2">
        <div className="flex items-center justify-between">
          <span className="text-[10px] uppercase font-extrabold tracking-wider text-[#E6B85C]">
            OIBSIP — Task 3
          </span>
          <span className="flex h-2 w-2 relative">
            <span className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${isOnline ? 'bg-emerald-400' : 'bg-amber-400'}`}></span>
            <span className={`relative inline-flex rounded-full h-2 w-2 ${isOnline ? 'bg-emerald-500' : 'bg-amber-500'}`}></span>
          </span>
        </div>
        <div className="text-[11px] text-[#F7F5F0]/80 leading-snug">
          Car Price Prediction
        </div>
        <div className="inline-flex items-center space-x-1.5 px-2 py-0.5 rounded-lg bg-[#125B48] text-[#E6B85C] text-[10px] font-mono font-bold">
          <Sparkles className="w-3 h-3" />
          <span>Regression Pipeline (R²: 0.712)</span>
        </div>
      </div>
    </aside>
  );
}
