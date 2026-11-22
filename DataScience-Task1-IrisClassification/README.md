# 🌸 Iris Flower Classification Using Machine Learning
### **OASIS INFOBYTE Data Science Internship — Task 1**

![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3%2B-orange?style=for-the-badge&logo=scikit-learn)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B?style=for-the-badge&logo=streamlit)
![License](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)

---

## 📌 Project Overview
The **Iris Flower Classification Project** is a foundational machine learning solution developed for the **OASIS INFOBYTE Data Science Internship (Task 1)**. The objective of this project is to develop, evaluate, and deploy an automated supervised learning system that accurately classifies Iris flowers into three distinct botanical species:
1. **Iris Setosa**
2. **Iris Versicolor**
3. **Iris Virginica**

The classification is performed based on four fundamental morphological features:
* **Sepal Length (cm)**
* **Sepal Width (cm)**
* **Petal Length (cm)**
* **Petal Width (cm)**

---

## 🎯 Problem Statement & Objectives
### Problem Statement
In botanical taxonomy, distinguishing closely related plant species through manual anatomical inspection is labor-intensive and prone to human error, particularly for morphologically similar taxa like *Iris versicolor* and *Iris virginica*. Machine learning offers an automated, data-driven approach to map morphological measurements to precise taxonomical classifications.

### Objectives
1. **Data Ingestion & Integrity:** Ingest the canonical Iris dataset from Scikit-Learn, format it with standardized feature columns, and inspect schema, data types, missing values, duplicates, and class balance.
2. **Exploratory Data Analysis (EDA):** Generate 8 high-resolution visualisations to analyze inter-class feature distributions, correlations, and variances.
3. **Discriminative Feature Analysis:** Statistically examine why petal dimensions possess superior discriminative capability compared to sepal dimensions.
4. **Machine Learning Pipeline:** Implement and benchmark three candidate supervised classification models:
   - Logistic Regression (Scaled, L2 Regularized)
   - K-Nearest Neighbours (Scaled, k=5)
   - Random Forest Classifier (100 Ensemble Trees)
5. **Rigorous Evaluation:** Prevent data leakage via stratified 80/20 train/test splitting and Scikit-Learn preprocessing pipelines. Benchmark using Accuracy, Macro & Weighted Precision, Recall, and F1-Scores.
6. **Model Serialization:** Persist the optimal production pipeline and feature metadata using `joblib`.
7. **Interactive Application:** Provide an intuitive Streamlit web application for real-time inference with species probability distribution charts and quick presets.

---

## 💻 Tech Stack & Dependencies
* **Core Language:** Python 3.10+ (tested on Python 3.14)
* **Data Processing & Manipulation:** Pandas, NumPy
* **Machine Learning & Preprocessing:** Scikit-Learn (`sklearn.pipeline`, `sklearn.preprocessing`, `sklearn.metrics`, `sklearn.ensemble`, `sklearn.neighbors`, `sklearn.linear_model`)
* **Data Visualisation:** Matplotlib, Seaborn
* **Model Serialization:** Joblib
* **Interactive UI:** Streamlit
* **Notebook Development:** Jupyter Notebook, Nbformat

---

## 📂 Project Architecture
```text
DataScience-Task1-IrisClassification/
├── data/
│   └── iris.csv                      # Standardized Iris dataset with target names
├── models/
│   ├── best_iris_model.joblib        # Serialized pipeline, scaler, & metadata
│   └── model_metadata.json           # JSON benchmark metrics and architecture specs
├── notebooks/
│   └── Iris_Flower_Classification.ipynb  # End-to-end interactive Jupyter Notebook
├── src/
│   ├── __init__.py                   # Package initialization
│   ├── data_loader.py                # Dataset extraction, cleaning, and inspection
│   ├── eda.py                        # Exploratory Data Analysis & visual generation
│   ├── train.py                      # Model training, evaluation, comparison, & export
│   ├── predict.py                    # Production CLI & programmatic inference API
│   └── app.py                        # Interactive Streamlit Web Application
├── visualizations/
│   ├── species_distribution.png      # Balanced 33.3% class distribution
│   ├── pairplot.png                  # Multi-feature pairwise scatter with KDE
│   ├── sepal_length_distribution.png # Sepal length histogram & KDE
│   ├── sepal_width_distribution.png  # Sepal width histogram & KDE
│   ├── petal_length_distribution.png # Petal length histogram & KDE
│   ├── petal_width_distribution.png  # Petal width histogram & KDE
│   ├── feature_boxplots.png          # Boxplots showing IQR & outlier analysis
│   ├── correlation_heatmap.png       # Pearson correlation coefficient matrix
│   ├── confusion_matrices.png        # Comparative confusion matrix heatmaps
│   └── model_comparison.png          # Benchmark bar chart across all metrics
├── README.md                         # Detailed project documentation
├── requirements.txt                  # Python dependencies
└── .gitignore                        # Git exclusion rules
```

