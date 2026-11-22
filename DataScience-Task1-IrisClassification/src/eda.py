"""
eda.py
======
Exploratory Data Analysis and Feature Analysis module
for the Iris Flower Classification project.

Generates 8 high-resolution visualisations saved to `visualizations/`:
1. Species distribution chart
2. Multi-feature pairplot with KDE diagonals
3. Sepal length distribution (Hist + KDE)
4. Sepal width distribution (Hist + KDE)
5. Petal length distribution (Hist + KDE)
6. Petal width distribution (Hist + KDE)
7. Boxplots for all four features grouped by species
8. Correlation matrix heatmap

Also prints in-depth feature analysis and domain conclusions.
"""

import os
import sys

# Ensure src directory is in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from data_loader import load_and_prepare_iris_data

# Set global visualization aesthetics
sns.set_theme(style="whitegrid", palette="muted")
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

SPECIES_PALETTE = {
    "Setosa": "#1f77b4",       # Deep Blue
    "Versicolor": "#2ca02c",   # Rich Green
    "Virginica": "#d62728"     # Crimson Red
}


def run_exploratory_data_analysis(df: pd.DataFrame, output_dir: str):
    """
    Executes full exploratory data analysis, writes all plots to output_dir,
    and logs detailed botanical and statistical observations.
    """
    os.makedirs(output_dir, exist_ok=True)
    print("\n" + "=" * 70)
    print("PHASE 4 & 5: EXPLORATORY DATA ANALYSIS & FEATURE ANALYSIS")
    print("=" * 70)

    # -------------------------------------------------------------
    # 1. Species Distribution Chart
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(7, 5), dpi=300)
    species_counts = df["species"].value_counts()
    bars = ax.bar(
        species_counts.index,
        species_counts.values,
        color=[SPECIES_PALETTE[s] for s in species_counts.index],
        edgecolor="black",
        linewidth=0.8,
        width=0.55
    )

    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            f"{int(height)} ({height / len(df) * 100:.1f}%)",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontweight="bold"
        )

    ax.set_title("Iris Flower Species Distribution (Target Balance)", fontweight="bold")
    ax.set_xlabel("Species Category")
    ax.set_ylabel("Sample Count")
    ax.set_ylim(0, 60)
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    plot1_path = os.path.join(output_dir, "species_distribution.png")
    fig.savefig(plot1_path, bbox_inches="tight")
    plt.close(fig)

    print("\n[Visual 1] Species Distribution Plot Saved -> species_distribution.png")
    print("Observation: The dataset contains exactly 50 samples for each of the 3 classes")
    print("(Setosa, Versicolor, Virginica), yielding a 33.33% balanced distribution.")
    print("Consequently, class imbalance mitigations (e.g. SMOTE) are not necessary.")

    # -------------------------------------------------------------
    # 2. Pairplot
    # -------------------------------------------------------------
    pairplot = sns.pairplot(
        df[["sepal_length", "sepal_width", "petal_length", "petal_width", "species"]],
        hue="species",
        palette=SPECIES_PALETTE,
        diag_kind="kde",
        corner=False,
        plot_kws={"alpha": 0.85, "s": 40, "edgecolor": "k", "linewidth": 0.5},
        diag_kws={"fill": True, "alpha": 0.4}
    )
    pairplot.fig.suptitle("Pairwise Feature Relationships Across Iris Species", y=1.02, fontweight="bold")

    plot2_path = os.path.join(output_dir, "pairplot.png")
    pairplot.savefig(plot2_path, bbox_inches="tight", dpi=300)
    plt.close()

    print("\n[Visual 2] Pairwise Scatter & Density Plot Saved -> pairplot.png")
    print("Observation: Iris-setosa is completely linearly separable from the other two species")
    print("across all petal feature planes. Versicolor and Virginica exhibit slight boundary overlap")
    print("in sepal dimensions, but distinct clustering along petal length and petal width.")

    # -------------------------------------------------------------
    # 3. Sepal Length Distribution
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
    for sp, color in SPECIES_PALETTE.items():
        subset = df[df["species"] == sp]["sepal_length"]
        sns.histplot(
            subset,
            kde=True,
            color=color,
            label=f"{sp} (μ={subset.mean():.2f})",
            ax=ax,
            bins=12,
            alpha=0.45,
            edgecolor="black"
        )
    ax.set_title("Distribution of Sepal Length by Species", fontweight="bold")
    ax.set_xlabel("Sepal Length (cm)")
    ax.set_ylabel("Frequency")
    ax.legend(title="Species")
    ax.grid(True, linestyle="--", alpha=0.6)

    plot3_path = os.path.join(output_dir, "sepal_length_distribution.png")
    fig.savefig(plot3_path, bbox_inches="tight")
    plt.close(fig)

    print("\n[Visual 3] Sepal Length Distribution Saved -> sepal_length_distribution.png")
    print("Observation: Setosa displays shorter sepal lengths (mean ~5.01 cm), while Virginica")
    print("has the longest sepals (mean ~6.59 cm). However, substantial overlap exists between")
    print("Versicolor (mean ~5.94 cm) and the others, making this feature alone insufficient.")

    # -------------------------------------------------------------
    # 4. Sepal Width Distribution
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
    for sp, color in SPECIES_PALETTE.items():
        subset = df[df["species"] == sp]["sepal_width"]
        sns.histplot(
            subset,
            kde=True,
            color=color,
            label=f"{sp} (μ={subset.mean():.2f})",
            ax=ax,
            bins=12,
            alpha=0.45,
            edgecolor="black"
        )
    ax.set_title("Distribution of Sepal Width by Species", fontweight="bold")
    ax.set_xlabel("Sepal Width (cm)")
    ax.set_ylabel("Frequency")
    ax.legend(title="Species")
    ax.grid(True, linestyle="--", alpha=0.6)

    plot4_path = os.path.join(output_dir, "sepal_width_distribution.png")
    fig.savefig(plot4_path, bbox_inches="tight")
    plt.close(fig)

    print("\n[Visual 4] Sepal Width Distribution Saved -> sepal_width_distribution.png")
    print("Observation: Iris-setosa possesses distinctly wider sepals (mean ~3.43 cm),")
    print("whereas Versicolor has the narrowest sepals (mean ~2.77 cm). Sepal width follows")
    print("an approximately Gaussian distribution across the total population.")

    # -------------------------------------------------------------
    # 5. Petal Length Distribution
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
    for sp, color in SPECIES_PALETTE.items():
        subset = df[df["species"] == sp]["petal_length"]
        sns.histplot(
            subset,
            kde=True,
            color=color,
            label=f"{sp} (μ={subset.mean():.2f})",
            ax=ax,
            bins=12,
            alpha=0.45,
            edgecolor="black"
        )
    ax.set_title("Distribution of Petal Length by Species (High Discriminative Power)", fontweight="bold")
    ax.set_xlabel("Petal Length (cm)")
    ax.set_ylabel("Frequency")
    ax.legend(title="Species")
    ax.grid(True, linestyle="--", alpha=0.6)

    plot5_path = os.path.join(output_dir, "petal_length_distribution.png")
    fig.savefig(plot5_path, bbox_inches="tight")
    plt.close(fig)

    print("\n[Visual 5] Petal Length Distribution Saved -> petal_length_distribution.png")
    print("Observation: Petal length is exceptionally discriminative. Setosa petal lengths")
    print("range strictly between 1.0 cm and 1.9 cm with zero overlap with Versicolor (3.0 - 5.1 cm)")
    print("or Virginica (4.5 - 6.9 cm). A clear bimodal/multimodal landscape is evident.")

    # -------------------------------------------------------------
    # 6. Petal Width Distribution
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
    for sp, color in SPECIES_PALETTE.items():
        subset = df[df["species"] == sp]["petal_width"]
        sns.histplot(
            subset,
            kde=True,
            color=color,
            label=f"{sp} (μ={subset.mean():.2f})",
            ax=ax,
            bins=12,
            alpha=0.45,
            edgecolor="black"
        )
    ax.set_title("Distribution of Petal Width by Species (High Discriminative Power)", fontweight="bold")
    ax.set_xlabel("Petal Width (cm)")
    ax.set_ylabel("Frequency")
    ax.legend(title="Species")
    ax.grid(True, linestyle="--", alpha=0.6)

    plot6_path = os.path.join(output_dir, "petal_width_distribution.png")
    fig.savefig(plot6_path, bbox_inches="tight")
    plt.close(fig)

    print("\n[Visual 6] Petal Width Distribution Saved -> petal_width_distribution.png")
    print("Observation: Petal width demonstrates similar discriminative strength. Setosa petal widths")
    print("are tiny (mean ~0.25 cm). Versicolor ranges around ~1.33 cm, and Virginica around ~2.03 cm.")

    # -------------------------------------------------------------
    # 7. Boxplots for All Four Features
    # -------------------------------------------------------------
    features = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
    feature_labels = ["Sepal Length (cm)", "Sepal Width (cm)", "Petal Length (cm)", "Petal Width (cm)"]

    fig, axes = plt.subplots(2, 2, figsize=(12, 10), dpi=300)
    axes = axes.flatten()

    for i, (feat, label) in enumerate(zip(features, feature_labels)):
        sns.boxplot(
            data=df,
            x="species",
            y=feat,
            hue="species",
            palette=SPECIES_PALETTE,
            legend=False,
            ax=axes[i],
            width=0.5,
            boxprops=dict(alpha=0.85)
        )
        sns.stripplot(
            data=df,
            x="species",
            y=feat,
            color="black",
            size=4,
            jitter=0.2,
            alpha=0.6,
            ax=axes[i]
        )
        axes[i].set_title(f"Boxplot: {label}", fontweight="bold")
        axes[i].set_xlabel("Species")
        axes[i].set_ylabel(label)
        axes[i].grid(True, linestyle="--", alpha=0.6)

    fig.suptitle("Feature Dispersion & Outlier Analysis Across Iris Classes", y=1.01, fontweight="bold")
    plot7_path = os.path.join(output_dir, "feature_boxplots.png")
    fig.savefig(plot7_path, bbox_inches="tight")
    plt.close(fig)

    print("\n[Visual 7] Boxplots Saved -> feature_boxplots.png")
    print("Observation: Outliers are minimal, appearing primarily in Sepal Width for Setosa and Virginica.")
    print("Petal length and petal width show virtually distinct interquartile ranges (IQR) across all three classes.")

    # -------------------------------------------------------------
    # 8. Correlation Heatmap
    # -------------------------------------------------------------
    corr = df[features].corr(method="pearson")
    fig, ax = plt.subplots(figsize=(7, 6), dpi=300)
    sns.heatmap(
        corr,
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
    ax.set_title("Pearson Feature Correlation Matrix", fontweight="bold", pad=12)
    ax.set_xticklabels(["Sepal Length", "Sepal Width", "Petal Length", "Petal Width"], rotation=30, ha="right")
    ax.set_yticklabels(["Sepal Length", "Sepal Width", "Petal Length", "Petal Width"], rotation=0)

    plot8_path = os.path.join(output_dir, "correlation_heatmap.png")
    fig.savefig(plot8_path, bbox_inches="tight")
    plt.close(fig)

    print("\n[Visual 8] Correlation Heatmap Saved -> correlation_heatmap.png")
    print("Observation: Petal length and petal width share a very strong positive correlation (r = 0.963).")
    print("Sepal length also strongly correlates with petal dimensions (r > 0.81).")
    print("Sepal width displays negative correlation with petal measurements (r ~ -0.37 to -0.43).")

    # -------------------------------------------------------------
    # Phase 5 Synthesis: Feature Importance & Discriminative Analysis
    # -------------------------------------------------------------
    print("\n" + "=" * 70)
    print("PHASE 5: FEATURE DISCRIMINATIVE SYNTHESIS")
    print("=" * 70)
    print("1. Most Discriminative Features: Petal Length and Petal Width.")
    print("2. Why Petal Measurements are Superior:")
    print("   - Botanical evolution creates species-specific petal morphologies for distinct pollinators.")
    print("   - Petal length creates non-overlapping decision boundaries separating Setosa (1.0-1.9 cm)")
    print("     from Versicolor (3.0-5.1 cm) and Virginica (4.5-6.9 cm).")
    print("   - Combining petal length and petal width yields near-orthogonal separability with")
    print("     only marginal overlap between Versicolor and Virginica.")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(current_dir)
    data_frame, _, _ = load_and_prepare_iris_data()
    visualizations_path = os.path.join(base_dir, "visualizations")
    run_exploratory_data_analysis(data_frame, visualizations_path)
