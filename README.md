# OASIS INFOBYTE Data Science Internship (OIBSIP)

This repository contains professional, industry-standard data science and machine learning projects developed for the **OASIS INFOBYTE Data Science Internship**.

---

## 📂 Internship Tasks Portfolio

| Task | Project Name | Description | Status | Directory |
| :---: | :--- | :--- | :---: | :--- |
| **Task 1** | **Iris Flower Classification** | Machine learning classification system to predict Iris flower species (*Setosa*, *Versicolor*, *Virginica*) from morphological measurements. Includes EDA, 3 ML algorithms benchmark (Random Forest: 96.67% accuracy), model serialization, and interactive Streamlit UI. | ✅ Completed | [`DataScience-Task1-IrisClassification/`](./DataScience-Task1-IrisClassification/) |
| **Task 2** | **Unemployment Analysis with Python (India)** | Macroeconomic empirical analysis investigating state-wise unemployment trends, rural vs. urban dynamics, and COVID-19 lockdown shocks (May 2019 – June 2020) using CMIE labor data. Includes statistical hypothesis testing, 8 publication visualisations, and a modern Streamlit analytics portal. | ✅ Completed | [`DataScience-Task2-UnemploymentAnalysis/`](./DataScience-Task2-UnemploymentAnalysis/) |
| **Task 3** | **Car Price Prediction with Machine Learning** | Production machine learning system to predict used-car selling prices using CarDekho market listings. Features leakage-safe ColumnTransformer pipelines, 4 algorithms benchmarked with 5-fold CV, 12 publication visualisations, model explainability, and an interactive Streamlit valuation portal. | ✅ Completed | [`DataScience-Task3-CarPricePrediction/`](./DataScience-Task3-CarPricePrediction/) |
| **Task 4** | **Email / SMS Spam Detection with Machine Learning** | NLP-based binary classification system distinguishing Spam from Ham using the Kaggle SMS Spam Collection dataset. Features regex preprocessing with Porter Stemming, TF-IDF vectorization (max_features=5000, ngram_range=(1,2)), pipeline-based leak-free benchmarking (Multinomial Naive Bayes & Logistic Regression), confusion matrices, and custom message inference. | ✅ Completed | [`OIBSIP_Task4_Spam_Detection/`](./OIBSIP_Task4_Spam_Detection/) |
| **Task 5** | **Independent Validation of BERT-Tiny SMS Spam Detection** | Independent out-of-distribution validation study using non-overlapping modern SMS/smishing data (ACM 2025). Features zero-leakage overlap auditing, BERT logit-collapse analysis, and a calibrated 3-way hybrid triage architecture (HAM, SPAM, SUSPICIOUS/REVIEW) with full audit reports. | ✅ Completed | [`independent_validation/`](./independent_validation/) |

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

---

## 📱 Task 4: Email / SMS Spam Detection Quick Summary
* **Primary Source:** Kaggle / UCI SMS Spam Collection dataset ($N = 5,572$ records, 4,825 Ham [86.59%] and 747 Spam [13.41%]). Note: Contains mobile SMS messages rather than standard email formats.
* **Text Preprocessing:** Case folding, URL/email stripping, punctuation & digit removal, NLTK stopword elimination, and Porter Stemming.
* **Feature Extraction:** `TfidfVectorizer(max_features=5000, ngram_range=(1, 2))` fitted strictly on training data via Scikit-Learn `Pipeline` to prevent data leakage.
* **Algorithms Benchmarked:** Multinomial Naive Bayes vs. Logistic Regression evaluated with stratified 80:20 split ($N_{\text{test}} = 1,115$).
* **Best Model:** **Multinomial Naive Bayes** achieved **96.95% Test Accuracy**, **99.15% Precision**, **77.85% Recall**, and **0.8722 F1-Score** (Confusion Matrix: 965 TN, 1 FP, 33 FN, 116 TP).
* **Recall Importance:** High precision protects legitimate user communications from false positive spam filtering, but critical spam filtering requires optimizing recall to prevent malicious phishing or financial scams from reaching inboxes.
* **Interactive Notebook:** Fully executed Jupyter Notebook in [`OIBSIP_Task4_Spam_Detection/notebooks/Task4_Spam_Detection.ipynb`](./OIBSIP_Task4_Spam_Detection/notebooks/Task4_Spam_Detection.ipynb).
* **Full Documentation:** Refer to [`OIBSIP_Task4_Spam_Detection/README.md`](./OIBSIP_Task4_Spam_Detection/README.md).

---

## 🔬 Task 5: Independent Validation Study Quick Summary
* **Primary Source:** Modern Smishing & SMS dataset (`shaghayegh-hp/Smishing_Dataset`, ACM 2025).
* **Provenance & Overlap Audit:** 4,718 matching records with UCI SMS Spam Collection strictly eliminated; 2,000 non-overlapping messages sampled (1,000 validation, 1,000 held-out test).
* **Models Evaluated (Unchanged):** Multinomial Naive Bayes (Task 4 Pipeline) vs. BERT-Tiny Transformer (`mrm8488/bert-tiny-finetuned-sms-spam-detection`).
* **Key Findings:** Naive Bayes suffered out-of-vocabulary collapse on unseen modern terminology ($7.20\%$ recall), while BERT-Tiny generalized better ($76.60\%$ recall, $87.10\%$ accuracy) but exhibited logit collapse on messages lacking 2003-era carrier dial codes.
* **3-Way Hybrid Triage:** Automated $80.9\%$ of traffic with **$96.66\%$ accuracy**, **$96.69\%$ precision**, and **$95.89\%$ recall**, while sequestering 135 ambiguous spams into a **SUSPICIOUS / REVIEW** queue.
* **Documentation & Audit:** Full technical report in [`independent_validation/README.md`](./independent_validation/README.md) and forensic audit in [`independent_validation/AUDIT_REPORT.md`](./independent_validation/AUDIT_REPORT.md).
