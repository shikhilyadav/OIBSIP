# 🌿 IrisAI — Botanical Intelligence Studio
> **Where Nature Meets Intelligence.**  
> *OASIS INFOBYTE Data Science Internship (OIBSIP) — Task 1: Iris Flower Classification*

---

## 📌 Executive Overview

**IrisAI Botanical Intelligence Studio** is a premier machine learning SaaS application engineered with a **React + TypeScript + Tailwind CSS** frontend and a high-performance **FastAPI** backend adapter. Built using modern design references (Urban Bloom, laboratory surveillance consoles, and botanical SaaS dashboards), IrisAI delivers real-time taxonomic classification, interactive morphometric charts, specimen exploration, and scientific model performance tracking.

All original Task 1 artifacts—including the pre-trained `best_iris_model.joblib`, the 150-sample dataset, historical evaluation metrics, notebooks, and the legacy Streamlit application (`src/app.py`)—are **strictly preserved without modification**.

---

## 🏛️ System Architecture

```
                  IrisAI React Frontend (Vite + TypeScript + Tailwind)
                                        │
                                        │ HTTP REST (Port 3001)
                                        ▼
                         IrisAI FastAPI Backend Adapter (Port 8000)
                                        │
                         ┌──────────────┴──────────────┐
                         ▼                             ▼
              Random Forest Pipeline           Fisher's Iris Dataset
           (best_iris_model.joblib)                 (iris.csv)
```

---

## 🌸 Visual Reference Design Language

- **Canvas Palette:** `#F1F6F2` soft mint canvas, `#FFFFFF` crisp white floating cards, `#E3EBE3` organic borders.
- **Botanical Accents:** `#285943` Forest Green, `#5C9A72` Sage, `#DFF4E5` Soft Mint, `#19362A` Deep Organic Charcoal.
- **Species Color Identity:**
  - **Setosa:** `#76649D` (Muted Lavender)
  - **Versicolor:** `#C18E61` (Warm Amber)
  - **Virginica:** `#2C6A50` (Botanical Forest Teal)
- **Typography:** Manrope & Inter for high editorial readability.

---

## 📱 Five Integrated Application Views

1. **Overview & Botanical Dashboard:**
   - Visual botanical hero banner: *"Where Nature Meets Intelligence"*.
   - 4 floating pastel KPI telemetry cards (Dataset Specimens, Distinct Species, Input Dimensions, Audited Accuracy).
   - Petal Length vs. Petal Width scatter chart demonstrating orthogonal separability.
   - Species cohort balance donut chart and empirical baseline means table.

2. **Flower Classifier (Two-Column Interactive Console):**
   - Left Panel: Continuous sliders bounded by empirical coordinates with **quick preset profiles** (🌸 Setosa, 🌾 Versicolor, 🌺 Virginica, 🔄 Reset).
   - Right Panel: Floating taxonomic diagnosis card with species color branding, Softmax probability distribution bars, and measurement recap pill.

3. **Dataset Explorer:**
   - Searchable, filterable specimen records table.
   - Species multi-select filter, pagination, and descriptive statistical moments.

4. **Species Insights:**
   - 3 profile cards displaying empirical morphometric means, dimensional extremes, and botanical characteristics.
   - Comparative Petal Length and Sepal Width boxplot dispersion charts.

5. **Model Diagnostics & Scientific Evaluation:**
   - Audited historical metrics: **96.67% Test Accuracy**, **96.97% Macro Precision**, **0.9666 Macro F1-score**.
   - Held-out test split confusion matrix heatmap ($N=30$).
   - 5-fold cross-model benchmark matrix comparing Random Forest, KNN (93.33%), and Logistic Regression (93.33%).

---

## 🧪 Model Invariance Verification

Predictions match the original pipeline with 100% numerical invariance:

| Preset Name | Sepal L (cm) | Sepal W (cm) | Petal L (cm) | Petal W (cm) | Predicted Class | Model Confidence |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Setosa Sample** | 5.0 | 3.4 | 1.5 | 0.2 | **Iris Setosa** | **100.00%** |
| **Versicolor Sample** | 5.9 | 2.8 | 4.3 | 1.3 | **Iris Versicolor** | **99.64%** |
| **Virginica Sample** | 6.6 | 3.0 | 5.6 | 2.0 | **Iris Virginica** | **99.72%** |
| **Default Midpoint** | 5.8 | 3.0 | 4.3 | 1.3 | **Iris Versicolor** | **99.64%** |

---

## 🚀 How to Run IrisAI Studio

### 1. Launch FastAPI Backend
```powershell
cd DataScience-Task1-IrisClassification/backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
- Interactive Swagger API documentation: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/api/health`

### 2. Launch React Frontend
```powershell
cd DataScience-Task1-IrisClassification/frontend
npm.cmd run dev -- --host 127.0.0.1 --port 3001
```
- Application console: `http://localhost:3001`

### 3. Run Automated Backend Test Suite
```powershell
python DataScience-Task1-IrisClassification/backend/test_api.py
```

### 4. Legacy Streamlit Application
The original Streamlit application remains accessible at:
```powershell
streamlit run DataScience-Task1-IrisClassification/src/app.py
```
