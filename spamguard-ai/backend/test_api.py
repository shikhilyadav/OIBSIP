"""
Backend API Validation Suite for SpamGuard AI
"""
import sys
import os
from fastapi.testclient import TestClient

# Ensure backend root is on Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["healthy", "initializing"]
    assert "version" in data
    print("  [PASS] Health check")


def test_models_catalog():
    response = client.get("/api/models")
    assert response.status_code == 200
    data = response.json()
    assert "models" in data
    assert len(data["models"]) >= 3
    model_ids = [m["id"] for m in data["models"]]
    assert "hybrid" in model_ids
    assert "bert_tiny" in model_ids
    assert "naive_bayes" in model_ids
    print("  [PASS] Model catalog")


def test_benchmark_metrics():
    response = client.get("/api/metrics/benchmark")
    assert response.status_code == 200
    data = response.json()
    assert "in_distribution_uci" in data
    assert "independent_benchmark" in data
    assert "audited_hybrid_metrics" in data
    
    hybrid = data["audited_hybrid_metrics"]
    assert hybrid["selective_metrics"]["selective_accuracy"] == 0.9666
    assert hybrid["review_queue_count"] == 191
    print("  [PASS] Benchmark metrics & audited thresholds")


def test_threat_intel():
    response = client.get("/api/threat-intel")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "active"
    assert len(data["threat_catalog"]) >= 5
    print("  [PASS] Threat intelligence rules")


def test_analyze_spam():
    payload = {
        "message": "WINNER! You have won £1,000 cash! Claim your prize now by calling 08712400600 or text CLAIM to 86021. Urgent!",
        "model_preference": "hybrid"
    }
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["hybrid_decision"] in ["SPAM", "SUSPICIOUS / REVIEW"]
    assert data["risk_score"] > 0.50
    assert len(data["threat_signals"]) > 0
    assert "model_predictions" in data
    print("  [PASS] Analyze SPAM sample")


def test_analyze_ham():
    payload = {
        "message": "Hey are you coming to lunch today? Let me know what time works best.",
        "model_preference": "hybrid"
    }
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["hybrid_decision"] == "HAM"
    assert data["risk_score"] < 0.20
    print("  [PASS] Analyze HAM sample")


def test_history_endpoints():
    response = client.get("/api/history")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["total_records"] >= 2
    print("  [PASS] Scan history & session persistence")


if __name__ == "__main__":
    print("\n==========================================")
    print(" Running SpamGuard AI Backend Test Suite  ")
    print("==========================================")
    test_health()
    test_models_catalog()
    test_benchmark_metrics()
    test_threat_intel()
    test_analyze_spam()
    test_analyze_ham()
    test_history_endpoints()
    print("\n All Backend API Tests Passed Successfully!\n")
