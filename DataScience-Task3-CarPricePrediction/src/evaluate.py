"""
evaluate.py
===========
Model Evaluation, Diagnostic Verification, and Visualizations Engine
for Task 3: Car Price Prediction with Machine Learning.

Generates 4 publication-grade model diagnostic figures saved to `visualizations/`:
9.  `model_comparison.png`: Cross-Validation vs. Test R2 and MAE across all models
10. `feature_importance.png`: Top positive and negative coefficients / feature importances
11. `actual_vs_predicted.png`: Actual vs Predicted prices with diagonal reference line
12. `residual_distribution.png`: Histogram & KDE of residuals + Residual vs Fitted plot
"""

import os
import sys
import json
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Dict, Any
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from data_loader import get_project_paths
from feature_engineering import extract_features
from train import RANDOM_STATE, TEST_SIZE

THEME_PRIMARY = "#059669"    # Emerald Green
THEME_SECONDARY = "#2563eb"  # Royal Blue
THEME_ACCENT = "#dc2626"     # Crimson Red
THEME_PURPLE = "#7c3aed"     # Violet

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


def generate_model_evaluation_visualizations(
    model_comparison: Dict[str, Any],
    feature_importances: Dict[str, float],
    y_test: np.ndarray,
    y_pred: np.ndarray,
    output_dir: str
) -> None:
    """Generates the 4 diagnostic figures."""
    os.makedirs(output_dir, exist_ok=True)

    # -------------------------------------------------------------------------
    # 9. Model Comparison (R2 Score and MAE Across Models)
    # -------------------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5), dpi=300)

    model_names = list(model_comparison.keys())
    cv_r2 = [model_comparison[m]["cv_r2_mean"] for m in model_names]
    test_r2 = [model_comparison[m]["test_r2"] for m in model_names]
    test_mae = [model_comparison[m]["test_mae"] / 1e5 for m in model_names]

    x = np.arange(len(model_names))
    width = 0.35

    ax1.bar(x - width/2, cv_r2, width, label="5-Fold CV $R^2$", color=THEME_PRIMARY, edgecolor="#047857")
    ax1.bar(x + width/2, test_r2, width, label="Held-Out Test $R^2$", color=THEME_SECONDARY, edgecolor="#1d4ed8")
    ax1.set_ylabel("$R^2$ Score", fontweight="bold")
    ax1.set_title("Model Generalization: Validation vs. Test $R^2$", fontweight="bold", pad=12)
    ax1.set_xticks(x)
    ax1.set_xticklabels(model_names, rotation=15, ha="right")
    ax1.set_ylim(0, 1.0)
    ax1.legend(frameon=True)
    ax1.grid(True)

    bars2 = ax2.bar(x, test_mae, width=0.5, color=THEME_PURPLE, edgecolor="#6d28d9")
    ax2.set_ylabel("Test MAE (₹ in Lakhs)", fontweight="bold")
    ax2.set_title("Prediction Error: Mean Absolute Error (Lower is Better)", fontweight="bold", pad=12)
    ax2.set_xticks(x)
    ax2.set_xticklabels(model_names, rotation=15, ha="right")
    for bar in bars2:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, yval + 0.03, f"₹{yval:.2f}L", ha="center", va="bottom", fontsize=9, fontweight="bold")
    ax2.grid(True)

    plt.tight_layout()
    p9 = os.path.join(output_dir, "model_comparison.png")
    fig.savefig(p9, bbox_inches="tight")
    plt.close(fig)
    print(f"[EVAL Visual 9] Saved -> {p9}")

    # -------------------------------------------------------------------------
    # 10. Feature Importance / Log-Coefficients
    # -------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 7.5), dpi=300)
    s_fi = pd.Series(feature_importances).sort_values()

    # Select top 10 positive and top 10 negative drivers
    if len(s_fi) > 20:
        top_neg = s_fi.head(10)
        top_pos = s_fi.tail(10)
        s_plot = pd.concat([top_neg, top_pos])
    else:
        s_plot = s_fi

    # Clean display labels
    clean_labels = [l.replace("cat__", "").replace("num__", "") for l in s_plot.index]
    colors = [THEME_ACCENT if v < 0 else THEME_PRIMARY for v in s_plot.values]

    ax.barh(clean_labels, s_plot.values, color=colors, edgecolor="#334155")
    ax.axvline(0, color="#64748b", linewidth=1.2)
    ax.set_title("Feature Impact on Log Selling Price (Coefficients / Importance)", fontweight="bold", pad=12)
    ax.set_xlabel("Relative Weight / Log-Elasticity Coefficient", fontweight="bold")
    ax.set_ylabel("Transformed Feature", fontweight="bold")
    ax.grid(True, axis="x")

    p10 = os.path.join(output_dir, "feature_importance.png")
    fig.savefig(p10, bbox_inches="tight")
    plt.close(fig)
    print(f"[EVAL Visual 10] Saved -> {p10}")

    # -------------------------------------------------------------------------
    # 11. Actual vs. Predicted Plot
    # -------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(9, 6.5), dpi=300)
    y_test_lakhs = y_test / 1e5
    y_pred_lakhs = y_pred / 1e5

    ax.scatter(y_test_lakhs, y_pred_lakhs, alpha=0.55, color=THEME_PRIMARY, edgecolors="white", s=32, label="Test Vehicles")
    max_val = max(y_test_lakhs.max(), y_pred_lakhs.max()) * 1.05
    ax.plot([0, max_val], [0, max_val], color=THEME_ACCENT, linestyle="--", linewidth=2.0, label="Ideal Line (y = x)")

    ax.set_title("Actual vs. Predicted Selling Price (Held-Out Test Set)", fontweight="bold", pad=12)
    ax.set_xlabel("Actual Price (₹ in Lakhs)", fontweight="bold")
    ax.set_ylabel("Predicted Price (₹ in Lakhs)", fontweight="bold")
    ax.set_xlim(0, max_val)
    ax.set_ylim(0, max_val)
    ax.legend(frameon=True)
    ax.grid(True)

    p11 = os.path.join(output_dir, "actual_vs_predicted.png")
    fig.savefig(p11, bbox_inches="tight")
    plt.close(fig)
    print(f"[EVAL Visual 11] Saved -> {p11}")

    # -------------------------------------------------------------------------
    # 12. Residual Distribution and Diagnostics
    # -------------------------------------------------------------------------
    fig, (ax_hist, ax_res) = plt.subplots(1, 2, figsize=(13, 5.5), dpi=300)
    residuals = y_test - y_pred
    res_lakhs = residuals / 1e5

    sns.histplot(res_lakhs, kde=True, color=THEME_SECONDARY, bins=35, ax=ax_hist)
    ax_hist.axvline(0, color=THEME_ACCENT, linestyle="--", linewidth=1.8, label="Zero Error")
    ax_hist.set_title("Residual Error Distribution (Actual - Predicted)", fontweight="bold", pad=12)
    ax_hist.set_xlabel("Residual (₹ in Lakhs)", fontweight="bold")
    ax_hist.set_ylabel("Frequency", fontweight="bold")
    ax_hist.legend(frameon=True)
    ax_hist.grid(True)

    ax_res.scatter(y_pred_lakhs, res_lakhs, alpha=0.45, color=THEME_PURPLE, s=26)
    ax_res.axhline(0, color=THEME_ACCENT, linestyle="--", linewidth=1.8)
    ax_res.set_title("Residuals vs. Fitted Values (Homoscedasticity Check)", fontweight="bold", pad=12)
    ax_res.set_xlabel("Predicted Price (₹ in Lakhs)", fontweight="bold")
    ax_res.set_ylabel("Residual (₹ in Lakhs)", fontweight="bold")
    ax_res.grid(True)

    plt.tight_layout()
    p12 = os.path.join(output_dir, "residual_distribution.png")
    fig.savefig(p12, bbox_inches="tight")
    plt.close(fig)
    print(f"[EVAL Visual 12] Saved -> {p12}")


