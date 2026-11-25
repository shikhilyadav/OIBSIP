import React, { useState, useEffect } from 'react';
import { NavLink } from 'react-router-dom';
import { 
  ShieldCheck, 
  LayoutDashboard, 
  ScanSearch, 
  Files, 
  Cpu, 
  Database, 
  FlaskConical, 
  BookOpen,
  Activity,
  CheckCircle2,
  AlertCircle
} from 'lucide-react';
import { fetchHealth } from '../../api/client';

const navItems = [
  { name: 'Overview', path: '/', icon: LayoutDashboard },
  { name: 'Message Detector', path: '/detector', icon: ScanSearch, badge: 'Live' },
  { name: 'Batch Analysis', path: '/batch', icon: Files },
  { name: 'Model Intelligence', path: '/models', icon: Cpu },
  { name: 'Dataset Explorer', path: '/dataset', icon: Database },
  { name: 'Validation Lab', path: '/validation', icon: FlaskConical },
  { name: 'Documentation', path: '/documentation', icon: BookOpen },
];

export default function Sidebar() {
  const [health, setHealth] = useState(null);

  useEffect(() => {
    fetchHealth()
      .then(setHealth)
      .catch(() => setHealth({ status: 'offline', engines: {} }));
    const interval = setInterval(() => {
      fetchHealth()
        .then(setHealth)
        .catch(() => setHealth({ status: 'offline', engines: {} }));
    }, 20000);
    return () => clearInterval(interval);
  }, []);

  const engines = health?.engines || {};
  const isHealthy = health?.status === 'healthy';

  return (
    <aside className="w-64 bg-[#542B38] text-white flex flex-col shrink-0 h-screen sticky top-0 select-none border-r border-[#421E2A] z-30">
      {/* Brand Header */}
      <div className="p-5 border-b border-white/10 flex items-center space-x-3">
        <div className="w-10 h-10 rounded-2xl bg-[#D5BDA4] text-[#542B38] flex items-center justify-center shadow-md shrink-0">
          <ShieldCheck className="w-6 h-6 stroke-[2.2]" />
        </div>
        <div className="min-w-0">
          <div className="flex items-center space-x-1.5">
            <span className="font-extrabold text-base tracking-tight font-display text-white">
              SpamShield
            </span>
            <span className="text-[10px] font-extrabold px-1.5 py-0.5 rounded bg-[#A83F55] text-white tracking-wider">
              AI
            </span>
          </div>
          <p className="text-[11px] text-[#D5BDA4] font-medium tracking-tight truncate">
            Intelligent Spam Detection
          </p>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
        <div className="text-[10px] font-bold uppercase text-[#D5BDA4]/70 px-3 mb-2 tracking-widest">
          Platform Workspace
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
                    ? 'bg-[#A83F55] text-white shadow-md font-bold'
                    : 'text-[#EAE1D7] hover:bg-white/10 hover:text-white'
                }`
              }
            >
              <div className="flex items-center space-x-3">
                <Icon className="w-4 h-4 shrink-0 opacity-90" />
                <span>{item.name}</span>
              </div>
              {item.badge && (
                <span className="text-[9px] font-bold px-1.5 py-0.5 rounded-full bg-[#D5BDA4] text-[#542B38] tracking-wider uppercase">
                  {item.badge}
                </span>
              )}
            </NavLink>
          );
        })}
      </nav>

      {/* ML Models Panel (Bottom) */}
      <div className="p-4 m-3 rounded-2xl bg-[#3D1D27]/80 border border-white/10 space-y-2.5">
        <div className="flex items-center justify-between">
          <span className="text-[10px] uppercase font-extrabold tracking-wider text-[#D5BDA4]">
            ML Models Cluster
          </span>
          <span className="flex h-2 w-2 relative">
            <span className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${isHealthy ? 'bg-emerald-400' : 'bg-amber-400'}`}></span>
            <span className={`relative inline-flex rounded-full h-2 w-2 ${isHealthy ? 'bg-emerald-500' : 'bg-amber-500'}`}></span>
          </span>
        </div>

        <div className="space-y-1.5 text-[11px]">
          <div className="flex items-center justify-between text-[#EAE1D7]">
            <span>Multinomial NB</span>
            <span className={`font-mono text-[10px] font-bold ${engines.naive_bayes ? 'text-emerald-300' : 'text-amber-300'}`}>
              {engines.naive_bayes ? 'ACTIVE' : 'READY'}
            </span>
          </div>
          <div className="flex items-center justify-between text-[#EAE1D7]">
            <span>Logistic Regression</span>
            <span className={`font-mono text-[10px] font-bold ${engines.logistic_regression ? 'text-emerald-300' : 'text-amber-300'}`}>
              {engines.logistic_regression ? 'ACTIVE' : 'READY'}
            </span>
          </div>
          <div className="flex items-center justify-between text-[#EAE1D7]">
            <span>BERT-Tiny (4.39M)</span>
            <span className={`font-mono text-[10px] font-bold ${engines.bert_tiny ? 'text-emerald-300' : 'text-amber-300'}`}>
              {engines.bert_tiny ? 'ACTIVE' : 'READY'}
            </span>
          </div>
        </div>
      </div>
    </aside>
  );
}
