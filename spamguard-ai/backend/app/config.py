"""
SpamGuard AI Backend Configuration
"""

from pathlib import Path

# Paths to existing OIBSIP artifacts
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
TASK4_DIR = BASE_DIR / "OIBSIP_Task4_Spam_Detection"
INDEP_DIR = BASE_DIR / "independent_validation"

TASK4_DATASET = TASK4_DIR / "dataset" / "spam.csv"
INDEP_BENCHMARK = INDEP_DIR / "dataset" / "independent_sms_benchmark.csv"

TASK4_METRICS_JSON = TASK4_DIR / "outputs" / "summary_metrics.json"
BERT_METRICS_JSON = TASK4_DIR / "outputs" / "bert_metrics.json"
INDEP_METRICS_JSON = INDEP_DIR / "metrics.json"

# Strict Audited Hybrid Triage Thresholds
TH_SPAM = 0.60
TH_HAM = 0.10

# Pre-trained BERT Checkpoint (Local cached or HuggingFace ID)
BERT_MODEL_NAME = "mrm8488/bert-tiny-finetuned-sms-spam-detection"

# Server configuration
API_PREFIX = "/api"
CORS_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
]
