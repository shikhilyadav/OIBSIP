/**
 * Central API Client for IrisAI Botanical Studio
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

export interface PredictionInput {
  sepal_length: number;
  sepal_width: number;
  petal_length: number;
  petal_width: number;
}

export interface PredictionResult {
  class_id: number;
  species: string;
  confidence: number;
  probabilities: {
    setosa: number;
    versicolor: number;
    virginica: number;
  };
}

export interface PredictionResponse {
  success: boolean;
  prediction: PredictionResult;
  input: PredictionInput;
  model_name: string;
}

export interface HealthResponse {
  status: string;
  model_loaded: boolean;
  dataset_loaded: boolean;
  version: string;
  model_name: string;
}

export interface DatasetSummary {
  total_specimens: number;
  distinct_species: number;
  species_names: string[];
  feature_names: string[];
  class_distribution: Record<string, number>;
  descriptive_statistics: Record<string, Record<string, number>>;
}

export interface SpeciesInsightItem {
  species: string;
  count: number;
  means: Record<string, number>;
  stds: Record<string, number>;
  mins: Record<string, number>;
  maxs: Record<string, number>;
  profile: {
    tagline: string;
    accent: string;
    description: string;
    morphology: string;
  };
}

export async function checkHealth(): Promise<HealthResponse> {
  const res = await fetch(`${API_BASE_URL}/health`);
  if (!res.ok) throw new Error('Backend health check failed');
  return res.json();
}

export async function predictSpecimen(input: PredictionInput): Promise<PredictionResponse> {
  const res = await fetch(`${API_BASE_URL}/predict`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(input),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Prediction request failed');
  }
  return res.json();
}

export async function fetchDatasetSummary(): Promise<DatasetSummary> {
  const res = await fetch(`${API_BASE_URL}/dataset/summary`);
  if (!res.ok) throw new Error('Failed to load dataset summary');
  return res.json();
}

export async function fetchDatasetRecords(params: { species?: string; search?: string; page?: number; page_size?: number } = {}) {
  const q = new URLSearchParams();
  if (params.species && params.species !== 'all') q.append('species', params.species);
  if (params.search) q.append('search', params.search);
  if (params.page) q.append('page', params.page.toString());
  if (params.page_size) q.append('page_size', params.page_size.toString());

  const res = await fetch(`${API_BASE_URL}/dataset/records?${q.toString()}`);
  if (!res.ok) throw new Error('Failed to fetch dataset records');
  return res.json();
}

export async function fetchSpeciesInsights(): Promise<{ insights: Record<string, SpeciesInsightItem> }> {
  const res = await fetch(`${API_BASE_URL}/species/insights`);
  if (!res.ok) throw new Error('Failed to load species insights');
  return res.json();
}

export async function fetchMetrics(): Promise<any> {
  const res = await fetch(`${API_BASE_URL}/metrics`);
  if (!res.ok) throw new Error('Failed to load model metrics');
  return res.json();
}
