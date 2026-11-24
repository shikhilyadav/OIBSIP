import React from 'react';
import { Cpu, Zap, Activity } from 'lucide-react';

export default function ModelScoreCard({ modelKey, scoreData }) {
  if (!scoreData) return null;

  const isSpam = scoreData.predicted_label === 'SPAM';
  const spamPct = Math.round(scoreData.spam_probability * 100);

  return (
    <div className="bg-cyber-surface border border-cyber-border rounded-lg p-4">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center space-x-2">
          <Cpu className="w-4 h-4 text-cyber-cyan" />
          <span className="text-sm font-semibold text-white font-mono">
            {scoreData.display_name}
          </span>
        </div>
        <span
          className={`text-[10px] font-mono px-2 py-0.5 rounded border font-bold ${
            isSpam
              ? 'bg-rose-500/10 text-cyber-danger border-rose-500/30'
              : 'bg-emerald-500/10 text-cyber-accent border-emerald-500/30'
          }`}
        >
          {scoreData.predicted_label}
        </span>
      </div>

      <p className="text-xs text-cyber-muted font-sans mb-3 line-clamp-1">
        {scoreData.architecture}
      </p>

      {/* Progress Bar */}
      <div className="space-y-1 mb-3">
        <div className="flex justify-between text-xs font-mono">
          <span className="text-slate-400">Spam Probability</span>
          <span className={isSpam ? 'text-cyber-danger font-bold' : 'text-cyber-accent font-bold'}>
            {spamPct}%
          </span>
        </div>
        <div className="w-full bg-cyber-card h-2 rounded-full overflow-hidden border border-cyber-border">
          <div
            className={`h-full transition-all duration-500 ${
              isSpam ? 'bg-cyber-danger' : 'bg-cyber-accent'
            }`}
            style={{ width: `${spamPct}%` }}
          />
        </div>
      </div>

      {/* Latency & Logits */}
      <div className="flex items-center justify-between text-[11px] font-mono text-cyber-muted border-t border-cyber-border/60 pt-2">
        <span className="flex items-center space-x-1">
          <Zap className="w-3 h-3 text-amber-400" />
          <span>{scoreData.latency_ms} ms</span>
        </span>
        {scoreData.raw_logits && (
          <span className="text-[10px]">
            Logits: [{scoreData.raw_logits.join(', ')}]
          </span>
        )}
      </div>
    </div>
  );
}
