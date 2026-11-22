"""
visualizations.py
=================
Publication-grade Visualization Suite for Oasis Infobyte Task 2:
Unemployment Analysis with Python (India).

Generates 8 high-resolution PNG charts saved to `visualizations/`:
1. `unemployment_distribution.png`: Distribution (Histogram + KDE + Boxplot)
2. `regional_unemployment.png`: Horizontal bar chart of state unemployment rankings
3. `monthly_trend.png`: Monthly aggregated time-series with lockdown markers
4. `state_comparison.png`: Multi-state time-series comparison across major economies
5. `top10_regions.png`: Bar chart of the Top 10 highest unemployment states
6. `correlation_heatmap.png`: Pearson correlation matrix heatmap
7. `covid_impact.png`: Pre-COVID vs. COVID/Post-COVID comparative timeline & bars
8. `employment_labour_participation.png`: Labour market dynamics scatter & regression
"""

import os
import sys
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd
import numpy as np

# Ensure src in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from data_loader import get_project_paths

# Professional styling palette: Emerald Green accent with clean whites/slates
PALETTE_PRIMARY = "#059669"    # Emerald Green
PALETTE_SECONDARY = "#2563eb"  # Royal Blue
PALETTE_ACCENT = "#dc2626"     # Crimson Red
PALETTE_MUTED = "#64748b"      # Slate Grey
PALETTE_PRE = "#3b82f6"        # Pre-COVID Blue
PALETTE_POST = "#ef4444"       # COVID Red

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "figure.titlesize": 14,
    "figure.autolayout": True
})
sns.set_theme(style="whitegrid")


