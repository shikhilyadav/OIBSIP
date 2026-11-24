"""
Message Analysis Router (POST /api/analyze)
"""

import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException

from ..models import AnalyzeRequest, AnalyzeResponse, ModelScore, ThreatSignal
from ..ml.model_service import ModelService
from ..ml.hybrid_engine import HybridTriageEngine
from ..ml.preprocessor import preprocess_text
from ..services.threat_detector import ThreatDetector
from ..services.history_store import HistoryStore

router = APIRouter(prefix="/analyze", tags=["Analysis"])

@router.post("", response_model=AnalyzeResponse)
def analyze_message(req: AnalyzeRequest):
    raw_text = req.get_message()
    if not raw_text:
        raise HTTPException(status_code=400, detail="Message text cannot be empty.")

    service = ModelService.get_instance()
    if not service.is_initialized:
        service.initialize()

    # 1. Run all models
    predictions = service.predict_all(raw_text)
    nb_pred = predictions["naive_bayes"]
    lr_pred = predictions["logistic_regression"]
    bert_pred = predictions["bert_tiny"]

    # 2. Run Hybrid Triage
    hybrid_result = HybridTriageEngine.evaluate(nb_pred, bert_pred, lr_pred)

    # 3. Threat Intelligence signals
    threat_signals_raw = ThreatDetector.analyze(raw_text)
    threat_signals = [ThreatSignal(**s) for s in threat_signals_raw]

    # Preprocessed tokens preview
    tokens_clean = preprocess_text(raw_text)

    # Generate response
    item_id = str(uuid.uuid4())[:8]
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    preview = raw_text[:65] + "..." if len(raw_text) > 65 else raw_text

    response_data = {
        "id": item_id,
        "timestamp": timestamp,
        "message_preview": preview,
        "full_message": raw_text,
        "char_count": len(raw_text),
        "word_count": len(raw_text.split()),
        "hybrid_decision": hybrid_result["hybrid_decision"],
        "risk_level": hybrid_result["risk_level"],
        "risk_score": hybrid_result["risk_score"],
        "requires_review": hybrid_result["requires_review"],
        "explanation": hybrid_result["explanation"],
        "preprocessed_tokens": tokens_clean,
        "model_predictions": {
            "naive_bayes": ModelScore(**nb_pred),
            "logistic_regression": ModelScore(**lr_pred),
            "bert_tiny": ModelScore(**bert_pred)
        },
        "threat_signals": threat_signals
    }

    # Store in history
    HistoryStore.get_instance().add_entry({
        "id": item_id,
        "timestamp": timestamp,
        "message_preview": preview,
        "full_message": raw_text,
        "decision": hybrid_result["hybrid_decision"],
        "risk_score": hybrid_result["risk_score"],
        "risk_level": hybrid_result["risk_level"],
        "model_used": req.model_preference or "hybrid",
        "requires_review": hybrid_result["requires_review"],
        "threat_count": len(threat_signals)
    })

    return AnalyzeResponse(**response_data)
