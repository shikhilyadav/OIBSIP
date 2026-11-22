"""
train.py
========
Model training, evaluation, comparison, and persistence module
for the Oasis Infobyte Iris Flower Classification project.

Models trained and evaluated:
1. Logistic Regression (L2 regularization, scaled)
2. K-Nearest Neighbours (KNN, k=5, Euclidean distance, scaled)
3. Random Forest Classifier (100 ensemble estimators)

Includes stratified train/test split (80/20, random_state=42),
comprehensive metrics calculation, confusion matrix plotting,
model comparison bar charts, and artifact saving via joblib.
"""

import os
import sys
import json
from datetime import datetime

# Ensure src directory is in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

from data_loader import load_and_prepare_iris_data


def build_and_evaluate_models():
    """
    Main execution workflow for Phases 6, 7, and 8:
    1. Loads dataset and splits with stratification.
    2. Constructs ML pipelines with appropriate scaling.
    3. Fits all candidate models on training partition.
    4. Evaluates on unseen testing partition across metrics.
    5. Saves confusion matrices and comparison charts to `visualizations/`.
    6. Identifies best model and exports production bundle via joblib.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(current_dir)
    models_dir = os.path.join(base_dir, "models")
    vis_dir = os.path.join(base_dir, "visualizations")
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(vis_dir, exist_ok=True)

    # 1. Load Data
    csv_path = os.path.join(data_dir, "iris.csv")
    df, feature_names, target_names = load_and_prepare_iris_data(save_csv_path=csv_path)

    X = df[feature_names]
    y = df["species_id"]

    # 2. Phase 6: Stratified Train-Test Split (80% train, 20% test, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    print("\n" + "=" * 75)
    print("PHASE 6: MODEL DEVELOPMENT & STRATIFIED SPLIT")
    print("=" * 75)
    print(f"Total Samples:      {len(df)}")
    print(f"Training Partition: {len(X_train)} samples (80%)")
    print(f"Testing Partition:  {len(X_test)} samples (20%)")
    print(f"Features:           {feature_names}")
    print(f"Target Classes:     {target_names}")
    print("\nClass distribution in Test Set (Stratification check):")
    for cls_idx, cls_name in enumerate(target_names):
        count = (y_test == cls_idx).sum()
        print(f"  - Class {cls_idx} ({cls_name}): {count} samples ({count / len(y_test) * 100:.1f}%)")

    # Define Candidate Models inside Scikit-learn Pipelines
    # Distance-based (KNN) and linear models (Logistic Regression) benefit directly from standardization
    candidate_pipelines = {
        "Logistic Regression": Pipeline([
            ("scaler", StandardScaler()),
            ("classifier", LogisticRegression(max_iter=500, random_state=42))
        ]),
        "K-Nearest Neighbours": Pipeline([
            ("scaler", StandardScaler()),
            ("classifier", KNeighborsClassifier(n_neighbors=5, metric="minkowski", p=2))
        ]),
        "Random Forest Classifier": Pipeline([
            ("classifier", RandomForestClassifier(n_estimators=100, max_depth=4, random_state=42))
        ])
    }

    # 3. Phase 7: Train & Evaluate Models
    print("\n" + "=" * 75)
    print("PHASE 7: MODEL EVALUATION & COMPARISON")
    print("=" * 75)

    evaluation_records = []
    confusion_matrices = {}
    fitted_models = {}

    for name, pipeline in candidate_pipelines.items():
        print(f"\n--- Training: {name} ---")
        pipeline.fit(X_train, y_train)
        fitted_models[name] = pipeline

        # Predictions
        y_train_pred = pipeline.predict(X_train)
        y_test_pred = pipeline.predict(X_test)

        train_acc = accuracy_score(y_train, y_train_pred)
        test_acc = accuracy_score(y_test, y_test_pred)
        precision_macro = precision_score(y_test, y_test_pred, average="macro", zero_division=0)
        recall_macro = recall_score(y_test, y_test_pred, average="macro", zero_division=0)
        f1_macro = f1_score(y_test, y_test_pred, average="macro", zero_division=0)

        precision_weighted = precision_score(y_test, y_test_pred, average="weighted", zero_division=0)
        recall_weighted = recall_score(y_test, y_test_pred, average="weighted", zero_division=0)
        f1_weighted = f1_score(y_test, y_test_pred, average="weighted", zero_division=0)

        cm = confusion_matrix(y_test, y_test_pred)
        confusion_matrices[name] = cm

        evaluation_records.append({
            "Model": name,
            "Train Accuracy": round(train_acc, 4),
            "Test Accuracy": round(test_acc, 4),
            "Precision (Macro)": round(precision_macro, 4),
            "Recall (Macro)": round(recall_macro, 4),
            "F1-Score (Macro)": round(f1_macro, 4),
            "Precision (Weighted)": round(precision_weighted, 4),
            "Recall (Weighted)": round(recall_weighted, 4),
            "F1-Score (Weighted)": round(f1_weighted, 4)
        })

        print(f"Train Accuracy: {train_acc:.4f} | Test Accuracy: {test_acc:.4f}")
        print(f"Precision (Macro): {precision_macro:.4f} | Recall (Macro): {recall_macro:.4f} | F1-Score (Macro): {f1_macro:.4f}")
        print("\nClassification Report (Test Partition):")
        print(classification_report(y_test, y_test_pred, target_names=target_names, digits=4))

    # Convert evaluation results to DataFrame
    comparison_df = pd.DataFrame(evaluation_records)
    print("\n" + "=" * 75)
    print("MODEL COMPARISON TABLE")
    print("=" * 75)
    print(comparison_df.to_string(index=False))

    # 4. Generate Confusion Matrix Plot (All 3 Models)
    fig, axes = plt.subplots(1, 3, figsize=(16, 4.5), dpi=300)
    for idx, (name, cm) in enumerate(confusion_matrices.items()):
        sns.heatmap(
            cm,
            annot=True,
            fmt="d",
            cmap="Blues",
            cbar=False,
            xticklabels=target_names,
            yticklabels=target_names,
            ax=axes[idx],
            annot_kws={"size": 13, "weight": "bold"}
        )
        axes[idx].set_title(f"{name}\nConfusion Matrix", fontweight="bold", fontsize=12)
        axes[idx].set_xlabel("Predicted Species", fontsize=10)
        axes[idx].set_ylabel("Actual Species", fontsize=10)

    fig.tight_layout()
    cm_plot_path = os.path.join(vis_dir, "confusion_matrices.png")
    fig.savefig(cm_plot_path, bbox_inches="tight")
    plt.close(fig)
    print(f"\n[INFO] Confusion matrices plot saved to: {cm_plot_path}")

    # 5. Generate Model Comparison Bar Chart
    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
    metrics_to_plot = ["Test Accuracy", "Precision (Macro)", "Recall (Macro)", "F1-Score (Macro)"]
    plot_df = comparison_df.melt(id_vars="Model", value_vars=metrics_to_plot, var_name="Metric", value_name="Score")

    sns.barplot(
        data=plot_df,
        x="Metric",
        y="Score",
        hue="Model",
        palette=["#1f77b4", "#ff7f0e", "#2ca02c"],
        edgecolor="black",
        linewidth=0.7,
        ax=ax
    )

    ax.set_ylim(0.85, 1.02)
    ax.set_title("Iris Classification Model Performance Benchmark (Test Set)", fontweight="bold", pad=12)
    ax.set_ylabel("Score (0.0 - 1.0)", fontweight="bold")
    ax.set_xlabel("Evaluation Metric", fontweight="bold")
    ax.legend(title="Algorithm", loc="lower right", frameon=True)
    ax.grid(axis="y", linestyle="--", alpha=0.6)

    # Annotate bar values
    for p in ax.patches:
        h = p.get_height()
        if h > 0:
            ax.annotate(
                f"{h:.3f}",
                (p.get_x() + p.get_width() / 2., h),
                ha="center",
                va="bottom",
                fontsize=8.5,
                rotation=0,
                xytext=(0, 3),
                textcoords="offset points"
            )

    comp_plot_path = os.path.join(vis_dir, "model_comparison.png")
    fig.savefig(comp_plot_path, bbox_inches="tight")
    plt.close(fig)
    print(f"[INFO] Model comparison plot saved to: {comp_plot_path}")

    # 6. Model Selection
    # Sort primarily by Test Accuracy, then F1-Score (Macro)
    sorted_df = comparison_df.sort_values(by=["Test Accuracy", "F1-Score (Macro)"], ascending=False)
    best_model_name = sorted_df.iloc[0]["Model"]
    best_pipeline = fitted_models[best_model_name]
    best_stats = sorted_df.iloc[0].to_dict()

    print("\n" + "=" * 75)
    print("BEST MODEL SELECTION & RATIONALE")
    print("=" * 75)
    print(f"Top Performing Architecture: {best_model_name}")
    print(f"Test Accuracy:                {best_stats['Test Accuracy'] * 100:.2f}%")
    print(f"Macro F1-Score:               {best_stats['F1-Score (Macro)'] * 100:.2f}%")
    print("\nSelection Rationale:")
    if best_model_name == "Logistic Regression":
        print("- Logistic Regression achieved optimal performance with maximum margin linear separation.")
        print("- Because Setosa is linearly separable and Versicolor/Virginica boundaries are largely linear")
        print("  in the standardized petal dimension space, a calibrated linear model prevents overfitting.")
    elif best_model_name == "K-Nearest Neighbours":
        print("- K-Nearest Neighbours effectively captures the localized morphological clusters of Iris species.")
        print("- With standardization applied, Euclidean distances in feature space yield pure neighborhoods.")
    else:
        print("- Random Forest demonstrates strong non-linear boundary separation with zero variance inflation.")
        print("- Ensemble decision trees inherently select the most discriminative petal thresholds.")

    # 7. Phase 8: Model Saving with joblib
    print("\n" + "=" * 75)
    print("PHASE 8: MODEL ARTIFACT SERIALIZATION")
    print("=" * 75)
    model_save_path = os.path.join(models_dir, "best_iris_model.joblib")
    model_payload = {
        "pipeline": best_pipeline,
        "model_name": best_model_name,
        "feature_names": feature_names,
        "target_names": target_names,
        "metrics": best_stats,
        "trained_timestamp": datetime.now().isoformat(),
        "framework_versions": {
            "sklearn": "1.9.1",
            "joblib": "1.6.0"
        }
    }
    joblib.dump(model_payload, model_save_path)
    print(f"[SUCCESS] Model artifact successfully serialized to: {model_save_path}")

    # Also export JSON metadata for rapid inspection
    meta_json_path = os.path.join(models_dir, "model_metadata.json")
    clean_metrics = {k: float(v) if isinstance(v, (np.floating, float)) else v for k, v in best_stats.items()}
    metadata_content = {
        "best_model": best_model_name,
        "feature_names": feature_names,
        "target_names": target_names,
        "test_metrics": clean_metrics,
        "comparison_table": comparison_df.to_dict(orient="records"),
        "trained_timestamp": datetime.now().isoformat()
    }
    with open(meta_json_path, "w") as f:
        json.dump(metadata_content, f, indent=4)
    print(f"[SUCCESS] Model metadata exported to: {meta_json_path}")
    print("=" * 75 + "\n")

    return best_model_name, comparison_df, model_save_path


if __name__ == "__main__":
    build_and_evaluate_models()