---

## 📊 Dataset Description
The Iris dataset contains 150 biological records categorized into three species (50 instances per class):
* **Class 0:** *Iris Setosa*
* **Class 1:** *Iris Versicolor*
* **Class 2:** *Iris Virginica*

### Descriptive Statistics Summary
| Feature Name | Count | Mean | Std Dev | Min | 25% | Median | 75% | Max | Skewness |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sepal Length (cm)** | 150 | 5.843 | 0.828 | 4.30 | 5.10 | 5.80 | 6.40 | 7.90 | +0.315 |
| **Sepal Width (cm)**  | 150 | 3.057 | 0.436 | 2.00 | 2.80 | 3.00 | 3.30 | 4.40 | +0.319 |
| **Petal Length (cm)** | 150 | 3.758 | 1.765 | 1.00 | 1.60 | 4.35 | 5.10 | 6.90 | -0.275 |
| **Petal Width (cm)**  | 150 | 1.199 | 0.762 | 0.10 | 0.30 | 1.30 | 1.80 | 2.50 | -0.103 |

* **Missing Values:** `0` (100% complete dataset).
* **Duplicates:** `1` natural duplicate record across the feature space (retained to preserve botanical observation distribution).

---

## 🔬 Exploratory Data Analysis & Feature Insights
All visualisations are automatically generated by `src/eda.py` and exported to `visualizations/`:

1. **Species Distribution (`species_distribution.png`):** Confirms ideal 33.33% class balance (50 samples each). No synthetic rebalancing (SMOTE) is necessary.
2. **Pairwise Feature Scatter (`pairplot.png`):** Reveals that *Iris Setosa* is completely linearly separable from the other two species across all petal projections.
3. **Petal vs. Sepal Discrimination (`petal_length_distribution.png` & `petal_width_distribution.png`):**
   * *Iris Setosa* petal lengths are strictly between **1.0 cm and 1.9 cm** with 0% overlap with Versicolor (3.0 - 5.1 cm) or Virginica (4.5 - 6.9 cm).
   * Petal measurements show high mutual correlation (**r = 0.963**), serving as the primary drivers of classifier decision boundaries.
4. **Correlation Matrix (`correlation_heatmap.png`):** Petal length and width exhibit a strong positive correlation (+0.963), while sepal width displays a moderate negative correlation with petal dimensions (-0.37 to -0.43).
5. **Dispersion & Outliers (`feature_boxplots.png`):** Demonstrates that petal lengths and widths increase monotonically from Setosa → Versicolor → Virginica with distinct interquartile ranges.

---

## ⚙️ Model Development & Evaluation Benchmark
The dataset was partitioned into **80% Training (120 samples)** and **20% Testing (30 samples)** using **stratified sampling (`random_state=42`)** to guarantee exactly 10 test samples per species.

### Comparative Performance Table (Test Partition: 30 Samples)
| Model Architecture | Train Acc | Test Acc | Precision (Macro) | Recall (Macro) | F1-Score (Macro) | Precision (Weighted) | Recall (Weighted) | F1-Score (Weighted) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Random Forest Classifier** | **1.0000** | **0.9667** | **0.9697** | **0.9667** | **0.9666** | **0.9697** | **0.9667** | **0.9666** |
| **Logistic Regression (Scaled)** | 0.9583 | 0.9333 | 0.9333 | 0.9333 | 0.9333 | 0.9333 | 0.9333 | 0.9333 |
| **K-Nearest Neighbours (Scaled)** | 0.9750 | 0.9333 | 0.9444 | 0.9333 | 0.9327 | 0.9444 | 0.9333 | 0.9327 |

