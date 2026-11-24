import React, { useState, useEffect } from 'react';
import { ShieldCheck, ShieldAlert, Users, Zap, ArrowUpRight, Activity } from 'lucide-react';
import { StatCard } from '../components/common/Cards';
import { fetchAnalytics } from '../api/client';
import { 
  ResponsiveContainer, 
  AreaChart, 
  Area, 
  XAxis, 
  YAxis, 
  Tooltip, 
  PieChart, 
  Pie, 
  Cell 
} from 'recharts';

export default function OverviewPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAnalytics()
      .then(setData)
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  if (loading || !data) {
    return (
      <div className="flex items-center justify-center h-64 text-cyber-muted font-mono text-sm">
        <Activity className="w-5 h-5 animate-spin mr-2 text-cyber-accent" />
        Loading Threat Telemetry...
      </div>
    );
  }

  const { kpis, detection_trend, threat_distribution } = data;

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b border-cyber-border pb-5">
        <div>
          <h1 className="text-2xl font-bold font-mono text-white tracking-tight flex items-center gap-2">
            Enterprise Threat Telemetry
          </h1>
          <p className="text-sm text-cyber-muted mt-1">
            Real-time hybrid NLP inference, abstention routing & automated quarantine overview.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-mono font-medium bg-emerald-500/10 text-cyber-accent border border-emerald-500/30">
            <span className="w-2 h-2 rounded-full bg-cyber-accent animate-pulse"></span>
            Triage Active: θ=[0.10, 0.60]
          </span>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Total Messages Scanned"
          value={kpis.total_scans}
          subtitle="Processed through hybrid triage"
          icon={Activity}
          color="cyan"
        />
        <StatCard
          title="Threats Quarantined"
          value={kpis.threats_neutralized}
          subtitle="Malicious shortcodes & phish"
          icon={ShieldAlert}
          color="rose"
        />
        <StatCard
          title="Selective Accuracy"
          value={`${kpis.hybrid_selective_accuracy}%`}
          subtitle="On automated decisions (80.9% coverage)"
          icon={ShieldCheck}
          color="emerald"
        />
        <StatCard
          title="Avg Inference Latency"
          value={`${kpis.average_inspection_latency_ms} ms`}
          subtitle="CPU optimized pipeline"
          icon={Zap}
          color="amber"
        />
      </div>

      {/* Chart Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Trend Area Chart */}
        <div className="lg:col-span-2 bg-cyber-card border border-cyber-border rounded-xl p-5">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-sm font-semibold font-mono text-white uppercase tracking-wider">
                Detection Velocity (7 Days)
              </h2>
              <p className="text-xs text-cyber-muted">Clean vs Quarantined vs Review Queue</p>
            </div>
            <div className="flex items-center gap-3 text-xs font-mono">
              <span className="flex items-center gap-1 text-cyber-accent">
                <span className="w-2.5 h-2.5 rounded-full bg-cyber-accent"></span> Clean
              </span>
              <span className="flex items-center gap-1 text-cyber-danger">
                <span className="w-2.5 h-2.5 rounded-full bg-cyber-danger"></span> Spam
              </span>
              <span className="flex items-center gap-1 text-amber-400">
                <span className="w-2.5 h-2.5 rounded-full bg-amber-400"></span> Review
              </span>
            </div>
          </div>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={detection_trend}>
                <defs>
                  <linearGradient id="cleanGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#00F5A0" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#00F5A0" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="spamGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#FF3B5C" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#FF3B5C" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <XAxis dataKey="day" stroke="#475569" tick={{ fill: '#8A99AD', fontSize: 11 }} />
                <YAxis stroke="#475569" tick={{ fill: '#8A99AD', fontSize: 11 }} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0D1422', borderColor: '#1E2D44', borderRadius: '8px' }}
                  labelStyle={{ color: '#E2E8F0', fontFamily: 'monospace' }}
                />
                <Area type="monotone" dataKey="clean" stroke="#00F5A0" fillOpacity={1} fill="url(#cleanGrad)" />
                <Area type="monotone" dataKey="spam" stroke="#FF3B5C" fillOpacity={1} fill="url(#spamGrad)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Threat Distribution Donut */}
        <div className="bg-cyber-card border border-cyber-border rounded-xl p-5">
          <h2 className="text-sm font-semibold font-mono text-white uppercase tracking-wider mb-1">
            Attack Vector Profile
          </h2>
          <p className="text-xs text-cyber-muted mb-4">Structural pattern breakdown</p>
          <div className="h-48">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={threat_distribution}
                  cx="50%"
                  cy="50%"
                  innerRadius={50}
                  outerRadius={75}
                  paddingAngle={4}
                  dataKey="value"
                >
                  {threat_distribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{ backgroundColor: '#0D1422', borderColor: '#1E2D44', borderRadius: '8px' }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="space-y-1.5 mt-2">
            {threat_distribution.map((item, idx) => (
              <div key={idx} className="flex items-center justify-between text-xs font-mono">
                <span className="flex items-center gap-1.5 text-slate-300">
                  <span className="w-2 h-2 rounded-full" style={{ backgroundColor: item.color }}></span>
                  {item.name}
                </span>
                <span className="text-white font-bold">{item.value}%</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
