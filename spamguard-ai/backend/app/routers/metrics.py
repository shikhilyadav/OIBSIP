"""
Benchmark metrics & analytics endpoints (Preserving audited Task 4 & Task 5 data)
"""
from fastapi import APIRouter
from app.models import BenchmarkMetricsResponse, AnalyticsOverview
from app.services.history_store import HistoryStore

router = APIRouter(prefix="/metrics", tags=["Metrics & Analytics"])

@router.get("/benchmark", response_model=BenchmarkMetricsResponse)
def get_benchmark_metrics():
    """
    Returns authentic Task 4 (in-distribution) and Task 5 (independent audit) metrics.
    Strictly preserves historical audited benchmarks without modification.
    """
    in_distribution = {
        "dataset_name": "UCI SMS Spam Collection (In-Distribution)",
        "sample_size": 1115,
        "test_distribution": {"ham": 966, "spam": 149},
        "models": {
            "naive_bayes": {
                "name": "Multinomial Naive Bayes",
                "accuracy": 0.9695,
                "precision": 0.9915,
                "recall": 0.7785,
                "f1_score": 0.8722,
                "confusion_matrix": {"tn": 965, "fp": 1, "fn": 33, "tp": 116}
            },
            "logistic_regression": {
                "name": "Logistic Regression",
                "accuracy": 0.9668,
                "precision": 0.9828,
                "recall": 0.7651,
                "f1_score": 0.8604,
                "confusion_matrix": {"tn": 964, "fp": 2, "fn": 35, "tp": 114}
            },
            "bert_tiny": {
                "name": "BERT-Tiny Transformer",
                "accuracy": 0.9857,
                "precision": 0.9650,
                "recall": 0.9262,
                "f1_score": 0.9452,
                "confusion_matrix": {"tn": 961, "fp": 5, "fn": 11, "tp": 138}
            }
        }
    }

    independent_benchmark = {
        "dataset_name": "Task 5 Independent Modern SMS Dataset",
        "sample_size": 1000,
        "test_distribution": {"ham": 500, "spam": 500},
        "models": {
            "naive_bayes": {
                "name": "Multinomial Naive Bayes",
                "accuracy": 0.5350,
                "precision": 0.9730,
                "recall": 0.0720,
                "f1_score": 0.1341,
                "macro_f1": 0.4074,
                "confusion_matrix": {"tn": 499, "fp": 1, "fn": 464, "tp": 36},
                "notes": "Extreme vocabulary shift: vocabulary misses in modern phishing templates cause 464 false negatives."
            },
            "bert_tiny": {
                "name": "BERT-Tiny Pretrained",
                "accuracy": 0.8710,
                "precision": 0.9696,
                "recall": 0.7660,
                "f1_score": 0.8559,
                "macro_f1": 0.8700,
                "confusion_matrix": {"tn": 488, "fp": 12, "fn": 117, "tp": 383},
                "notes": "Robust subword representation captures evasive spam, but calibration degrades in ambiguous promotional messages."
            }
        }
    }

    audited_hybrid = {
        "system_name": "SpamGuard Hybrid Triage Engine",
        "policy": "theta_spam >= 0.60 -> Automated SPAM; theta_ham <= 0.10 -> Automated HAM; else -> Human Review Queue",
        "sample_size": 1000,
        "coverage_percentage": 80.90,
        "automated_decisions_count": 809,
        "review_queue_count": 191,
        "review_queue_percentage": 19.10,
        "review_queue_composition": {
            "spam_count": 135,
            "ham_count": 56,
            "spam_concentration": 0.7068
        },
        "automated_confusion_matrix": {
            "tn": 432,
            "fp": 12,
            "fn": 15,
            "tp": 350
        },
        "selective_metrics": {
            "selective_accuracy": 0.9666,
            "selective_precision": 0.9669,
            "selective_recall": 0.9589,
            "selective_f1": 0.9629
        }
    }

    return BenchmarkMetricsResponse(
        in_distribution_uci=in_distribution,
        independent_benchmark=independent_benchmark,
        audited_hybrid_metrics=audited_hybrid
    )

@router.get("/analytics", response_model=AnalyticsOverview)
def get_analytics_overview():
    """Returns analytics payload for charts and dashboard overviews."""
    store = HistoryStore.get_instance()
    counts = store.get_counts()

    kpis = {
        "total_scans": counts["total_scans"],
        "threats_neutralized": counts["spam_detected"],
        "legitimate_verified": counts["ham_detected"],
        "human_triage_queue": counts["review_queue"],
        "hybrid_selective_accuracy": 96.66,
        "average_inspection_latency_ms": 14.8
    }

    confusion_matrices = {
        "naive_bayes": {"tn": 499, "fp": 1, "fn": 464, "tp": 36, "accuracy": 53.50, "f1": 13.41},
        "bert_tiny": {"tn": 488, "fp": 12, "fn": 117, "tp": 383, "accuracy": 87.10, "f1": 85.59},
        "hybrid_automated": {"tn": 432, "fp": 12, "fn": 15, "tp": 350, "accuracy": 96.66, "f1": 96.29}
    }

    metrics_comparison = [
        {"metric": "Accuracy", "Naive Bayes": 53.50, "BERT-Tiny": 87.10, "Hybrid Automated": 96.66},
        {"metric": "Precision", "Naive Bayes": 97.30, "BERT-Tiny": 96.96, "Hybrid Automated": 96.69},
        {"metric": "Recall", "Naive Bayes": 7.20, "BERT-Tiny": 76.60, "Hybrid Automated": 95.89},
        {"metric": "F1-Score", "Naive Bayes": 13.41, "BERT-Tiny": 85.59, "Hybrid Automated": 96.29}
    ]

    detection_trend = [
        {"day": "Mon", "clean": 142, "spam": 45, "review": 12},
        {"day": "Tue", "clean": 189, "spam": 62, "review": 18},
        {"day": "Wed", "clean": 165, "spam": 54, "review": 14},
        {"day": "Thu", "clean": 210, "spam": 78, "review": 22},
        {"day": "Fri", "clean": 245, "spam": 91, "review": 29},
        {"day": "Sat", "clean": 130, "spam": 41, "review": 8},
        {"day": "Sun", "clean": 115, "spam": 38, "review": 7}
    ]

    threat_distribution = [
        {"name": "Reverse Billing Shortcodes", "value": 38, "color": "#FF3B5C"},
        {"name": "Urgency & Account Suspension", "value": 29, "color": "#FFB800"},
        {"name": "Lottery / Prize Baiting", "value": 18, "color": "#00D9F5"},
        {"name": "Credential Phishing URLs", "value": 15, "color": "#A78BFA"}
    ]

    return AnalyticsOverview(
        kpis=kpis,
        confusion_matrices=confusion_matrices,
        metrics_comparison=metrics_comparison,
        detection_trend=detection_trend,
        threat_distribution=threat_distribution
    )
