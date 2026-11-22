# OASIS INFOBYTE Data Science Internship (OIBSIP)

This repository contains professional, industry-standard data science and machine learning projects developed for the **OASIS INFOBYTE Data Science Internship**.

---

## 📂 Internship Tasks Portfolio

| Task | Project Name | Description | Status | Directory |
| :---: | :--- | :--- | :---: | :--- |
| **Task 1** | **Iris Flower Classification** | Machine learning classification system to predict Iris flower species (*Setosa*, *Versicolor*, *Virginica*) from morphological measurements. Includes EDA, 3 ML algorithms benchmark (Random Forest: 96.67% accuracy), model serialization, and interactive Streamlit UI. | ✅ Completed | [`DataScience-Task1-IrisClassification/`](./DataScience-Task1-IrisClassification/) |
| **Task 2** | **Unemployment Analysis with Python (India)** | Macroeconomic empirical analysis investigating state-wise unemployment trends, rural vs. urban dynamics, and COVID-19 lockdown shocks (May 2019 – June 2020) using CMIE labor data. Includes statistical hypothesis testing, 8 publication visualisations, and a modern Streamlit analytics portal. | ✅ Completed | [`DataScience-Task2-UnemploymentAnalysis/`](./DataScience-Task2-UnemploymentAnalysis/) |

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
* **Sectoral Divergence:** Urban unemployment reached **19.46%** post-lockdown due to commercial service closures, while rural unemployment was partially buffered at **16.08%** by agriculture and MGNREGA.
* **Extreme Regions:** Highest average unemployment recorded in **Tripura (28.35%)** and **Haryana (26.28%)**; lowest in **Meghalaya (4.80%)** and **Odisha (5.66%)**.
* **Interactive Dashboard:** Modern Streamlit Analytics Portal in `DataScience-Task2-UnemploymentAnalysis/dashboard/app.py`.
* **Full Documentation:** Refer to [`DataScience-Task2-UnemploymentAnalysis/README.md`](./DataScience-Task2-UnemploymentAnalysis/README.md).
