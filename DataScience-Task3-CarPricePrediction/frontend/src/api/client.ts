/**
 * AutoValue AI — Central API Client
 */

const API_BASE = '/api';

export interface PredictInput {
  brand: string;
  year: number;
  km_driven: number;
  fuel: string;
  seller_type: string;
  transmission: string;
  owner: string;
}

export interface PredictResult {
  predicted_price: number;
  formatted_price: string;
  price_in_lakhs: number;
  lower_bound: number;
  upper_bound: number;
  inputs: PredictInput & { car_age: number };
  model_used: string;
  timestamp: string;
}

export interface PredictResponse {
  success: boolean;
  data: PredictResult;
}

export interface DatasetSummary {
  total_records: number;
  unique_brands: number;
  unique_models: number;
  number_of_features: number;
  target_variable: string;
  selected_algorithm: string;
  test_r2_score: number;
  average_price: number;
  median_price: number;
  average_km: number;
  average_age: number;
  year_range: { min: number; max: number };
  price_range: { min: number; max: number };
}

export interface DatasetOptions {
  brands: string[];
  fuels: string[];
  transmissions: string[];
  seller_types: string[];
  owners: string[];
  years: number[];
}

export interface CarRecord {
  name: string;
  year: number;
  selling_price: number;
  formatted_price: string;
  km_driven: number;
  fuel: string;
  seller_type: string;
  transmission: string;
  owner: string;
  brand: string;
  car_age: number;
}

export interface RecordsResponse {
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
  records: CarRecord[];
}

export interface FeatureImportanceItem {
  feature: string;
  display_name: string;
  coefficient: number;
  abs_impact: number;
  direction: 'positive' | 'negative';
}

export async function fetchHealth() {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) throw new Error('Health check failed');
  return res.json();
}

export async function predictPrice(input: PredictInput): Promise<PredictResponse> {
  const res = await fetch(`${API_BASE}/predict`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(input)
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Valuation prediction failed');
  }
  return res.json();
}

export async function fetchDatasetSummary(): Promise<DatasetSummary> {
  const res = await fetch(`${API_BASE}/dataset/summary`);
  if (!res.ok) throw new Error('Failed to fetch dataset summary');
  return res.json();
}

export async function fetchDatasetOptions(): Promise<DatasetOptions> {
  const res = await fetch(`${API_BASE}/dataset/options`);
  if (!res.ok) throw new Error('Failed to fetch dataset options');
  return res.json();
}

export async function fetchDatasetRecords(params: {
  brand?: string;
  fuel?: string;
  transmission?: string;
  min_year?: number;
  max_year?: number;
  search?: string;
  page?: number;
  page_size?: number;
} = {}): Promise<RecordsResponse> {
  const query = new URLSearchParams();
  if (params.brand && params.brand !== 'all') query.append('brand', params.brand);
  if (params.fuel && params.fuel !== 'all') query.append('fuel', params.fuel);
  if (params.transmission && params.transmission !== 'all') query.append('transmission', params.transmission);
  if (params.min_year) query.append('min_year', params.min_year.toString());
  if (params.max_year) query.append('max_year', params.max_year.toString());
  if (params.search) query.append('search', params.search);
  if (params.page) query.append('page', params.page.toString());
  if (params.page_size) query.append('page_size', params.page_size.toString());

  const res = await fetch(`${API_BASE}/dataset/records?${query.toString()}`);
  if (!res.ok) throw new Error('Failed to fetch dataset records');
  return res.json();
}

export async function fetchMetrics(): Promise<any> {
  const res = await fetch(`${API_BASE}/metrics`);
  if (!res.ok) throw new Error('Failed to fetch evaluation metrics');
  return res.json();
}

export async function fetchFeatureImportance(): Promise<FeatureImportanceItem[]> {
  const res = await fetch(`${API_BASE}/models/feature-importance`);
  if (!res.ok) throw new Error('Failed to fetch feature importance');
  return res.json();
}

export async function fetchModelInfo(): Promise<any> {
  const res = await fetch(`${API_BASE}/models/info`);
  if (!res.ok) throw new Error('Failed to fetch model info');
  return res.json();
}
