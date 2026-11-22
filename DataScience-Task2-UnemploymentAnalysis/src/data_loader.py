"""
data_loader.py
==============
Data Ingestion and Provenance Tracking module for
Oasis Infobyte Task 2: Unemployment Analysis with Python (India).

Preserves authentic raw datasets in `data/raw/` and documents
provenance, source URLs, and data dictionaries.
"""

import os
import sys
import urllib.request
from typing import Tuple, Dict, Any, Optional
import pandas as pd

# Source attribution & metadata
DATASET_METADATA = {
    "source_name": "Centre for Monitoring Indian Economy (CMIE) - Consumer Pyramids Household Survey",
    "provider": "Kaggle Public Datasets / CMIE Open Data",
    "license": "CC BY-SA 4.0 / Public Open Data for Educational & Research Use",
    "primary_url": "https://raw.githubusercontent.com/yuvrajsaraogi/Unemployment-Analysis-with-Python/main/Unemployment%20in%20India.csv",
    "secondary_url": "https://raw.githubusercontent.com/amankharwal/Website-data/master/unemployment.csv",
    "geographical_coverage": "28 Indian States and Union Territories across Rural & Urban Sectors",
    "time_span": "May 2019 to June 2020 (Monthly observations covering Pre-COVID and Peak Pandemic Lockdown)"
}


def get_project_paths() -> Dict[str, str]:
    """Resolves absolute paths for project directories."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    return {
        "root": project_root,
        "raw_dir": os.path.join(project_root, "data", "raw"),
        "processed_dir": os.path.join(project_root, "data", "processed"),
        "vis_dir": os.path.join(project_root, "visualizations"),
        "models_dir": os.path.join(project_root, "models"),
        "raw_csv": os.path.join(project_root, "data", "raw", "Unemployment_in_India.csv"),
        "state_coords_csv": os.path.join(project_root, "data", "raw", "Unemployment_Rate_upto_11_2020.csv"),
        "clean_csv": os.path.join(project_root, "data", "processed", "unemployment_cleaned.csv")
    }


def download_dataset_if_missing() -> Tuple[str, str]:
    """
    Verifies that raw datasets exist in data/raw/; downloads from authentic
    public mirrors if not present.
    """
    paths = get_project_paths()
    os.makedirs(paths["raw_dir"], exist_ok=True)

    # 1. Primary dataset (Rural + Urban split)
    if not os.path.exists(paths["raw_csv"]):
        print(f"[INFO] Downloading primary raw dataset from {DATASET_METADATA['primary_url']}...")
        req = urllib.request.Request(DATASET_METADATA["primary_url"], headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp, open(paths["raw_csv"], "wb") as f:
            f.write(resp.read())
        print(f"[SUCCESS] Downloaded primary raw dataset ({os.path.getsize(paths['raw_csv'])} bytes).")

    # 2. Secondary dataset (Coordinates & macro regions)
    if not os.path.exists(paths["state_coords_csv"]):
        print(f"[INFO] Downloading secondary raw dataset from {DATASET_METADATA['secondary_url']}...")
        req = urllib.request.Request(DATASET_METADATA["secondary_url"], headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp, open(paths["state_coords_csv"], "wb") as f:
            f.write(resp.read())
        print(f"[SUCCESS] Downloaded secondary raw dataset ({os.path.getsize(paths['state_coords_csv'])} bytes).")

    return paths["raw_csv"], paths["state_coords_csv"]


def load_raw_unemployment_data(raw_path: Optional[str] = None) -> pd.DataFrame:
    """
    Loads raw unmodified unemployment dataset.

    Args:
        raw_path: Optional file path. If None, default project path is used.

    Returns:
        pd.DataFrame: Raw dataset.
    """
    if raw_path is None:
        raw_path, _ = download_dataset_if_missing()

    df = pd.read_csv(raw_path)
    print(f"[DATA LOADER] Raw dataset loaded: {df.shape[0]} rows x {df.shape[1]} columns.")
    print(f"[DATA LOADER] Raw column names: {list(df.columns)}")
    return df


if __name__ == "__main__":
    download_dataset_if_missing()
    raw_df = load_raw_unemployment_data()
    print("\nDataset Metadata:")
    for k, v in DATASET_METADATA.items():
        print(f"  {k}: {v}")
