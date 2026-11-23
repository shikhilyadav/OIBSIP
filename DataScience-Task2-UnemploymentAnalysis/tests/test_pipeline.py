"""
test_pipeline.py
================
Unit and Integration Tests for Oasis Infobyte Task 2:
Unemployment Analysis with Python (India).
"""

import os
import sys
import unittest
import pandas as pd
import numpy as np
from PIL import Image

# Ensure src in sys.path
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(TEST_DIR)
SRC_DIR = os.path.join(PROJECT_DIR, "src")
DATA_DIR = os.path.join(PROJECT_DIR, "data")
VIS_DIR = os.path.join(PROJECT_DIR, "visualizations")

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from data_loader import load_raw_unemployment_data
from data_cleaning import clean_unemployment_data
from analysis import (
    compute_descriptive_statistics,
    compute_regional_analysis,
    compute_monthly_trends,
    compute_covid_impact_analysis,
    compute_correlation_analysis,
    run_full_analysis
)


class TestUnemploymentPipeline(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        raw_csv = os.path.join(DATA_DIR, "raw", "Unemployment_in_India.csv")
        cls.raw_df = load_raw_unemployment_data(raw_csv)
        cls.clean_df, cls.quality_report = clean_unemployment_data(cls.raw_df)

    def test_01_raw_data_shape(self):
        """Verify raw CMIE dataset has 768 rows and 7 raw columns."""
        self.assertEqual(self.raw_df.shape[0], 768)
        self.assertEqual(self.raw_df.shape[1], 7)

    def test_02_cleaning_empty_rows_dropped(self):
        """Verify exactly 28 trailing empty padding rows are dropped, yielding 740 observations."""
        self.assertEqual(self.quality_report["dropped_empty_rows"], 28)
        self.assertEqual(self.clean_df.shape[0], 740)

    def test_03_zero_missing_values_post_cleaning(self):
        """Verify cleaned dataset contains zero null or NaN values."""
        self.assertEqual(int(self.clean_df.isnull().sum().sum()), 0)

    def test_04_zero_duplicates_post_cleaning(self):
        """Verify cleaned dataset contains zero duplicate observation records."""
        subset_cols = ["State", "Date", "Area"]
        self.assertEqual(int(self.clean_df.duplicated(subset=subset_cols).sum()), 0)

    def test_05_date_parsing_and_temporal_features(self):
        """Verify Datetime conversion and derived temporal fields."""
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(self.clean_df["Date"]))
        self.assertIn("Year", self.clean_df.columns)
        self.assertIn("Month", self.clean_df.columns)
        self.assertIn("Month_Name", self.clean_df.columns)
        self.assertIn("Year_Month", self.clean_df.columns)
        self.assertEqual(self.clean_df["Date"].min(), pd.Timestamp("2019-05-31"))
        self.assertEqual(self.clean_df["Date"].max(), pd.Timestamp("2020-06-30"))

    def test_06_state_coverage(self):
        """Verify exactly 28 unique Indian States / UTs are covered."""
        self.assertEqual(self.clean_df["State"].nunique(), 28)

    def test_07_macro_zone_mapping(self):
        """Verify macro geographic zone assignment (North, South, East, West, Central, Northeast)."""
        self.assertIn("Zone", self.clean_df.columns)
        unique_zones = self.clean_df["Zone"].unique().tolist()
        expected_zones = ["South", "North", "East", "West", "Central", "Northeast"]
        for z in expected_zones:
            self.assertIn(z, unique_zones)

    def test_08_covid_phase_partitioning(self):
        """Verify COVID-19 boundary: Pre-COVID (<2020-03-01) vs COVID/Post-COVID (>=2020-03-01)."""
        pre_df = self.clean_df[self.clean_df["Date"] < pd.Timestamp("2020-03-01")]
        post_df = self.clean_df[self.clean_df["Date"] >= pd.Timestamp("2020-03-01")]
        self.assertTrue((pre_df["COVID_Phase"] == "Pre-COVID").all())
        self.assertTrue((post_df["COVID_Phase"] == "COVID/Post-COVID").all())
        self.assertEqual(len(pre_df), 536)
        self.assertEqual(len(post_df), 204)

    def test_09_descriptive_statistics_calculations(self):
        """Verify descriptive statistics output for macroeconomic features."""
        stats = compute_descriptive_statistics(self.clean_df)
        self.assertEqual(len(stats), 3)
        unemp_stat = stats[stats["Indicator"] == "Estimated_Unemployment_Rate"].iloc[0]
        self.assertAlmostEqual(unemp_stat["Mean"], 11.79, places=1)
        self.assertAlmostEqual(unemp_stat["Median"], 8.35, places=1)

    def test_10_regional_rankings(self):
        """Verify regional analysis outputs rankings for all 28 states."""
        state_ranks, zone_ranks = compute_regional_analysis(self.clean_df)
        self.assertEqual(len(state_ranks), 28)
        self.assertEqual(state_ranks.iloc[0]["State"], "Tripura")  # Highest avg rate
        self.assertEqual(state_ranks.iloc[-1]["State"], "Meghalaya")  # Lowest avg rate

    def test_11_covid_impact_metrics(self):
        """Verify Pre vs Post COVID unemployment rate surge calculation."""
        impact = compute_covid_impact_analysis(self.clean_df)
        self.assertGreater(impact["post_covid_mean"], impact["pre_covid_mean"])
        self.assertAlmostEqual(impact["pre_covid_mean"], 9.51, places=1)
        self.assertAlmostEqual(impact["post_covid_mean"], 17.77, places=1)
        self.assertAlmostEqual(impact["percent_change_mean"], 86.91, places=1)

    def test_12_visualizations_exist_and_valid(self):
        """Verify all 8 visual PNG files exist and are valid non-empty images."""
        expected_files = [
            "unemployment_distribution.png",
            "regional_unemployment.png",
            "monthly_trend.png",
            "state_comparison.png",
            "top10_regions.png",
            "correlation_heatmap.png",
            "covid_impact.png",
            "employment_labour_participation.png"
        ]
        for fname in expected_files:
            fpath = os.path.join(VIS_DIR, fname)
            self.assertTrue(os.path.exists(fpath), f"Missing plot: {fname}")
            self.assertGreater(os.path.getsize(fpath), 1000, f"Empty plot: {fname}")
            with Image.open(fpath) as img:
                self.assertGreater(img.size[0], 0)
                self.assertGreater(img.size[1], 0)

    def test_13_state_multiselect_independent_of_zone_filter(self):
        """Verify that state options are independent of the selected Macro-Geographical Zone."""
        df_full = self.clean_df

        # 1. Option list always contains all 28 states
        all_states_sorted = sorted(df_full["State"].unique().tolist())
        self.assertEqual(len(all_states_sorted), 28)

        # 2. Test filtering under All Zones, Central, North, and South
        # Scenario A: All Zones with no states selected (defaults to all)
        df_all = df_full.copy()
        self.assertEqual(len(df_all), 740)
        self.assertEqual(df_all["State"].nunique(), 28)

        # Scenario B: Central zone with no states selected
        df_central = df_full[df_full["Zone"] == "Central"]
        self.assertEqual(df_central["State"].nunique(), 2)
        self.assertSetEqual(set(df_central["State"].unique()), {"Chhattisgarh", "Madhya Pradesh"})
        self.assertEqual(len(all_states_sorted), 28)  # Options remain all 28

        # Scenario C: North zone with no states selected
        df_north = df_full[df_full["Zone"] == "North"]
        self.assertEqual(df_north["State"].nunique(), 8)
        self.assertIn("Delhi", df_north["State"].unique())
        self.assertIn("Haryana", df_north["State"].unique())
        self.assertEqual(len(all_states_sorted), 28)  # Options remain all 28

        # Scenario D: South zone with specific state selection
        selected_states = ["Kerala", "Karnataka"]
        df_south_states = df_full[(df_full["Zone"] == "South") & (df_full["State"].isin(selected_states))]
        self.assertEqual(df_south_states["State"].nunique(), 2)
        self.assertSetEqual(set(df_south_states["State"].unique()), {"Kerala", "Karnataka"})

        # Scenario E: State selected outside the chosen zone produces empty slice handled gracefully
        df_mismatch = df_full[(df_full["Zone"] == "Central") & (df_full["State"].isin(["Kerala"]))]
        self.assertTrue(df_mismatch.empty)


if __name__ == "__main__":
    unittest.main()
