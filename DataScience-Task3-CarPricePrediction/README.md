# 🚗 Car Price Prediction Using Machine Learning
### **OASIS INFOBYTE Data Science Internship — Task 3**

![Python](https://img.shields.io/badge/Python-3.14.6-blue?style=for-the-badge&logo=python)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.9.1-F7931E?style=for-the-badge&logo=scikitlearn)
![Joblib](https://img.shields.io/badge/Joblib-1.6.0-green?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B?style=for-the-badge&logo=streamlit)
![License](https://img.shields.io/badge/License-ODbL%20%2F%20Database%20Contents-blue?style=for-the-badge)

---

## 📌 Project Overview
The **Car Price Prediction with Machine Learning** system is an industry-grade regression modeling project developed for the **OASIS INFOBYTE Data Science Internship (Task 3)**.

The objective is to accurately predict the resale price of used cars in India based on key vehicle attributes: **brand, car age, odometer distance (km driven), fuel type, seller type, transmission, and ownership history**. The system integrates automated data cleaning, exploratory data analysis, leakage-safe scikit-learn pipelines, model explainability, 12 publication-grade figures, and an interactive **Streamlit Resale Valuation Dashboard**.

> **⚠️ Historical Valuation Scope (2020 Baseline):** The training data consists of 2020 historical CarDekho listings, with feature engineering computing $\text{car\_age} = 2020 - \text{year}$. All predictions are estimates reflecting historical 2020 market conditions and dynamics, not present 2026 market valuations.

---

## 🎯 Problem Statement & Objectives
### Problem Statement
Accurate used car valuation is critical for automotive marketplaces, dealerships, and consumers. Vehicle depreciation is a non-linear process driven by vehicle age, mechanical wear, brand perception, fuel economics, and transmission preferences. Developing an econometric and machine learning system provides fair, transparent valuations while eliminating arbitrary pricing bias.

### Core Objectives
1. **Dataset Provenance & Ingestion:** Ingest and archive authentic CarDekho listings ($N = 4,340$).
2. **Data Cleaning & Deduplication:** Audit missing values, drop exact duplicate listings to prevent train/test leakage, standardise brand names, and engineer `car_age`.
3. **Exploratory Data Analysis (EDA):** Quantify depreciation curves, transmission premiums, fuel distributions, and brand value tiers across 29 manufacturers.
4. **Leakage-Safe Machine Learning:** Construct `ColumnTransformer` pipelines with median imputation, `StandardScaler`, and `OneHotEncoder(handle_unknown="ignore")`.
5. **Rigorous Benchmarking:** Split data via randomized 80:20 `train_test_split(random_state=42)` and benchmark 4 algorithms (Linear Regression, Ridge Regression, Random Forest Regressor, Gradient Boosting Regressor) using 5-fold cross-validation on the training set.
6. **Log-Transformed Target Formulation:** Employ `TransformedTargetRegressor(func=np.log1p, inverse_func=np.expm1)` to linearize compound exponential depreciation and guarantee strictly positive price predictions.
7. **Production Deployment:** Serialize the complete pipeline via `joblib` and build an interactive Streamlit application.

---

## 🌐 Dataset Provenance & Data Dictionary
* **Primary Origin:** Publicly listed used-car advertisements on **CarDekho.com**.
* **Provider / Host:** Kaggle Public Datasets (*Vehicle Dataset from CarDekho* by Nehal Birla / Akshay Khare).
* **Dataset License:** Database: Open Database, Contents: Database Contents (ODbL / Database Contents Kaggle classification). Sourced from CarDekho.com via Kaggle contributors. For educational and research purposes.
* **Direct Archive Mirror:** `https://raw.githubusercontent.com/IMvision12/Car-Price_prediction/main/CAR%20DETAILS%20FROM%20CAR%20DEKHO.csv`
* **Raw Observations:** 4,340 rows $\times$ 8 columns.
* **Cleaned Observations:** 3,577 unique records post-deduplication.

### Data Dictionary
| Feature | Column Name | Data Type | Description | Values / Range |
| :--- | :--- | :---: | :--- | :--- |
| **Brand** | `brand` | Categorical | Manufacturer make extracted from car name | 29 unique brands (Maruti, Hyundai, BMW, etc.) |
| **Car Age** | `car_age` | Integer | Vehicle age in years ($2020 - \text{year}$) | 0 to 28 years (Median: 7 years) |
| **Kilometres** | `km_driven` | Integer | Total odometer distance travelled | 1 to 806,599 km (Median: 60,000 km) |
| **Fuel Type** | `fuel` | Categorical | Vehicle fuel powertrain | Petrol, Diesel, CNG, LPG, Electric |
| **Seller Type** | `seller_type` | Categorical | Channel offering the vehicle | Individual, Dealer, Trustmark Dealer |
| **Transmission** | `transmission`| Categorical | Gearbox mechanism | Manual, Automatic |
| **Owner** | `owner` | Categorical | Number of previous registered owners | First, Second, Third, Fourth & Above, Test Drive |
| **Target Price**| `selling_price`| Integer | Actual transaction / listing price in INR | ₹20,000 to ₹89,00,000 (Median: ₹3,50,000) |

---

## 🧹 Data Cleaning & Quality Audit
The raw dataset contains 4,340 rows. Data cleaning verified that there are **0 missing values**. An audit identified **763 exact duplicate listings** across all 8 columns. Retaining exact duplicates across a random train/test split causes data leakage (where the test set memorizes identical training rows). Dropping duplicates yields **3,577 unique records**.

### Quality Audit Before vs. After
| Metric | Raw State | Cleaned State | Quality Resolution |
| :--- | :---: | :---: | :--- |
| **Total Records** | 4,340 | 3,577 | Removed 763 exact duplicates to prevent leakage |
| **Missing Values** | 0 | 0 | 100% complete observations |
| **Unique Brands** | 29 | 29 | Standardised `OpelCorsa` $\rightarrow$ `Opel`, `Land Rover` |
| **Manufacturing Year** | 1992 – 2020 | 1992 – 2020 | Verified genuine historical vehicle entries |
| **Selling Price (Min / Max)**| ₹20,000 / ₹89,00,000 | ₹20,000 / ₹89,00,000 | Verified genuine market extremes (Nano to Audi RS7) |
| **Median Selling Price** | ₹3,50,000 | ₹3,50,000 | Robust central tendency |

---

## 📊 Exploratory Data Analysis & Market Findings
The exploratory suite generates 8 publication-grade charts saved in [`visualizations/`](./visualizations/):

1. **Selling Price Distribution (`selling_price_distribution.png`):**
   - Pronounced right skewness (Median: ₹3.50 Lakh, Mean: ₹4.74 Lakh).
   - Long right tail comprises luxury German marques (BMW, Mercedes-Benz, Audi) reaching up to ₹89.0 Lakh.
2. **Vehicle Depreciation Curve (`price_vs_car_age.png`):**
   - Demonstrates compound exponential decay: used cars lose $\sim 35\text{--}45\%$ of their value in the first 3–4 years, stabilizing into an asymptotic linear depreciation thereafter.
3. **Price vs. Kilometres Driven (`price_vs_km_driven.png`):**
   - Moderate negative correlation ($r = -0.192$) with prices clustering below ₹15 Lakh once odometer mileage exceeds 100,000 km.
4. **Price by Fuel Type (`price_by_fuel.png`):**
   - Diesel vehicles command higher median prices (₹4.50 Lakh) than Petrol equivalents (₹2.70 Lakh) due to torque preference and commercial viability.
5. **Transmission Premium (`price_by_transmission.png`):**
   - Automatic cars command a **+71.4% median price premium** over manual transmissions.
6. **Brand Value Ranking (`brand_avg_selling_price.png`):**
   - Distinct brand tiers: Luxury (Land Rover ₹46.5L, BMW ₹29.5L, Mercedes-Benz ₹28.1L, Audi ₹27.4L), Mid-tier (Jeep, Volvo, Toyota, Ford), Mass-market (Hyundai ₹4.1L, Maruti ₹3.4L, Tata ₹2.7L).
7. **Correlation Heatmap (`correlation_heatmap.png`):**
   - Strongest negative correlation with price is `car_age` ($r = -0.420$), followed by `km_driven` ($r = -0.192$).
8. **Multivariate Interactions (`feature_relationships.png`):**
   - Interaction of Age $\times$ Fuel $\times$ Transmission highlights that luxury diesel automatics maintain the highest value retention over time.

---

## 🤖 Machine Learning Benchmarking & Results
All 4 models were evaluated with **5-Fold Cross-Validation** on the 80% training set ($N = 2,861$), followed by final evaluation on the 20% held-out test set ($N = 716$).

### Actual Measured Model Performance
| Algorithm | Target Space | Mean 5-Fold CV $R^2$ | CV $R^2$ Std Dev | CV MAE (INR) | Held-Out Test $R^2$ | Test MAE (INR) | Test RMSE (INR) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Linear Regression (Best)** | **$\log(1+y)$** | **0.6981** | **$\pm 0.0720$** | **₹1,36,929** | **0.7120** | **₹1,44,221** | **₹3,04,582** |
| **Ridge Regression** | $\log(1+y)$ | 0.6955 | $\pm 0.0901$ | ₹1,38,146 | 0.6884 | ₹1,45,432 | ₹3,16,841 |
| **Random Forest Regressor** | $\log(1+y)$ | 0.6685 | $\pm 0.1198$ | ₹1,40,985 | 0.6275 | ₹1,45,000 | ₹3,46,417 |
| **Gradient Boosting Regressor**| $\log(1+y)$ | 0.6822 | $\pm 0.0996$ | ₹1,36,753 | 0.5437 | ₹1,48,131 | ₹3,83,372 |

### Why Log-Linear Regression Won
Vehicle resale value follows an exponential depreciation formula:
$$\text{Price} \approx \text{BasePrice} \times e^{-\lambda \cdot \text{Age}}$$
Applying the natural logarithm transforms this non-linear dynamic into a strictly linear additive model:
$$\log(1 + \text{Price}) = \beta_0 + \beta_{\text{age}} \cdot \text{Age} + \beta_{\text{km}} \cdot \text{Km} + \sum \beta_i \cdot \text{Brand}_i + \gamma \cdot \text{Trans} + \dots$$
This formulation captures multiplicative brand multipliers and compound depreciation rates, avoiding the boundary overfitting and tree-stepping artifacts of decision trees.

---

## 💡 Model Explainability & Feature Drivers
From the fitted production pipeline (`models/model_metadata.json`), the coefficients represent additive effects in the logarithmic target space ($\beta = \frac{\partial \ln(1+y)}{\partial x}$):

> **Statistical Interpretation Note:** These weights are log-target regression coefficients, not direct Rupee (INR) amounts, and reflect empirical statistical associations within the historical 2020 CarDekho dataset rather than deterministic or causal effects.

1. **Top Positive Value Drivers (Log-Scale Multipliers):**
   - **Luxury Marque Coefficients:** Land Rover ($+1.3205$), Jaguar ($+1.1552$), Mercedes-Benz ($+0.8383$), Mitsubishi ($+0.7992$), Volvo ($+0.7991$), Audi ($+0.7684$), BMW ($+0.6941$).
   - **Transmission Mechanism:** `transmission_Automatic` ($+0.1828$) vs `transmission_Manual` ($-0.1828$). The net contrast ($\Delta \beta = +0.3657$) corresponds to an estimated $\approx +44.2\%$ multiplicative price premium for automatic gearboxes, holding other attributes fixed.
   - **Fuel Powertrain:** `fuel_Diesel` ($+0.3707$) commands a substantial premium over `fuel_Petrol` ($-0.0518$), `fuel_CNG` ($-0.1360$), and `fuel_LPG` ($-0.1829$).
   - **Seller Channel & Fresh Inventory:** `owner_Test Drive Car` ($+0.2275$), `seller_type_Trustmark Dealer` ($+0.1426$).
2. **Top Negative Value Drivers (Depreciation & Wear):**
   - **Vehicle Age (`car_age`):** Standardized coefficient $\beta = -0.4753$ (equivalent to an annual rate of $\approx -0.117$ log-points per year of vehicle age), capturing compound exponential depreciation over time.
   - **Odometer Distance (`km_driven`):** Standardized coefficient $\beta = -0.0355$, reflecting value decay from mechanical wear.
   - **Ownership Penalty:** Progressive log penalty for prior owners: `owner_Second Owner` ($-0.0157$), `owner_Third Owner` ($-0.1116$), `owner_Fourth & Above Owner` ($-0.1289$).

---

## 🖥️ Streamlit Interactive Dashboard
The interactive web portal is located at [`dashboard/app.py`](./dashboard/app.py).

### Dashboard Capabilities:
* **Dynamic Vehicle Valuation:** User selects Brand (29 makes), Manufacturing Year, Mileage, Fuel, Transmission, and Owner; clicking **🚀 Calculate Estimated Selling Price** generates instant resale valuation in INR.
* **Illustrative Typical Error Range (± Test MAE):** Displays a typical error margin around the estimate based on test set MAE (₹1,44,221), clearly distinguishing average absolute error from statistical confidence intervals.
* **Historical Benchmark Scope:** Prominently alerts users that predictions reflect 2020 historical CarDekho listings.
* **Integrated Visualisation Gallery:** Embedded display of all 12 publication-grade figures.
* **Model Diagnostic Reports:** Real-time benchmark table, residual plots, and actual-vs-predicted curves.
* **Dataset Browser:** Multi-filter vehicle inventory browser with CSV export.

---

## 🚀 Installation & Execution Guide

### Verified Environment & Dependency Specifications
* **Tested Python Version:** Python 3.14.6
* **Serialized Scikit-Learn:** `scikit-learn==1.9.1` (The serialized model `car_price_pipeline.joblib` was created with scikit-learn 1.9.1 and must be loaded using the same version to prevent `InconsistentVersionWarning` or unpickling incompatibility; compatibility with earlier versions such as 1.8.0 is not claimed)
* **Tested Joblib Version:** `joblib==1.6.0`

### Step 1: Install Locked Dependencies
```powershell
pip install -r DataScience-Task3-CarPricePrediction/requirements.txt
```

### Step 2: Clean Dataset & Engineer Features
```powershell
python DataScience-Task3-CarPricePrediction/src/data_cleaning.py
```

### Step 3: Generate Exploratory Visualizations (Visuals 1–8)
```powershell
python DataScience-Task3-CarPricePrediction/src/eda.py
```

### Step 4: Train Machine Learning Pipeline
```powershell
python DataScience-Task3-CarPricePrediction/src/train.py
```

### Step 5: Evaluate Model Diagnostics (Visuals 9–12)
```powershell
python DataScience-Task3-CarPricePrediction/src/evaluate.py
```

### Step 6: Run Automated Test Suite (16 Unit Tests)
```powershell
python -m unittest DataScience-Task3-CarPricePrediction/tests/test_pipeline.py
```

### Step 7: Launch Interactive Streamlit Dashboard
```powershell
python -m streamlit run DataScience-Task3-CarPricePrediction/dashboard/app.py
```

---

## ⚠️ Known Limitations & Future Improvements
1. **Historical 2020 Market Valuation Scope:** The dataset consists of 2020 vehicle listings with feature engineering benchmarked to reference year 2020 ($\text{car\_age} = 2020 - \text{year}$). Predictions represent historical 2020 valuations rather than current 2026 market prices. They do not account for subsequent inflation, post-COVID automotive supply disruptions, or regulatory phase-outs (such as the 10-year diesel / 15-year petrol vehicle scrappage mandate in Delhi NCR).
2. **Mechanical & Condition Details:** The CarDekho dataset lacks accident history, insurance validity, service log records, and tyre condition, which strongly influence individual valuations.
3. **Geographical Variance:** Car prices in India vary substantially by state due to road tax differentials (e.g., Delhi vs. Bangalore/Mumbai); state/RTO registration data is not captured in this dataset version.

---

## 📜 Authorship & Attribution
* **Project Name:** Car Price Prediction with Machine Learning
* **Internship:** OASIS INFOBYTE Data Science Internship (Task 3)
* **Data Origin:** CarDekho.com via Kaggle Open Datasets
* **Repository:** [https://github.com/shikhilyadav/OIBSIP](https://github.com/shikhilyadav/OIBSIP)
