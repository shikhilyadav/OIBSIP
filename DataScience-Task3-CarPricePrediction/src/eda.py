"""
eda.py
======
Exploratory Data Analysis and Visualization Suite for Task 3:
Car Price Prediction with Machine Learning.

Generates 8 high-resolution publication-grade PNG figures saved to `visualizations/`:
1. `selling_price_distribution.png`: Histogram + KDE + Boxplot of selling price
2. `price_vs_car_age.png`: Price depreciation vs car age with regression curve
3. `price_vs_km_driven.png`: Price vs odometer mileage
4. `price_by_fuel.png`: Price distributions across fuel types
5. `price_by_transmission.png`: Price comparison between Manual and Automatic
6. `brand_avg_selling_price.png`: Brand-wise average price ranking
7. `correlation_heatmap.png`: Correlation matrix of numeric features
8. `feature_relationships.png`: Multi-attribute interactions across fuel & transmission
"""

import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Dict, Any

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from data_loader import get_project_paths

# Professional emerald-green palette
THEME_PRIMARY = "#059669"    # Emerald Green
THEME_SECONDARY = "#2563eb"  # Royal Blue
THEME_ACCENT = "#dc2626"     # Crimson Red
THEME_DARK = "#1e293b"       # Slate 800
THEME_LIGHT = "#f8fafc"      # Slate 50

plt.rcParams.update({
    "font.family": "sans-serif",
    "figure.titlesize": 14,
    "axes.titlesize": 12,
    "axes.labelsize": 11,
    "xtick.labelsize": 9.5,
    "ytick.labelsize": 9.5,
    "axes.edgecolor": "#cbd5e1",
    "axes.linewidth": 1.0,
    "grid.color": "#e2e8f0",
    "grid.linestyle": "--",
    "grid.alpha": 0.65
})


def format_inr(val: float) -> str:
    """Formats numeric value into INR Lakhs / Crores string."""
    if val >= 1e7:
        return f"₹{val/1e7:.2f} Cr"
    elif val >= 1e5:
        return f"₹{val/1e5:.2f} Lakh"
    else:
        return f"₹{val:,.0f}"


