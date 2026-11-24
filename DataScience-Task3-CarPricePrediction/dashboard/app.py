"""
app.py
======
AutoValue AI — Intelligent Car Valuation Platform
OASIS INFOBYTE Data Science Internship | Task 3: Car Price Prediction with Machine Learning.

Features:
- Dark Automotive Digital Cockpit UI/UX with Charcoal (#090D16), Metallic Silver (#94A3B8), and Electric Blue (#38BDF8) accents.
- Preserves all authentic CarDekho dataset features, scikit-learn regression pipeline, and non-negative bounds guarantees.
- 5 Modular Cockpit Views:
  1. Cockpit Overview & Market Telemetry
  2. Vehicle Valuation Calculator (Real-Time Inference Console)
  3. Brand & Fleet Insights (Price distributions, fuel & transmission comparisons)
  4. Market Depreciation Analytics (Mileage vs. Age OLS trends)
  5. Valuation Model Diagnostics (Audited R², MAE, RMSE metrics)
"""

import os
import sys
import json
import joblib
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Configure paths
DASHBOARD_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(DASHBOARD_DIR)
SRC_DIR = os.path.join(PROJECT_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from data_loader import get_project_paths
from predict import CarPricePredictor

# Page Configuration
st.set_page_config(
    page_title="AutoValue AI | Intelligent Car Valuation",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark Automotive Digital Cockpit Styling
THEME_BG = "#090D16"
THEME_CARD = "#0F1524"
THEME_BORDER = "#1E293B"
THEME_BLUE = "#38BDF8"
THEME_GREEN = "#10B981"
THEME_AMBER = "#F59E0B"
THEME_PURPLE = "#A855F7"

st.markdown(f"""
<style>
    /* Global Base */
    .stApp {{
        background-color: {THEME_BG};
        color: #E2E8F0;
        font-family: 'Inter', -apple-system, sans-serif;
    }}
    
    /* Cockpit Branding */
    .cockpit-title {{
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        background: linear-gradient(135deg, #38BDF8 0%, #A855F7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.1rem;
    }}
    .cockpit-sub {{
        font-size: 0.95rem;
        color: #94A3B8;
        margin-bottom: 1.5rem;
    }}
    
    /* Metric Cards */
    .telemetry-card {{
        background-color: {THEME_CARD};
        border-radius: 12px;
        padding: 20px;
        border: 1px solid {THEME_BORDER};
        border-top: 3px solid {THEME_BLUE};
        box-shadow: 0 4px 15px -3px rgba(0, 0, 0, 0.5);
    }}
    .telemetry-label {{
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #94A3B8;
    }}
    .telemetry-value {{
        font-size: 1.9rem;
        font-weight: 800;
        font-family: 'JetBrains Mono', monospace;
        color: #FFFFFF;
        margin-top: 4px;
    }}
    .telemetry-sub {{
        font-size: 0.8rem;
        color: {THEME_BLUE};
        margin-top: 4px;
    }}
    
    /* Content Cards */
    .auto-card {{
        background-color: {THEME_CARD};
        border: 1px solid {THEME_BORDER};
        border-radius: 14px;
        padding: 22px;
        margin-bottom: 16px;
    }}
    
    /* Valuation Hero Badge */
    .valuation-hero {{
        background: rgba(56, 189, 248, 0.08);
        border: 1px solid rgba(56, 189, 248, 0.4);
        border-radius: 14px;
        padding: 24px;
        text-align: center;
        margin-bottom: 18px;
    }}
    .valuation-price {{
        font-size: 2.6rem;
        font-weight: 800;
        font-family: 'JetBrains Mono', monospace;
        color: #38BDF8;
        margin: 6px 0;
    }}
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_predictor_and_metadata():
    """Loads inference pipeline and evaluation metadata."""
    paths = get_project_paths()
    predictor = CarPricePredictor(paths["pipeline_model"])
    with open(paths["model_metadata"], "r", encoding="utf-8") as f:
        meta = json.load(f)
    return predictor, meta


@st.cache_data
def load_cleaned_data():
    """Loads standardized CarDekho dataset."""
    paths = get_project_paths()
    return pd.read_csv(paths["processed_csv"])


def main():
    try:
        predictor, meta = load_predictor_and_metadata()
        df = load_cleaned_data()
    except Exception as e:
        st.error(f"Inference artifact loading failure: {e}")
        st.info("Execute `python src/train.py` from project root to generate model joblib.")
        return

    # Sidebar Navigation
    with st.sidebar:
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px;">
            <div style="font-size: 2rem;">🏎️</div>
            <div>
                <div style="font-size: 1.25rem; font-weight: 800; color: #FFFFFF; font-family: monospace;">AutoValue AI</div>
                <div style="font-size: 0.72rem; color: #38BDF8; font-weight: 700; letter-spacing: 0.05em;">VEHICLE INTELLIGENCE</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        page = st.radio(
            "Cockpit Navigation",
            [
                "Market Telemetry & Overview",
                "Vehicle Valuation Calculator",
                "Brand & Fleet Insights",
                "Depreciation Analytics",
                "Model Performance & Audit"
            ],
            index=0
        )

        st.markdown("---")
        best_name = meta.get("best_model_name", "Random Forest Regressor")
        best_r2 = meta.get("model_comparison", {}).get(best_name, {}).get("test_r2", 0.6558)

        st.markdown(f"""
        <div style="font-size: 0.75rem; color: #64748B; font-family: monospace;">
            <div>MODEL: <b>{best_name.split()[0]} Pipeline</b></div>
            <div>TEST R²: <b>{best_r2:.4f}</b></div>
            <div>CATALOG: <b>{len(df):,d} Verified Cars</b></div>
        </div>
        """, unsafe_allow_html=True)

    # PAGE 1: OVERVIEW & TELEMETRY
    if page == "Market Telemetry & Overview":
        st.markdown('<div class="cockpit-title">AutoValue AI Market Telemetry</div>', unsafe_allow_html=True)
        st.markdown('<div class="cockpit-sub">Algorithmic secondary-market valuation, residual appraisal, and fleet depreciation intelligence.</div>', unsafe_allow_html=True)

        # Telemetry KPI Row
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""
            <div class="telemetry-card">
                <div class="telemetry-label">Analyzed Vehicles</div>
                <div class="telemetry-value">{len(df):,d}</div>
                <div class="telemetry-sub">Clean listings across 29 brands</div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            med_price = df['selling_price'].median()
            st.markdown(f"""
            <div class="telemetry-card" style="border-top-color: #10B981;">
                <div class="telemetry-label">Median Selling Price</div>
                <div class="telemetry-value" style="color: #10B981;">{predictor.format_price_inr(med_price)}</div>
                <div class="telemetry-sub" style="color: #10B981;">Mean: {predictor.format_price_inr(df['selling_price'].mean())}</div>
            </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div class="telemetry-card" style="border-top-color: #A855F7;">
                <div class="telemetry-label">Mean Vehicle Age</div>
                <div class="telemetry-value" style="color: #A855F7;">{df['car_age'].mean():.1f} Yrs</div>
                <div class="telemetry-sub" style="color: #A855F7;">Avg Odo: {df['km_driven'].mean():,.0f} km</div>
            </div>
            """, unsafe_allow_html=True)
        with c4:
            mae_val = meta["model_comparison"][best_name]["test_mae"]
            st.markdown(f"""
            <div class="telemetry-card" style="border-top-color: #F59E0B;">
                <div class="telemetry-label">Mean Absolute Error (MAE)</div>
                <div class="telemetry-value" style="color: #F59E0B;">{predictor.format_price_inr(mae_val)}</div>
                <div class="telemetry-sub" style="color: #F59E0B;">Generalization verification</div>
            </div>
            """, unsafe_allow_html=True)

        # Market Charts
        col_m1, col_m2 = st.columns([1.1, 0.9])
        with col_m1:
            st.markdown('<div class="auto-card">', unsafe_allow_html=True)
            st.markdown("### 🏆 Top 10 Vehicle Brands by Market Volume")
            top_brands = df["brand"].value_counts().head(10).reset_index()
            top_brands.columns = ["brand", "count"]
            fig_brand = px.bar(
                top_brands,
                x="count",
                y="brand",
                orientation="h",
                color="count",
                color_continuous_scale="Blues",
                template="plotly_dark",
                labels={"count": "Listings", "brand": "Brand"}
            )
            fig_brand.update_layout(yaxis=dict(autorange="reversed"), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_brand, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_m2:
            st.markdown('<div class="auto-card">', unsafe_allow_html=True)
            st.markdown("### ⛽ Market Composition by Fuel Type")
            fuel_counts = df["fuel"].value_counts().reset_index()
            fuel_counts.columns = ["fuel", "count"]
            fig_fuel = px.pie(
                fuel_counts,
                names="fuel",
                values="count",
                hole=0.45,
                color_discrete_sequence=["#38BDF8", "#10B981", "#A855F7", "#F59E0B"],
                template="plotly_dark"
            )
            fig_fuel.update_layout(paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_fuel, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # PAGE 2: VALUATION CALCULATOR
    elif page == "Vehicle Valuation Calculator":
        st.markdown('<div class="cockpit-title">Algorithmic Resale Valuation Console</div>', unsafe_allow_html=True)
        st.markdown('<div class="cockpit-sub">Select verified specifications to compute real-time machine learning price appraisal.</div>', unsafe_allow_html=True)

        col_form, col_result = st.columns([6, 5])

        with col_form:
            st.markdown('<div class="auto-card">', unsafe_allow_html=True)
            st.markdown("### ⚙️ Vehicle Specifications")

            brand_list = sorted(df["brand"].unique().tolist())
            selected_brand = st.selectbox("Manufacturer Brand:", brand_list, index=brand_list.index("Maruti") if "Maruti" in brand_list else 0)

            c_f1, c_f2 = st.columns(2)
            with c_f1:
                year_val = st.slider("Manufacturing Year:", min_value=1992, max_value=2020, value=2016, step=1)
                car_age = 2020 - year_val
                st.caption(f"Historical Car Age: **{car_age} years** (relative to 2020)")
            with c_f2:
                km_val = st.number_input("Kilometers Driven:", min_value=500, max_value=800000, value=45000, step=2500)

            c_f3, c_f4 = st.columns(2)
            with c_f3:
                fuel_opts = sorted(df["fuel"].unique().tolist())
                selected_fuel = st.selectbox("Fuel Type:", fuel_opts, index=fuel_opts.index("Petrol") if "Petrol" in fuel_opts else 0)
            with c_f4:
                trans_opts = sorted(df["transmission"].unique().tolist())
                selected_trans = st.selectbox("Transmission:", trans_opts, index=trans_opts.index("Manual") if "Manual" in trans_opts else 0)

            c_f5, c_f6 = st.columns(2)
            with c_f5:
                seller_opts = sorted(df["seller_type"].unique().tolist())
                selected_seller = st.selectbox("Seller Classification:", seller_opts, index=0)
            with c_f6:
                owner_opts = sorted(df["owner"].unique().tolist())
                selected_owner = st.selectbox("Ownership Lineage:", owner_opts, index=0)

            st.markdown('</div>', unsafe_allow_html=True)

        with col_result:
            st.markdown('<div class="auto-card">', unsafe_allow_html=True)
            st.markdown("### 🏷️ Estimated Resale Valuation")

            car_input = {
                "brand": selected_brand,
                "year": year_val,
                "km_driven": km_val,
                "fuel": selected_fuel,
                "seller_type": selected_seller,
                "transmission": selected_trans,
                "owner": selected_owner
            }

            try:
                pred_res = predictor.predict_one(car_input)
                raw_price = pred_res["predicted_price_raw"]
                formatted_price = pred_res["predicted_price_inr"]

                st.markdown(f"""
                <div class="valuation-hero">
                    <div style="font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 600; color: #94A3B8;">Estimated Resale Value</div>
                    <div class="valuation-price">{formatted_price}</div>
                    <div style="font-size: 0.9rem; color: #38BDF8; font-family: monospace;">Raw Estimate: ₹{raw_price:,.0f} ({pred_res['predicted_price_lakhs']} Lakhs)</div>
                </div>
                """, unsafe_allow_html=True)

                # Valuation Context
                brand_mean = df[df["brand"] == selected_brand]["selling_price"].mean()
                st.markdown(f"""
                <div style="font-size: 0.85rem; line-height: 1.6; color: #94A3B8;">
                    <div>• Brand Baseline Average: <b style="color: #FFFFFF;">{predictor.format_price_inr(brand_mean)}</b></div>
                    <div>• Vehicle Age Factor: <b style="color: #FFFFFF;">{car_age} years</b> depreciation applied</div>
                    <div>• Mileage Impact: <b style="color: #FFFFFF;">{km_val:,d} km</b> recorded usage</div>
                </div>
                """, unsafe_allow_html=True)

            except Exception as ex:
                st.error(f"Valuation inference error: {ex}")

            st.markdown('</div>', unsafe_allow_html=True)

    # PAGE 3: BRAND & FLEET INSIGHTS
    elif page == "Brand & Fleet Insights":
        st.markdown('<div class="cockpit-title">Brand Economics & Fleet Diagnostics</div>', unsafe_allow_html=True)
        st.markdown('<div class="cockpit-sub">Price variance across premium vs. budget manufacturers and transmission premiums.</div>', unsafe_allow_html=True)

        c_b1, c_b2 = st.columns(2)
        with c_b1:
            st.markdown('<div class="auto-card">', unsafe_allow_html=True)
            st.markdown("### 💰 Average Selling Price by Top Brands")
            brand_avg = df.groupby("brand")["selling_price"].mean().sort_values(ascending=False).head(12).reset_index()
            fig_bavg = px.bar(
                brand_avg,
                x="selling_price",
                y="brand",
                orientation="h",
                color="selling_price",
                color_continuous_scale="Purples",
                template="plotly_dark",
                labels={"selling_price": "Mean Selling Price (₹)", "brand": "Brand"}
            )
            fig_bavg.update_layout(yaxis=dict(autorange="reversed"), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_bavg, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with c_b2:
            st.markdown('<div class="auto-card">', unsafe_allow_html=True)
            st.markdown("### 🕹️ Transmission Resale Premium")
            fig_trans = px.box(
                df,
                x="transmission",
                y="selling_price",
                color="transmission",
                color_discrete_map={"Manual": "#38BDF8", "Automatic": "#A855F7"},
                template="plotly_dark",
                labels={"selling_price": "Selling Price (₹)", "transmission": "Transmission"}
            )
            fig_trans.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_trans, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # PAGE 4: DEPRECIATION ANALYTICS
    elif page == "Depreciation Analytics":
        st.markdown('<div class="cockpit-title">Market Depreciation Curves</div>', unsafe_allow_html=True)
        st.markdown('<div class="cockpit-sub">Empirical decay analysis evaluating price trajectory against vehicle age and accumulated mileage.</div>', unsafe_allow_html=True)

        st.markdown('<div class="auto-card">', unsafe_allow_html=True)
        st.markdown("### 📉 Selling Price vs. Vehicle Age (Depreciation Curve)")
        sample_df = df.sample(min(1200, len(df)), random_state=42)
        fig_age = px.scatter(
            sample_df,
            x="car_age",
            y="selling_price",
            color="fuel",
            trendline="ols",
            color_discrete_sequence=["#38BDF8", "#10B981", "#A855F7", "#F59E0B"],
            template="plotly_dark",
            labels={"car_age": "Vehicle Age (Years)", "selling_price": "Selling Price (₹)"}
        )
        fig_age.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_age, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # PAGE 5: MODEL PERFORMANCE & AUDIT
    elif page == "Model Performance & Audit":
        st.markdown('<div class="cockpit-title">Valuation Engine Diagnostics</div>', unsafe_allow_html=True)
        st.markdown('<div class="cockpit-sub">Audited regression metrics, error distributions, and benchmark model comparison.</div>', unsafe_allow_html=True)

        comp = meta.get("model_comparison", {})
        c_p1, c_p2, c_p3 = st.columns(3)
        with c_p1:
            st.markdown(f"""
            <div class="telemetry-card">
                <div class="telemetry-label">Champion Pipeline</div>
                <div class="telemetry-value" style="font-size: 1.4rem;">{best_name}</div>
                <div class="telemetry-sub">OneHotEncoder + Regressor</div>
            </div>
            """, unsafe_allow_html=True)
        with c_p2:
            st.markdown(f"""
            <div class="telemetry-card" style="border-top-color: #10B981;">
                <div class="telemetry-label">Test Set R² Score</div>
                <div class="telemetry-value" style="color: #10B981;">{best_r2:.4f}</div>
                <div class="telemetry-sub" style="color: #10B981;">Explained variance ratio</div>
            </div>
            """, unsafe_allow_html=True)
        with c_p3:
            rmse_val = comp[best_name]["test_rmse"]
            st.markdown(f"""
            <div class="telemetry-card" style="border-top-color: #A855F7;">
                <div class="telemetry-label">Root Mean Squared Error</div>
                <div class="telemetry-value" style="color: #A855F7; font-size: 1.3rem;">{predictor.format_price_inr(rmse_val)}</div>
                <div class="telemetry-sub" style="color: #A855F7;">Test sample penalization</div>
            </div>
            """, unsafe_allow_html=True)

        # Model Comparison Table
        st.markdown('<div class="auto-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Benchmark Model Comparison Matrix")
        comp_rows = []
        for m_name, m_stats in comp.items():
            comp_rows.append({
                "Model Architecture": m_name,
                "Train R²": round(m_stats.get("train_r2", 0), 4),
                "Test R²": round(m_stats.get("test_r2", 0), 4),
                "Test MAE (₹)": f"₹{m_stats.get('test_mae', 0):,.0f}",
                "Test RMSE (₹)": f"₹{m_stats.get('test_rmse', 0):,.0f}"
            })
        st.dataframe(pd.DataFrame(comp_rows), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
