import React from 'react';

export function StatCard({ title, value, subtitle, change, icon: Icon, color = 'emerald' }) {
  const colorMap = {
    emerald: 'text-cyber-accent border-emerald-500/20 bg-emerald-500/10',
    rose: 'text-cyber-danger border-rose-500/20 bg-rose-500/10',
    cyan: 'text-cyber-cyan border-cyan-500/20 bg-cyan-500/10',
    amber: 'text-cyber-warning border-amber-500/20 bg-amber-500/10',
    purple: 'text-purple-400 border-purple-500/20 bg-purple-500/10'
  };

  const badgeStyle = colorMap[color] || colorMap.emerald;

  return (
    <div className="bg-cyber-card border border-cyber-border rounded-xl p-5 hover:border-cyber-subtle transition-all">
      <div className="flex items-center justify-between mb-3">
        <span className="text-xs font-mono uppercase tracking-wider text-cyber-muted font-medium">
          {title}
        </span>
        {Icon && (
          <div className={`p-2 rounded-lg border ${badgeStyle}`}>
            <Icon className="w-4 h-4" />
          </div>
        )}
      </div>
      <div className="flex items-baseline space-x-2">
        <span className="text-2xl font-bold font-mono text-white tracking-tight">
          {value}
        </span>
        {change && (
          <span className="text-xs font-mono text-cyber-accent font-medium">
            {change}
          </span>
        )}
      </div>
      {subtitle && (
        <p className="text-xs text-cyber-muted mt-1.5 font-sans">
          {subtitle}
        </p>
      )}
    </div>
  );
}

export function RiskBadge({ level }) {
  const configs = {
    LOW: { label: 'LOW THREAT', bg: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30' },
    MEDIUM: { label: 'MEDIUM THREAT', bg: 'bg-amber-500/10 text-amber-400 border-amber-500/30' },
    HIGH: { label: 'HIGH RISK', bg: 'bg-rose-500/10 text-rose-400 border-rose-500/30' },
    CRITICAL: { label: 'CRITICAL THREAT', bg: 'bg-red-600/20 text-red-400 border-red-500/40 glow-danger' }
  };
  const c = configs[level] || configs.LOW;
  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-[11px] font-mono font-bold border ${c.bg}`}>
      {c.label}
    </span>
  );
}

export function DecisionBadge({ decision }) {
  if (decision === 'SPAM') {
    return (
      <span className="inline-flex items-center px-2.5 py-1 rounded-md text-xs font-mono font-bold bg-rose-500/15 text-cyber-danger border border-rose-500/30">
        SPAM / BLOCKED
      </span>
    );
  }
  if (decision === 'HAM') {
    return (
      <span className="inline-flex items-center px-2.5 py-1 rounded-md text-xs font-mono font-bold bg-emerald-500/15 text-cyber-accent border border-emerald-500/30">
        LEGITIMATE / HAM
      </span>
    );
  }
  return (
    <span className="inline-flex items-center px-2.5 py-1 rounded-md text-xs font-mono font-bold bg-amber-500/15 text-cyber-warning border border-amber-500/30">
      REVIEW QUEUE (θ=0.10-0.60)
    </span>
  );
}
