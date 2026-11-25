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


from typing import List, Optional
from pydantic import BaseModel

class BatchAnalyzeRequest(BaseModel):
    messages: List[str]
    model_preference: Optional[str] = "hybrid"

class BatchAnalyzeItemResult(BaseModel):
    index: int
    message: str
    prediction: str
    confidence: float
    model_used: str
    latency_ms: float
    requires_review: bool

class BatchAnalyzeResponse(BaseModel):
    total_processed: int
    spam_count: int
    ham_count: int
    review_count: int
    model_used: str
    results: List[BatchAnalyzeItemResult]


@router.post("/batch", response_model=BatchAnalyzeResponse)
def analyze_batch(req: BatchAnalyzeRequest):
    if not req.messages:
        raise HTTPException(status_code=400, detail="Batch message list cannot be empty.")
    
    # Cap batch size at 200 items for responsive throughput
    messages = req.messages[:200]
    service = ModelService.get_instance()
    if not service.is_initialized:
        service.initialize()

    results = []
    spam_count = 0
    ham_count = 0
    review_count = 0
    model_pref = (req.model_preference or "hybrid").lower()

    for idx, msg in enumerate(messages):
        clean_msg = str(msg).strip()
        if not clean_msg:
            continue
        
        preds = service.predict_all(clean_msg)
        nb_pred = preds["naive_bayes"]
        lr_pred = preds["logistic_regression"]
        bert_pred = preds["bert_tiny"]

        if model_pref in ["nb", "naive_bayes"]:
            pred_label = nb_pred["predicted_label"]
            conf = nb_pred["spam_probability"] if pred_label == "SPAM" else nb_pred["ham_confidence"]
            model_used_name = "Multinomial Naive Bayes"
            lat = nb_pred["latency_ms"]
            req_rev = False
        elif model_pref in ["lr", "logistic_regression"]:
            pred_label = lr_pred["predicted_label"]
            conf = lr_pred["spam_probability"] if pred_label == "SPAM" else lr_pred["ham_confidence"]
            model_used_name = "Logistic Regression"
            lat = lr_pred["latency_ms"]
            req_rev = False
        elif model_pref in ["bert", "bert_tiny"]:
            pred_label = bert_pred["predicted_label"]
            conf = bert_pred["spam_probability"] if pred_label == "SPAM" else bert_pred["ham_confidence"]
            model_used_name = "BERT-Tiny"
            lat = bert_pred["latency_ms"]
            req_rev = False
        else:
            hybrid_eval = HybridTriageEngine.evaluate(nb_pred, bert_pred, lr_pred)
            pred_label = hybrid_eval["hybrid_decision"]
            conf = hybrid_eval["risk_score"] if pred_label == "SPAM" else (1.0 - hybrid_eval["risk_score"])
            model_used_name = "Hybrid Triage"
            lat = nb_pred["latency_ms"] + lr_pred["latency_ms"] + bert_pred["latency_ms"]
            req_rev = hybrid_eval["requires_review"]

        if req_rev:
            review_count += 1
        elif pred_label == "SPAM":
            spam_count += 1
        else:
            ham_count += 1

        results.append(BatchAnalyzeItemResult(
            index=idx + 1,
            message=clean_msg[:100] + "..." if len(clean_msg) > 100 else clean_msg,
            prediction=pred_label,
            confidence=round(conf, 4),
            model_used=model_used_name,
            latency_ms=round(lat, 2),
            requires_review=req_rev
        ))

    return BatchAnalyzeResponse(
        total_processed=len(results),
        spam_count=spam_count,
        ham_count=ham_count,
        review_count=review_count,
        model_used=model_pref,
        results=results
    )

