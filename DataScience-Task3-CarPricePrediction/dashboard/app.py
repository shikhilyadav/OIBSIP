"""
app.py
======
Interactive Car Price Prediction & Valuation Portal
OASIS INFOBYTE Data Science Internship - Task 3.

Features:
- Live vehicle specification input form with dynamic brand, fuel, transmission, and owner selections
- Instant machine learning valuation loading the pre-trained scikit-learn pipeline
- Clear INR pricing cards (₹ and Lakhs/Crores)
- EDA insights gallery, model diagnostic comparisons, and feature importance explanations
"""

import os
import sys
import json
import joblib
import pandas as pd
import numpy as np
import streamlit as st

# Configure paths
DASHBOARD_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(DASHBOARD_DIR)
SRC_DIR = os.path.join(PROJECT_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from data_loader import get_project_paths
from predict import CarPricePredictor

# Set page config
st.set_page_config(
    page_title="Car Price Prediction | Oasis Infobyte Task 3",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Emerald Green & Clean Slate)
THEME_PRIMARY = "#059669"
THEME_SECONDARY = "#2563eb"
THEME_DARK = "#1e293b"

st.markdown(f"""
<style>
    .main-title {{
        font-size: 2.2rem;
        font-weight: 800;
        color: {THEME_DARK};
        margin-bottom: 0px;
    }}
    .sub-title {{
        font-size: 1.05rem;
        color: #64748b;
        margin-bottom: 24px;
    }}
    .kpi-card {{
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 12px;
    }}
    .kpi-label {{
        font-size: 0.82rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
    }}
    .kpi-value {{
        font-size: 1.9rem;
        font-weight: 800;
        color: {THEME_PRIMARY};
        margin-top: 4px;
    }}
    .kpi-subtext {{
        font-size: 0.85rem;
        color: #475569;
        margin-top: 4px;
    }}
    .valuation-box {{
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        border: 2px solid {THEME_PRIMARY};
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        margin-top: 15px;
        margin-bottom: 20px;
    }}
    .stTabs [data-baseweb="tab"] {{
        font-weight: 600;
        height: 48px;
    }}
    .stTabs [aria-selected="true"] {{
        color: {THEME_PRIMARY} !important;
        border-bottom-color: {THEME_PRIMARY} !important;
    }}
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_predictor_and_metadata():
    """Loads predictor inference engine and training metadata."""
    paths = get_project_paths()
    predictor = CarPricePredictor(paths["pipeline_model"])
    with open(paths["model_metadata"], "r", encoding="utf-8") as f:
        meta = json.load(f)
    return predictor, meta


@st.cache_data
def load_cleaned_data():
    """Loads cleaned CarDekho dataset."""
    paths = get_project_paths()
    return pd.read_csv(paths["processed_csv"])


def main():
    paths = get_project_paths()
    try:
        predictor, meta = load_predictor_and_metadata()
        df = load_cleaned_data()
    except Exception as e:
        st.error(f"Error loading model artifacts: {e}")
        st.info("Please run `python src/train.py` from the project root to generate the model artifacts.")
        return

    # Header
    st.markdown('<div class="main-title">🚗 Used Car Price Prediction & Valuation Portal</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">OASIS INFOBYTE Data Science Internship | Task 3: Machine Learning Resale Valuation System</div>', unsafe_allow_html=True)
    st.caption("ℹ️ **Historical Benchmark Notice:** Valuations are estimates based on historical 2020 CarDekho market listings (reference year 2020, where car_age = 2020 - manufacturing year). They represent historical 2020 price dynamics rather than current 2026 market valuations.")

    # -------------------------------------------------------------------------
    # TOP KPI OVERVIEW CARDS
    # -------------------------------------------------------------------------
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Analyzed Vehicles</div>
            <div class="kpi-value">{len(df):,d}</div>
            <div class="kpi-subtext">Clean unique listings (29 brands)</div>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Median Market Price</div>
            <div class="kpi-value">{predictor.format_price_inr(df['selling_price'].median())}</div>
            <div class="kpi-subtext">Mean: {predictor.format_price_inr(df['selling_price'].mean())}</div>
        </div>
        """, unsafe_allow_html=True)
    with k3:
        best_name = meta["best_model_name"]
        best_r2 = meta["model_comparison"][best_name]["test_r2"]
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Best ML Model</div>
            <div class="kpi-value" style="color: {THEME_SECONDARY};">{best_name.split()[0]}</div>
            <div class="kpi-subtext">Test $R^2$: <b>{best_r2:.4f}</b></div>
        </div>
        """, unsafe_allow_html=True)
    with k4:
        best_mae = meta["model_comparison"][best_name]["test_mae"]
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Mean Absolute Error</div>
            <div class="kpi-value" style="color: #7c3aed;">{predictor.format_price_inr(best_mae)}</div>
            <div class="kpi-subtext">Held-out test verification</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # DASHBOARD TABS
    # -------------------------------------------------------------------------
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔮 Instant Valuation",
        "📊 Market EDA Gallery",
        "🤖 Model Benchmarks",
        "💡 Explainability & Drivers",
        "📋 Dataset Browser"
    ])

    # -------------------------------------------------------------------------
    # TAB 1: INSTANT VALUATION CALCULATOR
    # -------------------------------------------------------------------------
    with tab1:
        st.subheader("Vehicle Valuation Calculator")
        st.markdown("Input vehicle specifications below to estimate historical resale value in Indian Rupees (INR), based on the 2020 CarDekho dataset.")

        col_in1, col_in2 = st.columns([1.1, 0.9])

        with col_in1:
            st.markdown("#### Vehicle Identity & Age")
            all_brands = sorted(df["brand"].unique().tolist())
            sel_brand = st.selectbox("Manufacturer / Brand:", all_brands, index=all_brands.index("Maruti") if "Maruti" in all_brands else 0)

            c_year, c_km = st.columns(2)
            with c_year:
                sel_year = st.slider("Manufacturing Year:", min_value=1995, max_value=2020, value=2016, step=1)
                car_age = 2020 - sel_year
                st.caption(f"Estimated Car Age: **{car_age} years** (relative to 2020 historical baseline)")
            with c_km:
                sel_km = st.number_input("Kilometres Driven:", min_value=500, max_value=800000, value=45000, step=5000)

            st.markdown("#### Mechanical & Commercial Details")
            c_fuel, c_trans = st.columns(2)
            with c_fuel:
                fuel_options = ["Petrol", "Diesel", "CNG", "LPG", "Electric"]
                sel_fuel = st.selectbox("Fuel Type:", fuel_options, index=0)
            with c_trans:
                sel_transmission = st.selectbox("Transmission Type:", ["Manual", "Automatic"], index=0)

            c_owner, c_seller = st.columns(2)
            with c_owner:
                owner_options = ["First Owner", "Second Owner", "Third Owner", "Fourth & Above Owner", "Test Drive Car"]
                sel_owner = st.selectbox("Ownership History:", owner_options, index=0)
            with c_seller:
                seller_options = ["Individual", "Dealer", "Trustmark Dealer"]
                sel_seller = st.selectbox("Seller Category:", seller_options, index=0)

            predict_button = st.button("🚀 Calculate Estimated Selling Price", type="primary", use_container_width=True)

        with col_in2:
            st.markdown("#### Predicted Market Valuation")

            if "valuation_result" not in st.session_state:
                st.session_state.valuation_result = None

            if predict_button:
                car_specs = {
                    "brand": sel_brand,
                    "car_age": float(car_age),
                    "km_driven": float(sel_km),
                    "fuel": sel_fuel,
                    "seller_type": sel_seller,
                    "transmission": sel_transmission,
                    "owner": sel_owner
                }
                pred_out = predictor.predict_one(car_specs)
                st.session_state.valuation_result = (pred_out, car_specs, sel_year)

            if st.session_state.valuation_result is not None:
                pred_out, car_specs, evaluated_year = st.session_state.valuation_result
                est_price = pred_out["predicted_price_raw"]
                mae_val = meta["model_comparison"][best_name]["test_mae"]

                st.markdown(f"""
                <div class="valuation-box">
                    <div style="font-size: 0.9rem; font-weight: 700; color: #047857; text-transform: uppercase;">
                        Estimated Resale Valuation (2020 Historical Benchmark)
                    </div>
                    <div style="font-size: 2.8rem; font-weight: 900; color: {THEME_PRIMARY}; margin: 8px 0;">
                        {pred_out['predicted_price_inr']}
                    </div>
                    <div style="font-size: 1.1rem; font-weight: 600; color: #065f46;">
                        Exact Model Estimate: ₹ {est_price:,.0f}
                    </div>
                    <div style="font-size: 0.85rem; color: #047857; margin-top: 10px;">
                        Illustrative Typical Error Range (± Test MAE):<br>
                        <b>{predictor.format_price_inr(max(15000, est_price - mae_val))} — {predictor.format_price_inr(est_price + mae_val)}</b>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.caption(f"📌 **Note on Error Range:** Test MAE ({predictor.format_price_inr(mae_val)}) is the mean absolute error across held-out test predictions, serving as an illustrative typical benchmark rather than a statistical prediction interval or guaranteed market boundary.")

                st.info(f"""
                **Valuation Context for {evaluated_year} {car_specs['brand']}:**
                - **Depreciation Factor:** {car_specs['car_age']:.0f} years of age from manufacturing date (reference year 2020).
                - **Odometer Impact:** {car_specs['km_driven']:,.0f} km driven.
                - **Powertrain:** {car_specs['fuel']} engine with {car_specs['transmission']} transmission.
                - **Ownership:** {car_specs['owner']} selling via {car_specs['seller_type']}.
                - **Market Context:** Valuation based on historical 2020 market pricing.
                """)
            else:
                st.info("👈 Set vehicle specifications on the left and click **🚀 Calculate Estimated Selling Price** to generate a machine learning valuation.")

    # -------------------------------------------------------------------------
    # TAB 2: EXPLORATORY DATA ANALYSIS GALLERY
    # -------------------------------------------------------------------------
    with tab2:
        st.subheader("Automated Exploratory Data Analysis Suite")
        st.markdown("All 8 exploratory charts generated from the cleaned 3,577 records at 300 DPI.")

        vis_dir = paths["visualizations_dir"]
        c1, c2 = st.columns(2)
        with c1:
            p1 = os.path.join(vis_dir, "selling_price_distribution.png")
            if os.path.exists(p1):
                st.image(p1, caption="1. Selling Price Distribution (Right-Skewed with Luxury Tail)", use_container_width=True)

            p3 = os.path.join(vis_dir, "price_vs_km_driven.png")
            if os.path.exists(p3):
                st.image(p3, caption="3. Odometer Mileage vs. Selling Price Across Fuels", use_container_width=True)

            p5 = os.path.join(vis_dir, "price_by_transmission.png")
            if os.path.exists(p5):
                st.image(p5, caption="5. Automatic vs. Manual Transmission Price Premium", use_container_width=True)

            p7 = os.path.join(vis_dir, "correlation_heatmap.png")
            if os.path.exists(p7):
                st.image(p7, caption="7. Pearson Correlation Heatmap", use_container_width=True)

        with c2:
            p2 = os.path.join(vis_dir, "price_vs_car_age.png")
            if os.path.exists(p2):
                st.image(p2, caption="2. Vehicle Depreciation Curve (Price vs. Age)", use_container_width=True)

            p4 = os.path.join(vis_dir, "price_by_fuel.png")
            if os.path.exists(p4):
                st.image(p4, caption="4. Selling Price Distributions by Fuel Type", use_container_width=True)

            p6 = os.path.join(vis_dir, "brand_avg_selling_price.png")
            if os.path.exists(p6):
                st.image(p6, caption="6. Brand-Wise Average Resale Price Ranking", use_container_width=True)

            p8 = os.path.join(vis_dir, "feature_relationships.png")
            if os.path.exists(p8):
                st.image(p8, caption="8. Multivariate Interactions: Age, Fuel & Transmission", use_container_width=True)

    # -------------------------------------------------------------------------
    # TAB 3: MODEL BENCHMARKS & EVALUATION
    # -------------------------------------------------------------------------
    with tab3:
        st.subheader("Machine Learning Algorithm Comparison & Metrics")
        st.markdown("All 4 regression algorithms were cross-validated on the 80% training set ($N = 2,861$) and tested on the 20% held-out test set ($N = 716$).")

        # Table comparison
        comp_df = pd.DataFrame(meta["model_comparison"]).T
        comp_df.reset_index(inplace=True)
        comp_df.rename(columns={
            "index": "Algorithm",
            "cv_r2_mean": "Mean CV R²",
            "cv_r2_std": "CV R² Std Dev",
            "cv_mae": "CV MAE (INR)",
            "test_r2": "Held-Out Test R²",
            "test_mae": "Test MAE (INR)",
            "test_rmse": "Test RMSE (INR)"
        }, inplace=True)

        st.dataframe(comp_df, hide_index=True, use_container_width=True)

        col_m1, col_m2 = st.columns(2)
        with col_m1:
            p9 = os.path.join(vis_dir, "model_comparison.png")
            if os.path.exists(p9):
                st.image(p9, caption="9. Cross-Validation vs. Test Performance Comparison", use_container_width=True)

            p11 = os.path.join(vis_dir, "actual_vs_predicted.png")
            if os.path.exists(p11):
                st.image(p11, caption="11. Actual vs. Predicted Prices with Ideal Line", use_container_width=True)

        with col_m2:
            p10 = os.path.join(vis_dir, "feature_importance.png")
            if os.path.exists(p10):
                st.image(p10, caption="10. Feature Elasticity / Importance Weights", use_container_width=True)

            p12 = os.path.join(vis_dir, "residual_distribution.png")
            if os.path.exists(p12):
                st.image(p12, caption="12. Residual Error Distribution & Homoscedasticity Check", use_container_width=True)

    # -------------------------------------------------------------------------
    # TAB 4: EXPLAINABILITY & DRIVERS
    # -------------------------------------------------------------------------
    with tab4:
        st.subheader("Model Explainability & Key Resale Value Drivers")
        st.markdown(r"""
        ### 🔍 How Vehicle Characteristics Impact Resale Price (Log-Target Regression Model):
        The selected production model is a **Log-Transformed Linear Regression** predicting $\ln(1 + \text{selling\_price})$. The coefficients represent additive effects in log-price space for standardized continuous features and one-hot categorical features.
        
        > **Important Interpretability Note:** These numbers are log-target regression coefficients ($\beta = \frac{\partial \ln(1+y)}{\partial x}$), not direct Rupee (INR) amounts. They reflect associative statistical patterns observed in historical 2020 CarDekho listings, rather than deterministic or causal effects.

        1. **Vehicle Depreciation (Car Age):**
           - `car_age` coefficient: **$-0.4753$** per standardized standard deviation of age (corresponding to an annual rate of $\approx -0.117$ log-points per year of vehicle age).
           - This exponential decay means vehicle depreciation is steepest in initial years before flattening asymptotically.
        2. **Brand Tier & Luxury Marque Multipliers:**
           - Highest positive log-coefficients: **Land Rover (+1.3205)**, **Jaguar (+1.1552)**, **Mercedes-Benz (+0.8383)**, **Mitsubishi (+0.7992)**, **Volvo (+0.7991)**, **Audi (+0.7684)**, **BMW (+0.6941)**.
           - High-volume mass-market brands (Maruti $-0.4448$, Hyundai $-0.3216$, Tata $-0.8115$) reflect accessible economy segments.
        3. **Transmission Mechanism:**
           - `transmission_Automatic`: **$+0.1828$** vs `transmission_Manual`: **$-0.1828$**.
           - The net contrast ($\Delta \beta \approx +0.3657$) corresponds to an estimated $\approx +44\%$ multiplicative price premium for automatic transmissions, holding other features equal.
        4. **Powertrain / Fuel Economics:**
           - `fuel_Diesel`: **$+0.3707$**, `fuel_Petrol`: **$-0.0518$**, `fuel_CNG`: **$-0.1360$**, `fuel_LPG`: **$-0.1829$**.
           - Diesel models command higher resale values due to fuel efficiency, durability, and highway torque.
        5. **Ownership History & Seller Channel:**
           - `owner_First Owner`: **$+0.0287$**, `owner_Second Owner`: **$-0.0157$**, `owner_Third Owner`: **$-0.1116$**, `owner_Fourth & Above Owner`: **$-0.1289$**.
           - Each additional previous owner introduces a progressive penalty in log-price.
           - `seller_type_Trustmark Dealer`: **$+0.1426$** commands a premium over `Individual`: **$-0.1131$**.

        > **Historical & Causal Disclaimer:** Machine learning estimates reflect empirical patterns from historical 2020 CarDekho listings. Statistical correlation does not establish causation. Actual individual market transactions depend on physical vehicle inspection, maintenance history, accident history, and local RTO registration taxes.
        """)

    # -------------------------------------------------------------------------
    # TAB 5: DATASET BROWSER
    # -------------------------------------------------------------------------
    with tab5:
        st.subheader("Processed CarDekho Dataset Browser")
        st.markdown(f"Browsing **{len(df):,d}** cleaned, deduplicated used vehicle records.")

        f_brand = st.multiselect("Filter by Brand:", sorted(df["brand"].unique()), default=[])
        f_fuel = st.multiselect("Filter by Fuel:", sorted(df["fuel"].unique()), default=[])

        display_df = df.copy()
        if f_brand:
            display_df = display_df[display_df["brand"].isin(f_brand)]
        if f_fuel:
            display_df = display_df[display_df["fuel"].isin(f_fuel)]

        st.dataframe(display_df, hide_index=True, use_container_width=True)
        st.caption(f"Showing {len(display_df):,d} matching records.")

        csv_bytes = display_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv_bytes,
            file_name="car_details_filtered.csv",
            mime="text/csv"
        )


if __name__ == "__main__":
    main()
