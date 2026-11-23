"""
train.py
========
Machine Learning Training, Cross-Validation Benchmarking,
and Model Serialization Engine for Task 3: Car Price Prediction.

Compares 4 Regressors:
1. Linear Regression (Log-Transformed Target)
2. Ridge Regression (Log-Transformed Target)
3. Random Forest Regressor (Log-Transformed Target)
4. Gradient Boosting Regressor (Log-Transformed Target)

Uses ordinary randomized train_test_split (80:20 partition, random_state=42),
appropriate for continuous regression targets without artificial stratification.
Strictly prevents train/test leakage by isolating preprocessing and cross-validation
to the training partition only.
"""

import os
import sys
import json
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple

from sklearn.model_selection import train_test_split, KFold, cross_validate
from sklearn.compose import ColumnTransformer, TransformedTargetRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from data_loader import get_project_paths
from feature_engineering import extract_features, FEATURE_COLUMNS, CATEGORICAL_FEATURES, NUMERICAL_FEATURES

RANDOM_STATE = 42
TEST_SIZE = 0.20
CV_FOLDS = 5


def build_pipeline_preprocessor() -> ColumnTransformer:
    """
    Constructs a robust, production-grade ColumnTransformer.
    Includes SimpleImputer to guard against missing inputs in production.
    """
    num_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    cat_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", num_pipeline, NUMERICAL_FEATURES),
            ("cat", cat_pipeline, CATEGORICAL_FEATURES)
        ],
        remainder="drop"
    )
    return preprocessor


def train_and_compare_models(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    y_test: pd.Series
) -> Tuple[Dict[str, Any], Any, str]:
    """
    Trains and cross-validates 4 regression models on training data,
    evaluates on held-out test data, and returns comparison dictionary and best model.
    """
    preprocessor = build_pipeline_preprocessor()
    kf = KFold(n_splits=CV_FOLDS, shuffle=True, random_state=RANDOM_STATE)

    candidate_models = {
        "Linear Regression": LinearRegression(),
        "Ridge Regression": Ridge(alpha=2.0),
        "Random Forest": RandomForestRegressor(
            n_estimators=180, max_depth=16, min_samples_split=4,
            random_state=RANDOM_STATE, n_jobs=-1
        ),
        "Gradient Boosting": GradientBoostingRegressor(
            n_estimators=180, learning_rate=0.08, max_depth=5,
            random_state=RANDOM_STATE
        )
    }

    results: Dict[str, Any] = {}
    fitted_pipelines: Dict[str, Any] = {}

    print(f"\n[TRAIN] Executing {CV_FOLDS}-Fold Cross-Validation on Training Set (N = {len(X_train)})...")

    scoring = {
        "r2": "r2",
        "neg_mae": "neg_mean_absolute_error",
        "neg_rmse": "neg_root_mean_squared_error"
    }

    for name, base_reg in candidate_models.items():
        base_pipe = Pipeline([
            ("preprocessor", preprocessor),
            ("regressor", base_reg)
        ])

        # Target transformation: log1p ensures exponential depreciation linearity and non-negative predictions
        t_model = TransformedTargetRegressor(
            regressor=base_pipe,
            func=np.log1p,
            inverse_func=np.expm1
        )

        cv_res = cross_validate(t_model, X_train, y_train, cv=kf, scoring=scoring, n_jobs=-1)
        mean_cv_r2 = float(cv_res["test_r2"].mean())
        std_cv_r2 = float(cv_res["test_r2"].std())
        mean_cv_mae = float(-cv_res["test_neg_mae"].mean())
        mean_cv_rmse = float(-cv_res["test_neg_rmse"].mean())

        # Fit on entire training partition
        t_model.fit(X_train, y_train)
        fitted_pipelines[name] = t_model

        # Evaluate on held-out test partition
        test_preds = t_model.predict(X_test)
        test_r2 = float(r2_score(y_test, test_preds))
        test_mae = float(mean_absolute_error(y_test, test_preds))
        test_rmse = float(np.sqrt(mean_squared_error(y_test, test_preds)))

        results[name] = {
            "cv_r2_mean": round(mean_cv_r2, 4),
            "cv_r2_std": round(std_cv_r2, 4),
            "cv_mae": round(mean_cv_mae, 2),
            "cv_rmse": round(mean_cv_rmse, 2),
            "test_r2": round(test_r2, 4),
            "test_mae": round(test_mae, 2),
            "test_rmse": round(test_rmse, 2),
            "test_predictions": test_preds.tolist()
        }

        print(f"  {name:20s} | CV R2: {mean_cv_r2:.4f} (+/- {std_cv_r2:.4f}) | Test R2: {test_r2:.4f} | Test MAE: INR {test_mae:,.0f}")

    # Select best model strictly by validation (CV R2)
    best_model_name = max(results.keys(), key=lambda k: results[k]["cv_r2_mean"])
    best_pipeline = fitted_pipelines[best_model_name]
    print(f"\n[TRAIN] Best Model Selected: '{best_model_name}' (CV R2 = {results[best_model_name]['cv_r2_mean']:.4f})")

    return results, best_pipeline, best_model_name


