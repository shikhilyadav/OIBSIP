"""
Service layer for AutoValue AI.
Wraps the serialized scikit-learn regression pipeline and dataset without modification.
"""
import json
import joblib
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
from datetime import datetime
from app.config import MODEL_PATH, METADATA_PATH, DATA_PATH

class CarPriceService:
    _instance = None

    def __init__(self):
        self.pipeline = None
        self.metadata = None
        self.df: Optional[pd.DataFrame] = None
        self.is_initialized = False

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def initialize(self):
        if self.is_initialized:
            return

        # 1. Load trained model pipeline
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Model pipeline not found at {MODEL_PATH}")
        self.pipeline = joblib.load(MODEL_PATH)

        # 2. Load model metadata
        if METADATA_PATH.exists():
            with open(METADATA_PATH, "r", encoding="utf-8") as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {}

        # 3. Load cleaned dataset
        if DATA_PATH.exists():
            self.df = pd.read_csv(DATA_PATH)
        else:
            raise FileNotFoundError(f"Cleaned dataset not found at {DATA_PATH}")

        self.is_initialized = True

    def predict(
        self,
        brand: str,
        year: int,
        km_driven: float,
        fuel: str,
        seller_type: str,
        transmission: str,
        owner: str
    ) -> Dict[str, Any]:
        if not self.is_initialized:
            self.initialize()

        current_year = 2020  # Consistent with Task 3 training dataset
        car_age = max(0, current_year - int(year))

        # Build raw single-row DataFrame matching training feature columns
        input_data = pd.DataFrame([{
            "brand": str(brand).strip(),
            "car_age": int(car_age),
            "km_driven": float(km_driven),
            "fuel": str(fuel).strip(),
            "seller_type": str(seller_type).strip(),
            "transmission": str(transmission).strip(),
            "owner": str(owner).strip()
        }])

        # Predict through TransformedTargetRegressor pipeline
        raw_pred = self.pipeline.predict(input_data)[0]
        # Guaranteed non-negative lower bound
        predicted_price = max(20000.0, float(raw_pred))

        # Format price in Indian Rupee notation (Lakhs / Crores)
        if predicted_price >= 1e7:
            formatted_price = f"₹{predicted_price / 1e7:.2f} Cr"
        elif predicted_price >= 1e5:
            formatted_price = f"₹{predicted_price / 1e5:.2f} Lakh"
        else:
            formatted_price = f"₹{predicted_price:,.0f}"

        # Standard error / estimated valuation range (based on test MAE ₹144,221)
        test_mae = self.metadata.get("model_comparison", {}).get("Linear Regression", {}).get("test_mae", 144221.02)
        lower_bound = max(15000.0, predicted_price - (test_mae * 0.75))
        upper_bound = predicted_price + (test_mae * 0.75)

        return {
            "predicted_price": round(predicted_price, 2),
            "formatted_price": formatted_price,
            "price_in_lakhs": round(predicted_price / 1e5, 2),
            "lower_bound": round(lower_bound, 2),
            "upper_bound": round(upper_bound, 2),
            "inputs": {
                "brand": brand,
                "year": year,
                "car_age": car_age,
                "km_driven": km_driven,
                "fuel": fuel,
                "seller_type": seller_type,
                "transmission": transmission,
                "owner": owner
            },
            "model_used": self.metadata.get("best_model_name", "Linear Regression"),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def get_summary(self) -> Dict[str, Any]:
        if not self.is_initialized:
            self.initialize()

        df = self.df
        total = len(df)
        avg_price = float(df["selling_price"].mean())
        median_price = float(df["selling_price"].median())
        avg_km = float(df["km_driven"].mean())
        avg_age = float(df["car_age"].mean())

        return {
            "total_records": total,
            "unique_brands": int(df["brand"].nunique()),
            "unique_models": int(df["name"].nunique()),
            "number_of_features": len(self.metadata.get("feature_columns", [])),
            "target_variable": "selling_price (INR)",
            "selected_algorithm": self.metadata.get("best_model_name", "Linear Regression"),
            "test_r2_score": self.metadata.get("model_comparison", {}).get("Linear Regression", {}).get("test_r2", 0.712),
            "average_price": round(avg_price, 2),
            "median_price": round(median_price, 2),
            "average_km": round(avg_km, 1),
            "average_age": round(avg_age, 1),
            "year_range": {"min": int(df["year"].min()), "max": int(df["year"].max())},
            "price_range": {"min": float(df["selling_price"].min()), "max": float(df["selling_price"].max())}
        }

    def get_records(
        self,
        brand: Optional[str] = None,
        fuel: Optional[str] = None,
        transmission: Optional[str] = None,
        min_year: Optional[int] = None,
        max_year: Optional[int] = None,
        search: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:
        if not self.is_initialized:
            self.initialize()

        filtered = self.df.copy()

        if brand and brand.lower() != "all":
            filtered = filtered[filtered["brand"].str.lower() == brand.lower()]

        if fuel and fuel.lower() != "all":
            filtered = filtered[filtered["fuel"].str.lower() == fuel.lower()]

        if transmission and transmission.lower() != "all":
            filtered = filtered[filtered["transmission"].str.lower() == transmission.lower()]

        if min_year:
            filtered = filtered[filtered["year"] >= min_year]
        if max_year:
            filtered = filtered[filtered["year"] <= max_year]

        if search:
            q = search.lower().strip()
            filtered = filtered[filtered["name"].str.lower().str.contains(q, na=False)]

        total = len(filtered)
        total_pages = max(1, (total + page_size - 1) // page_size)

        start = (page - 1) * page_size
        end = start + page_size

        records_slice = filtered.iloc[start:end].to_dict(orient="records")

        # Format price in each record for display
        for r in records_slice:
            p = float(r["selling_price"])
            if p >= 1e7:
                r["formatted_price"] = f"₹{p / 1e7:.2f} Cr"
            elif p >= 1e5:
                r["formatted_price"] = f"₹{p / 1e5:.2f} Lakh"
            else:
                r["formatted_price"] = f"₹{p:,.0f}"

        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
            "records": records_slice
        }

    def get_options(self) -> Dict[str, Any]:
        if not self.is_initialized:
            self.initialize()

        df = self.df
        return {
            "brands": sorted(df["brand"].unique().tolist()),
            "fuels": sorted(df["fuel"].unique().tolist()),
            "transmissions": sorted(df["transmission"].unique().tolist()),
            "seller_types": sorted(df["seller_type"].unique().tolist()),
            "owners": ["First Owner", "Second Owner", "Third Owner", "Fourth & Above Owner", "Test Drive Car"],
            "years": sorted(df["year"].unique().tolist(), reverse=True)
        }

    def get_metrics(self) -> Dict[str, Any]:
        if not self.is_initialized:
            self.initialize()
        return self.metadata

    def get_feature_importance(self) -> List[Dict[str, Any]]:
        if not self.is_initialized:
            self.initialize()

        coefs = self.metadata.get("feature_importances_or_coefs", {})
        # Sort coefficients by absolute impact
        items = []
        for feat, val in coefs.items():
            impact_direction = "positive" if val > 0 else "negative"
            # Friendly label
            clean_name = feat.replace("brand_", "Brand: ").replace("fuel_", "Fuel: ").replace("transmission_", "Transmission: ").replace("seller_type_", "Seller: ").replace("owner_", "Owner: ")
            items.append({
                "feature": feat,
                "display_name": clean_name,
                "coefficient": round(float(val), 4),
                "abs_impact": round(abs(float(val)), 4),
                "direction": impact_direction
            })

        items.sort(key=lambda x: x["abs_impact"], reverse=True)
        return items
