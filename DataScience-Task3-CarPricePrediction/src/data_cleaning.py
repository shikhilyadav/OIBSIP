"""
data_cleaning.py
================
Data Cleaning and Validation Engine for Task 3:
Car Price Prediction with Machine Learning.

Handles missing values, duplicate detection, string whitespace trimming,
brand naming standardisation, and statistical anomaly validation.
"""

import os
import sys
import pandas as pd
from typing import Tuple, Dict, Any, Optional

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from data_loader import load_raw_data, get_project_paths


def clean_car_data(
    df_raw: pd.DataFrame,
    export_path: Optional[str] = None
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Cleans raw CarDekho dataset and returns cleaned DataFrame along with quality report.
    
    Cleaning Pipeline:
    1. Whitespace stripping on all string columns.
    2. Missing value audit (confirms 0 missing values).
    3. Duplicate record detection and elimination (763 exact duplicates dropped to prevent train/test leakage).
    4. Brand extraction and name standardisation (e.g., OpelCorsa -> Opel, Land Rover).
    5. Numeric sanity verification on year, km_driven, and selling_price.
    6. Export cleaned dataset to data/processed/car_details_cleaned.csv.
    """
    df = df_raw.copy()
    initial_rows = len(df)
    
    # 1. Strip whitespace on string columns
    str_cols = df.select_dtypes(include=["object", "string"]).columns
    for c in str_cols:
        df[c] = df[c].astype(str).str.strip()
        
    # 2. Missing value evaluation
    missing_counts = df.isnull().sum().to_dict()
    total_missing = sum(missing_counts.values())
    
    # 3. Duplicate detection & removal
    duplicate_count = int(df.duplicated().sum())
    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True)
    dedup_rows = len(df)
    
    # 4. Standardize brand from car name
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

    df["brand"] = df["name"].apply(get_clean_brand)
    
    # 5. Calculate car_age (Data collected up to 2020)
    REFERENCE_YEAR = 2020
    df["car_age"] = REFERENCE_YEAR - df["year"]
    
    # Sanity bounds check
    assert (df["car_age"] >= 0).all(), "Car age must be non-negative relative to reference year 2020."
    assert (df["km_driven"] > 0).all(), "Kilometres driven must be positive."
    assert (df["selling_price"] > 0).all(), "Selling price must be strictly positive."
    
    # 6. Quality audit summary
    quality_report: Dict[str, Any] = {
        "initial_rows": initial_rows,
        "cleaned_rows": dedup_rows,
        "dropped_duplicates": duplicate_count,
        "total_missing_values": total_missing,
        "unique_brands": int(df["brand"].nunique()),
        "year_min": int(df["year"].min()),
        "year_max": int(df["year"].max()),
        "km_min": int(df["km_driven"].min()),
        "km_max": int(df["km_driven"].max()),
        "price_min": int(df["selling_price"].min()),
        "price_max": int(df["selling_price"].max()),
        "price_median": float(df["selling_price"].median()),
        "price_mean": float(df["selling_price"].mean())
    }
    
    # 7. Export if requested
    paths = get_project_paths()
    save_dest = export_path or paths["processed_csv"]
    os.makedirs(os.path.dirname(save_dest), exist_ok=True)
    df.to_csv(save_dest, index=False)
    
    return df, quality_report


if __name__ == "__main__":
    df_raw = load_raw_data()
    df_clean, report = clean_car_data(df_raw)
    print("\n" + "=" * 65)
    print("DATA CLEANING & QUALITY AUDIT SUMMARY")
    print("=" * 65)
    for k, v in report.items():
        print(f"  {k:28s}: {v}")
    print("=" * 65)