def run_evaluation() -> Dict[str, Any]:
    """Loads artifacts and runs diagnostic evaluation and chart generation."""
    paths = get_project_paths()
    if not os.path.exists(paths["pipeline_model"]) or not os.path.exists(paths["model_metadata"]):
        raise FileNotFoundError("Trained pipeline or metadata not found. Run train.py first.")

    with open(paths["model_metadata"], "r", encoding="utf-8") as f:
        meta = json.load(f)

    pipeline = joblib.load(paths["pipeline_model"])

    df = pd.read_csv(paths["processed_csv"])
    X, y = extract_features(df)

    from sklearn.model_selection import train_test_split
    _, X_test, _, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )

    y_pred = pipeline.predict(X_test)
    test_r2 = r2_score(y_test, y_pred)
    test_mae = mean_absolute_error(y_test, y_pred)
    test_rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    generate_model_evaluation_visualizations(
        meta["model_comparison"],
        meta["feature_importances_or_coefs"],
        y_test.values,
        y_pred,
        paths["visualizations_dir"]
    )

    eval_summary = {
        "best_model": meta["best_model_name"],
        "test_r2": round(test_r2, 4),
        "test_mae": round(test_mae, 2),
        "test_rmse": round(test_rmse, 2)
    }

    print("\n" + "=" * 65)
    print("FINAL HELD-OUT MODEL EVALUATION REPORT")
    print("=" * 65)
    for k, v in eval_summary.items():
        print(f"  {k:28s}: {v}")
    print("=" * 65)

    return eval_summary


if __name__ == "__main__":
    run_evaluation()