def generate_all_visualizations(df: pd.DataFrame, output_dir: str):
    """
    Renders and exports all 8 requested publication-quality charts.
    """
    os.makedirs(output_dir, exist_ok=True)
    print("\n" + "=" * 75)
    print("PHASE 7: GENERATING HIGH-RESOLUTION VISUALIZATION SUITE")
    print("=" * 75)

    # -------------------------------------------------------------
    # 1. Unemployment Rate Distribution
    # -------------------------------------------------------------
    fig, (ax_box, ax_hist) = plt.subplots(
        2, 1, figsize=(10, 6.5), dpi=300, sharex=True, gridspec_kw={"height_ratios": [0.22, 0.78]}
    )
    sns.boxplot(x=df["Estimated_Unemployment_Rate"], ax=ax_box, color=PALETTE_PRIMARY, fliersize=4)
    ax_box.set(xlabel="")
    ax_box.set_title("Distribution of Estimated Unemployment Rate in India (2019-2020)", fontweight="bold")

    sns.histplot(
        df["Estimated_Unemployment_Rate"],
        kde=True,
        ax=ax_hist,
        color=PALETTE_PRIMARY,
        bins=30,
        edgecolor="black",
        alpha=0.5
    )
    mean_val = df["Estimated_Unemployment_Rate"].mean()
    median_val = df["Estimated_Unemployment_Rate"].median()
    ax_hist.axvline(mean_val, color=PALETTE_ACCENT, linestyle="--", linewidth=1.5, label=f"Mean: {mean_val:.2f}%")
    ax_hist.axvline(median_val, color=PALETTE_SECONDARY, linestyle="-", linewidth=1.5, label=f"Median: {median_val:.2f}%")
    ax_hist.set_xlabel("Estimated Unemployment Rate (%)", fontweight="bold")
    ax_hist.set_ylabel("Frequency (Observation Count)", fontweight="bold")
    ax_hist.legend(loc="upper right", frameon=True)

    p1 = os.path.join(output_dir, "unemployment_distribution.png")
    fig.savefig(p1, bbox_inches="tight")
    plt.close(fig)
    print(f"[Visual 1] Saved -> {p1}")

    # -------------------------------------------------------------
    # 2. Regional Unemployment Ranking (Horizontal Bar Chart)
    # -------------------------------------------------------------
    state_avg = df.groupby("State")["Estimated_Unemployment_Rate"].mean().sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(10, 11), dpi=300)
    bars = ax.barh(state_avg.index, state_avg.values, color=PALETTE_PRIMARY, edgecolor="black", height=0.65)

    for bar in bars:
        w = bar.get_width()
        ax.annotate(
            f"{w:.2f}%",
            xy=(w, bar.get_y() + bar.get_height() / 2),
            xytext=(4, 0),
            textcoords="offset points",
            ha="left",
            va="center",
            fontsize=8.5,
            fontweight="bold"
        )

    national_avg = df["Estimated_Unemployment_Rate"].mean()
    ax.axvline(national_avg, color=PALETTE_ACCENT, linestyle="--", linewidth=1.5, label=f"National Mean ({national_avg:.2f}%)")
    ax.set_title("State-Wise Average Unemployment Rate in India (Ranked)", fontweight="bold", pad=12)
    ax.set_xlabel("Average Unemployment Rate (%)", fontweight="bold")
    ax.set_ylabel("State / Union Territory", fontweight="bold")
    ax.set_xlim(0, max(state_avg.values) * 1.15)
    ax.legend(loc="lower right")

    p2 = os.path.join(output_dir, "regional_unemployment.png")
    fig.savefig(p2, bbox_inches="tight")
    plt.close(fig)
    print(f"[Visual 2] Saved -> {p2}")

    # -------------------------------------------------------------
    # 3. Monthly Unemployment Trend (Time Series Line Chart)
    # -------------------------------------------------------------
    monthly = df.groupby("Date")["Estimated_Unemployment_Rate"].agg(["mean", "std", "count"]).reset_index()
    monthly["ci"] = 1.96 * monthly["std"] / np.sqrt(monthly["count"])

    fig, ax = plt.subplots(figsize=(12, 6), dpi=300)
    ax.plot(monthly["Date"], monthly["mean"], marker="o", color=PALETTE_PRIMARY, linewidth=2.5, label="Monthly Mean Rate")
    ax.fill_between(
        monthly["Date"],
        monthly["mean"] - monthly["ci"],
        monthly["mean"] + monthly["ci"],
        color=PALETTE_PRIMARY,
        alpha=0.18,
        label="95% Confidence Interval"
    )

    # Highlight COVID-19 Lockdown Surge (March 24, 2020)
    lockdown_date = pd.Timestamp("2020-03-24")
    ax.axvline(lockdown_date, color=PALETTE_ACCENT, linestyle="--", linewidth=1.8, label="National Lockdown Imposed (Mar 24, 2020)")
    ax.annotate(
        "Peak Shock\nApr-May 2020\n(23.5% - 24.6%)",
        xy=(pd.Timestamp("2020-05-01"), 23.5),
        xytext=(pd.Timestamp("2020-01-01"), 26),
        arrowprops=dict(facecolor=PALETTE_ACCENT, arrowstyle="->", lw=1.5),
        fontweight="bold",
        color=PALETTE_ACCENT,
        bbox=dict(boxstyle="round,pad=0.4", fc="#fee2e2", ec=PALETTE_ACCENT, lw=1)
    )

    ax.set_title("Timeline of Monthly Unemployment Rate in India (May 2019 - June 2020)", fontweight="bold", pad=12)
    ax.set_xlabel("Observation Month", fontweight="bold")
    ax.set_ylabel("Unemployment Rate (%)", fontweight="bold")
    ax.set_xlim(pd.Timestamp("2019-05-15"), pd.Timestamp("2020-06-30"))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.legend(loc="upper left", frameon=True)

    p3 = os.path.join(output_dir, "monthly_trend.png")
    fig.savefig(p3, bbox_inches="tight")
    plt.close(fig)
    print(f"[Visual 3] Saved -> {p3}")

    # -------------------------------------------------------------
    # 4. State/Region Comparison (Multi-Line Chart for Major States)
    # -------------------------------------------------------------
    major_states = ["Maharashtra", "Uttar Pradesh", "Bihar", "Delhi", "Tamil Nadu"]
    df_major = df[df["State"].isin(major_states)].groupby(["Date", "State"])["Estimated_Unemployment_Rate"].mean().reset_index()

    fig, ax = plt.subplots(figsize=(12, 6.5), dpi=300)
    state_palette = {
        "Maharashtra": "#1e40af",
        "Uttar Pradesh": "#059669",
        "Bihar": "#d97706",
        "Delhi": "#dc2626",
        "Tamil Nadu": "#7c3aed"
    }
    sns.lineplot(
        data=df_major,
        x="Date",
        y="Estimated_Unemployment_Rate",
        hue="State",
        palette=state_palette,
        marker="o",
        linewidth=2.2,
        ax=ax
    )
    ax.axvline(lockdown_date, color="black", linestyle=":", linewidth=1.5, alpha=0.7, label="National Lockdown (Mar 2020)")
    ax.set_title("Comparative Unemployment Trajectory Across Major Indian Economies", fontweight="bold", pad=12)
    ax.set_xlabel("Date", fontweight="bold")
    ax.set_ylabel("Estimated Unemployment Rate (%)", fontweight="bold")
    ax.set_xlim(pd.Timestamp("2019-05-15"), pd.Timestamp("2020-06-30"))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.legend(title="State", loc="upper left", frameon=True)

    p4 = os.path.join(output_dir, "state_comparison.png")
    fig.savefig(p4, bbox_inches="tight")
    plt.close(fig)
    print(f"[Visual 4] Saved -> {p4}")

    # -------------------------------------------------------------
    # 5. Top 10 Regions with Highest Average Unemployment
    # -------------------------------------------------------------
    top10 = df.groupby("State")["Estimated_Unemployment_Rate"].mean().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
    bars = ax.bar(top10.index, top10.values, color="#e11d48", edgecolor="black", width=0.6)

    for bar in bars:
        h = bar.get_height()
        ax.annotate(
            f"{h:.1f}%",
            xy=(bar.get_x() + bar.get_width() / 2, h),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontweight="bold",
            fontsize=9
        )

    ax.set_title("Top 10 Indian States / UTs with Highest Average Unemployment", fontweight="bold", pad=12)
    ax.set_xlabel("State / UT", fontweight="bold")
    ax.set_ylabel("Average Unemployment Rate (%)", fontweight="bold")
    ax.set_xticks(range(len(top10)))
    ax.set_xticklabels(top10.index, rotation=35, ha="right")
    ax.set_ylim(0, max(top10.values) * 1.18)

    p5 = os.path.join(output_dir, "top10_regions.png")
    fig.savefig(p5, bbox_inches="tight")
    plt.close(fig)
    print(f"[Visual 5] Saved -> {p5}")

    # -------------------------------------------------------------
    # 6. Correlation Heatmap
    # -------------------------------------------------------------
    corr_cols = ["Estimated_Unemployment_Rate", "Estimated_Employed", "Estimated_Labour_Participation_Rate"]
    corr_matrix = df[corr_cols].corr()
    fig, ax = plt.subplots(figsize=(7, 5.5), dpi=300)
    sns.heatmap(
        corr_matrix,
        annot=True,
        fmt=".3f",
        cmap="coolwarm",
        vmin=-1,
        vmax=1,
        square=True,
        linewidths=1.2,
        cbar_kws={"shrink": 0.8},
        ax=ax
    )
    labels = ["Unemployment Rate (%)", "Employed (Count)", "Labour Participation (%)"]
    ax.set_xticklabels(labels, rotation=25, ha="right")
    ax.set_yticklabels(labels, rotation=0)
    ax.set_title("Pearson Correlation Heatmap (Macroeconomic Indicators)", fontweight="bold", pad=12)

    p6 = os.path.join(output_dir, "correlation_heatmap.png")
    fig.savefig(p6, bbox_inches="tight")
    plt.close(fig)
    print(f"[Visual 6] Saved -> {p6}")

    # -------------------------------------------------------------
    # 7. COVID-19 Impact: Pre vs Post Comparison
    # -------------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300, gridspec_kw={"width_ratios": [0.4, 0.6]})

    # A: Sector Breakdown (Rural vs Urban)
    sector_covid = df.groupby(["Area", "COVID_Phase"])["Estimated_Unemployment_Rate"].mean().unstack()
    sector_covid[["Pre-COVID", "COVID/Post-COVID"]].plot(
        kind="bar",
        ax=axes[0],
        color=[PALETTE_PRE, PALETTE_POST],
        edgecolor="black",
        width=0.55
    )
    axes[0].set_title("Pre-COVID vs. Post-COVID Mean Rate by Sector", fontweight="bold")
    axes[0].set_xlabel("Sector (Area)", fontweight="bold")
    axes[0].set_ylabel("Unemployment Rate (%)", fontweight="bold")
    axes[0].set_xticklabels(["Rural", "Urban"], rotation=0)
    axes[0].legend(title="Period")
    for p in axes[0].patches:
        h = p.get_height()
        if h > 0:
            axes[0].annotate(f"{h:.1f}%", (p.get_x() + p.get_width() / 2, h + 0.4), ha="center", fontweight="bold")

    # B: Top States experiencing highest absolute surge
    state_pivot = df.pivot_table(
        index="State",
        columns="COVID_Phase",
        values="Estimated_Unemployment_Rate",
        aggfunc="mean"
    )
    state_pivot["Surge"] = state_pivot["COVID/Post-COVID"] - state_pivot["Pre-COVID"]
    top_surge = state_pivot.sort_values(by="Surge", ascending=False).head(7)

    x = np.arange(len(top_surge))
    w = 0.35
    axes[1].bar(x - w / 2, top_surge["Pre-COVID"], width=w, label="Pre-COVID", color=PALETTE_PRE, edgecolor="black")
    axes[1].bar(x + w / 2, top_surge["COVID/Post-COVID"], width=w, label="COVID/Post-COVID", color=PALETTE_POST, edgecolor="black")
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(top_surge.index, rotation=35, ha="right")
    axes[1].set_title("States Experiencing Highest Absolute Pandemic Surge", fontweight="bold")
    axes[1].set_ylabel("Average Unemployment Rate (%)", fontweight="bold")
    axes[1].legend(title="Period")

    fig.tight_layout()
    p7 = os.path.join(output_dir, "covid_impact.png")
    fig.savefig(p7, bbox_inches="tight")
    plt.close(fig)
    print(f"[Visual 7] Saved -> {p7}")

    # -------------------------------------------------------------
    # 8. Employment and Labour Participation Analysis
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    sns.scatterplot(
        data=df,
        x="Estimated_Labour_Participation_Rate",
        y="Estimated_Unemployment_Rate",
        hue="COVID_Phase",
        style="Area",
        palette={"Pre-COVID": PALETTE_PRE, "COVID/Post-COVID": PALETTE_POST},
        alpha=0.75,
        s=55,
        ax=ax
    )
    sns.regplot(
        data=df,
        x="Estimated_Labour_Participation_Rate",
        y="Estimated_Unemployment_Rate",
        scatter=False,
        color="black",
        line_kws={"linestyle": "--", "linewidth": 1.2},
        ax=ax
    )
    ax.set_title("Labour Participation Rate vs. Unemployment Rate", fontweight="bold", pad=12)
    ax.set_xlabel("Estimated Labour Participation Rate (%)", fontweight="bold")
    ax.set_ylabel("Estimated Unemployment Rate (%)", fontweight="bold")
    ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", frameon=True)

    p8 = os.path.join(output_dir, "employment_labour_participation.png")
    fig.savefig(p8, bbox_inches="tight")
    plt.close(fig)
    print(f"[Visual 8] Saved -> {p8}")
    print("=" * 75)
    print("ALL 8 PUBLICATION VISUALIZATIONS GENERATED SUCCESSFULLY.")
    print("=" * 75 + "\n")


if __name__ == "__main__":
    paths = get_project_paths()
    clean_csv = paths["clean_csv"]
    if not os.path.exists(clean_csv):
        print(f"[ERROR] Cleaned dataset not found at {clean_csv}. Please run data_cleaning.py first.")
        sys.exit(1)

    clean_df = pd.read_csv(clean_csv)
    clean_df["Date"] = pd.to_datetime(clean_df["Date"])
    generate_all_visualizations(clean_df, paths["vis_dir"])
