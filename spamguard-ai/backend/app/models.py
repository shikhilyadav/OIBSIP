"""
SpamGuard AI Pydantic Data Models & Schemas
"""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class AnalyzeRequest(BaseModel):
    message: Optional[str] = Field(None, min_length=1, max_length=5000, description="Raw SMS or email text to evaluate.")
    text: Optional[str] = Field(None, min_length=1, max_length=5000, description="Alias for message field.")
    model_preference: Optional[str] = Field("hybrid", description="Target model: hybrid, bert_tiny, naive_bayes, or logistic_regression.")
    model_id: Optional[str] = Field(None, description="Alias for model_preference.")
    detailed_tokens: Optional[bool] = Field(True, description="Whether to include normalized tokens.")

    def get_message(self) -> str:
        msg = self.message or self.text or ""
        return msg.strip()

    def get_model(self) -> str:
        return self.model_id or self.model_preference or "hybrid"

class ModelScore(BaseModel):
    model_name: str
    display_name: str
    architecture: str
    predicted_label: str  # HAM or SPAM
    spam_probability: float
    ham_confidence: float
    latency_ms: float
    raw_logits: Optional[List[float]] = None

class ThreatSignal(BaseModel):
    signal_type: str
    indicator: str
    severity: str  # low, medium, high, critical
    description: str

class AnalyzeResponse(BaseModel):
    id: str
    timestamp: str
    message_preview: str
    full_message: str
    char_count: int
    word_count: int
    hybrid_decision: str  # HAM, SPAM, or SUSPICIOUS / REVIEW
    risk_level: str       # LOW, MEDIUM, HIGH, CRITICAL
    risk_score: float     # 0.0 to 1.0 (composite spam probability)
    requires_review: bool
    explanation: str
    preprocessed_tokens: str
    model_predictions: Dict[str, ModelScore]
    threat_signals: List[ThreatSignal]

class ModelInfo(BaseModel):
    id: str
    name: str
    architecture: str
    parameter_count: str
    description: str
    in_distribution_accuracy: float
    in_distribution_recall: float
    out_of_distribution_accuracy: Optional[float] = None
    out_of_distribution_recall: Optional[float] = None
    latency_per_sample_ms: float
    status: str

class ModelsResponse(BaseModel):
    models: List[ModelInfo]
    hybrid_triage_config: Dict[str, Any]

class HistoryItem(BaseModel):
    id: str
    timestamp: str
    message_preview: str
    full_message: str
    decision: str
    risk_score: float
    risk_level: str
    model_used: str
    requires_review: bool
    threat_count: int

class HistoryResponse(BaseModel):
    total_records: int
    items: List[HistoryItem]

class BenchmarkMetricsResponse(BaseModel):
    in_distribution_uci: Dict[str, Any]
    independent_benchmark: Dict[str, Any]
    audited_hybrid_metrics: Dict[str, Any]

class AnalyticsOverview(BaseModel):
    kpis: Dict[str, Any]
    confusion_matrices: Dict[str, Any]
    metrics_comparison: List[Dict[str, Any]]
    detection_trend: List[Dict[str, Any]]
    threat_distribution: List[Dict[str, Any]]
