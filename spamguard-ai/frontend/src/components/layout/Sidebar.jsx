import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  ShieldAlert, 
  LayoutDashboard, 
  ScanSearch, 
  Cpu, 
  BarChart3, 
  Terminal, 
  History, 
  Settings,
  ShieldCheck,
  Radio
} from 'lucide-react';

const navItems = [
  { name: 'Overview', path: '/', icon: LayoutDashboard },
  { name: 'Message Analyzer', path: '/analyzer', icon: ScanSearch, badge: 'Active' },
  { name: 'Model Intelligence', path: '/models', icon: Cpu },
  { name: 'Performance Analytics', path: '/analytics', icon: BarChart3 },
  { name: 'Threat Intelligence', path: '/threat-intel', icon: Terminal },
  { name: 'Scan History', path: '/history', icon: History },
  { name: 'Settings', path: '/settings', icon: Settings },
];

export default function Sidebar() {
  return (
    <aside className="w-64 bg-cyber-card border-r border-cyber-border flex flex-col shrink-0 h-screen sticky top-0 select-none">
      {/* Brand Header */}
      <div className="p-5 border-b border-cyber-border flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-9 h-9 rounded-lg bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center glow-accent">
            <ShieldCheck className="w-5 h-5 text-cyber-accent" />
          </div>
          <div>
            <div className="flex items-center space-x-1.5">
              <span className="font-bold tracking-tight text-white font-mono text-base">SpamGuard</span>
              <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-emerald-500/20 text-cyber-accent uppercase border border-emerald-500/30">AI</span>
            </div>
            <p className="text-[11px] text-cyber-muted font-medium">SecOps Intelligence</p>
          </div>
        </div>
      </div>

      {/* Engine Status Banner */}
      <div className="mx-4 mt-4 p-2.5 rounded-lg bg-cyber-surface/60 border border-cyber-border/80 flex items-center justify-between text-xs">
        <div className="flex items-center space-x-2">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
          </span>
          <span className="text-slate-300 font-mono text-[11px]">Hybrid Engine</span>
        </div>
        <span className="text-[10px] text-cyber-accent font-mono font-medium">ONLINE</span>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
        <div className="text-[10px] font-mono uppercase text-cyber-muted px-3 mb-2 font-semibold tracking-wider">
          Security Console
        </div>
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center justify-between px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-cyber-surface text-white border-l-2 border-cyber-accent shadow-sm'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-cyber-surface/50'
                }`
              }
            >
              <div className="flex items-center space-x-3">
                <Icon className="w-4 h-4 shrink-0 text-slate-400 group-hover:text-white" />
                <span>{item.name}</span>
              </div>
              {item.badge && (
                <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-cyber-accent/15 text-cyber-accent border border-cyber-accent/30 font-semibold">
                  {item.badge}
                </span>
              )}
            </NavLink>
          );
        })}
      </nav>

      {/* Footer Info */}
      <div className="p-4 border-t border-cyber-border text-xs text-cyber-muted">
        <div className="flex items-center justify-between font-mono text-[11px] mb-1">
          <span>Triage Policy</span>
          <span className="text-slate-300">θ=0.60/0.10</span>
        </div>
        <div className="flex items-center justify-between font-mono text-[11px]">
          <span>Ensemble</span>
          <span className="text-emerald-400 font-medium">BERT + MNB</span>
        </div>
      </div>
    </aside>
  );
}
