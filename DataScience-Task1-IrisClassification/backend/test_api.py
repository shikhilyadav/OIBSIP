"""
Automated Backend API Test Suite for IrisAI
"""
import sys
import os
from fastapi.testclient import TestClient

BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BACKEND_DIR)

from app.main import app

client = TestClient(app)

def test_health():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert data["model_loaded"] is True
    print("  [PASS] /api/health")

def test_model_info():
    res = client.get("/api/model/info")
    assert res.status_code == 200
    data = res.json()
    assert data["model_type"] == "Random Forest Classifier"
    assert len(data["features"]) == 4
    print("  [PASS] /api/model/info")

def test_dataset_summary():
    res = client.get("/api/dataset/summary")
    assert res.status_code == 200
    data = res.json()
    assert data["total_specimens"] == 150
    assert data["distinct_species"] == 3
    print("  [PASS] /api/dataset/summary")

def test_dataset_records():
    res = client.get("/api/dataset/records?species=Setosa&page=1&page_size=10")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] == 50
    assert len(data["records"]) == 10
    print("  [PASS] /api/dataset/records")

def test_species_insights():
    res = client.get("/api/species/insights")
    assert res.status_code == 200
    data = res.json()
    assert "Setosa" in data["insights"]
    assert "Versicolor" in data["insights"]
    assert "Virginica" in data["insights"]
    print("  [PASS] /api/species/insights")

def test_metrics():
    res = client.get("/api/metrics")
    assert res.status_code == 200
    data = res.json()
    assert "test_metrics" in data
    assert data["test_metrics"]["Test Accuracy"] == 0.9667
    print("  [PASS] /api/metrics")

def test_prediction_invariance():
    # Setosa Baseline
    res_set = client.post("/api/predict", json={"sepal_length": 5.0, "sepal_width": 3.4, "petal_length": 1.5, "petal_width": 0.2})
    assert res_set.status_code == 200
    d_set = res_set.json()["prediction"]
    assert d_set["species"] == "Iris Setosa"
    assert d_set["class_id"] == 0
    assert d_set["confidence"] == 1.0

    # Versicolor Baseline
    res_ver = client.post("/api/predict", json={"sepal_length": 5.9, "sepal_width": 2.8, "petal_length": 4.3, "petal_width": 1.3})
    assert res_ver.status_code == 200
    d_ver = res_ver.json()["prediction"]
    assert d_ver["species"] == "Iris Versicolor"
    assert d_ver["class_id"] == 1
    assert d_ver["confidence"] == 0.9964

    # Virginica Baseline
    res_vir = client.post("/api/predict", json={"sepal_length": 6.6, "sepal_width": 3.0, "petal_length": 5.6, "petal_width": 2.0})
    assert res_vir.status_code == 200
    d_vir = res_vir.json()["prediction"]
    assert d_vir["species"] == "Iris Virginica"
    assert d_vir["class_id"] == 2
    assert d_vir["confidence"] == 0.9972

    print("  [PASS] /api/predict (All 3 Baselines Match Original Model 100%!)")

if __name__ == "__main__":
    print("\n=== RUNNING IRISAI BACKEND TEST SUITE ===")
    test_health()
    test_model_info()
    test_dataset_summary()
    test_dataset_records()
    test_species_insights()
    test_metrics()
    test_prediction_invariance()
    print("=== ALL BACKEND TESTS PASSED SUCCESSFULLY! ===\n")
