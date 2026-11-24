import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  ScanEye,
  Database,
  Flower2,
  Award,
  Sparkles,
  Layers,
  Leaf
} from 'lucide-react';

const navItems = [
  { name: 'Overview', path: '/', icon: LayoutDashboard },
  { name: 'Flower Classifier', path: '/classifier', icon: ScanEye, badge: 'Inference' },
  { name: 'Dataset Explorer', path: '/dataset', icon: Database },
  { name: 'Species Insights', path: '/insights', icon: Flower2 },
  { name: 'Model Performance', path: '/performance', icon: Award },
];

export default function Sidebar() {
  return (
    <aside className="w-64 bg-white border-r border-[#E3EBE3] flex flex-col shrink-0 h-screen sticky top-0 select-none z-10">
      {/* Brand Header */}
      <div className="p-6 border-b border-[#E3EBE3]">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-[#DFF4E5] border border-[#C7E2CE] flex items-center justify-center text-[#285943] shadow-sm">
            <Leaf className="w-5 h-5 text-[#285943]" />
          </div>
          <div>
            <div className="flex items-center space-x-1.5">
              <span className="font-extrabold tracking-tight text-[#19362A] text-lg font-sans">IrisAI</span>
              <span className="text-[10px] font-bold px-1.5 py-0.5 rounded-full bg-[#DFF4E5] text-[#285943] uppercase tracking-wider">
                Studio
              </span>
            </div>
            <p className="text-[11px] text-[#728177] font-medium tracking-wide">
              Botanical Intelligence
            </p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 py-5 space-y-1.5 overflow-y-auto">
        <div className="text-[10px] uppercase font-bold tracking-wider text-[#8BAA91] px-3 mb-2">
          Laboratory Console
        </div>
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center justify-between px-3.5 py-2.5 rounded-xl text-sm font-semibold transition-all ${
                  isActive
                    ? 'bg-[#EFF8F0] text-[#173D2D] font-bold border-l-4 border-[#285943] shadow-sm'
                    : 'text-[#728177] hover:text-[#19362A] hover:bg-[#F7FAF7]'
                }`
              }
            >
              <div className="flex items-center space-x-3">
                <Icon className="w-4 h-4 shrink-0" />
                <span>{item.name}</span>
              </div>
              {item.badge && (
                <span className="text-[10px] px-2 py-0.5 rounded-full bg-[#DFF4E5] text-[#285943] font-bold tracking-tight">
                  {item.badge}
                </span>
              )}
            </NavLink>
          );
        })}
      </nav>

      {/* Model Spec Footer */}
      <div className="p-4 mx-3 mb-4 rounded-xl bg-[#F7FAF7] border border-[#E3EBE3] text-xs text-[#728177] space-y-2">
        <div className="flex items-center justify-between font-semibold">
          <span className="text-[#19362A]">Engine Model</span>
          <span className="text-[#285943] font-bold">Random Forest</span>
        </div>
        <div className="flex items-center justify-between text-[11px]">
          <span>Test Accuracy</span>
          <span className="font-bold text-[#285943]">96.67% (Audited)</span>
        </div>
        <div className="flex items-center justify-between text-[11px]">
          <span>Taxonomy</span>
          <span>Fisher's 3 Species</span>
        </div>
      </div>
    </aside>
  );
}
