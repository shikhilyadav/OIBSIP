"""
app.py
======
Interactive Streamlit Web Application for Iris Flower Classification.
Oasis Infobyte Data Science Task 1.
"""

import os
import sys
import streamlit as st
import pandas as pd
import numpy as np

# Ensure src directory is in Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from predict import IrisPredictor

# Page Configuration
st.set_page_config(
    page_title="Iris Species Predictor | Oasis Infobyte",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.3rem;
        font-weight: 800;
        color: #1e3a8a;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4b5563;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #f8fafc;
        border-radius: 10px;
        padding: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
    }
    .prediction-badge {
        font-size: 1.8rem;
        font-weight: bold;
        padding: 10px 20px;
        border-radius: 8px;
        text-align: center;
        margin: 15px 0;
    }
    .badge-setosa {
        background-color: #e0f2fe;
        color: #0369a1;
        border: 2px solid #38bdf8;
    }
    .badge-versicolor {
        background-color: #dcfce7;
        color: #15803d;
        border: 2px solid #4ade80;
    }
    .badge-virginica {
        background-color: #fee2e2;
        color: #b91c1c;
        border: 2px solid #f87171;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_predictor():
    """Caches the model predictor instance for fast inference."""
    return IrisPredictor()


def main():
    st.markdown('<div class="main-header">🌸 Iris Flower Species Classifier</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">OASIS INFOBYTE Data Science Internship | Task 1 Machine Learning System</div>', unsafe_allow_html=True)

    try:
        predictor = get_predictor()
    except Exception as e:
        st.error(f"Error loading model: {e}")
        st.info("Please run `python src/train.py` to generate and save the model artifact before launching the web app.")
        return

    # Sidebar: Input Controls and Presets
    st.sidebar.header("🔍 Flower Measurement Inputs")
    st.sidebar.markdown("Provide sepal and petal dimensions in centimeters.")

    # Preset Quick-select
    st.sidebar.subheader("Quick Presets")
    preset = st.sidebar.selectbox(
        "Load sample botanical measurements:",
        ("Custom Input", "Iris Setosa (Typical)", "Iris Versicolor (Typical)", "Iris Virginica (Typical)")
    )

    # Defaults according to preset
    if preset == "Iris Setosa (Typical)":
        d_sl, d_sw, d_pl, d_pw = 5.1, 3.5, 1.4, 0.2
    elif preset == "Iris Versicolor (Typical)":
        d_sl, d_sw, d_pl, d_pw = 5.9, 2.8, 4.2, 1.3
    elif preset == "Iris Virginica (Typical)":
        d_sl, d_sw, d_pl, d_pw = 6.5, 3.0, 5.5, 2.0
    else:
        d_sl, d_sw, d_pl, d_pw = 5.8, 3.0, 4.3, 1.3

    col1, col2 = st.sidebar.columns(2)
    with col1:
        sepal_length = st.number_input("Sepal Length (cm)", min_value=1.0, max_value=10.0, value=d_sl, step=0.1)
        petal_length = st.number_input("Petal Length (cm)", min_value=0.5, max_value=10.0, value=d_pl, step=0.1)
    with col2:
        sepal_width = st.number_input("Sepal Width (cm)", min_value=1.0, max_value=6.0, value=d_sw, step=0.1)
        petal_width = st.number_input("Petal Width (cm)", min_value=0.1, max_value=5.0, value=d_pw, step=0.1)

    predict_btn = st.sidebar.button("🌸 Predict Iris Species", type="primary", use_container_width=True)

    # Main Interface Layout: 2 Columns
    left_col, right_col = st.columns([1.1, 0.9])

    with left_col:
        st.subheader("Prediction Dashboard")

        # Execute Prediction
        result = predictor.predict(
            sepal_length=sepal_length,
            sepal_width=sepal_width,
            petal_length=petal_length,
            petal_width=petal_width
        )

        pred_species = result["predicted_species"]
        confidence = result["confidence"]
        probs = result["probabilities"]

        # Species Badge Styling
        badge_class = f"badge-{pred_species.lower()}"
        st.markdown(
            f'<div class="prediction-badge {badge_class}">Predicted: Iris {pred_species}</div>',
            unsafe_allow_html=True
        )

        # Confidence and Model Metrics
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Model Confidence", f"{confidence * 100:.1f}%")
        with m2:
            st.metric("Algorithm", predictor.model_name)
        with m3:
            test_acc = predictor.metrics.get("Test Accuracy", 1.0)
            st.metric("Model Test Accuracy", f"{test_acc * 100:.1f}%")

        # Probability Distribution Bar Chart
        st.markdown("#### Prediction Probability Distribution")
        prob_df = pd.DataFrame({
            "Species": list(probs.keys()),
            "Probability": [v * 100 for v in probs.values()]
        })

        st.bar_chart(
            data=prob_df.set_index("Species"),
            y="Probability",
            color="#2563eb",
            use_container_width=True
        )

        # Botanical Profile Card
        st.markdown("#### Botanical Morphological Profile")
        if pred_species == "Setosa":
            st.info("""
            **Iris Setosa Profile:**
            - Petals are characteristically short and narrow (< 2 cm).
            - Sepals are prominently wide relative to petal dimensions.
            - Easily separable linearly from all other species with 100% boundary margin.
            """)
        elif pred_species == "Versicolor":
            st.success("""
            **Iris Versicolor Profile:**
            - Intermediate petal dimensions (lengths ~3.0 - 5.1 cm, widths ~1.0 - 1.8 cm).
            - Slender sepal width compared to Setosa.
            - Represents the evolutionary medium between Setosa and Virginica.
            """)
        else:
            st.error("""
            **Iris Virginica Profile:**
            - Large, prominent floral dimensions (petals > 4.5 cm, widths > 1.4 cm).
            - Robust sepal structure with the highest overall floral biomass.
            - Exhibits subtle boundary overlap with Versicolor in extreme edge cases.
            """)

    with right_col:
        st.subheader("Model & Feature Intelligence")

        # Tabbed Details
        tab1, tab2, tab3 = st.tabs(["📊 Input Summary", "🧠 Model Architecture", "🌿 Key Observations"])

        with tab1:
            st.markdown("**User Provided Feature Vector:**")
            feat_summary = pd.DataFrame({
                "Feature Name": ["Sepal Length", "Sepal Width", "Petal Length", "Petal Width"],
                "Input Value (cm)": [sepal_length, sepal_width, petal_length, petal_width],
                "Dataset Mean (cm)": [5.84, 3.05, 3.76, 1.20]
            })
            st.dataframe(feat_summary, hide_index=True, use_container_width=True)

        with tab2:
            st.markdown(f"**Selected Model:** `{predictor.model_name}`")
            st.markdown("""
            **Model Highlights:**
            - **Stratified Split:** 80% Training (120 samples), 20% Testing (30 samples).
            - **Preprocessing:** Scikit-learn `StandardScaler` inside `Pipeline` to prevent data leakage.
            - **Persistence:** Serialized with `joblib` bundle containing model, feature metadata, and class labels.
            """)
            if predictor.metrics:
                st.markdown("**Test Set Evaluation Metrics:**")
                st.json(predictor.metrics)

        with tab3:
            st.markdown("""
            **Why Petal Features are Key Discriminators:**
            1. **Petal Length & Petal Width** have a Pearson correlation of **0.963**.
            2. Setosa petal lengths (1.0 - 1.9 cm) have **zero overlap** with other classes.
            3. Together, petal dimensions yield near-orthogonal boundaries for high-confidence classification.
            """)


if __name__ == "__main__":
    main()