def generate_exploratory_visualizations(df: pd.DataFrame, output_dir: str) -> None:
    """Generates the 8 core exploratory visualizations."""
    os.makedirs(output_dir, exist_ok=True)

    # -------------------------------------------------------------------------
    # 1. Selling Price Distribution (Boxplot + Histogram + KDE)
    # -------------------------------------------------------------------------
    fig, (ax_box, ax_hist) = plt.subplots(
        2, 1, figsize=(10, 6.5), sharex=True,
        gridspec_kw={"height_ratios": [0.22, 0.78]}, dpi=300
    )
    sns.boxplot(x=df["selling_price"] / 1e5, ax=ax_box, color=THEME_PRIMARY, fliersize=3)
    ax_box.set(xlabel="", title="Selling Price Distribution (in Lakhs INR)")
    ax_box.grid(True)

    sns.histplot(df["selling_price"] / 1e5, kde=True, ax=ax_hist, color=THEME_PRIMARY, bins=40)
    ax_hist.axvline(df["selling_price"].median() / 1e5, color=THEME_ACCENT, linestyle="--",
                    linewidth=1.8, label=f"Median: {format_inr(df['selling_price'].median())}")
    ax_hist.axvline(df["selling_price"].mean() / 1e5, color=THEME_SECONDARY, linestyle=":",
                    linewidth=1.8, label=f"Mean: {format_inr(df['selling_price'].mean())}")
    ax_hist.set_xlabel("Selling Price (₹ in Lakhs)", fontweight="bold")
    ax_hist.set_ylabel("Vehicle Frequency", fontweight="bold")
    ax_hist.legend(frameon=True)
    ax_hist.grid(True)

    p1 = os.path.join(output_dir, "selling_price_distribution.png")
    fig.savefig(p1, bbox_inches="tight")
    plt.close(fig)
    print(f"[EDA Visual 1] Saved -> {p1}")

    # -------------------------------------------------------------------------
    # 2. Price vs. Car Age (Depreciation Curve)
    # -------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    sns.regplot(
        data=df, x="car_age", y=df["selling_price"] / 1e5,
        scatter_kws={"alpha": 0.35, "color": THEME_PRIMARY, "s": 24},
        line_kws={"color": THEME_ACCENT, "linewidth": 2.2},
        order=2, ax=ax
    )
    ax.set_title("Vehicle Depreciation: Selling Price vs. Car Age", fontweight="bold", pad=12)
    ax.set_xlabel("Car Age (Years from 2020)", fontweight="bold")
    ax.set_ylabel("Selling Price (₹ in Lakhs)", fontweight="bold")
    ax.grid(True)

    p2 = os.path.join(output_dir, "price_vs_car_age.png")
    fig.savefig(p2, bbox_inches="tight")
    plt.close(fig)
    print(f"[EDA Visual 2] Saved -> {p2}")

    # -------------------------------------------------------------------------
    # 3. Price vs. Kilometres Driven
    # -------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    sns.scatterplot(
        data=df, x=df["km_driven"] / 1000, y=df["selling_price"] / 1e5,
        hue="fuel", palette="viridis", alpha=0.6, s=28, ax=ax
    )
    ax.set_title("Odometer Mileage vs. Selling Price Across Fuel Types", fontweight="bold", pad=12)
    ax.set_xlabel("Kilometres Driven (in Thousands)", fontweight="bold")
    ax.set_ylabel("Selling Price (₹ in Lakhs)", fontweight="bold")
    ax.legend(title="Fuel Type", frameon=True)
    ax.grid(True)

    p3 = os.path.join(output_dir, "price_vs_km_driven.png")
    fig.savefig(p3, bbox_inches="tight")
    plt.close(fig)
    print(f"[EDA Visual 3] Saved -> {p3}")

    # -------------------------------------------------------------------------
    # 4. Price by Fuel Type
    # -------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    fuel_order = df.groupby("fuel")["selling_price"].median().sort_values(ascending=False).index
    sns.boxplot(
        data=df, x="fuel", y=df["selling_price"] / 1e5,
        order=fuel_order, palette="Blues_r", hue="fuel", legend=False, ax=ax, fliersize=2.5
    )
    ax.set_title("Selling Price Distribution by Fuel Type", fontweight="bold", pad=12)
    ax.set_xlabel("Fuel Type", fontweight="bold")
    ax.set_ylabel("Selling Price (₹ in Lakhs)", fontweight="bold")
    ax.grid(True)

    p4 = os.path.join(output_dir, "price_by_fuel.png")
    fig.savefig(p4, bbox_inches="tight")
    plt.close(fig)
    print(f"[EDA Visual 4] Saved -> {p4}")

    # -------------------------------------------------------------------------
    # 5. Price by Transmission Type
    # -------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8, 5.5), dpi=300)
    sns.boxplot(
        data=df, x="transmission", y=df["selling_price"] / 1e5,
        palette=[THEME_PRIMARY, THEME_SECONDARY], hue="transmission", legend=False, ax=ax, fliersize=2.5
    )
    auto_med = df[df["transmission"] == "Automatic"]["selling_price"].median()
    man_med = df[df["transmission"] == "Manual"]["selling_price"].median()
    premium_pct = ((auto_med - man_med) / man_med) * 100
    ax.set_title(f"Transmission Premium: Automatic vs. Manual (+{premium_pct:.1f}% Median Premium)",
                 fontweight="bold", pad=12)
    ax.set_xlabel("Transmission Type", fontweight="bold")
    ax.set_ylabel("Selling Price (₹ in Lakhs)", fontweight="bold")
    ax.grid(True)

    p5 = os.path.join(output_dir, "price_by_transmission.png")
    fig.savefig(p5, bbox_inches="tight")
    plt.close(fig)
    print(f"[EDA Visual 5] Saved -> {p5}")

    # -------------------------------------------------------------------------
    # 6. Brand-wise Average Selling Price
    # -------------------------------------------------------------------------
    brand_price = df.groupby("brand")["selling_price"].mean().sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
    bars = ax.barh(brand_price.index, brand_price.values / 1e5, color=THEME_PRIMARY, edgecolor="#047857")
    ax.set_title("Brand-Wise Average Selling Price Ranking (in Lakhs INR)", fontweight="bold", pad=12)
    ax.set_xlabel("Average Selling Price (₹ in Lakhs)", fontweight="bold")
    ax.set_ylabel("Car Manufacturer / Brand", fontweight="bold")
    ax.grid(True, axis="x")

    p6 = os.path.join(output_dir, "brand_avg_selling_price.png")
    fig.savefig(p6, bbox_inches="tight")
    plt.close(fig)
    print(f"[EDA Visual 6] Saved -> {p6}")

    # -------------------------------------------------------------------------
    # 7. Correlation Heatmap
    # -------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8, 6), dpi=300)
    num_df = df[["selling_price", "car_age", "km_driven", "year"]].copy()
    corr = num_df.corr(method="pearson")
    sns.heatmap(
        corr, annot=True, fmt=".3f", cmap="Blues",
        cbar_kws={"label": "Pearson Correlation r"},
        linewidths=1.2, linecolor="white", ax=ax
    )
    ax.set_title("Pearson Correlation Matrix of Numeric Attributes", fontweight="bold", pad=12)

    p7 = os.path.join(output_dir, "correlation_heatmap.png")
    fig.savefig(p7, bbox_inches="tight")
    plt.close(fig)
    print(f"[EDA Visual 7] Saved -> {p7}")

    # -------------------------------------------------------------------------
    # 8. Feature Relationships (Price vs Age by Transmission & Fuel)
    # -------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    common_fuels = ["Petrol", "Diesel"]
    sub_df = df[df["fuel"].isin(common_fuels)].copy()
    sns.scatterplot(
        data=sub_df, x="car_age", y=sub_df["selling_price"] / 1e5,
        hue="fuel", style="transmission", palette={"Petrol": THEME_SECONDARY, "Diesel": THEME_PRIMARY},
        alpha=0.65, s=36, ax=ax
    )
    ax.set_title("Multivariate Interaction: Selling Price vs. Age by Fuel & Transmission", fontweight="bold", pad=12)
    ax.set_xlabel("Car Age (Years)", fontweight="bold")
    ax.set_ylabel("Selling Price (₹ in Lakhs)", fontweight="bold")
    ax.legend(title="Fuel & Transmission", frameon=True)
    ax.grid(True)

    p8 = os.path.join(output_dir, "feature_relationships.png")
    fig.savefig(p8, bbox_inches="tight")
    plt.close(fig)
    print(f"[EDA Visual 8] Saved -> {p8}")


