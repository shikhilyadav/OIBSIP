"""
data_cleaning.py
================
Data Cleaning, Schema Standardization, and Feature Engineering module
for Oasis Infobyte Task 2: Unemployment Analysis with Python.

Performs:
- Header whitespace stripping & standard nomenclature mapping.
- Trailing null row removal with documented economic reasoning.
- ISO-compliant Datetime parsing (%d-%m-%Y).
- Categorical region & area whitespace trimming.
- Macro-zone geographic classification (North, South, East, West, Northeast).
- Temporal feature engineering (Year, Month, Month Name, COVID Phase).
- Outlier investigation using IQR method with domain contextualization.
- Generation of Before vs. After Data Quality Audit Report.
- Export to `data/processed/unemployment_cleaned.csv`.
"""

import os
import sys
import numpy as np
import pandas as pd
from typing import Tuple, Dict, Any

# Ensure src in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from data_loader import get_project_paths, load_raw_unemployment_data

# Standard column mapping dictionary
COLUMN_RENAME_MAP = {
    "Region": "State",
    "Date": "Date",
    "Frequency": "Frequency",
    "Estimated Unemployment Rate (%)": "Estimated_Unemployment_Rate",
    "Estimated Employed": "Estimated_Employed",
    "Estimated Labour Participation Rate (%)": "Estimated_Labour_Participation_Rate",
    "Area": "Area"
}

# Indian State -> Macro Geographical Zone Mapping
MACRO_ZONE_MAPPING = {
    "Andhra Pradesh": "South",
    "Telangana": "South",
    "Karnataka": "South",
    "Kerala": "South",
    "Tamil Nadu": "South",
    "Puducherry": "South",
    "Delhi": "North",
    "Haryana": "North",
    "Himachal Pradesh": "North",
    "Jammu & Kashmir": "North",
    "Punjab": "North",
    "Rajasthan": "North",
    "Chandigarh": "North",
    "Uttar Pradesh": "North",
    "Uttarakhand": "North",
    "Bihar": "East",
    "Jharkhand": "East",
    "Odisha": "East",
    "West Bengal": "East",
    "Gujarat": "West",
    "Maharashtra": "West",
    "Goa": "West",
    "Madhya Pradesh": "Central",
    "Chhattisgarh": "Central",
    "Assam": "Northeast",
    "Meghalaya": "Northeast",
    "Sikkim": "Northeast",
    "Tripura": "Northeast"
}