### Detailed Classification Report (Best Model: Random Forest Classifier)
```text
              precision    recall  f1-score   support

      Setosa     1.0000    1.0000    1.0000        10
  Versicolor     1.0000    0.9000    0.9474        10
   Virginica     0.9091    1.0000    0.9524        10

    accuracy                         0.9667        30
   macro avg     0.9697    0.9667    0.9666        30
weighted avg     0.9697    0.9667    0.9666        30
```

### Optimal Model Selection & Rationale
* **Selected Model:** **Random Forest Classifier** (`n_estimators=100`, `max_depth=4`, `random_state=42`).
* **Test Accuracy:** **96.67%** (29/30 correct classifications).
* **Macro F1-Score:** **96.66%**.
* **Rationale:** Ensemble decision trees naturally isolate the non-linear decision boundaries between *Iris versicolor* and *Iris virginica* without inflating variance. In contrast, linear classifiers face ambiguity along overlapping boundary margins.

---

## 🚀 Installation & Execution Guide

### 1. Clone or Open the Repository
```bash
cd DataScience-Task1-IrisClassification
```

### 2. Create and Activate a Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Required Dependencies
```bash
pip install -r requirements.txt
```

### 4. Execute the End-to-End Pipeline
```bash
# Step 1: Ingest dataset & inspect properties
python src/data_loader.py

# Step 2: Generate all 8 exploratory data analysis visual plots
python src/eda.py

# Step 3: Train models, benchmark, plot confusion matrices, and serialize best model
python src/train.py
```

### 5. Run Single CLI Inferences
You can query the saved model artifact using `src/predict.py`:
```bash
# Predict a Setosa flower
python src/predict.py --sepal-length 5.1 --sepal-width 3.5 --petal-length 1.4 --petal-width 0.2

# Predict a Versicolor flower
python src/predict.py --sepal-length 5.9 --sepal-width 3.0 --petal-length 4.2 --petal-width 1.5

# Predict a Virginica flower
python src/predict.py --sepal-length 6.5 --sepal-width 3.0 --petal-length 5.5 --petal-width 1.8
```

### 6. Launch the Interactive Streamlit Web Application
```bash
streamlit run src/app.py
```
Open your browser at `http://localhost:8501` to test custom inputs, quick presets, and live probability distributions.

---

## 📈 Visualizations Gallery
All generated charts are located in the `visualizations/` folder:

| Visualization | Description |
| :--- | :--- |
| `species_distribution.png` | Class frequency and percentage verification |
| `pairplot.png` | Complete 4x4 feature scatter matrix with KDE distributions |
| `sepal_length_distribution.png` | Histograms and KDE curves for Sepal Length by species |
| `sepal_width_distribution.png` | Histograms and KDE curves for Sepal Width by species |
| `petal_length_distribution.png` | Distinct multimodal distributions for Petal Length |
| `petal_width_distribution.png` | Separability analysis for Petal Width |
| `feature_boxplots.png` | 2x2 grid of boxplots depicting IQR, medians, and outliers |
| `correlation_heatmap.png` | Pearson correlation matrix with annotated coefficients |
| `confusion_matrices.png` | Side-by-side confusion matrix comparisons for all 3 models |
| `model_comparison.png` | Benchmark bar chart comparing Accuracy, Precision, Recall, and F1 |

---

## 🔮 Future Improvements
1. **Hyperparameter Tuning:** Conduct `GridSearchCV` or `Optuna` Bayesian optimization for deeper ensemble trees and regularizers.
2. **Additional Classifiers:** Benchmark Support Vector Machines (SVM with RBF kernel) and LightGBM / XGBoost.
3. **Containerization:** Package the application into a lightweight Docker image for seamless cloud deployment on platforms like Render, AWS ECS, or Hugging Face Spaces.
4. **REST API Endpoint:** Wrap the `IrisPredictor` in a FastAPI service with OpenAPI / Swagger documentation.

---

## 👤 Author & Acknowledgments
* **Project:** Iris Flower Classification Using Machine Learning
* **Internship Program:** OASIS INFOBYTE Internship in Data Science
* **Author:** Data Science Intern
* **Dataset Attribution:** Fisher, R. A. (1936). *The use of multiple measurements in taxonomic problems*.
