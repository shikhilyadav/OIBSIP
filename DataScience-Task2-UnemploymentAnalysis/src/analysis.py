"""
analysis.py
===========
Core Analytical Engine for Oasis Infobyte Task 2:
Unemployment Analysis with Python (India).

Calculates descriptive statistics, state and regional rankings,
monthly aggregations, correlation matrices, and Pre vs. Post COVID-19
impact evaluations with economic rigor.
"""

import os
import sys
import json
from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np

# Ensure src in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from data_loader import get_project_paths


def compute_descriptive_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes Mean, Median, Mode, Std Dev, Min, Max, and Quartiles (25%, 75%)
    for all core macroeconomic indicators.
    """
    indicators = [
        "Estimated_Unemployment_Rate",
        "Estimated_Employed",
        "Estimated_Labour_Participation_Rate"
    ]
    summary_records = []
    for ind in indicators:
        s = df[ind].dropna()
        mode_val = s.mode().iloc[0] if not s.mode().empty else np.nan
        summary_records.append({
            "Indicator": ind,
            "Mean": round(float(s.mean()), 2),
            "Median": round(float(s.median()), 2),
            "Mode": round(float(mode_val), 2),
            "Std_Dev": round(float(s.std()), 2),
            "Min": round(float(s.min()), 2),
            "Q1_25%": round(float(s.quantile(0.25)), 2),
            "Q3_75%": round(float(s.quantile(0.75)), 2),
            "Max": round(float(s.max()), 2)
        })
    return pd.DataFrame(summary_records)


def compute_regional_analysis(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Computes state-level and macro-zone-level average unemployment rates,
    rankings, and variance metrics.
    """
    # 1. State-level ranking
    state_summary = df.groupby("State").agg(
        Avg_Unemployment_Rate=("Estimated_Unemployment_Rate", "mean"),
        Median_Unemployment_Rate=("Estimated_Unemployment_Rate", "median"),
        Std_Unemployment_Rate=("Estimated_Unemployment_Rate", "std"),
        Avg_Labour_Participation=("Estimated_Labour_Participation_Rate", "mean"),
        Total_Employed_Mean=("Estimated_Employed", "mean"),
        Sample_Count=("Estimated_Unemployment_Rate", "count")
    ).reset_index()

    state_summary["Avg_Unemployment_Rate"] = state_summary["Avg_Unemployment_Rate"].round(2)
    state_summary["Median_Unemployment_Rate"] = state_summary["Median_Unemployment_Rate"].round(2)
    state_summary["Std_Unemployment_Rate"] = state_summary["Std_Unemployment_Rate"].round(2)
    state_summary["Avg_Labour_Participation"] = state_summary["Avg_Labour_Participation"].round(2)
    state_summary["Total_Employed_Mean"] = state_summary["Total_Employed_Mean"].round(0)

    state_summary.sort_values(by="Avg_Unemployment_Rate", ascending=False, inplace=True)
    state_summary["Rank"] = range(1, len(state_summary) + 1)

    # 2. Macro-zone ranking
    zone_summary = df.groupby("Zone").agg(
        Avg_Unemployment_Rate=("Estimated_Unemployment_Rate", "mean"),
        Median_Unemployment_Rate=("Estimated_Unemployment_Rate", "median"),
        Avg_Labour_Participation=("Estimated_Labour_Participation_Rate", "mean"),
        Total_Employed_Mean=("Estimated_Employed", "mean")
    ).reset_index()

    zone_summary = zone_summary.round(2).sort_values(by="Avg_Unemployment_Rate", ascending=False)
    return state_summary, zone_summary