def compute_eda_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """Computes descriptive statistics and key business insights from cleaned data."""
    price = df["selling_price"]
    km = df["km_driven"]
    age = df["car_age"]

    return {
        "total_records": len(df),
        "price_mean": float(price.mean()),
        "price_median": float(price.median()),
        "price_std": float(price.std()),
        "price_q1": float(price.quantile(0.25)),
        "price_q3": float(price.quantile(0.75)),
        "price_min": float(price.min()),
        "price_max": float(price.max()),
        "km_median": float(km.median()),
        "age_median": float(age.median()),
        "top_brand": str(df["brand"].mode().iloc[0]),
        "top_fuel": str(df["fuel"].mode().iloc[0]),
        "auto_transmission_share": float((df["transmission"] == "Automatic").mean() * 100),
        "diesel_share": float((df["fuel"] == "Diesel").mean() * 100),
        "first_owner_share": float((df["owner"] == "First Owner").mean() * 100)
    }


if __name__ == "__main__":
    paths = get_project_paths()
    if os.path.exists(paths["processed_csv"]):
        df_clean = pd.read_csv(paths["processed_csv"])
        summary = compute_eda_summary(df_clean)
        print("\n" + "=" * 65)
        print("EDA MACROECONOMIC & VEHICLE MARKET METRICS")
        print("=" * 65)
        for k, v in summary.items():
            print(f"  {k:28s}: {v}")
        print("=" * 65)
        generate_exploratory_visualizations(df_clean, paths["visualizations_dir"])
    else:
        print("[EDA] Cleaned dataset not found. Run data_cleaning.py first.")
