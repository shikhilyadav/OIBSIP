/**
 * SpamGuard AI - Central API Client
 */
const API_BASE = '/api';

export async function fetchHealth() {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) throw new Error('Health check failed');
  return res.json();
}

export async function fetchModels() {
  const res = await fetch(`${API_BASE}/models`);
  if (!res.ok) throw new Error('Failed to fetch models');
  return res.json();
}

export async function fetchBenchmarkMetrics() {
  const res = await fetch(`${API_BASE}/metrics/benchmark`);
  if (!res.ok) throw new Error('Failed to fetch benchmark metrics');
  return res.json();
}

export async function fetchAnalytics() {
  const res = await fetch(`${API_BASE}/metrics/analytics`);
  if (!res.ok) throw new Error('Failed to fetch analytics');
  return res.json();
}

export async function fetchThreatIntel() {
  const res = await fetch(`${API_BASE}/threat-intel`);
  if (!res.ok) throw new Error('Failed to fetch threat intelligence');
  return res.json();
}

export async function fetchHistory(params = {}) {
  const query = new URLSearchParams();
  const filterVal = params.filter || params.label;
  if (filterVal) query.append('filter', filterVal);
  if (params.threat_level) query.append('threat_level', params.threat_level);
  if (params.search) query.append('search', params.search);
  if (params.page) query.append('page', params.page);
  if (params.page_size) query.append('page_size', params.page_size);
  if (params.limit) query.append('limit', params.limit);

  const res = await fetch(`${API_BASE}/history?${query.toString()}`);
  if (!res.ok) throw new Error('Failed to fetch history');
  return res.json();
}

export async function clearHistory() {
  const res = await fetch(`${API_BASE}/history`, { method: 'DELETE' });
  if (!res.ok) throw new Error('Failed to clear history');
  return res.json();
}

export async function analyzeMessage(text, modelId = 'hybrid', detailedTokens = true) {
  const res = await fetch(`${API_BASE}/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message: text,
      text: text,
      model_preference: modelId,
      model_id: modelId,
      detailed_tokens: detailedTokens
    })
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || 'Inference analysis failed');
  }
  return res.json();
}

