# OASIS INFOBYTE Data Science Internship (OIBSIP)
> **Executive Portfolio: 5 Domain-Specific Intelligent Machine Learning Applications**

This repository contains five enterprise-grade data science and machine learning applications developed for the **OASIS INFOBYTE Data Science Internship (OIBSIP)**. Each project has been transformed into a production-caliber web platform featuring its own domain-specific visual identity, real model inference, responsive analytics, and zero-compromise scientific preservation.

---

## 🌟 Intelligent Applications Showcase

| Application | Domain & Visual Theme | Technology Stack | Key Model Architecture | Audited Benchmark | Launch Command |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **🌸 IrisAI**<br>*(Task 1)* | **Botanical Intelligence**<br>Emerald & Deep Violet (`#10B981`, `#8B5CF6`) | Streamlit + Plotly 3D + Scikit-Learn | Random Forest Classifier Pipeline | **100% Test Accuracy**<br>(1.0000 Macro F1) | `streamlit run DataScience-Task1-IrisClassification/src/app.py` |
| **📈 EmployIQ**<br>*(Task 2)* | **Labour Market Intelligence**<br>Navy, Teal & Cyan (`#070C18`, `#00F5A0`, `#00D9F5`) | Streamlit + Plotly Express + CMIE India | Macroeconomic Surveillance Engine | **National Shock: +86.9%**<br>(Peak >24% during lockdown) | `streamlit run DataScience-Task2-UnemploymentAnalysis/dashboard/app.py` |
| **🏎️ AutoValue AI**<br>*(Task 3)* | **Automotive Cockpit Valuation**<br>Charcoal & Electric Blue (`#090D16`, `#38BDF8`) | Streamlit + Plotly + Scikit-Learn | Random Forest & Log-Y Regressors | **$R^2 = 0.7120$**<br>(MAE = ₹1.44 Lakhs) | `streamlit run DataScience-Task3-CarPricePrediction/dashboard/app.py` |
| **🛡️ SpamGuard AI**<br>*(Task 4 & 5)* | **Cybersecurity Threat Intelligence**<br>Dark SecOps Console (`#080D18`, `#00F5A0`) | React 18 + Vite + Tailwind + FastAPI + PyTorch | Dual-Threshold Hybrid Triage (BERT-Tiny + MNB) | **96.66% Selective Acc**<br>(80.9% Automated Coverage) | Backend: `python -m uvicorn app.main:app`<br>Frontend: `npm run dev` |

---

## 📂 Repository Directory Structure

```
OIBSIP/
├── DataScience-Task1-IrisClassification/     # Task 1: IrisAI — Flower Intelligence
│   ├── src/app.py                            # Streamlit Web Application (5 modular pages)
│   ├── src/predict.py                        # IrisPredictor inference wrapper
│   ├── models/best_iris_model.joblib         # Trained Random Forest pipeline
│   └── data/iris.csv                         # 150-sample Iris dataset
│
├── DataScience-Task2-UnemploymentAnalysis/   # Task 2: EmployIQ — Labour Market Intelligence
│   ├── dashboard/app.py                      # Streamlit Analytics Dashboard (6 views)
│   ├── data/processed/unemployment_cleaned.csv# Cleaned CMIE 740-record dataset
│   └── src/                                  # Data loader & cleaning pipeline
│
├── DataScience-Task3-CarPricePrediction/     # Task 3: AutoValue AI — Car Valuation
│   ├── dashboard/app.py                      # Automotive Cockpit Dashboard (5 views)
│   ├── src/predict.py                        # CarPricePredictor inference wrapper
│   ├── models/car_price_pipeline.joblib      # Trained regression pipeline
│   └── data/processed/car_details_cleaned.csv# 3,577 deduplicated CarDekho records
│
├── spamguard-ai/                             # Task 4 & 5: SpamGuard AI Cybersecurity SaaS
│   ├── backend/                              # FastAPI REST API & Model Lifespan Service
│   ├── frontend/                             # React 18 + Vite + Tailwind CSS (7 pages)
│   └── README.md                             # Architectural deep-dive & audit reports
│
├── OIBSIP_Task4_Spam_Detection/              # Original Task 4 Notebooks, Models & Datasets
├── independent_validation/                   # Original Task 5 Forensic Audit & Metrics
└── README.md                                 # Master Portfolio Documentation
```

---

## 🌸 Task 1: IrisAI — Flower Intelligence Platform

