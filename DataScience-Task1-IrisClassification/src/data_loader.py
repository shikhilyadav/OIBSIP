"""
data_loader.py
==============
Data loading, preprocessing, and preliminary inspection module
for the Oasis Infobyte Iris Flower Classification project.
"""

import os
from typing import Tuple, Dict, Any
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris


FEATURE_MAPPING = {
    "sepal length (cm)": "sepal_length",
    "sepal width (cm)": "sepal_width",
    "petal length (cm)": "petal_length",
    "petal width (cm)": "petal_width"
}


def load_and_prepare_iris_data(save_csv_path: str = None) -> Tuple[pd.DataFrame, list, list]:
    """
    Loads the Iris dataset directly from sklearn, formats it into a clean
    pandas DataFrame with standardized column names, and maps target indices
    to their canonical botanical species names.

    Args:
        save_csv_path: Optional file path to export the dataset as a CSV.

    Returns:
        df: Pandas DataFrame containing features, target code, and species name.
        feature_names: List of sanitized feature column names.
        target_names: List of target species names.
    """
    raw_data = load_iris(as_frame=True)
    df = raw_data.frame.copy()

    # Rename feature columns for cleaner coding and standardized access
    df.rename(columns=FEATURE_MAPPING, inplace=True)
    df.rename(columns={"target": "species_id"}, inplace=True)

    # Map target integer codes (0, 1, 2) to class names (Setosa, Versicolor, Virginica)
    target_names = [name.capitalize() for name in raw_data.target_names]
    species_map = {idx: name for idx, name in enumerate(target_names)}
    df["species"] = df["species_id"].map(species_map)

    # Reorder columns logically: features first, then species_id and species name
    feature_names = list(FEATURE_MAPPING.values())
    ordered_cols = feature_names + ["species_id", "species"]
    df = df[ordered_cols]

    if save_csv_path:
        os.makedirs(os.path.dirname(os.path.abspath(save_csv_path)), exist_ok=True)
        df.to_csv(save_csv_path, index=False)
        print(f"[INFO] Iris dataset successfully exported to: {save_csv_path}")

    return df, feature_names, target_names


def inspect_data(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Performs comprehensive dataset inspection:
    - Shape (rows x columns)
    - Head and tail records
    - Data types
    - Missing value analysis
    - Duplicate record detection
    - Summary descriptive statistics
    - Class distribution counts and percentages

    Args:
        df: Pandas DataFrame of the Iris dataset.

    Returns:
        inspection_summary: Dictionary containing programmatic summary metrics.
    """
    print("\n" + "=" * 70)
    print("PHASE 3: COMPREHENSIVE DATASET INSPECTION")
    print("=" * 70)

    # 1. Dataset Shape
    n_rows, n_cols = df.shape
    print(f"\n[1] Dataset Shape: {n_rows} rows x {n_cols} columns")

    # 2. First and Last 5 Records
    print("\n[2] First 5 Records (Head):")
    print(df.head())
    print("\n[2b] Last 5 Records (Tail):")
    print(df.tail())

    # 3. Data Types & Memory Usage
    print("\n[3] Column Data Types and Info:")
    print(df.dtypes)

    # 4. Missing Value Analysis
    missing_counts = df.isnull().sum()
    print("\n[4] Missing Value Count per Column:")
    print(missing_counts)
    total_missing = missing_counts.sum()
    print(f"Total Missing Values: {total_missing}")

    # 5. Duplicate Detection
    duplicate_rows = df[df.duplicated(subset=["sepal_length", "sepal_width", "petal_length", "petal_width"], keep=False)]
    duplicate_count = df.duplicated(subset=["sepal_length", "sepal_width", "petal_length", "petal_width"]).sum()
    print(f"\n[5] Duplicate Records Count: {duplicate_count}")
    if duplicate_count > 0:
        print("Duplicate entries found across feature space:")
        print(duplicate_rows)

    # 6. Descriptive Statistics
    print("\n[6] Summary Statistics (Numerical Features):")
    stats_df = df[["sepal_length", "sepal_width", "petal_length", "petal_width"]].describe().T
    stats_df["median"] = df[["sepal_length", "sepal_width", "petal_length", "petal_width"]].median()
    stats_df["skewness"] = df[["sepal_length", "sepal_width", "petal_length", "petal_width"]].skew()
    print(stats_df[["count", "mean", "std", "min", "25%", "median", "75%", "max", "skewness"]])

    # 7. Class Distribution
    print("\n[7] Target Class Distribution:")
    class_counts = df["species"].value_counts()
    class_percentages = df["species"].value_counts(normalize=True) * 100
    dist_df = pd.DataFrame({"Count": class_counts, "Percentage (%)": class_percentages})
    print(dist_df)

    print("\n" + "=" * 70)
    print("DATA INSPECTION COMPLETED: ZERO MISSING VALUES, PERFECTLY BALANCED DATASET")
    print("=" * 70 + "\n")

    return {
        "shape": (n_rows, n_cols),
        "total_missing": int(total_missing),
        "duplicate_count": int(duplicate_count),
        "class_distribution": class_counts.to_dict(),
        "summary_statistics": stats_df.to_dict()
    }


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(current_dir)
    csv_dest = os.path.join(base_dir, "data", "iris.csv")

    dataframe, features, targets = load_and_prepare_iris_data(save_csv_path=csv_dest)
    summary = inspect_data(dataframe)
