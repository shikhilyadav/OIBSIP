"""
test_pipeline.py
================
Comprehensive Automated Unit and Integration Test Suite for Task 3:
Car Price Prediction with Machine Learning.

Tests:
1. Raw dataset presence and shape (4,340 rows x 8 cols)
2. Data cleaning & deduplication integrity (3,577 clean rows, 763 duplicates dropped)
3. Zero missing values post-cleaning
4. Feature engineering and brand extraction logic
5. Preprocessor ColumnTransformer transformation shapes
6. Model artifact persistence (joblib pipeline & JSON metadata exist)
7. Model pipeline loading and inference
8. Graceful handling of unknown categorical values (handle_unknown='ignore')
9. Prediction finiteness and non-negativity guarantees
10. Single dictionary prediction vs DataFrame prediction equivalence
11. Robust handling of missing input features with default fallbacks
12. All 12 visualization image files presence and validity
"""

import os
import sys
import json
import warnings
import unittest
import joblib
import numpy as np
import pandas as pd
from PIL import Image

# Path configuration
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(TEST_DIR)
SRC_DIR = os.path.join(PROJECT_DIR, "src")
DATA_DIR = os.path.join(PROJECT_DIR, "data")
MODELS_DIR = os.path.join(PROJECT_DIR, "models")
VIS_DIR = os.path.join(PROJECT_DIR, "visualizations")

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from data_loader import load_raw_data, get_project_paths, DATASET_METADATA
from data_cleaning import clean_car_data
from feature_engineering import extract_features, build_preprocessor, FEATURE_COLUMNS
from predict import CarPricePredictor, predict_car_price


