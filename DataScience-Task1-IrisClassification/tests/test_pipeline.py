"""
test_pipeline.py
================
Unit tests for data loader, feature consistency, model serialization,
and inference prediction in DataScience-Task1-IrisClassification.
"""

import os
import sys
import unittest
import pandas as pd
import numpy as np

# Add src to sys.path
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(TEST_DIR)
SRC_DIR = os.path.join(PROJECT_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from data_loader import load_and_prepare_iris_data, inspect_data
from predict import IrisPredictor


class TestIrisPipeline(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.df, cls.features, cls.targets = load_and_prepare_iris_data()
        model_path = os.path.join(PROJECT_DIR, "models", "best_iris_model.joblib")
        cls.predictor = IrisPredictor(model_path)

    def test_01_dataset_dimensions(self):
        """Verify dataset has 150 rows, 4 features, and target columns."""
        self.assertEqual(len(self.df), 150)
        self.assertEqual(len(self.features), 4)
        self.assertEqual(len(self.targets), 3)
        self.assertIn("species", self.df.columns)
        self.assertIn("species_id", self.df.columns)

    def test_02_class_balance(self):
        """Verify perfectly balanced distribution (50 per species)."""
        counts = self.df["species"].value_counts().to_dict()
        for species_name in ["Setosa", "Versicolor", "Virginica"]:
            self.assertEqual(counts[species_name], 50)

    def test_03_zero_missing_values(self):
        """Verify zero null or NaN values in dataset."""
        self.assertEqual(int(self.df.isnull().sum().sum()), 0)

    def test_04_feature_data_types(self):
        """Verify feature column data types are floating-point."""
        for feat in self.features:
            self.assertTrue(np.issubdtype(self.df[feat].dtype, np.floating))

    def test_05_predict_setosa(self):
        """Verify known Setosa sample prediction and high confidence."""
        res = self.predictor.predict(5.1, 3.5, 1.4, 0.2)
        self.assertEqual(res["predicted_species"], "Setosa")
        self.assertGreater(res["confidence"], 0.95)
        self.assertAlmostEqual(sum(res["probabilities"].values()), 1.0, places=2)

    def test_06_predict_versicolor(self):
        """Verify known Versicolor sample prediction and high confidence."""
        res = self.predictor.predict(5.9, 3.0, 4.2, 1.5)
        self.assertEqual(res["predicted_species"], "Versicolor")
        self.assertGreater(res["confidence"], 0.85)

    def test_07_predict_virginica(self):
        """Verify known Virginica sample prediction and high confidence."""
        res = self.predictor.predict(6.5, 3.0, 5.5, 1.8)
        self.assertEqual(res["predicted_species"], "Virginica")
        self.assertGreater(res["confidence"], 0.90)

    def test_08_input_validation_negative_values(self):
        """Verify ValueError is raised when negative values are provided."""
        with self.assertRaises(ValueError):
            self.predictor.predict(-5.0, 3.0, 1.4, 0.2)

    def test_09_input_validation_zero_values(self):
        """Verify ValueError is raised when zero values are provided."""
        with self.assertRaises(ValueError):
            self.predictor.predict(5.0, 0.0, 1.4, 0.2)


if __name__ == "__main__":
    unittest.main()
