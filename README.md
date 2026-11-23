# OASIS INFOBYTE Data Science Internship (OIBSIP)

This repository contains professional, industry-standard data science and machine learning projects developed for the **OASIS INFOBYTE Data Science Internship**.

---

## 📂 Internship Tasks Portfolio

| Task | Project Name | Description | Status | Directory |
| :---: | :--- | :--- | :---: | :--- |
| **Task 1** | **Iris Flower Classification** | Machine learning classification system to predict Iris flower species (*Setosa*, *Versicolor*, *Virginica*) from morphological measurements. Includes EDA, 3 ML algorithms benchmark (Random Forest: 96.67% accuracy), model serialization, and interactive Streamlit UI. | ✅ Completed | [`DataScience-Task1-IrisClassification/`](./DataScience-Task1-IrisClassification/) |
| **Task 2** | **Unemployment Analysis with Python (India)** | Macroeconomic empirical analysis investigating state-wise unemployment trends, rural vs. urban dynamics, and COVID-19 lockdown shocks (May 2019 – June 2020) using CMIE labor data. Includes statistical hypothesis testing, 8 publication visualisations, and a modern Streamlit analytics portal. | ✅ Completed | [`DataScience-Task2-UnemploymentAnalysis/`](./DataScience-Task2-UnemploymentAnalysis/) |
| **Task 3** | **Car Price Prediction with Machine Learning** | Production machine learning system to predict used-car selling prices using CarDekho market listings. Features leakage-safe ColumnTransformer pipelines, 4 algorithms benchmarked with 5-fold CV, 12 publication visualisations, model explainability, and an interactive Streamlit valuation portal. | ✅ Completed | [`DataScience-Task3-CarPricePrediction/`](./DataScience-Task3-CarPricePrediction/) |

---

## 🌸 Task 1: Iris Flower Classification Quick Summary
* **Algorithms Benchmarked:** Logistic Regression, K-Nearest Neighbours, Random Forest Classifier.
* **Best Model:** **Random Forest Classifier** with **96.67% Test Accuracy** and **96.66% Macro F1-score**.
* **Key Finding:** Petal length and petal width are the most discriminative features (Pearson correlation $r = 0.963$), providing near-orthogonal boundaries between classes.
* **Interactive UI:** Streamlit Web Application in `DataScience-Task1-IrisClassification/src/app.py`.
* **Full Documentation:** Refer to [`DataScience-Task1-IrisClassification/README.md`](./DataScience-Task1-IrisClassification/README.md).

---

## 🇮🇳 Task 2: Unemployment Analysis Quick Summary
* **Primary Source:** Centre for Monitoring Indian Economy (CMIE) Consumer Pyramids Household Survey (May 2019 to June 2020).
* **Coverage:** 28 Indian States & Union Territories across Rural and Urban sectors (740 cleaned observations).
* **COVID-19 Shock:** National mean unemployment rose from **9.51% (Pre-COVID)** to **17.77% (Post-March 2020)**, an **86.91% relative surge**, peaking above **24%** in April–May 2020.
* **Sectoral Divergence:** Urban unemployment rose from **10.84%** to **19.28%** post-lockdown, while rural unemployment rose from **8.09%** to **16.18%** (+99.90% relative increase). Contextual literature notes that agricultural harvesting and MGNREGA public works helped buffer initial rural disruption.
* **Extreme Regions:** Highest average unemployment recorded in **Tripura (28.35%)**, **Haryana (26.28%)**, and **Jharkhand (20.58%)**; lowest in **Meghalaya (4.80%)**, **Odisha (5.66%)**, and **Assam (6.43%)**.
* **Interactive Dashboard:** Modern Streamlit Analytics Portal in `DataScience-Task2-UnemploymentAnalysis/dashboard/app.py`.
* **Full Documentation:** Refer to [`DataScience-Task2-UnemploymentAnalysis/README.md`](./DataScience-Task2-UnemploymentAnalysis/README.md).

---

## 🚗 Task 3: Car Price Prediction Quick Summary
* **Primary Source:** CarDekho used-car market listings dataset ($N = 4,340$ raw listings, 3,577 deduplicated records).
* **Algorithms Benchmarked:** Linear Regression (Log-Y), Ridge Regression (Log-Y), Random Forest Regressor (Log-Y), Gradient Boosting Regressor (Log-Y).
* **Best Model:** **Linear Regression with Log-Transformed Target** with **$R^2 = 0.7120$**, **Test MAE = ₹1,44,221**, and **Test RMSE = ₹3,04,582**.
* **Key Finding:** Vehicle resale values follow compound exponential depreciation ($\sim -10.5\%$ compounding annually per year of age). Automatic transmissions command an empirical $+71.4\%$ median price premium.
* **Interactive UI:** Streamlit Vehicle Valuation Portal in `DataScience-Task3-CarPricePrediction/dashboard/app.py`.
* **Full Documentation:** Refer to [`DataScience-Task3-CarPricePrediction/README.md`](./DataScience-Task3-CarPricePrediction/README.md).
