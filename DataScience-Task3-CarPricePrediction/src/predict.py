"""
predict.py
==========
Production Prediction Interface for Task 3:
Car Price Prediction with Machine Learning.

Loads the serialized scikit-learn pipeline and predicts used-car selling prices
with input validation, unknown category handling, and non-negative bounds guarantees.
"""

import os
import sys
import joblib
import pandas as pd
import numpy as np
from typing import Dict, Any, Union, List

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from data_loader import get_project_paths
from feature_engineering import FEATURE_COLUMNS


class CarPricePredictor:
    """Production inference wrapper around the serialized Car Price Prediction Pipeline."""

    def __init__(self, model_path: str = None):
        paths = get_project_paths()
        self.model_path = model_path or paths["pipeline_model"]
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(
                f"Trained model not found at '{self.model_path}'. "
                "Please run train.py first to train and persist the model pipeline."
            )
        self.pipeline = joblib.load(self.model_path)

    @staticmethod
    def format_price_inr(price_inr: float) -> str:
        """Formats price in Indian National Rupee notation."""
        if price_inr >= 1e7:
            return f"₹{price_inr / 1e7:.2f} Crore"
        elif price_inr >= 1e5:
            return f"₹{price_inr / 1e5:.2f} Lakh"
        else:
            return f"₹{price_inr:,.0f}"

    def predict_one(self, car_specs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predicts selling price for a single vehicle dictionary.
        
        Expected keys in car_specs:
        - brand: str (e.g., 'Maruti', 'Hyundai', 'Honda')
        - year or car_age: int
        - km_driven: int / float
        - fuel: str ('Petrol', 'Diesel', 'CNG', 'LPG', 'Electric')
        - seller_type: str ('Individual', 'Dealer', 'Trustmark Dealer')
        - transmission: str ('Manual', 'Automatic')
        - owner: str ('First Owner', 'Second Owner', etc.)
        """
        df_input = pd.DataFrame([car_specs])
        return self.predict_dataframe(df_input)[0]

    def predict_dataframe(self, df_input: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Predicts selling prices for a DataFrame of vehicle inputs.
        """
        data = df_input.copy()

        # Handle brand extraction from name if 'name' is supplied instead of 'brand'
        if "brand" not in data.columns and "name" in data.columns:
            def extract_b(val: str) -> str:
                toks = str(val).split()
                if not toks:
                    return "Unknown"
                if toks[0] == "OpelCorsa":
                    return "Opel"
                if toks[0] == "Land" and len(toks) > 1 and toks[1] == "Rover":
                    return "Land Rover"
                return toks[0]
            data["brand"] = data["name"].apply(extract_b)

        # Handle car_age computation if 'year' is supplied instead of 'car_age'
        if "car_age" not in data.columns and "year" in data.columns:
            data["car_age"] = 2020 - pd.to_numeric(data["year"], errors="coerce").fillna(2015)

        # Default fallback values for missing features
        defaults = {
            "brand": "Maruti",
            "car_age": 6.0,
            "km_driven": 60000.0,
            "fuel": "Petrol",
            "seller_type": "Individual",
            "transmission": "Manual",
            "owner": "First Owner"
        }
        for col in FEATURE_COLUMNS:
            if col not in data.columns:
                data[col] = defaults.get(col, "Unknown")
            else:
                data[col] = data[col].fillna(defaults.get(col, "Unknown"))

        X = data[FEATURE_COLUMNS]

        # Raw model prediction
        raw_preds = self.pipeline.predict(X)

        # Enforce realistic non-negative price floor
        MIN_PRICE_FLOOR = 15000.0  # ₹15,000 scrap/entry floor
        clipped_preds = np.clip(raw_preds, a_min=MIN_PRICE_FLOOR, a_max=None)

        results = []
        for p in clipped_preds:
            p_float = float(p)
            results.append({
                "predicted_price_raw": round(p_float, 2),
                "predicted_price_inr": self.format_price_inr(p_float),
                "predicted_price_lakhs": round(p_float / 1e5, 2)
            })

        return results


def predict_car_price(specs: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience helper function to predict car price."""
    predictor = CarPricePredictor()
    return predictor.predict_one(specs)


if __name__ == "__main__":
    sample_car = {
        "brand": "Maruti",
        "year": 2017,
        "km_driven": 45000,
        "fuel": "Petrol",
        "seller_type": "Individual",
        "transmission": "Manual",
        "owner": "First Owner"
    }
    pred = predict_car_price(sample_car)
    print("\n" + "=" * 55)
    print("SAMPLE CAR PRICE PREDICTION INFERENCE")
    print("=" * 55)
    print("Input Vehicle Specifications:")
    for k, v in sample_car.items():
        print(f"  {k:18s}: {v}")
    print("\nPrediction Output:")
    for k, v in pred.items():
        print(f"  {k:24s}: {v}")
    print("=" * 55)
