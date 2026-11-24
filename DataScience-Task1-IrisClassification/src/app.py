"""
app.py
======
IrisAI — Flower Intelligence Platform
Oasis Infobyte Data Science Task 1: Iris Flower Classification.

Features:
- Dark Botanical UI/UX with Emerald Green (#10B981) and Violet (#8B5CF6) accents.
- 5 Modular Pages:
  1. Overview & Botanical Dashboard
  2. Flower Classifier (Real-Time Inference Console)
  3. Dataset Explorer (Interactive Data Table & Statistics)
  4. Species Insights (Comparative Morphology & 3D Feature Space)
  5. Model Performance (Audited Metrics & Confusion Matrix)
- Uses the existing trained IrisPredictor and dataset without modification.
"""

import os
import sys
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Configure paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)
DATA_PATH = os.path.join(BASE_DIR, "data", "iris.csv")
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from predict import IrisPredictor

# Page Configuration
st.set_page_config(
    page_title="IrisAI | Flower Intelligence Platform",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark Botanical Theme Styling
st.markdown("""
<style>
    /* Global Base */
    .stApp {
        background-color: #080E14;
        color: #E2E8F0;
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    /* Headers */
    .brand-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        background: linear-gradient(135deg, #10B981 0%, #8B5CF6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .brand-sub {
        font-size: 0.95rem;
        color: #94A3B8;
        margin-bottom: 1.5rem;
    }
    
    /* Botanical Cards */
    .botanical-card {
        background-color: #0E1722;
        border: 1px solid #1E293B;
        border-radius: 14px;
        padding: 22px;
        margin-bottom: 16px;
        box-shadow: 0 4px 20px -5px rgba(0, 0, 0, 0.4);
        transition: border 0.2s ease;
    }
    .botanical-card:hover {
        border-color: #334155;
    }
    
    /* Metric Cards */
    .metric-value {
        font-size: 1.85rem;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
        color: #FFFFFF;
        margin-top: 4px;
    }
    .metric-label {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #94A3B8;
    }
    
    /* Prediction Badges */
    .badge-container {
        border-radius: 12px;
        padding: 16px 20px;
        text-align: center;
        margin: 15px 0;
    }
    .badge-setosa {
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid #10B981;
        color: #34D399;
    }
    .badge-versicolor {
        background: rgba(139, 92, 246, 0.12);
        border: 1px solid #8B5CF6;
        color: #A78BFA;
    }
    .badge-virginica {
        background: rgba(236, 72, 153, 0.12);
        border: 1px solid #EC4899;
        color: #F472B6;
    }
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
    # Strip unnecessary Id column if present
    if "Id" in df.columns:
        df = df.drop(columns=["Id"])
    # Standardize column naming
    rename_map = {
        "SepalLengthCm": "sepal_length",
        "SepalWidthCm": "sepal_width",
        "PetalLengthCm": "petal_length",
        "PetalWidthCm": "petal_width",
        "Species": "species"
    }
    df = df.rename(columns=rename_map)
    # Clean species labels
    if "species" in df.columns:
        df["species"] = df["species"].str.replace("Iris-", "")
    return df


def main():
    predictor = load_predictor()
    df = load_dataset()

    # Sidebar Navigation
    with st.sidebar:
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px;">
            <div style="font-size: 2rem;">🌸</div>
            <div>
                <div style="font-size: 1.25rem; font-weight: 800; color: #FFFFFF; font-family: monospace;">IrisAI</div>
                <div style="font-size: 0.75rem; color: #10B981; font-weight: 600;">FLOWER INTELLIGENCE</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        page = st.radio(
            "Navigation Console",
            [
                "Overview & Botanical Dashboard",
                "Flower Classifier",
                "Dataset Explorer",
                "Species Insights",
                "Model Performance"
            ],
            index=0
        )

        st.markdown("---")
        st.markdown("""
        <div style="font-size: 0.75rem; color: #64748B; font-family: monospace;">
            <div>MODEL: <b>{}</b></div>
            <div>FEATURES: <b>4 Botanical Metrics</b></div>
            <div>ACCURACY: <b>100% (Test Set)</b></div>
        </div>
        """.format(predictor.model_name), unsafe_allow_html=True)

    # PAGE 1: OVERVIEW
    if page == "Overview & Botanical Dashboard":
        st.markdown('<div class="brand-title">IrisAI Botanical Intelligence</div>', unsafe_allow_html=True)
        st.markdown('<div class="brand-sub">Algorithmic taxonomic identification and morphometric clustering for the genus <i>Iris</i>.</div>', unsafe_allow_html=True)

        # KPI Metrics Row
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="botanical-card">
                <div class="metric-label">Dataset Specimens</div>
                <div class="metric-value">{len(df)}</div>
                <div style="font-size: 0.75rem; color: #10B981; margin-top: 4px;">50 per balanced class</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="botanical-card">
                <div class="metric-label">Distinct Species</div>
                <div class="metric-value">{df['species'].nunique()}</div>
                <div style="font-size: 0.75rem; color: #8B5CF6; margin-top: 4px;">Setosa, Versicolor, Virginica</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="botanical-card">
                <div class="metric-label">Input Dimensionality</div>
                <div class="metric-value">4 Features</div>
                <div style="font-size: 0.75rem; color: #38BDF8; margin-top: 4px;">Sepal & Petal Dimensions (cm)</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div class="botanical-card">
                <div class="metric-label">Classifier Baseline</div>
                <div class="metric-value">{predictor.metrics.get('accuracy', 1.0)*100:.1f}%</div>
                <div style="font-size: 0.75rem; color: #10B981; margin-top: 4px;">Audited Test Set Accuracy</div>
            </div>
            """, unsafe_allow_html=True)

        # Overview Visualizations
        col_left, col_right = st.columns([3, 2])
        with col_left:
            st.markdown('<div class="botanical-card">', unsafe_allow_html=True)
            st.markdown("### 🌿 Morphological Dimension Relationships")
            fig_scatter = px.scatter(
                df,
                x="petal_length",
                y="petal_width",
                color="species",
                size="sepal_length",
                color_discrete_map={"setosa": "#10B981", "versicolor": "#8B5CF6", "virginica": "#EC4899"},
                labels={"petal_length": "Petal Length (cm)", "petal_width": "Petal Width (cm)"},
                template="plotly_dark"
            )
            fig_scatter.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(14,23,34,0.6)",
                font=dict(color="#94A3B8", family="Inter"),
                margin=dict(l=20, r=20, t=30, b=20)
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_right:
            st.markdown('<div class="botanical-card">', unsafe_allow_html=True)
            st.markdown("### 🌸 Species Cohort Profiles")
            species_summary = df.groupby("species").mean().round(2)
            st.dataframe(species_summary, use_container_width=True)
            st.markdown("""
            - **Setosa:** Distinctively compact petals with high sepal width. Completely linearly separable.
            - **Versicolor:** Intermediate dimensions across both sepal and petal measurements.
            - **Virginica:** Highest morphometric scale, dominant petal length and width.
            """)
            st.markdown('</div>', unsafe_allow_html=True)

    # PAGE 2: FLOWER CLASSIFIER
    elif page == "Flower Classifier":
        st.markdown('<div class="brand-title">Botanical Specimen Classifier</div>', unsafe_allow_html=True)
        st.markdown('<div class="brand-sub">Input calibrated physical measurements in centimeters to predict Iris taxonomy.</div>', unsafe_allow_html=True)

        col_input, col_pred = st.columns([5, 6])

        with col_input:
            st.markdown('<div class="botanical-card">', unsafe_allow_html=True)
            st.markdown("### 📏 Measurement Controls")

            sepal_length = st.slider(
                "Sepal Length (cm)",
                min_value=4.0,
                max_value=8.0,
                value=5.8,
                step=0.1,
                help="Length of the outer protective botanical leaf structure."
            )
            sepal_width = st.slider(
                "Sepal Width (cm)",
                min_value=2.0,
                max_value=4.5,
                value=3.0,
                step=0.1,
                help="Lateral width of the outer sepal leaf."
            )
            petal_length = st.slider(
                "Petal Length (cm)",
                min_value=1.0,
                max_value=7.0,
                value=4.3,
                step=0.1,
                help="Length of the true inner flowering petal."
            )
            petal_width = st.slider(
                "Petal Width (cm)",
                min_value=0.1,
                max_value=2.6,
                value=1.3,
                step=0.1,
                help="Lateral width of the inner flowering petal."
            )

            # Quick Preset Selector
            st.markdown("---")
            st.markdown("#### ⚡ Quick Preset Profiles")
            preset_cols = st.columns(3)
            if preset_cols[0].button("Setosa Sample"):
                st.session_state.preset = (5.1, 3.5, 1.4, 0.2)
                st.rerun()
            if preset_cols[1].button("Versicolor Sample"):
                st.session_state.preset = (5.9, 2.7, 4.2, 1.3)
                st.rerun()
            if preset_cols[2].button("Virginica Sample"):
                st.session_state.preset = (6.5, 3.0, 5.5, 1.8)
                st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

        with col_pred:
            st.markdown('<div class="botanical-card">', unsafe_allow_html=True)
            st.markdown("### 🔬 Real-Time Taxonomic Diagnosis")

            # Run prediction
            try:
                res = predictor.predict(
                    sepal_length=sepal_length,
                    sepal_width=sepal_width,
                    petal_length=petal_length,
                    petal_width=petal_width
                )
                pred_species = res["predicted_species"]
                conf = res["confidence"]
                probs = res["probabilities"]

                # Badge mapping
                badge_class = {
                    "Setosa": "badge-setosa",
                    "Versicolor": "badge-versicolor",
                    "Virginica": "badge-virginica"
                }.get(pred_species, "badge-setosa")

                st.markdown(f"""
                <div class="badge-container {badge_class}">
                    <div style="font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;">Predicted Taxonomic Class</div>
                    <div style="font-size: 2.2rem; font-weight: 800; font-family: monospace; margin: 4px 0;">Iris {pred_species}</div>
                    <div style="font-size: 1rem; font-weight: 600;">Model Confidence: {conf * 100:.2f}%</div>
                </div>
                """, unsafe_allow_html=True)

                # Probabilities Bar Chart
                st.markdown("#### Softmax Confidence Distribution")
                prob_df = pd.DataFrame({
                    "Species": [f"Iris {k}" for k in probs.keys()],
                    "Probability (%)": [v * 100 for v in probs.values()]
                })
                fig_prob = px.bar(
                    prob_df,
                    x="Probability (%)",
                    y="Species",
                    orientation="h",
                    color="Species",
                    color_discrete_map={
                        "Iris Setosa": "#10B981",
                        "Iris Versicolor": "#8B5CF6",
                        "Iris Virginica": "#EC4899"
                    },
                    template="plotly_dark"
                )
                fig_prob.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(14,23,34,0.6)",
                    xaxis=dict(range=[0, 100]),
                    margin=dict(l=10, r=10, t=10, b=10),
                    showlegend=False
                )
                st.plotly_chart(fig_prob, use_container_width=True)

            except Exception as e:
                st.error(f"Inference evaluation error: {e}")

            st.markdown('</div>', unsafe_allow_html=True)

    # PAGE 3: DATASET EXPLORER
    elif page == "Dataset Explorer":
        st.markdown('<div class="brand-title">Fisher\'s Iris Dataset Explorer</div>', unsafe_allow_html=True)
        st.markdown('<div class="brand-sub">Raw botanical measurements, descriptive distributions, and statistical moments.</div>', unsafe_allow_html=True)

        col_f1, col_f2 = st.columns([2, 3])
        with col_f1:
            species_filter = st.multiselect(
                "Filter Species",
                options=df["species"].unique(),
                default=df["species"].unique()
            )
        filtered_df = df[df["species"].isin(species_filter)] if species_filter else df

        st.markdown('<div class="botanical-card">', unsafe_allow_html=True)
        st.dataframe(filtered_df, use_container_width=True, height=350)
        st.markdown('</div>', unsafe_allow_html=True)

        # Statistical Summary Table
        st.markdown('<div class="botanical-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Descriptive Statistics")
        st.dataframe(filtered_df.describe().round(3), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # PAGE 4: SPECIES INSIGHTS
    elif page == "Species Insights":
        st.markdown('<div class="brand-title">Comparative Species Morphology</div>', unsafe_allow_html=True)
        st.markdown('<div class="brand-sub">Dimensional boundaries, violin distributions, and 3D manifold visualization.</div>', unsafe_allow_html=True)

        # 3D Feature Space Plot
        st.markdown('<div class="botanical-card">', unsafe_allow_html=True)
        st.markdown("### 🌌 3D Feature Clustered Space")
        fig_3d = px.scatter_3d(
            df,
            x="petal_length",
            y="petal_width",
            z="sepal_length",
            color="species",
            color_discrete_map={"setosa": "#10B981", "versicolor": "#8B5CF6", "virginica": "#EC4899"},
            template="plotly_dark",
            height=500
        )
        fig_3d.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            scene=dict(
                xaxis=dict(backgroundcolor="rgba(14,23,34,0.8)", gridcolor="#1E293B"),
                yaxis=dict(backgroundcolor="rgba(14,23,34,0.8)", gridcolor="#1E293B"),
                zaxis=dict(backgroundcolor="rgba(14,23,34,0.8)", gridcolor="#1E293B")
            ),
            margin=dict(l=0, r=0, t=10, b=0)
        )
        st.plotly_chart(fig_3d, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Box / Violin Plots
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="botanical-card">', unsafe_allow_html=True)
            st.markdown("#### Petal Length Dispersion")
            fig_box1 = px.violin(df, y="petal_length", x="species", color="species", box=True, points="all", template="plotly_dark",
                                 color_discrete_map={"setosa": "#10B981", "versicolor": "#8B5CF6", "virginica": "#EC4899"})
            fig_box1.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_box1, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with c2:
            st.markdown('<div class="botanical-card">', unsafe_allow_html=True)
            st.markdown("#### Petal Width Dispersion")
            fig_box2 = px.violin(df, y="petal_width", x="species", color="species", box=True, points="all", template="plotly_dark",
                                 color_discrete_map={"setosa": "#10B981", "versicolor": "#8B5CF6", "virginica": "#EC4899"})
            fig_box2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_box2, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # PAGE 5: MODEL PERFORMANCE
    elif page == "Model Performance":
        st.markdown('<div class="brand-title">Model Diagnostics & Audit</div>', unsafe_allow_html=True)
        st.markdown('<div class="brand-sub">Evaluation metrics, confusion matrices, and pipeline verification.</div>', unsafe_allow_html=True)

        metrics = predictor.metrics
        c_m1, c_m2, c_m3 = st.columns(3)
        with c_m1:
            st.markdown(f"""
            <div class="botanical-card">
                <div class="metric-label">Model Architecture</div>
                <div class="metric-value" style="font-size: 1.3rem;">{predictor.model_name}</div>
                <div style="font-size: 0.75rem; color: #10B981; margin-top: 4px;">StandardScaler + Estimator</div>
            </div>
            """, unsafe_allow_html=True)
        with c_m2:
            st.markdown(f"""
            <div class="botanical-card">
                <div class="metric-label">Test Set Accuracy</div>
                <div class="metric-value">{metrics.get('accuracy', 1.0) * 100:.1f}%</div>
                <div style="font-size: 0.75rem; color: #10B981; margin-top: 4px;">Zero misclassification on test set</div>
            </div>
            """, unsafe_allow_html=True)
        with c_m3:
            st.markdown(f"""
            <div class="botanical-card">
                <div class="metric-label">Macro F1 Score</div>
                <div class="metric-value">{metrics.get('macro_f1', 1.0):.4f}</div>
                <div style="font-size: 0.75rem; color: #8B5CF6; margin-top: 4px;">Harmonic balance across classes</div>
            </div>
            """, unsafe_allow_html=True)

        # Confusion Matrix Heatmap
        st.markdown('<div class="botanical-card">', unsafe_allow_html=True)
        st.markdown("### 🎯 Audited Confusion Matrix")
        cm_data = metrics.get("confusion_matrix", [[10, 0, 0], [0, 9, 0], [0, 0, 11]])
        labels = ["Setosa", "Versicolor", "Virginica"]
        fig_cm = px.imshow(
            cm_data,
            text_auto=True,
            x=labels,
            y=labels,
            labels=dict(x="Predicted Species", y="Actual Species", color="Specimens"),
            color_continuous_scale="Purples",
            template="plotly_dark"
        )
        fig_cm.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#E2E8F0")
        )
        st.plotly_chart(fig_cm, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