**Visual Identity:** Dark Botanical (`#080E14` base with Emerald `#10B981` and Violet `#8B5CF6`).

### Key Capabilities:
- **5 Integrated Pages:**
  1. *Overview & Botanical Dashboard:* KPI metric cards, dataset specimen breakdown, and feature scatter distributions.
  2. *Flower Classifier:* Real-time measurement sliders for Sepal Length, Sepal Width, Petal Length, and Petal Width with calibrated Softmax probabilities.
  3. *Dataset Explorer:* Searchable, filterable specimen records with summary moments.
  4. *Species Insights:* 3D morphometric manifold visualization in interactive Plotly space.
  5. *Model Performance:* Audited confusion matrix and classification metrics.
- **Inference Verification:** Evaluated with positive biological constraints, achieving **100% accuracy** on the held-out test split.

---

## 📈 Task 2: EmployIQ — Labour Market Intelligence Platform

**Visual Identity:** Executive Economic Surveillance (`#070C18` with Deep Teal `#00F5A0` and Cyan `#00D9F5`).

### Key Capabilities:
- **Strictly Preserved Independent State Selection:** State multi-select operates independently of the Macro-Geographical Zone filter, enabling unconstrained cross-regional benchmarking.
- **6 Integrated Views:**
  1. *Executive Overview:* National unemployment rate, highest/lowest state indicators, and labour participation ratios.
  2. *State-Level Analysis:* High-amplitude vs. low-volatility state leaderboards.
  3. *Regional & Zonal Dynamics:* Comparative dispersion across North, South, East, West, and North-East zones.
  4. *COVID-19 Lockdown Shock:* Pre-lockdown (9.51%) vs. Post-March 2020 (17.77%) sectoral shifts.
  5. *Labour & Sectoral Divergence:* OLS scatter plots correlating Labour Participation Rate (LPR) with unemployment.
  6. *Policy Recommendations:* Non-causal empirical insights derived from 740 CMIE observation records.

---

## 🏎️ Task 3: AutoValue AI — Intelligent Car Valuation Platform

**Visual Identity:** High-End Automotive Digital Cockpit (`#090D16` Charcoal, Metallic Silver, Electric Blue `#38BDF8`).

### Key Capabilities:
- **5 Cockpit Views:**
  1. *Market Telemetry & Overview:* Volume metrics across 29 brands, median market resale prices, and fuel type composition.
  2. *Vehicle Valuation Calculator:* Dynamic selection for Brand, Manufacturing Year (1992–2020), Odometer Kilometers, Fuel Type, Transmission, Seller Type, and Ownership Lineage.
  3. *Brand & Fleet Insights:* Premium brand premiums vs. mass-market baselines and Automatic transmission resale premiums (+71.4%).
  4. *Depreciation Analytics:* OLS exponential depreciation trajectories against vehicle age and mileage.
  5. *Model Diagnostics:* Audited $R^2 = 0.7120$, Test MAE = ₹1,44,221, and comparative benchmark matrices.

---

## 🛡️ Task 4 & 5: SpamGuard AI — Enterprise Threat Intelligence

**Visual Identity:** Cyber Threat Defense Console (`#080D18`, `#00F5A0`, `#FF3B5C`).

### Key Capabilities:
- **Full-Stack SaaS Architecture:** FastAPI REST API backend with PyTorch CPU inference and modern React 18 + Vite frontend.
- **Audited Dual-Threshold Triage:** Under $\theta_{\text{spam}} \ge 0.60$ and $\theta_{\text{ham}} \le 0.10$, automated decisions achieve **96.66% selective accuracy** across **80.90% coverage**, routing 191 ambiguous messages to human review ($70.68\%$ spam concentration).
- **Extracted Threat Signals:** Regex heuristic engine detecting reverse-billing shortcodes, deceptive dial-in vishing numbers, and credential phishing links aligned with MITRE ATT&CK.

---

## 🧪 Verification & Automated Testing

All applications have been verified with automated regression and test suites:
- **Task 1 (IrisAI):** `Ran 9 tests in 0.552s — OK`
- **Task 2 (EmployIQ):** `Ran 12 tests in 0.151s — OK`
- **Task 3 (AutoValue AI):** `Ran 17 tests in 0.462s — OK`
- **SpamGuard AI (Backend API):** `All 7 endpoints and live ML inference — PASS`
- **SpamGuard AI (React Frontend):** `Vite production bundle compiled cleanly (0 errors) — OK`
