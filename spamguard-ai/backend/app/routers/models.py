"""
Model catalog endpoint providing metadata on all integrated architectures.
"""
from fastapi import APIRouter
from app.models import ModelsResponse, ModelInfo

router = APIRouter(prefix="/models", tags=["Models"])

@router.get("", response_model=ModelsResponse)
def get_models():
    """Returns catalog of models and active triage configuration."""
    catalog = [
        ModelInfo(
            id="hybrid",
            name="SpamGuard Hybrid Triage Engine",
            architecture="2-Stage Decision Routing (BERT + MNB + Calibrated Abstention)",
            parameter_count="4.39M + 7.8K",
            description="Production ensemble: routes decisive samples to fast MNB or BERT, abstaining to human review when 0.10 < p_spam < 0.60.",
            in_distribution_accuracy=0.9857,
            in_distribution_recall=0.9262,
            out_of_distribution_accuracy=0.9666,
            out_of_distribution_recall=0.9589,
            latency_per_sample_ms=18.4,
            status="active"
        ),
        ModelInfo(
            id="bert_tiny",
            name="BERT-Tiny Transformer",
            architecture="2-Layer Transformer (mrm8488/bert-tiny-finetuned-sms-spam-detection)",
            parameter_count="4.39M",
            description="Fine-tuned Transformer SMS classifier. Subword tokenization captures obfuscations, but suffers domain shift on modern phishing.",
            in_distribution_accuracy=0.9857,
            in_distribution_recall=0.9262,
            out_of_distribution_accuracy=0.8710,
            out_of_distribution_recall=0.7660,
            latency_per_sample_ms=16.8,
            status="active"
        ),
        ModelInfo(
            id="naive_bayes",
            name="Multinomial Naive Bayes",
            architecture="TF-IDF N-gram + Multinomial Naive Bayes",
            parameter_count="7,821 Features",
            description="Classic Bag-of-Words baseline. Exceptional precision and low latency on known vocabulary, severe recall collapse on modern unseen templates.",
            in_distribution_accuracy=0.9695,
            in_distribution_recall=0.7785,
            out_of_distribution_accuracy=0.5350,
            out_of_distribution_recall=0.0720,
            latency_per_sample_ms=1.2,
            status="active"
        ),
        ModelInfo(
            id="logistic_regression",
            name="Logistic Regression",
            architecture="TF-IDF N-gram + L2 Regularized Logistic Regression",
            parameter_count="7,821 Features",
            description="Calibrated log-odds baseline trained on TF-IDF unigram and bigram tokens.",
            in_distribution_accuracy=0.9668,
            in_distribution_recall=0.7651,
            out_of_distribution_accuracy=0.5410,
            out_of_distribution_recall=0.0840,
            latency_per_sample_ms=1.5,
            status="active"
        )
    ]

    triage_config = {
        "engine_name": "SpamGuard Dual-Threshold Triage",
        "theta_spam": 0.60,
        "theta_ham": 0.10,
        "triage_coverage_pct": 80.90,
        "selective_accuracy_pct": 96.66,
        "review_queue_size_pct": 19.10,
        "status": "enforced"
    }

    return ModelsResponse(
        models=catalog,
        hybrid_triage_config=triage_config
    )
