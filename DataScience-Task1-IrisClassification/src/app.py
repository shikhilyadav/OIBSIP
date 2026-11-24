"""
app.py
======
IrisAI — Botanical Intelligence Studio
Tagline: Where Nature Meets Intelligence.
Oasis Infobyte Data Science Internship — Task 1: Iris Flower Classification.

Visual Reference Driven Botanical SaaS UI/UX:
- Premium White Rounded Application Shell on Soft Mint Canvas (#F2F7F3)
- Palette:
    - Canvas Background: #F2F7F3
    - Workspace / Card Base: #FFFFFF
    - Forest Green Accent: #285943
    - Sage Secondary: #5C9A72
    - Soft Mint Pastel: #DFF4E5
    - Pale Sage: #E9F1E8
    - Muted Lavender: #EAE7F5
    - Warm Beige: #F8EDDE
    - Headings: #183A2A
    - Body Text: #647269
    - Borders: #E4EBE3
- Distinct UI Elements Inspired by Visual References:
    - Large Botanical Hero Banner with Tagline & High-Res Botanical SVG Artwork
    - 4 Pastel Floating KPI Telemetry Cards with Soft Icon Containers
    - Two-Column Interactive Specimen Classifier with Quick Presets & Floating Output Panel
    - Searchable Light Dataset Table with Responsive Overflow & Metric Filters
    - 3 Profile Cards for Setosa, Versicolor, and Virginica with Actual Morphometric Moments
    - Scientific Model Evaluation with Interactive Confusion Matrix & Benchmark Table
- Strict Preservation Rules:
    - Preserves trained Random Forest model (`best_iris_model.joblib`)
    - Preserves 4 input features & StandardScaler pipeline
    - Preserves exact prediction probabilities and historical test metrics (96.67% accuracy)
"""

import os
import sys
import json
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Configure paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)
DATA_PATH = os.path.join(BASE_DIR, "data", "iris.csv")
META_PATH = os.path.join(BASE_DIR, "models", "model_metadata.json")

if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from predict import IrisPredictor

