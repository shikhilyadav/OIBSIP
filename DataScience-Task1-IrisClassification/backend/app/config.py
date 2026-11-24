import os
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
TASK1_DIR = BACKEND_DIR.parent
MODEL_PATH = TASK1_DIR / "models" / "best_iris_model.joblib"
METADATA_PATH = TASK1_DIR / "models" / "model_metadata.json"
DATA_PATH = TASK1_DIR / "data" / "iris.csv"

CORS_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
]
