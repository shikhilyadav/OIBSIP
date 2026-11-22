"""
predict.py
==========
Inference and Prediction module for Iris Flower Classification.
Loads serialized joblib artifact and provides CLI & programmatic APIs.
"""

import os
import sys
import argparse
from typing import Dict, Any, Union
import numpy as np
import pandas as pd
import joblib


class IrisPredictor:
    """
    Production-ready inference wrapper for the trained Iris classification model.
    """

    def __init__(self, model_path: str = None):
        if model_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            base_dir = os.path.dirname(current_dir)
            model_path = os.path.join(base_dir, "models", "best_iris_model.joblib")

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at: {model_path}. Please execute `python src/train.py` first.")

        artifact = joblib.load(model_path)
        self.pipeline = artifact["pipeline"]
        self.model_name = artifact.get("model_name", "Unknown Model")
        self.feature_names = artifact.get("feature_names", ["sepal_length", "sepal_width", "petal_length", "petal_width"])
        self.target_names = artifact.get("target_names", ["Setosa", "Versicolor", "Virginica"])
        self.metrics = artifact.get("metrics", {})

    def predict(
        self,
        sepal_length: float,
        sepal_width: float,
        petal_length: float,
        petal_width: float
    ) -> Dict[str, Any]:
        """
        Executes prediction on given four botanical flower measurements.

        Args:
            sepal_length: Sepal length in centimeters.
            sepal_width: Sepal width in centimeters.
            petal_length: Petal length in centimeters.
            petal_width: Petal width in centimeters.

        Returns:
            Dict containing predicted species, confidence, and class probabilities.
        """
        # Validate realistic biological ranges
        inputs = [sepal_length, sepal_width, petal_length, petal_width]
        if any(v <= 0 for v in inputs):
            raise ValueError("All measurements must be positive non-zero numbers.")

        input_df = pd.DataFrame([{
            "sepal_length": float(sepal_length),
            "sepal_width": float(sepal_width),
            "petal_length": float(petal_length),
            "petal_width": float(petal_width)
        }])

        pred_idx = int(self.pipeline.predict(input_df)[0])
        pred_species = self.target_names[pred_idx]

        # Extract probability distribution if supported
        probabilities = {}
        confidence = 1.0
        if hasattr(self.pipeline, "predict_proba"):
            probs = self.pipeline.predict_proba(input_df)[0]
            for idx, name in enumerate(self.target_names):
                probabilities[name] = round(float(probs[idx]), 4)
            confidence = probabilities[pred_species]
        else:
            for idx, name in enumerate(self.target_names):
                probabilities[name] = 1.0 if idx == pred_idx else 0.0

        return {
            "predicted_species": pred_species,
            "predicted_class_id": pred_idx,
            "confidence": confidence,
            "probabilities": probabilities,
            "model_used": self.model_name,
            "inputs": {
                "sepal_length": sepal_length,
                "sepal_width": sepal_width,
                "petal_length": petal_length,
                "petal_width": petal_width
            }
        }


def main():
    parser = argparse.ArgumentParser(description="Iris Flower Species Predictor CLI")
    parser.add_argument("--sepal-length", type=float, required=True, help="Sepal length in cm (e.g., 5.1)")
    parser.add_argument("--sepal-width", type=float, required=True, help="Sepal width in cm (e.g., 3.5)")
    parser.add_argument("--petal-length", type=float, required=True, help="Petal length in cm (e.g., 1.4)")
    parser.add_argument("--petal-width", type=float, required=True, help="Petal width in cm (e.g., 0.2)")

    args = parser.parse_args()

    predictor = IrisPredictor()
    result = predictor.predict(
        sepal_length=args.sepal_length,
        sepal_width=args.sepal_width,
        petal_length=args.petal_length,
        petal_width=args.petal_width
    )

    print("\n" + "=" * 50)
    print("IRIS FLOWER PREDICTION RESULT")
    print("=" * 50)
    print(f"Model:              {result['model_used']}")
    print(f"Predicted Species:  {result['predicted_species']}")
    print(f"Confidence:         {result['confidence'] * 100:.2f}%")
    print("\nClass Probabilities:")
    for species, prob in result["probabilities"].items():
        print(f"  - {species:12s}: {prob * 100:.2f}%")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    main()