class TestCarPricePipeline(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.raw_df = load_raw_data()
        cls.clean_df, cls.report = clean_car_data(cls.raw_df)
        cls.predictor = CarPricePredictor()

    def test_01_raw_dataset_dimensions(self):
        """Verify raw CarDekho dataset has exactly 4,340 rows and 8 expected columns."""
        self.assertEqual(self.raw_df.shape[0], 4340)
        self.assertEqual(self.raw_df.shape[1], 8)
        for col in DATASET_METADATA["columns"]:
            self.assertIn(col, self.raw_df.columns)

    def test_02_cleaning_deduplication(self):
        """Verify exact duplicates (763) are removed yielding 3,577 unique records."""
        self.assertEqual(self.report["dropped_duplicates"], 763)
        self.assertEqual(self.clean_df.shape[0], 3577)

    def test_03_zero_missing_values(self):
        """Verify cleaned dataset has zero missing values."""
        self.assertEqual(int(self.clean_df.isnull().sum().sum()), 0)

    def test_04_brand_and_age_feature_engineering(self):
        """Verify brand standardisation and car_age non-negativity."""
        self.assertIn("brand", self.clean_df.columns)
        self.assertIn("car_age", self.clean_df.columns)
        self.assertTrue((self.clean_df["car_age"] >= 0).all())
        self.assertNotIn("OpelCorsa", self.clean_df["brand"].unique())
        self.assertIn("Opel", self.clean_df["brand"].unique())
        self.assertIn("Land Rover", self.clean_df["brand"].unique())

    def test_05_column_transformer_fitting(self):
        """Verify ColumnTransformer fits without errors and outputs correct numerical shape."""
        X, y = extract_features(self.clean_df)
        prep = build_preprocessor()
        X_trans = prep.fit_transform(X)
        self.assertEqual(X_trans.shape[0], len(X))
        self.assertGreater(X_trans.shape[1], len(FEATURE_COLUMNS))
        self.assertFalse(np.isnan(X_trans).any())

    def test_06_model_artifacts_exist(self):
        """Verify serialized joblib pipeline and metadata JSON exist on disk."""
        paths = get_project_paths()
        self.assertTrue(os.path.exists(paths["pipeline_model"]), "Missing car_price_pipeline.joblib")
        self.assertTrue(os.path.exists(paths["model_metadata"]), "Missing model_metadata.json")
        self.assertGreater(os.path.getsize(paths["pipeline_model"]), 1000)

    def test_07_prediction_output_structure(self):
        """Verify single prediction returns correct dictionary schema."""
        sample = {
            "brand": "Maruti",
            "year": 2017,
            "km_driven": 45000,
            "fuel": "Petrol",
            "seller_type": "Individual",
            "transmission": "Manual",
            "owner": "First Owner"
        }
        res = self.predictor.predict_one(sample)
        self.assertIn("predicted_price_raw", res)
        self.assertIn("predicted_price_inr", res)
        self.assertIn("predicted_price_lakhs", res)
        self.assertIsInstance(res["predicted_price_raw"], float)

    def test_08_unknown_categorical_handling(self):
        """Verify pipeline handles completely unknown brands, fuels, and owners without throwing exceptions."""
        unseen_specs = {
            "brand": "FerrariSupercarUnknown",
            "car_age": 2.0,
            "km_driven": 10000.0,
            "fuel": "HydrogenUnknown",
            "seller_type": "AuctionUnknown",
            "transmission": "ContinuouslyVariable",
            "owner": "Fifth Owner Exotic"
        }
        res = self.predictor.predict_one(unseen_specs)
        self.assertTrue(np.isfinite(res["predicted_price_raw"]))
        self.assertGreater(res["predicted_price_raw"], 0)

    def test_09_prediction_bounds_non_negative(self):
        """Verify predictions are strictly positive and satisfy the minimum scrap floor."""
        old_wreck = {
            "brand": "Maruti",
            "year": 1990,
            "km_driven": 900000,
            "fuel": "LPG",
            "seller_type": "Individual",
            "transmission": "Manual",
            "owner": "Fourth & Above Owner"
        }
        res = self.predictor.predict_one(old_wreck)
        self.assertGreaterEqual(res["predicted_price_raw"], 15000.0)

    def test_10_missing_feature_graceful_defaults(self):
        """Verify predictor handles empty/sparse input dictionaries without crashing."""
        sparse_input = {"km_driven": 50000}
        res = self.predictor.predict_one(sparse_input)
        self.assertTrue(np.isfinite(res["predicted_price_raw"]))

    def test_11_convenience_helper_matches_class(self):
        """Verify predict_car_price convenience wrapper returns consistent output."""
        sample = {
            "brand": "Hyundai",
            "year": 2018,
            "km_driven": 30000,
            "fuel": "Petrol",
            "seller_type": "Dealer",
            "transmission": "Manual",
            "owner": "First Owner"
        }
        res_class = self.predictor.predict_one(sample)
        res_helper = predict_car_price(sample)
        self.assertEqual(res_class["predicted_price_raw"], res_helper["predicted_price_raw"])

    def test_12_all_twelve_visualizations_exist_and_valid(self):
        """Verify all 12 publication-grade visual artifacts exist and are valid non-corrupt images."""
        expected_plots = [
            "selling_price_distribution.png",
            "price_vs_car_age.png",
            "price_vs_km_driven.png",
            "price_by_fuel.png",
            "price_by_transmission.png",
            "brand_avg_selling_price.png",
            "correlation_heatmap.png",
            "feature_relationships.png",
            "model_comparison.png",
            "feature_importance.png",
            "actual_vs_predicted.png",
            "residual_distribution.png"
        ]
        for plot_name in expected_plots:
            fpath = os.path.join(VIS_DIR, plot_name)
            self.assertTrue(os.path.exists(fpath), f"Missing plot: {plot_name}")
            self.assertGreater(os.path.getsize(fpath), 1000, f"Empty plot file: {plot_name}")
            with Image.open(fpath) as img:
                self.assertGreater(img.size[0], 0)
                self.assertGreater(img.size[1], 0)

    def test_13_historical_reference_year_handling(self):
        """Verify car_age = 2020 - year calculation handles historical reference year correctly."""
        test_cases = [
            (2020, 0),
            (2016, 4),
            (2010, 10),
            (1995, 25),
        ]
        for year, expected_age in test_cases:
            computed_age = 2020 - year
            self.assertEqual(computed_age, expected_age)
            self.assertGreaterEqual(computed_age, 0)

        # In cleaned data, all car_age must be >= 0 and match 2020 - year
        recalculated_age = 2020 - self.clean_df["year"]
        self.assertTrue((self.clean_df["car_age"] == recalculated_age).all())

    def test_14_metadata_consistency_with_model(self):
        """Verify model_metadata.json matches evaluated models, dataset size, and brand count."""
        paths = get_project_paths()
        with open(paths["model_metadata"], "r", encoding="utf-8") as f:
            meta = json.load(f)

        self.assertEqual(meta["best_model_name"], "Linear Regression")
        self.assertEqual(meta["total_observations"], 3577)
        self.assertEqual(meta["train_observations"], 2861)
        self.assertEqual(meta["test_observations"], 716)
        self.assertEqual(meta["cv_folds"], 5)

        # 4 models present
        expected_models = ["Linear Regression", "Ridge Regression", "Random Forest", "Gradient Boosting"]
        for m in expected_models:
            self.assertIn(m, meta["model_comparison"])

        # Cleaned dataset brand count
        actual_brands = set(self.clean_df["brand"].unique())
        self.assertEqual(len(actual_brands), 29)

        # Verified metadata values
        self.assertAlmostEqual(meta["model_comparison"]["Random Forest"]["cv_mae"], 140985.25, places=1)
        self.assertAlmostEqual(meta["model_comparison"]["Random Forest"]["test_rmse"], 346417.04, places=1)
        self.assertAlmostEqual(meta["model_comparison"]["Gradient Boosting"]["cv_mae"], 136753.10, places=1)
        self.assertAlmostEqual(meta["model_comparison"]["Gradient Boosting"]["test_rmse"], 383371.75, places=1)

    def test_15_model_artifact_loading_without_warnings(self):
        """Verify serialized joblib model loads cleanly without version mismatch or corruption warnings."""
        paths = get_project_paths()
        with warnings.catch_warnings(record=True) as recorded_warnings:
            warnings.simplefilter("always")
            model = joblib.load(paths["pipeline_model"])

        # Check model loaded
        self.assertIsNotNone(model)
        self.assertTrue(hasattr(model, "predict"))

        # Verify no UserWarning/InconsistentVersionWarning on load
        version_warnings = [
            w for w in recorded_warnings
            if "InconsistentVersionWarning" in str(w.category) or "version mismatch" in str(w.message).lower()
        ]
        self.assertEqual(len(version_warnings), 0, f"Model load produced version warnings: {version_warnings}")

    def test_16_valid_prediction_input_ranges_and_monotonicity(self):
        """Verify predictions reflect reasonable economic behaviors across valid input ranges."""
        # 1. Monotonicity: Newer car should be worth more than older car (all else equal)
        newer_car = {
            "brand": "Maruti",
            "year": 2018,
            "km_driven": 40000,
            "fuel": "Petrol",
            "seller_type": "Individual",
            "transmission": "Manual",
            "owner": "First Owner"
        }
        older_car = dict(newer_car, year=2010)

        pred_newer = self.predictor.predict_one(newer_car)["predicted_price_raw"]
        pred_older = self.predictor.predict_one(older_car)["predicted_price_raw"]
        self.assertGreater(pred_newer, pred_older, "Newer car must predict higher price than older car")

        # 2. Luxury vs Mass-Market: BMW should predict higher than Maruti with identical specs
        bmw_car = dict(newer_car, brand="BMW")
        pred_bmw = self.predictor.predict_one(bmw_car)["predicted_price_raw"]
        self.assertGreater(pred_bmw, pred_newer, "Luxury marque must predict higher price than mass-market car")

        # 3. Minimum floor check
        extreme_old = dict(newer_car, year=1980, km_driven=1000000)
        pred_extreme = self.predictor.predict_one(extreme_old)["predicted_price_raw"]
        self.assertGreaterEqual(pred_extreme, 15000.0)

    def test_17_dashboard_prediction_button_simulation(self):
        """Simulate dashboard valuation trigger and verify resulting output and typical error bounds."""
        paths = get_project_paths()
        with open(paths["model_metadata"], "r", encoding="utf-8") as f:
            meta = json.load(f)

        mae_val = meta["model_comparison"][meta["best_model_name"]]["test_mae"]

        # Simulate user inputs
        user_inputs = {
            "brand": "Hyundai",
            "car_age": 4.0,  # 2016 model relative to 2020
            "km_driven": 45000.0,
            "fuel": "Diesel",
            "seller_type": "Dealer",
            "transmission": "Manual",
            "owner": "First Owner"
        }

        # Trigger prediction logic
        pred_result = self.predictor.predict_one(user_inputs)

        # Assert output schema and values
        self.assertIn("predicted_price_raw", pred_result)
        self.assertIn("predicted_price_inr", pred_result)
        est_price = pred_result["predicted_price_raw"]
        self.assertGreater(est_price, 0)

        # Assert typical error range computation
        lower_bound = max(15000.0, est_price - mae_val)
        upper_bound = est_price + mae_val
        self.assertLess(lower_bound, upper_bound)
        self.assertLessEqual(lower_bound, est_price)
        self.assertGreaterEqual(upper_bound, est_price)


if __name__ == "__main__":
    unittest.main()
