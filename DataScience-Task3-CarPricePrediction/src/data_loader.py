"""
data_loader.py
==============
Data Ingestion, Provenance, and Raw Dataset Loader for Task 3:
Car Price Prediction with Machine Learning.

Dataset Provenance:
- Source: CarDekho Used Car Dataset ("CAR DETAILS FROM CAR DEKHO.csv")
- Origin: Scraped from CarDekho.com public vehicle listings
- Provider: Kaggle Public Datasets (Vehicle Dataset from CarDekho by Nehal Birla / Akshay Khare)
- Terms of Use / License: Database: Open Database, Contents: Database Contents
- Origin Attribution: CarDekho.com public vehicle listings
- File Attributes: 4,340 records, 8 columns
"""

import os
import sys
import pandas as pd
from typing import Dict, Any, Optional

# Project paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(CURRENT_DIR)
DATA_DIR = os.path.join(PROJECT_DIR, "data")
RAW_DATA_PATH = os.path.join(DATA_DIR, "raw", "car_details.csv")
PROCESSED_DATA_PATH = os.path.join(DATA_DIR, "processed", "car_details_cleaned.csv")

DATASET_METADATA: Dict[str, Any] = {
    "dataset_name": "CarDekho Used Car Details Dataset",
    "filename": "car_details.csv",
    "expected_rows": 4340,
    "expected_cols": 8,
    "columns": [
        "name", "year", "selling_price", "km_driven",
        "fuel", "seller_type", "transmission", "owner"
    ],
    "source": "CarDekho.com listings via Kaggle Public Datasets",
    "license": "Database: Open Database, Contents: Database Contents",
    "primary_mirror_url": "https://raw.githubusercontent.com/IMvision12/Car-Price_prediction/main/CAR%20DETAILS%20FROM%20CAR%20DEKHO.csv"
}


def get_project_paths() -> Dict[str, str]:
    """Returns absolute paths for all key Task 3 directories and files."""
    return {
        "project_dir": PROJECT_DIR,
        "raw_csv": RAW_DATA_PATH,
        "processed_csv": PROCESSED_DATA_PATH,
        "models_dir": os.path.join(PROJECT_DIR, "models"),
        "visualizations_dir": os.path.join(PROJECT_DIR, "visualizations"),
        "pipeline_model": os.path.join(PROJECT_DIR, "models", "car_price_pipeline.joblib"),
        "model_metadata": os.path.join(PROJECT_DIR, "models", "model_metadata.json"),
    }


def load_raw_data(filepath: Optional[str] = None) -> pd.DataFrame:
    """
    Loads raw CarDekho dataset from disk.
    
    Parameters
    ----------
    filepath : str, optional
        Custom path to car_details.csv. Defaults to data/raw/car_details.csv.
        
    Returns
    -------
    pd.DataFrame
        Loaded raw DataFrame with shape (4340, 8).
    """
    path = filepath or RAW_DATA_PATH
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Raw dataset not found at '{path}'.\n"
            f"Please download the CarDekho dataset from {DATASET_METADATA['primary_mirror_url']} "
            f"and place it at '{RAW_DATA_PATH}'."
        )
    
    df = pd.read_csv(path)
    
    # Validation checks
    assert df.shape[0] == DATASET_METADATA["expected_rows"], (
        f"Expected {DATASET_METADATA['expected_rows']} rows, found {df.shape[0]}"
    )
    for col in DATASET_METADATA["columns"]:
        assert col in df.columns, f"Expected column '{col}' missing from raw dataset."
        
    return df


if __name__ == "__main__":
    df_raw = load_raw_data()
    print(f"[DATA LOADER] Raw dataset loaded successfully: {df_raw.shape[0]} rows, {df_raw.shape[1]} columns.")
    print("[DATA LOADER] Sample Records:")
    print(df_raw.head(3))