def extract_feature_names_and_importances(pipeline_model: Any, model_name: str) -> Dict[str, float]:
    """Extracts transformed feature names and coefficients/importances from the fitted pipeline."""
    base_pipe = pipeline_model.regressor_
    preprocessor = base_pipe.named_steps["preprocessor"]
    regressor = base_pipe.named_steps["regressor"]

    # Extract transformed feature names
    cat_encoder = preprocessor.named_transformers_["cat"].named_steps["encoder"]
    encoded_cat_names = cat_encoder.get_feature_names_out(CATEGORICAL_FEATURES).tolist()
    all_feature_names = NUMERICAL_FEATURES + encoded_cat_names

    importances: Dict[str, float] = {}
    if hasattr(regressor, "coef_"):
        coefs = regressor.coef_
        for name, c in zip(all_feature_names, coefs):
            importances[name] = float(c)
    elif hasattr(regressor, "feature_importances_"):
        fis = regressor.feature_importances_
        for name, fi in zip(all_feature_names, fis):
            importances[name] = float(fi)

    return importances


def run_training_pipeline() -> Dict[str, Any]:
    """Executes the complete training workflow and persists model artifacts."""
    paths = get_project_paths()
    if not os.path.exists(paths["processed_csv"]):
        raise FileNotFoundError(f"Cleaned dataset not found at '{paths['processed_csv']}'. Run data_cleaning.py first.")

    df = pd.read_csv(paths["processed_csv"])
    X, y = extract_features(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )

    results, best_pipeline, best_name = train_and_compare_models(X_train, y_train, X_test, y_test)
    importances = extract_feature_names_and_importances(best_pipeline, best_name)

    # Persist best pipeline
    os.makedirs(paths["models_dir"], exist_ok=True)
    joblib.dump(best_pipeline, paths["pipeline_model"])
    print(f"[SERIALIZE] Best pipeline serialized to '{paths['pipeline_model']}'")

    # Persist metadata
    clean_results = {}
    for k, v in results.items():
        entry = dict(v)
        entry.pop("test_predictions", None)
        clean_results[k] = entry

    metadata = {
        "best_model_name": best_name,
        "random_state": RANDOM_STATE,
        "test_size": TEST_SIZE,
        "cv_folds": CV_FOLDS,
        "total_observations": len(df),
        "train_observations": len(X_train),
        "test_observations": len(X_test),
        "feature_columns": FEATURE_COLUMNS,
        "categorical_features": CATEGORICAL_FEATURES,
        "numerical_features": NUMERICAL_FEATURES,
        "model_comparison": clean_results,
        "feature_importances_or_coefs": importances
    }

    with open(paths["model_metadata"], "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    print(f"[SERIALIZE] Model metadata saved to '{paths['model_metadata']}'")

    return {
        "metadata": metadata,
        "results": results,
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "best_pipeline": best_pipeline
    }


if __name__ == "__main__":
    run_training_pipeline()