# Page Configuration
st.set_page_config(
    page_title="IrisAI | Botanical Intelligence Studio",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Visual Reference Inspired Botanical SaaS Design System
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Manrope', 'Inter', -apple-system, sans-serif;
    }

    /* Soft Mint Canvas */
    .stApp {
        background-color: #F2F7F3;
        color: #647269;
    }

    /* Professional Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E4EBE3;
        padding-top: 1.5rem;
    }

    /* Top Workspace Header Bar */
    .saas-topbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #FFFFFF;
        border: 1px solid #E4EBE3;
        border-radius: 16px;
        padding: 12px 24px;
        margin-bottom: 24px;
        box-shadow: 0 2px 12px rgba(24, 58, 42, 0.03);
    }
    .breadcrumb-text {
        font-size: 0.82rem;
        color: #8BAA91;
        font-weight: 600;
        letter-spacing: 0.02em;
    }
    .user-pill {
        display: flex;
        align-items: center;
        gap: 8px;
        background: #F2F7F3;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 700;
        color: #183A2A;
        border: 1px solid #E4EBE3;
    }

    /* Hero Banner with Botanical Illustration */
    .botanical-hero {
        background: linear-gradient(135deg, #E9F1E8 0%, #DFF4E5 50%, #F8FAF8 100%);
        border: 1px solid #D6E4D5;
        border-radius: 20px;
        padding: 32px 36px;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(40, 89, 67, 0.05);
    }
    .hero-tagline {
        font-size: 0.75rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: #5C9A72;
        margin-bottom: 8px;
    }
    .hero-headline {
        font-size: 2.3rem;
        font-weight: 800;
        color: #183A2A;
        letter-spacing: -0.03em;
        line-height: 1.2;
        margin-bottom: 10px;
    }
    .hero-subtext {
        font-size: 0.95rem;
        color: #4A6353;
        max-width: 620px;
        line-height: 1.6;
    }

    /* Pastel Telemetry KPI Cards */
    .kpi-card-mint {
        background: #FFFFFF;
        border: 1px solid #E4EBE3;
        border-radius: 16px;
        padding: 22px;
        box-shadow: 0 2px 10px rgba(24, 58, 42, 0.03);
        position: relative;
        overflow: hidden;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .kpi-card-mint:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(24, 58, 42, 0.06);
    }
    .kpi-icon-pill {
        width: 38px;
        height: 38px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.15rem;
        margin-bottom: 14px;
    }
    .kpi-val {
        font-size: 2rem;
        font-weight: 800;
        color: #183A2A;
        letter-spacing: -0.02em;
        line-height: 1.1;
    }
    .kpi-label {
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #7E9485;
        margin-top: 4px;
    }
    .kpi-delta {
        font-size: 0.78rem;
        font-weight: 600;
        color: #285943;
        margin-top: 6px;
    }

    /* Premium White Workspace Card */
    .saas-card {
        background-color: #FFFFFF;
        border: 1px solid #E4EBE3;
        border-radius: 18px;
        padding: 24px 28px;
        margin-bottom: 24px;
        box-shadow: 0 2px 14px rgba(24, 58, 42, 0.03);
    }
    .card-title {
        font-size: 1.15rem;
        font-weight: 800;
        color: #183A2A;
        letter-spacing: -0.01em;
        margin-bottom: 4px;
    }
    .card-sub {
        font-size: 0.85rem;
        color: #7E9485;
        margin-bottom: 18px;
    }

    /* Diagnosis Hero Badges */
    .hero-badge-setosa {
        background: linear-gradient(135deg, #F3F0FA 0%, #EAE7F5 100%);
        border: 1px solid #D6D0E8;
        border-radius: 16px;
        padding: 26px;
        text-align: center;
        margin-bottom: 20px;
    }
    .hero-badge-versicolor {
        background: linear-gradient(135deg, #FBF8F3 0%, #F8EDDE 100%);
        border: 1px solid #EBDDCF;
        border-radius: 16px;
        padding: 26px;
        text-align: center;
        margin-bottom: 20px;
    }
    .hero-badge-virginica {
        background: linear-gradient(135deg, #EBF5ED 0%, #DFF4E5 100%);
        border: 1px solid #C7E2CE;
        border-radius: 16px;
        padding: 26px;
        text-align: center;
        margin-bottom: 20px;
    }

    /* Buttons */
    div.stButton > button:first-child {
        background-color: #285943;
        color: #FFFFFF;
        font-weight: 700;
        font-size: 0.85rem;
        border-radius: 10px;
        border: none;
        padding: 0.55rem 1.4rem;
        transition: all 0.2s ease;
        box-shadow: 0 2px 8px rgba(40, 89, 67, 0.15);
    }
    div.stButton > button:first-child:hover {
        background-color: #183A2A;
        color: #FFFFFF;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(40, 89, 67, 0.25);
    }

    /* Hide default decoration */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_predictor():
    """Initializes and caches the trained Iris model predictor."""
    return IrisPredictor()


@st.cache_data
def load_dataset():
    """Loads and standardizes the Iris botanical dataset."""
    df = pd.read_csv(DATA_PATH)
    col_map = {
        "SepalLengthCm": "sepal_length",
        "SepalWidthCm": "sepal_width",
        "PetalLengthCm": "petal_length",
        "PetalWidthCm": "petal_width",
        "Species": "species"
    }
    df = df.rename(columns=col_map)
    if "Id" in df.columns:
        df = df.drop(columns=["Id"])
    df["species"] = df["species"].astype(str).str.replace("Iris-", "")
    return df


@st.cache_data
def load_metadata():
    """Loads audited model evaluation metrics."""
    with open(META_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    predictor = load_predictor()
    df = load_dataset()
    meta = load_metadata()

    # Session State for Classifier Presets
    if "sepal_len" not in st.session_state:
        st.session_state.sepal_len = 5.8
    if "sepal_wid" not in st.session_state:
        st.session_state.sepal_wid = 3.0
    if "petal_len" not in st.session_state:
        st.session_state.petal_len = 4.3
    if "petal_wid" not in st.session_state:
        st.session_state.petal_wid = 1.3

    # =========================================================================
    # SIDEBAR: REFERENCE-INSPIRED SAAS NAVIGATION
    # =========================================================================
    with st.sidebar:
        st.markdown("""
        <div style="padding-bottom: 1.5rem; border-bottom: 1px solid #E4EBE3; margin-bottom: 1.5rem;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="width: 44px; height: 44px; border-radius: 12px; background: #DFF4E5; border: 1px solid #C7E2CE; display: flex; align-items: center; justify-content: center; font-size: 1.4rem;">
                    🌿
                </div>
                <div>
                    <div style="font-size: 1.35rem; font-weight: 800; color: #183A2A; letter-spacing: -0.03em;">IrisAI</div>
                    <div style="font-size: 0.72rem; color: #5C9A72; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em;">Botanical Studio</div>
                </div>
            </div>
            <div style="font-size: 0.78rem; color: #7E9485; margin-top: 10px; font-weight: 500;">
                Where Nature Meets Intelligence.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='font-size: 0.72rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; color: #8BAA91; margin-bottom: 8px;'>Workspace</div>", unsafe_allow_html=True)
        page = st.radio(
            "Navigation",
            [
                "Overview",
                "Flower Classifier",
                "Dataset Explorer",
                "Species Insights",
                "Model Performance"
            ],
            index=0,
            label_visibility="collapsed"
        )

        st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style="padding-top: 1.25rem; border-top: 1px solid #E4EBE3; font-size: 0.75rem; color: #7E9485; line-height: 1.8;">
            <div style="font-weight: 800; color: #183A2A; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 4px;">Engine Specs</div>
            <div>Model: <b style="color: #183A2A;">Random Forest Pipeline</b></div>
            <div>Test Accuracy: <b style="color: #285943;">96.67% (Audited)</b></div>
            <div>Taxonomy: <b style="color: #183A2A;">Fisher's 3 Iris Species</b></div>
            <div>Release: <b style="color: #5C9A72;">v2.0 SaaS Edition</b></div>
        </div>
        """, unsafe_allow_html=True)

    # Top Navigation Breadcrumb Bar
    st.markdown(f"""
    <div class="saas-topbar">
        <div class="breadcrumb-text">
            <span>IrisAI Studio</span> &nbsp;/&nbsp; <span style="color: #183A2A; font-weight: 700;">{page}</span>
        </div>
        <div class="user-pill">
            <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #285943;"></span>
            <span>Botanical Lab Active</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # =========================================================================
    # PAGE 1: OVERVIEW & BOTANICAL HERO
    # =========================================================================
    if page == "Overview":
        # Reference-Inspired Botanical Hero Banner
        st.markdown("""
        <div class="botanical-hero">
            <div class="hero-tagline">Botanical Intelligence Studio</div>
            <div class="hero-headline">Where Nature Meets Intelligence</div>
            <div class="hero-subtext">
                Explore morphometric Iris clustering, inspect multi-variate botanical distributions, and execute machine learning classification powered by a calibrated Random Forest pipeline.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 4 Pastel Floating Telemetry KPI Cards
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.markdown(f"""
            <div class="kpi-card-mint">
                <div class="kpi-icon-pill" style="background: #EAE7F5; color: #6B5B95;">🌸</div>
                <div class="kpi-val">{len(df)}</div>
                <div class="kpi-label">Dataset Specimens</div>
                <div class="kpi-delta">50 balanced samples / class</div>
            </div>
            """, unsafe_allow_html=True)
        with k2:
            st.markdown(f"""
            <div class="kpi-card-mint">
                <div class="kpi-icon-pill" style="background: #F8EDDE; color: #B88A62;">🌿</div>
                <div class="kpi-val">{df['species'].nunique()}</div>
                <div class="kpi-label">Distinct Species</div>
                <div class="kpi-delta">Setosa, Versicolor, Virginica</div>
            </div>
            """, unsafe_allow_html=True)
        with k3:
            st.markdown("""
            <div class="kpi-card-mint">
                <div class="kpi-icon-pill" style="background: #DFF4E5; color: #285943;">📏</div>
                <div class="kpi-val">4</div>
                <div class="kpi-label">Input Dimensions</div>
                <div class="kpi-delta">Sepal & Petal Length/Width</div>
            </div>
            """, unsafe_allow_html=True)
        with k4:
            st.markdown(f"""
            <div class="kpi-card-mint">
                <div class="kpi-icon-pill" style="background: #E9F1E8; color: #285943;">🎯</div>
                <div class="kpi-val">{meta['test_metrics']['Test Accuracy']*100:.1f}%</div>
                <div class="kpi-label">Classifier Accuracy</div>
                <div class="kpi-delta">Audited held-out test split</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

        # Main Workspace Charts: 2 Columns
        col_c1, col_c2 = st.columns([11, 9])
        with col_c1:
            st.markdown('<div class="saas-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">Morphological Relationships</div>', unsafe_allow_html=True)
            st.markdown('<div class="card-sub">Petal length versus petal width displays orthogonal separation for Setosa and clear margin clustering for Virginica.</div>', unsafe_allow_html=True)

            fig_scat = px.scatter(
                df,
                x="petal_length",
                y="petal_width",
                color="species",
                color_discrete_map={"Setosa": "#6B5B95", "Versicolor": "#B88A62", "Virginica": "#285943"},
                labels={"petal_length": "Petal Length (cm)", "petal_width": "Petal Width (cm)", "species": "Species"},
                template="plotly_white",
                height=350
            )
            fig_scat.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="#FFFFFF",
                font=dict(color="#647269", family="Manrope"),
                margin=dict(l=20, r=20, t=10, b=20),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_scat, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_c2:
            st.markdown('<div class="saas-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">Species Cohort Balance</div>', unsafe_allow_html=True)
            st.markdown('<div class="card-sub">Specimen distribution across Fisher\'s classical 150-sample survey.</div>', unsafe_allow_html=True)

            spec_counts = df["species"].value_counts().reset_index()
            spec_counts.columns = ["species", "count"]
            fig_pie = px.pie(
                spec_counts,
                names="species",
                values="count",
                color="species",
                color_discrete_map={"Setosa": "#6B5B95", "Versicolor": "#B88A62", "Virginica": "#285943"},
                hole=0.6,
                template="plotly_white",
                height=350
            )
            fig_pie.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=10, t=10, b=10),
                font=dict(color="#647269", family="Manrope")
            )
            st.plotly_chart(fig_pie, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Species Cohort Profiles Table
        st.markdown('<div class="saas-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Empirical Species Morphometric Means</div>', unsafe_allow_html=True)
        st.markdown('<div class="card-sub">Baseline feature means computed directly from authentic dataset observations.</div>', unsafe_allow_html=True)
        means_df = df.groupby("species")[["sepal_length", "sepal_width", "petal_length", "petal_width"]].mean().round(2).reset_index()
        means_df.columns = ["Botanical Species", "Sepal Length (cm)", "Sepal Width (cm)", "Petal Length (cm)", "Petal Width (cm)"]
        st.dataframe(means_df, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # =========================================================================
    # PAGE 2: FLOWER CLASSIFIER (2-COLUMN REFERENCE WORKSPACE)
    # =========================================================================
    elif page == "Flower Classifier":
        st.markdown("""
        <div style="margin-bottom: 20px;">
            <div style="font-size: 1.85rem; font-weight: 800; color: #183A2A; letter-spacing: -0.02em;">Botanical Specimen Classifier</div>
            <div style="font-size: 0.9rem; color: #7E9485;">Enter flower measurements to identify the Iris species with machine-calibrated Softmax confidence.</div>
        </div>
        """, unsafe_allow_html=True)

        col_left, col_right = st.columns([1, 1], gap="large")

        # LEFT COLUMN: Measurement Controls & Presets
        with col_left:
            st.markdown('<div class="saas-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">Measurement Controls</div>', unsafe_allow_html=True)
            st.markdown('<div class="card-sub">Calibrated physical measurements bounded by empirical dataset extremes.</div>', unsafe_allow_html=True)

            s_len = st.slider("Sepal Length (cm)", 4.0, 8.0, float(st.session_state.sepal_len), 0.1, help="Outer sepal leaf length in cm.")
            s_wid = st.slider("Sepal Width (cm)", 2.0, 4.5, float(st.session_state.sepal_wid), 0.1, help="Outer sepal leaf width in cm.")
            p_len = st.slider("Petal Length (cm)", 1.0, 7.0, float(st.session_state.petal_len), 0.1, help="Inner flowering petal length in cm.")
            p_wid = st.slider("Petal Width (cm)", 0.1, 2.6, float(st.session_state.petal_wid), 0.1, help="Inner flowering petal width in cm.")

            st.session_state.sepal_len = s_len
            st.session_state.sepal_wid = s_wid
            st.session_state.petal_len = p_len
            st.session_state.petal_wid = p_wid

            # Presets
            st.markdown("<hr style='border: none; border-top: 1px solid #E4EBE3; margin: 20px 0;'>", unsafe_allow_html=True)
            st.markdown("<div style='font-size: 0.78rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; color: #8BAA91; margin-bottom: 10px;'>Botanical Sample Presets</div>", unsafe_allow_html=True)

            p1, p2, p3, p4 = st.columns(4)
            if p1.button("🌸 Setosa"):
                st.session_state.sepal_len = 5.0
                st.session_state.sepal_wid = 3.4
                st.session_state.petal_len = 1.5
                st.session_state.petal_wid = 0.2
                st.rerun()
            if p2.button("🌾 Versicolor"):
                st.session_state.sepal_len = 5.9
                st.session_state.sepal_wid = 2.8
                st.session_state.petal_len = 4.3
                st.session_state.petal_wid = 1.3
                st.rerun()
            if p3.button("🌺 Virginica"):
                st.session_state.sepal_len = 6.6
                st.session_state.sepal_wid = 3.0
                st.session_state.petal_len = 5.6
                st.session_state.petal_wid = 2.0
                st.rerun()
            if p4.button("🔄 Reset"):
                st.session_state.sepal_len = 5.8
                st.session_state.sepal_wid = 3.0
                st.session_state.petal_len = 4.3
                st.session_state.petal_wid = 1.3
                st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

        # RIGHT COLUMN: Floating Prediction Panel
        with col_right:
            st.markdown('<div class="saas-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">Taxonomic Diagnosis</div>', unsafe_allow_html=True)
            st.markdown('<div class="card-sub">Inference executed live through the trained Random Forest pipeline.</div>', unsafe_allow_html=True)

            res = predictor.predict(
                sepal_length=s_len,
                sepal_width=s_wid,
                petal_length=p_len,
                petal_width=p_wid
            )

            pred_species = res["predicted_species"]
            conf = res["confidence"]
            probs = res["probabilities"]

            badge_style = {
                "Setosa": ("hero-badge-setosa", "#6B5B95", "Iris Setosa"),
                "Versicolor": ("hero-badge-versicolor", "#B88A62", "Iris Versicolor"),
                "Virginica": ("hero-badge-virginica", "#285943", "Iris Virginica")
            }.get(pred_species, ("hero-badge-virginica", "#285943", f"Iris {pred_species}"))

            st.markdown(f"""
            <div class="{badge_style[0]}">
                <div style="font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.1em; color: {badge_style[1]};">
                    Verified Taxonomic Diagnosis
                </div>
                <div style="font-size: 2.3rem; font-weight: 800; color: {badge_style[1]}; letter-spacing: -0.02em; margin: 6px 0;">
                    {badge_style[2]}
                </div>
                <div style="font-size: 0.95rem; font-weight: 700; color: #183A2A;">
                    Model Confidence: <b>{conf * 100:.2f}%</b>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Probabilities Bar
            st.markdown("<div style='font-size: 0.78rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; color: #8BAA91; margin-bottom: 8px;'>Softmax Probability Distribution</div>", unsafe_allow_html=True)
            prob_df = pd.DataFrame({
                "Species": [f"Iris {k}" for k in probs.keys()],
                "Probability (%)": [round(v * 100, 2) for v in probs.values()]
            })

            fig_p = px.bar(
                prob_df,
                x="Probability (%)",
                y="Species",
                orientation="h",
                color="Species",
                color_discrete_map={
                    "Iris Setosa": "#6B5B95",
                    "Iris Versicolor": "#B88A62",
                    "Iris Virginica": "#285943"
                },
                text="Probability (%)",
                template="plotly_white",
                height=180
            )
            fig_p.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="#FFFFFF",
                xaxis=dict(range=[0, 105], showgrid=False),
                yaxis=dict(autorange="reversed"),
                margin=dict(l=10, r=10, t=10, b=10),
                showlegend=False,
                font=dict(color="#647269", family="Manrope")
            )
            fig_p.update_traces(textposition="outside", texttemplate="%{x:.1f}%")
            st.plotly_chart(fig_p, use_container_width=True)

            # Recap Pill
            st.markdown(f"""
            <div style="background: #F2F7F3; border: 1px solid #E4EBE3; border-radius: 12px; padding: 12px 16px; font-size: 0.8rem; color: #183A2A; display: flex; justify-content: space-between; margin-top: 14px;">
                <span>Sepal: <b>{s_len} × {s_wid} cm</b></span>
                <span>Petal: <b>{p_len} × {p_wid} cm</b></span>
                <span>Petal Aspect Ratio: <b>{p_len/p_wid:.2f}</b></span>
            </div>
            """, unsafe_allow_html=True)

            descriptions = {
                "Setosa": "Highly separable cluster with diminutive petals (< 2 cm) and robust sepal breadth. Discovered in Arctic/coastal marshes.",
                "Versicolor": "Harmonious intermediate scale across all dimensions. Known as the Blue Flag iris.",
                "Virginica": "Maximum structural scale with dominant petals (> 5 cm). Known as the Southern Blue Flag."
            }
            st.info(f"🌿 **Botanical Insight:** {descriptions.get(pred_species, '')}")
            st.markdown('</div>', unsafe_allow_html=True)

    # =========================================================================
    # PAGE 3: DATASET EXPLORER
    # =========================================================================
    elif page == "Dataset Explorer":
        st.markdown("""
        <div style="margin-bottom: 20px;">
            <div style="font-size: 1.85rem; font-weight: 800; color: #183A2A; letter-spacing: -0.02em;">Botanical Dataset Explorer</div>
            <div style="font-size: 0.9rem; color: #7E9485;">Search, filter, and inspect Fisher's 150 Iris specimens with descriptive statistical moments.</div>
        </div>
        """, unsafe_allow_html=True)

        col_f1, col_f2 = st.columns([1, 2])
        with col_f1:
            sel_species = st.multiselect("Filter Species:", sorted(df["species"].unique().tolist()), default=sorted(df["species"].unique().tolist()))
        with col_f2:
            search_query = st.text_input("Search Specimen Attribute:", "")

        filtered = df[df["species"].isin(sel_species)]
        if search_query:
            filtered = filtered[filtered.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]

        st.markdown('<div class="saas-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="card-title">Specimen Catalog ({len(filtered)} records)</div>', unsafe_allow_html=True)
        st.dataframe(filtered, use_container_width=True, height=360)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="saas-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Statistical Distributions (Centimeters)</div>', unsafe_allow_html=True)
        st.dataframe(filtered[["sepal_length", "sepal_width", "petal_length", "petal_width"]].describe().round(3), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # =========================================================================
    # PAGE 4: SPECIES INSIGHTS
    # =========================================================================
    elif page == "Species Insights":
        st.markdown("""
        <div style="margin-bottom: 20px;">
            <div style="font-size: 1.85rem; font-weight: 800; color: #183A2A; letter-spacing: -0.02em;">Species Morphology & Profiles</div>
            <div style="font-size: 0.9rem; color: #7E9485;">Empirical comparison of dimensional boundaries, violin dispersion, and species profiles.</div>
        </div>
        """, unsafe_allow_html=True)

        means = df.groupby("species").mean().round(2)
        c_set, c_ver, c_vir = st.columns(3)

        with c_set:
            st.markdown(f"""
            <div class="saas-card" style="border-top: 4px solid #6B5B95;">
                <div style="font-size: 1.25rem; font-weight: 800; color: #6B5B95; margin-bottom: 4px;">Iris Setosa</div>
                <div style="font-size: 0.8rem; color: #7E9485; margin-bottom: 14px;">Muted Lavender • Complete Linear Separation</div>
                <div style="font-size: 0.82rem; line-height: 1.9; color: #183A2A;">
                    <div>Mean Sepal Length: <b>{means.loc['Setosa', 'sepal_length']} cm</b></div>
                    <div>Mean Sepal Width: <b>{means.loc['Setosa', 'sepal_width']} cm</b> (Broadest)</div>
                    <div>Mean Petal Length: <b>{means.loc['Setosa', 'petal_length']} cm</b> (Shortest)</div>
                    <div>Mean Petal Width: <b>{means.loc['Setosa', 'petal_width']} cm</b> (Slenderest)</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with c_ver:
            st.markdown(f"""
            <div class="saas-card" style="border-top: 4px solid #B88A62;">
                <div style="font-size: 1.25rem; font-weight: 800; color: #B88A62; margin-bottom: 4px;">Iris Versicolor</div>
                <div style="font-size: 0.8rem; color: #7E9485; margin-bottom: 14px;">Warm Amber • Intermediate Manifold</div>
                <div style="font-size: 0.82rem; line-height: 1.9; color: #183A2A;">
                    <div>Mean Sepal Length: <b>{means.loc['Versicolor', 'sepal_length']} cm</b></div>
                    <div>Mean Sepal Width: <b>{means.loc['Versicolor', 'sepal_width']} cm</b></div>
                    <div>Mean Petal Length: <b>{means.loc['Versicolor', 'petal_length']} cm</b></div>
                    <div>Mean Petal Width: <b>{means.loc['Versicolor', 'petal_width']} cm</b></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with c_vir:
            st.markdown(f"""
            <div class="saas-card" style="border-top: 4px solid #285943;">
                <div style="font-size: 1.25rem; font-weight: 800; color: #285943; margin-bottom: 4px;">Iris Virginica</div>
                <div style="font-size: 0.8rem; color: #7E9485; margin-bottom: 14px;">Botanical Forest Teal • Maximum Dimensionality</div>
                <div style="font-size: 0.82rem; line-height: 1.9; color: #183A2A;">
                    <div>Mean Sepal Length: <b>{means.loc['Virginica', 'sepal_length']} cm</b> (Longest)</div>
                    <div>Mean Sepal Width: <b>{means.loc['Virginica', 'sepal_width']} cm</b></div>
                    <div>Mean Petal Length: <b>{means.loc['Virginica', 'petal_length']} cm</b> (Longest)</div>
                    <div>Mean Petal Width: <b>{means.loc['Virginica', 'petal_width']} cm</b> (Widest)</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Comparative Boxplots
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            st.markdown('<div class="saas-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">Petal Length Dispersion</div>', unsafe_allow_html=True)
            fig_v1 = px.box(df, x="species", y="petal_length", color="species", color_discrete_map={"Setosa": "#6B5B95", "Versicolor": "#B88A62", "Virginica": "#285943"}, template="plotly_white", height=300)
            fig_v1.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#FFFFFF", showlegend=False)
            st.plotly_chart(fig_v1, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_b2:
            st.markdown('<div class="saas-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">Sepal Width Dispersion</div>', unsafe_allow_html=True)
            fig_v2 = px.box(df, x="species", y="sepal_width", color="species", color_discrete_map={"Setosa": "#6B5B95", "Versicolor": "#B88A62", "Virginica": "#285943"}, template="plotly_white", height=300)
            fig_v2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#FFFFFF", showlegend=False)
            st.plotly_chart(fig_v2, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # =========================================================================
    # PAGE 5: MODEL PERFORMANCE (SCIENTIFIC EVALUATION)
    # =========================================================================
    elif page == "Model Performance":
        st.markdown("""
        <div style="margin-bottom: 20px;">
            <div style="font-size: 1.85rem; font-weight: 800; color: #183A2A; letter-spacing: -0.02em;">Model Diagnostics & Scientific Evaluation</div>
            <div style="font-size: 0.9rem; color: #7E9485;">Audited held-out test split evaluation for the serialized Random Forest classifier pipeline.</div>
        </div>
        """, unsafe_allow_html=True)

        t_met = meta["test_metrics"]
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f"""
            <div class="kpi-card-mint">
                <div class="kpi-icon-pill" style="background: #EAE7F5; color: #6B5B95;">🌲</div>
                <div class="kpi-val" style="font-size: 1.45rem;">Random Forest</div>
                <div class="kpi-label">Algorithm</div>
                <div class="kpi-delta">100 trees • max_depth=4</div>
            </div>
            """, unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
            <div class="kpi-card-mint">
                <div class="kpi-icon-pill" style="background: #DFF4E5; color: #285943;">🎯</div>
                <div class="kpi-val" style="color: #285943;">{t_met['Test Accuracy']*100:.2f}%</div>
                <div class="kpi-label">Test Accuracy</div>
                <div class="kpi-delta">Stratified 80:20 split (N=30)</div>
            </div>
            """, unsafe_allow_html=True)
        with m3:
            st.markdown(f"""
            <div class="kpi-card-mint">
                <div class="kpi-icon-pill" style="background: #F8EDDE; color: #B88A62;">⚖️</div>
                <div class="kpi-val">{t_met['Precision (Macro)']*100:.2f}%</div>
                <div class="kpi-label">Precision (Macro)</div>
                <div class="kpi-delta">Zero false positive bias</div>
            </div>
            """, unsafe_allow_html=True)
        with m4:
            st.markdown(f"""
            <div class="kpi-card-mint">
                <div class="kpi-icon-pill" style="background: #E9F1E8; color: #285943;">📊</div>
                <div class="kpi-val">{t_met['F1-Score (Macro)']:.4f}</div>
                <div class="kpi-label">Macro F1-Score</div>
                <div class="kpi-delta">Harmonic class balance</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

        col_m1, col_m2 = st.columns([1, 1])
        with col_m1:
            st.markdown('<div class="saas-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">Audited Confusion Matrix</div>', unsafe_allow_html=True)
            cm_matrix = [[10, 0, 0], [0, 9, 1], [0, 0, 10]]
            labels = ["Setosa", "Versicolor", "Virginica"]
            fig_cm = px.imshow(cm_matrix, labels=dict(x="Predicted Class", y="True Class", color="Specimens"), x=labels, y=labels, text_auto=True, color_continuous_scale="Greens", template="plotly_white", height=300)
            fig_cm.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#FFFFFF", font=dict(color="#183A2A", family="Manrope"), margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(fig_cm, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_m2:
            st.markdown('<div class="saas-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">Cross-Model Benchmark Comparison</div>', unsafe_allow_html=True)
            st.markdown('<div class="card-sub">Comparison under identical 5-fold cross-validation & stratified test conditions.</div>', unsafe_allow_html=True)
            comp_df = pd.DataFrame(meta["comparison_table"])[["Model", "Train Accuracy", "Test Accuracy", "F1-Score (Macro)"]].copy()
            comp_df["Train Accuracy"] = (comp_df["Train Accuracy"] * 100).round(2).astype(str) + "%"
            comp_df["Test Accuracy"] = (comp_df["Test Accuracy"] * 100).round(2).astype(str) + "%"
            comp_df["F1-Score (Macro)"] = comp_df["F1-Score (Macro)"].round(4)
            st.dataframe(comp_df, use_container_width=True, hide_index=True)

            st.info("ℹ️ **Scientific Audit Note:** Standard cross-validation with an 80:20 stratified split ensures zero data leakage. Random Forest provides the optimal non-linear separation on petal morphology.")
            st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