def clean_unemployment_data(raw_df: pd.DataFrame, export_path: str = None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Transforms raw CMIE dataset into a high-integrity analytical dataset.

    Args:
        raw_df: Raw pandas DataFrame.
        export_path: Destination path for cleaned CSV.

    Returns:
        cleaned_df: Cleaned and feature-engineered DataFrame.
        quality_report: Dictionary with before-and-after audit metrics.
    """
    raw_rows, raw_cols = raw_df.shape
    raw_null_count = int(raw_df.isnull().sum().sum())
    raw_dup_count = int(raw_df.duplicated().sum())

    df = raw_df.copy()

    # 1. Strip whitespace from column headers
    df.columns = [c.strip() for c in df.columns]

    # 2. Rename columns to standardized snake_case format
    df.rename(columns=COLUMN_RENAME_MAP, inplace=True)

    # 3. Handle trailing empty rows
    # The raw CMIE dataset contains 28 completely blank trailing rows (rows 740-767).
    # These represent empty file padding rather than missing observation data.
    empty_row_mask = df["State"].isnull() & df["Date"].isnull()
    dropped_empty_rows = int(empty_row_mask.sum())
    df = df[~empty_row_mask].copy()

    # 4. Strip whitespace from string columns
    df["State"] = df["State"].astype(str).str.strip()
    df["Area"] = df["Area"].astype(str).str.strip()
    df["Frequency"] = df["Frequency"].astype(str).str.strip()

    # Standardize state naming conventions if needed
    state_cleanup = {
        "Jammu & Kashmir": "Jammu and Kashmir"
    }
    df["State"] = df["State"].replace(state_cleanup)

    # 5. Parse Datetime (%d-%m-%Y)
    df["Date"] = pd.to_datetime(df["Date"].str.strip(), format="%d-%m-%Y")

    # 6. Ensure numerical columns are correctly cast
    numeric_cols = ["Estimated_Unemployment_Rate", "Estimated_Employed", "Estimated_Labour_Participation_Rate"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # 7. Check for duplicate observation records
    subset_cols = ["State", "Date", "Area"]
    duplicate_count_cleaned = int(df.duplicated(subset=subset_cols).sum())

    # 8. Feature Engineering:
    # A. Macro Zone
    df["Zone"] = df["State"].map(MACRO_ZONE_MAPPING).fillna("Other")

    # B. Temporal features
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Month_Name"] = df["Date"].dt.strftime("%b")
    df["Year_Month"] = df["Date"].dt.strftime("%Y-%m")

    # C. COVID-19 Phase Indicator:
    # Pre-COVID: Prior to 1st March 2020 (May 2019 to February 2020)
    # COVID/Post-COVID: March 2020 onward (National Lockdown introduced March 24, 2020)
    df["COVID_Phase"] = np.where(df["Date"] < pd.Timestamp("2020-03-01"), "Pre-COVID", "COVID/Post-COVID")

    # 9. Outlier Investigation (Tukey's IQR method)
    q1 = df["Estimated_Unemployment_Rate"].quantile(0.25)
    q3 = df["Estimated_Unemployment_Rate"].quantile(0.75)
    iqr = q3 - q1
    lower_bound = max(0.0, q1 - 1.5 * iqr)
    upper_bound = q3 + 1.5 * iqr
    outlier_df = df[df["Estimated_Unemployment_Rate"] > upper_bound]
    outlier_count = len(outlier_df)

    # Note: Outliers during April-May 2020 (Unemployment > 30% up to 75.8%)
    # represent genuine macroeconomic lockdown shocks (e.g. Puducherry 75.8%, Jharkhand 59.2%),
    # NOT data entry errors. They are preserved to ensure authentic historical analysis.

    # Sort logically by Date, State, and Area
    df.sort_values(by=["Date", "State", "Area"], inplace=True)
    df.reset_index(drop=True, inplace=True)

    # 10. Compile Quality Audit Report
    quality_report = {
        "raw_shape": (raw_rows, raw_cols),
        "cleaned_shape": df.shape,
        "raw_null_count": raw_null_count,
        "cleaned_null_count": int(df.isnull().sum().sum()),
        "dropped_empty_rows": dropped_empty_rows,
        "raw_duplicates": raw_dup_count,
        "cleaned_duplicates": duplicate_count_cleaned,
        "outlier_count_iqr": outlier_count,
        "outlier_upper_threshold": round(upper_bound, 2),
        "date_range": (df["Date"].min().strftime("%Y-%m-%d"), df["Date"].max().strftime("%Y-%m-%d")),
        "unique_states_count": df["State"].nunique(),
        "sectors": df["Area"].value_counts().to_dict(),
        "covid_phase_distribution": df["COVID_Phase"].value_counts().to_dict()
    }

    # 11. Export to data/processed/
    if export_path:
        os.makedirs(os.path.dirname(os.path.abspath(export_path)), exist_ok=True)
        df.to_csv(export_path, index=False)
        print(f"[SUCCESS] Cleaned dataset saved to: {export_path}")

    return df, quality_report


if __name__ == "__main__":
    paths = get_project_paths()
    raw = load_raw_unemployment_data(paths["raw_csv"])
    clean_df, report = clean_unemployment_data(raw, export_path=paths["clean_csv"])

    print("\n" + "=" * 70)
    print("PHASE 4: DATA CLEANING QUALITY AUDIT REPORT")
    print("=" * 70)
    for k, v in report.items():
        print(f"  {k:30s}: {v}")
    print("=" * 70)