def compute_monthly_trends(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates national unemployment and employment indicators across months.
    """
    monthly = df.groupby(["Year", "Month", "Year_Month", "Month_Name", "COVID_Phase"]).agg(
        Avg_Unemployment_Rate=("Estimated_Unemployment_Rate", "mean"),
        Median_Unemployment_Rate=("Estimated_Unemployment_Rate", "median"),
        Min_Unemployment_Rate=("Estimated_Unemployment_Rate", "min"),
        Max_Unemployment_Rate=("Estimated_Unemployment_Rate", "max"),
        Avg_Labour_Participation=("Estimated_Labour_Participation_Rate", "mean"),
        Total_Employed_Sum=("Estimated_Employed", "sum")
    ).reset_index()

    monthly.sort_values(by=["Year", "Month"], inplace=True)
    monthly["Avg_Unemployment_Rate"] = monthly["Avg_Unemployment_Rate"].round(2)
    monthly["Median_Unemployment_Rate"] = monthly["Median_Unemployment_Rate"].round(2)
    monthly["Avg_Labour_Participation"] = monthly["Avg_Labour_Participation"].round(2)
    monthly["MoM_Rate_Change"] = monthly["Avg_Unemployment_Rate"].diff().round(2)
    return monthly


def compute_covid_impact_analysis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyzes Pre-COVID vs. COVID/Post-COVID macroeconomic shift.
    Pre-COVID: Date < 2020-03-01
    COVID/Post-COVID: Date >= 2020-03-01
    """
    pre = df[df["COVID_Phase"] == "Pre-COVID"]
    post = df[df["COVID_Phase"] == "COVID/Post-COVID"]

    pre_mean = pre["Estimated_Unemployment_Rate"].mean()
    post_mean = post["Estimated_Unemployment_Rate"].mean()
    pre_median = pre["Estimated_Unemployment_Rate"].median()
    post_median = post["Estimated_Unemployment_Rate"].median()

    abs_diff_mean = post_mean - pre_mean
    pct_change_mean = (abs_diff_mean / pre_mean) * 100

    # Sector breakdown (Rural vs Urban)
    rural_pre = pre[pre["Area"] == "Rural"]["Estimated_Unemployment_Rate"].mean()
    rural_post = post[post["Area"] == "Rural"]["Estimated_Unemployment_Rate"].mean()
    urban_pre = pre[pre["Area"] == "Urban"]["Estimated_Unemployment_Rate"].mean()
    urban_post = post[post["Area"] == "Urban"]["Estimated_Unemployment_Rate"].mean()

    # State-level Pre vs Post delta
    state_pivot = df.pivot_table(
        index="State",
        columns="COVID_Phase",
        values="Estimated_Unemployment_Rate",
        aggfunc="mean"
    ).reset_index()

    state_pivot["Abs_Increase"] = (state_pivot["COVID/Post-COVID"] - state_pivot["Pre-COVID"]).round(2)
    state_pivot["Pct_Increase"] = ((state_pivot["Abs_Increase"] / state_pivot["Pre-COVID"]) * 100).round(2)
    state_pivot.sort_values(by="Abs_Increase", ascending=False, inplace=True)

    return {
        "pre_covid_mean": round(float(pre_mean), 2),
        "post_covid_mean": round(float(post_mean), 2),
        "pre_covid_median": round(float(pre_median), 2),
        "post_covid_median": round(float(post_median), 2),
        "absolute_increase_mean": round(float(abs_diff_mean), 2),
        "percent_change_mean": round(float(pct_change_mean), 2),
        "rural_pre_covid_mean": round(float(rural_pre), 2),
        "rural_post_covid_mean": round(float(rural_post), 2),
        "urban_pre_covid_mean": round(float(urban_pre), 2),
        "urban_post_covid_mean": round(float(urban_post), 2),
        "state_impact_table": state_pivot.to_dict(orient="records")
    }


def compute_correlation_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes Pearson correlation matrix between macroeconomic features.
    """
    cols = [
        "Estimated_Unemployment_Rate",
        "Estimated_Employed",
        "Estimated_Labour_Participation_Rate"
    ]
    return df[cols].corr(method="pearson").round(3)


def run_full_analysis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Executes end-to-end analytical pipeline and returns consolidated dictionary.
    """
    desc_stats = compute_descriptive_statistics(df)
    state_ranks, zone_ranks = compute_regional_analysis(df)
    monthly_trends = compute_monthly_trends(df)
    covid_impact = compute_covid_impact_analysis(df)
    corr_matrix = compute_correlation_analysis(df)

    top_state = state_ranks.iloc[0]["State"]
    top_rate = state_ranks.iloc[0]["Avg_Unemployment_Rate"]
    lowest_state = state_ranks.iloc[-1]["State"]
    lowest_rate = state_ranks.iloc[-1]["Avg_Unemployment_Rate"]

    overall_avg_unemployment = round(float(df["Estimated_Unemployment_Rate"].mean()), 2)
    overall_avg_labour_part = round(float(df["Estimated_Labour_Participation_Rate"].mean()), 2)

    return {
        "kpis": {
            "overall_avg_unemployment": overall_avg_unemployment,
            "overall_avg_labour_part": overall_avg_labour_part,
            "highest_state": top_state,
            "highest_state_rate": top_rate,
            "lowest_state": lowest_state,
            "lowest_state_rate": lowest_rate
        },
        "descriptive_statistics": desc_stats.to_dict(orient="records"),
        "top_10_states": state_ranks.head(10).to_dict(orient="records"),
        "bottom_5_states": state_ranks.tail(5).to_dict(orient="records"),
        "state_rankings": state_ranks.to_dict(orient="records"),
        "zone_rankings": zone_ranks.to_dict(orient="records"),
        "monthly_trends": monthly_trends.to_dict(orient="records"),
        "covid_impact": covid_impact,
        "correlation_matrix": corr_matrix.to_dict()
    }


if __name__ == "__main__":
    paths = get_project_paths()
    clean_csv = paths["clean_csv"]
    if not os.path.exists(clean_csv):
        print(f"[ERROR] Cleaned dataset not found at {clean_csv}. Please run data_cleaning.py first.")
        sys.exit(1)

    clean_df = pd.read_csv(clean_csv)
    results = run_full_analysis(clean_df)
    print("\n" + "=" * 70)
    print("PHASE 5 & 6: ANALYTICAL SUMMARY & KEY KPIS")
    print("=" * 70)
    for k, v in results["kpis"].items():
        print(f"  {k:30s}: {v}")
    print("\nPre vs Post COVID Impact:")
    print(f"  Pre-COVID Mean Rate : {results['covid_impact']['pre_covid_mean']}%")
    print(f"  Post-COVID Mean Rate: {results['covid_impact']['post_covid_mean']}%")
    print(f"  Absolute Increase   : +{results['covid_impact']['absolute_increase_mean']}%")
    print(f"  Percent Change      : +{results['covid_impact']['percent_change_mean']}%")
    print("=" * 70)
