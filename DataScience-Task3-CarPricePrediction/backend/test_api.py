"""
Automated Backend Validation Suite for AutoValue AI.
"""
import sys
import os
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app.main import app

client = TestClient(app)

def test_all():
    print("=== RUNNING AUTOVALUE AI BACKEND TEST SUITE ===")

    # 1. Health
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["model_loaded"] is True
    assert r.json()["dataset_loaded"] is True
    print("  [PASS] /api/health")

    # 2. Dataset Summary
    r = client.get("/api/dataset/summary")
    assert r.status_code == 200
    data = r.json()
    assert data["total_records"] == 3577
    assert data["unique_brands"] == 29
    assert data["selected_algorithm"] == "Linear Regression"
    print("  [PASS] /api/dataset/summary")

    # 3. Dataset Options
    r = client.get("/api/dataset/options")
    assert r.status_code == 200
    opts = r.json()
    assert "Maruti" in opts["brands"]
    assert "Petrol" in opts["fuels"]
    assert "Manual" in opts["transmissions"]
    print("  [PASS] /api/dataset/options")

    # 4. Dataset Records
    r = client.get("/api/dataset/records?page=1&page_size=5")
    assert r.status_code == 200
    rec = r.json()
    assert rec["total"] == 3577
    assert len(rec["records"]) == 5
    print("  [PASS] /api/dataset/records")

    # 5. Metrics
    r = client.get("/api/metrics")
    assert r.status_code == 200
    m = r.json()
    assert "Linear Regression" in m["model_comparison"]
    print("  [PASS] /api/metrics")

    # 6. Feature Importance
    r = client.get("/api/models/feature-importance")
    assert r.status_code == 200
    fi = r.json()
    assert len(fi) > 10
    print("  [PASS] /api/models/feature-importance")

    # 7. Predict
    payload = {
        "brand": "Maruti",
        "year": 2017,
        "km_driven": 45000,
        "fuel": "Petrol",
        "seller_type": "Individual",
        "transmission": "Manual",
        "owner": "First Owner"
    }
    r = client.post("/api/predict", json=payload)
    assert r.status_code == 200
    pred = r.json()["data"]
    assert pred["predicted_price"] > 0
    assert "₹" in pred["formatted_price"]
    print(f"  [PASS] /api/predict (Maruti 2017 -> {pred['formatted_price']})")

    print("=== ALL AUTOVALUE AI BACKEND TESTS PASSED SUCCESSFULLY! ===")

if __name__ == "__main__":
    test_all()
