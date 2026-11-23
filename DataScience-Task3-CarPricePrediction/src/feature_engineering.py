"""
feature_engineering.py
======================
Feature Engineering and ColumnTransformer Pipeline Definitions for Task 3:
Car Price Prediction with Machine Learning.

Defines feature transformations, preprocessor pipelines, and column schemas
ensuring complete train/test isolation with zero data leakage.
"""

import os
import sys
import pandas as pd
from typing import List, Tuple
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from data_loader import get_project_paths

# Standard feature set
FEATURE_COLUMNS: List[str] = [
    "brand", "car_age", "km_driven", "fuel",
    "seller_type", "transmission", "owner"
]
TARGET_COLUMN: str = "selling_price"

CATEGORICAL_FEATURES: List[str] = [
    "brand", "fuel", "seller_type", "transmission", "owner"
]
NUMERICAL_FEATURES: List[str] = [
    "car_age", "km_driven"
]


def extract_features(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Extracts feature matrix X and target series y from cleaned or raw dataset.
    Computes brand and car_age if not already present.
    """
    data = df.copy()
    if "brand" not in data.columns and "name" in data.columns:
        def get_clean_brand(car_name: str) -> str:
            tokens = car_name.split()
            if not tokens:
                return "Unknown"
            first = tokens[0]
            if first == "OpelCorsa":
                return "Opel"
            if first == "Land" and len(tokens) > 1 and tokens[1] == "Rover":
                return "Land Rover"
            return first
        data["brand"] = data["name"].apply(get_clean_brand)
        
    if "car_age" not in data.columns and "year" in data.columns:
        data["car_age"] = 2020 - data["year"]
        
    for col in FEATURE_COLUMNS:
        assert col in data.columns, f"Required feature '{col}' missing from data."
        
    X = data[FEATURE_COLUMNS]
    y = data[TARGET_COLUMN] if TARGET_COLUMN in data.columns else None
    return X, y


def build_preprocessor(scale_numerics: bool = True) -> ColumnTransformer:
    """
    Builds a leakage-safe ColumnTransformer.
    - Numerical features: StandardScaler (optional)
    - Categorical features: OneHotEncoder with handle_unknown='ignore'
    
    Parameters
    ----------
    scale_numerics : bool, default=True
        Whether to scale numerical columns using StandardScaler.
        
    Returns
    -------
    ColumnTransformer
        Configured preprocessor instance ready for pipeline integration.
    """
    transformers = []
    if scale_numerics:
        transformers.append(("num", StandardScaler(), NUMERICAL_FEATURES))
    else:
        transformers.append(("num", "passthrough", NUMERICAL_FEATURES))
        
    transformers.append((
        "cat",
        OneHotEncoder(handle_unknown="ignore", sparse_output=False),
        CATEGORICAL_FEATURES
    ))
    
    preprocessor = ColumnTransformer(
        transformers=transformers,
        remainder="drop"
    )
    return preprocessor


if __name__ == "__main__":
    paths = get_project_paths()
    if os.path.exists(paths["processed_csv"]):
        df = pd.read_csv(paths["processed_csv"])
        X, y = extract_features(df)
        print(f"[FEATURE ENGINEERING] Feature matrix X shape: {X.shape}")
        print(f"[FEATURE ENGINEERING] Target y shape: {y.shape}")
        prep = build_preprocessor()
        X_trans = prep.fit_transform(X)
        print(f"[FEATURE ENGINEERING] Transformed shape: {X_trans.shape}")
    else:
        print("[FEATURE ENGINEERING] Processed dataset not found. Run data_cleaning.py first.")
