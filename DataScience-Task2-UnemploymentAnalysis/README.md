# 🇮🇳 Unemployment Analysis with Python – India
### **OASIS INFOBYTE Data Science Internship — Task 2**

![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458?style=for-the-badge&logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-5.15%2B-3F4F75?style=for-the-badge&logo=plotly)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B?style=for-the-badge&logo=streamlit)
![Data Source](https://img.shields.io/badge/Data_Source-CMIE_CPHS-blue?style=for-the-badge)
![Usage](https://img.shields.io/badge/Usage-Educational_%26_Research-success?style=for-the-badge)

---

## 📌 Project Overview
The **Unemployment Analysis with Python (India)** project is an industry-grade macroeconomic data analytics study developed for the **OASIS INFOBYTE Data Science Internship (Task 2)**. 

The primary objective is to investigate unemployment patterns across **28 Indian States and Union Territories** between **May 2019 and June 2020**, evaluating the catastrophic labor market shocks caused by the **COVID-19 national lockdown** in March–May 2020. The project integrates automated data cleaning, statistical hypothesis testing, publication-grade static visualization, and an interactive **Streamlit Analytics Dashboard**.

---

## 🎯 Problem Statement & Objectives
### Problem Statement
Unemployment is one of the most critical socio-economic indicators influencing national GDP, poverty indices, and consumer purchasing power. In early 2020, the onset of the COVID-19 pandemic and the subsequent enforcement of the world's largest national lockdown (March 24, 2020) precipitated an unprecedented labor crisis in India. Disentangling structural unemployment from pandemic shocks across rural and urban geographies is vital for countercyclical policy formulation.

### Core Objectives
1. **Data Ingestion & Provenance:** Collect and archive authentic historical labor records from the Centre for Monitoring Indian Economy (CMIE) via Kaggle open data repositories.
2. **Data Cleaning & Integrity:** Eliminate whitespace, handle trailing padding rows, parse dates, engineer macro-geographical zones, and generate an audited before-and-after quality report.
3. **Exploratory Data Analysis (EDA):** Quantify central tendency, dispersion, skewness, and extreme values across rural and urban cohorts.
4. **Regional & State Disparities:** Rank states by average unemployment rate and examine regional divergence between northern/eastern industrial hubs and southern/northeastern states.
5. **COVID-19 Shock Assessment:** Compare Pre-COVID baselines (May 2019 – Feb 2020) against COVID/Post-COVID periods (Mar 2020 – Jun 2020) with rigorous distinction between correlation, temporal association, and causation.
6. **Publication Visualizations:** Generate 8 high-resolution figures ($300\text{ dpi}$) with consistent Emerald Green branding.
7. **Interactive Dashboard:** Build a modern Streamlit analytics portal equipped with dynamic KPI cards, multi-parameter filters, and Plotly graphics.

---

## 💻 Tech Stack & Dependencies
* **Core Language:** Python 3.10+ (tested on Python 3.14)
* **Data Manipulation & Processing:** Pandas, NumPy
* **Static Visualizations:** Matplotlib, Seaborn
* **Interactive Visualizations:** Plotly Express, Plotly Graph Objects
* **Web Analytics Dashboard:** Streamlit
* **Notebook Development:** Jupyter Notebook, Nbformat
* **Quality Assurance & Testing:** Python `unittest`

---

## 📂 Project Architecture
```text
DataScience-Task2-UnemploymentAnalysis/
├── data/
│   ├── raw/
│   │   ├── Unemployment_in_India.csv               # Authentic CMIE raw CSV (768 rows)
│   │   └── Unemployment_Rate_upto_11_2020.csv      # State-level dataset with coordinates (267 rows)
│   └── processed/
│       └── unemployment_cleaned.csv                # Standardized cleaned analytical dataset (740 rows)
├── notebooks/
│   └── Unemployment_Analysis.ipynb                 # 27-cell end-to-end executed Jupyter Notebook
├── src/
│   ├── __init__.py                                 # Package initialization
│   ├── data_loader.py                              # Data ingestion & provenance tracking
│   ├── data_cleaning.py                            # Cleaning, schema mapping, & feature engineering
│   ├── analysis.py                                 # Statistical aggregations & COVID shock engine
│   └── visualizations.py                           # 8 high-resolution publication charts generator
├── dashboard/
│   └── app.py                                      # Modern Streamlit interactive dashboard
├── visualizations/
│   ├── unemployment_distribution.png               # Histogram, KDE, & Boxplot
│   ├── regional_unemployment.png                   # Horizontal ranked bar chart (28 states)
│   ├── monthly_trend.png                           # Time series with lockdown annotations
│   ├── state_comparison.png                        # Multi-line comparative trajectory
│   ├── top10_regions.png                           # Top 10 highest unemployment regions
│   ├── correlation_heatmap.png                     # Pearson correlation matrix heatmap
│   ├── covid_impact.png                            # Pre vs. Post COVID sector & state breakdown
│   └── employment_labour_participation.png         # Scatter & regression analysis
├── tests/
│   └── test_pipeline.py                            # Automated unit test suite (12 test cases)
├── README.md                                       # Comprehensive project documentation
├── AUDIT_REPORT.md                                 # Complete technical QA audit report
├── requirements.txt                                # Python dependencies
└── .gitignore                                      # Git exclusion rules
```

---

## 🌐 Dataset Provenance & Data Dictionary
* **Primary Origin:** Centre for Monitoring Indian Economy (CMIE) — Consumer Pyramids Household Survey (CPHS).
* **Provider / Distribution Mirror:** Kaggle Open Data community archive (`Unemployment in India`).
* **Usage & Licensing Terms:** Sourced from public open datasets for educational, analytical, and research applications. Users analyzing this data must attribute CMIE as the originating survey authority. Proprietary commercial CMIE microdata remains governed by CMIE service terms.
* **Direct Archive Mirror URL:** `https://raw.githubusercontent.com/yuvrajsaraogi/Unemployment-Analysis-with-Python/main/Unemployment%20in%20India.csv`
* **Coverage:** 28 Indian States & UTs; Rural and Urban sectors; Monthly frequency (May 31, 2019 to June 30, 2020 — exactly 14 calendar months).

### Data Dictionary
| Variable Name | Raw Header | Data Type | Description |
| :--- | :--- | :---: | :--- |
| `State` | `Region` | String | Indian State or Union Territory name (e.g. Maharashtra, Bihar) |
| `Date` | ` Date` | Datetime | Observation month timestamp (parsed as `%d-%m-%Y`) |
| `Frequency` | ` Frequency` | String | Observation frequency (Monthly: `M`) |
| `Estimated_Unemployment_Rate` | ` Estimated Unemployment Rate (%)` | Float64 | Percentage of active labor force unemployed |
| `Estimated_Employed` | ` Estimated Employed` | Int64 | Absolute estimated count of employed citizens |
| `Estimated_Labour_Participation_Rate` | ` Estimated Labour Participation Rate (%)` | Float64 | Proportion of working-age population active in labor pool |
| `Area` | `Area` | String | Sector classification (`Rural` vs. `Urban`) |
| `Zone` | *Derived* | String | Macro geographic zone (`North`, `South`, `East`, `West`, `Central`, `Northeast`) |
| `COVID_Phase` | *Derived* | String | Pandemic timeline partition (`Pre-COVID` vs. `COVID/Post-COVID`) |

---

## 🧹 Data Cleaning & Quality Audit
The raw dataset contains 768 rows. Data cleaning identified that rows 740 to 767 (28 rows) were trailing empty padding rows in the CSV file with null values across every column. These rows were eliminated.

### Quality Audit Before vs. After
| Dimension | Raw State | Cleaned State | Quality Resolution |
| :--- | :---: | :---: | :--- |
| **Total Rows** | 768 | 740 | Eliminated 28 trailing empty padding lines |
| **Total Columns** | 7 | 13 | Stripped header whitespace, added 6 temporal & zone features |
| **Missing Values** | 196 (in empty rows) | **0** | Clean, non-null observations across all records |
| **Duplicate Records** | 27 (in empty rows) | **0** | Verified zero duplicated observation tuples |
| **Date Format** | String (` 31-05-2019`) | `datetime64[ns]` | Standardized to ISO `%Y-%m-%d` format |
| **Outliers (IQR > 32.73%)** | 35 | 35 | Verified as authentic lockdown shocks (e.g., Puducherry 76.74%) |

---

## 📊 Exploratory Data Analysis & Empirical Findings

### 1. Descriptive Summary Statistics
| Indicator | Mean | Std Dev | Median | Q1 (25%) | Q3 (75%) | Min | Max | Skewness |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Unemployment Rate (%)** | **11.79** | 10.72 | **8.35** | 4.66 | 15.89 | 0.00 | **76.74** | **+2.22** |
| **Employed Headcount** | 5,314,721 | 5,839,769 | 2,746,640 | 1,190,424 | 7,456,645 | 49,420 | 45,777,509 | +2.57 |
| **Labour Participation Rate (%)** | **42.63** | 8.11 | **41.16** | 37.14 | 45.60 | 13.33 | 72.57 | +0.33 |

> *Note on Standard Deviation Calculation:* All standard deviation figures represent sample standard deviations with Bessel's correction ($s = 10.7213\%$, $\text{ddof}=1$), which is statistically appropriate for empirical survey sample data. Population standard deviation with $\text{ddof}=0$ equals $10.7141\%$.

### 2. State & Regional Rankings
* **Highest Average Unemployment:** **Tripura (28.35%)**, **Haryana (26.28%)**, **Jharkhand (20.58%)**, **Bihar (18.92%)**, **Himachal Pradesh (18.54%)**, **Delhi (16.50%)**.
* **Lowest Average Unemployment:** **Meghalaya (4.80%)**, **Odisha (5.66%)**, **Assam (6.43%)**, **Uttarakhand (6.58%)**, **Gujarat (6.66%)**.
* **Macro Zone Divergence:** Northern and Eastern zones experienced elevated volatility ($>14\%$) relative to Western and Southern zones.

### 3. Correlation Dynamics
* **Unemployment Rate vs. Labour Participation ($r \approx 0.003$):** Weak empirical correlation. During severe lockdown months, discouraged workers ceased active job seeking, which compressed the labor participation rate while unemployment spiked.
* **Unemployment Rate vs. Employed Count ($r \approx -0.223$):** Negative correlation reflecting workforce shrinkage during industrial suspensions.
* *Methodological Note:* Correlation does **not** equal causation.

---

## 🦠 COVID-19 Lockdown Shock Analysis
* **Pre-COVID Baseline (May 2019 – Feb 2020, 536 records):** **9.51%** mean unemployment rate.
* **COVID/Post-COVID Period (Mar 2020 – Jun 2020, 204 records):** **17.77%** mean unemployment rate.
* **Absolute Shock:** **+8.26 percentage points**.
* **Relative Surge:** **+86.91% increase** nationwide.

### Sectoral Vulnerability: Urban vs. Rural
| Sector | Pre-COVID Mean (%) | Post-COVID Mean (%) | Absolute Surge (% pts) | Relative Increase (%) |
| :--- | :---: | :---: | :---: | :---: |
| **Urban** | 10.84 | **19.28** | **+8.43** | **+77.79%** |
| **Rural** | 8.09 | **16.18** | **+8.09** | **+99.90%** |

### Empirical Observations vs. Economic Hypotheses
* **Directly Observed Empirical Findings:** Urban sectors experienced higher nominal baseline unemployment and reached higher peak levels (19.28%) due to contact-intensive commercial closures. Conversely, rural sectors experienced a sharper relative percentage surge (+99.90% vs. +77.79% urban) from their lower pre-crisis baseline.
* **Contextual Economic Hypotheses (Non-Causal External Context):**
  - *Rabi Harvest Buffer:* Macroeconomic reports (e.g., *Reserve Bank of India Monetary Policy Report 2020*) note that agricultural exemptions during the April 2020 Rabi crop harvest provided an initial absorptive cushion for rural labor.
  - *MGNREGA Countercyclical Support:* Public works enrollment under MGNREGA has been cited in literature as an emergency income stabilizer for distressed rural households.
  - *Reverse Migration Burden:* Economic surveys (e.g., *Economic Survey of India 2020-21*) highlight significant reverse migration of informal workers from metropolitan centers back to rural origin states (such as Bihar, Jharkhand, and Uttar Pradesh), which placed delayed labor absorption strain on village economies in May–June 2020.
  - *Survey Boundary Note:* The CMIE dataset measures self-reported labor force participation and does not track migration streams or fiscal disbursements directly.

---

## 📈 Visualizations Gallery
All high-resolution figures are located in [`visualizations/`](./visualizations/):

| Visual Artifact | Chart Type | Key Insight |
| :--- | :--- | :--- |
| `unemployment_distribution.png` | Boxplot + Histogram + KDE | Shows pronounced right skew ($+1.89$) with pandemic tail outliers |
| `regional_unemployment.png` | Horizontal Ranked Bar Chart | Complete 28-state benchmark relative to national mean ($11.79\%$) |
| `monthly_trend.png` | Time Series Line with CI | Highlights April-May 2020 peak shock reaching $23.5\% - 24.6\%$ |
| `state_comparison.png` | Multi-line Comparative Trajectory | Contrasts trajectories of Maharashtra, UP, Bihar, Delhi, & Tamil Nadu |
| `top10_regions.png` | Vertical Bar Chart with Data Labels | Highlights the 10 most crisis-impacted regional labor markets |
| `correlation_heatmap.png` | Pearson Correlation Heatmap | Quantifies relationships between Unemployment, Employed, and LPR |
| `covid_impact.png` | Grouped Bar Chart Comparison | Visualizes Pre vs Post COVID divergence across Rural and Urban sectors |
| `employment_labour_participation.png` | Scatter with Regression Trendline | Depicts labor force participation compression during crisis periods |

---

## 🖥️ Streamlit Interactive Dashboard
The interactive web application is located at [`dashboard/app.py`](./dashboard/app.py).

### Dashboard Capabilities:
1. **Dynamic Top KPI Cards:** Live recalculations of Average Unemployment, Highest Region, Lowest Region, and Labour Participation based on user filters.
2. **Multi-Parameter Sidebar Filters:** Filter simultaneously by Sector (All, Rural, Urban), Macro Zone, Specific States, COVID Period, and Observation Time Window.
3. **Interactive Plotly Visualizations:** Hover tooltips, zoom, pan, and dynamic data filtering.
4. **Structured Tab Layout:**
   - *Tab 1: Overview & Distribution*
   - *Tab 2: Regional & State-Wise Analysis*
   - *Tab 3: Monthly Trends & Trajectories*
   - *Tab 4: COVID-19 Pandemic Impact*
   - *Tab 5: Employment & Labour Market Participation*
   - *Tab 6: Economic Insights & Policy Recommendations*

```bash
# Option A: From inside DataScience-Task2-UnemploymentAnalysis/
python -m streamlit run dashboard/app.py

# Option B: From OIBSIP root workspace
python -m streamlit run DataScience-Task2-UnemploymentAnalysis/dashboard/app.py
```
> **Note for Windows PowerShell:** Always prefer `python -m streamlit run` rather than bare `streamlit run` to ensure execution regardless of whether the Python Scripts folder is added to your Windows user `PATH`. An automatic fallback wrapper is also embedded in `dashboard/app.py` so accidental execution via `python dashboard/app.py` forwards seamlessly to Streamlit.

---

## 🚀 Installation & Execution Guide

### 1. Navigate to Project Directory
```bash
cd DataScience-Task2-UnemploymentAnalysis
```

### 2. Create and Activate Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Required Dependencies
```bash
pip install -r requirements.txt
```

### 4. Execute End-to-End Pipeline
```bash
# Step 1: Ingest & verify raw data
python src/data_loader.py

# Step 2: Clean data & engineer features
python src/data_cleaning.py

# Step 3: Compute macroeconomic analysis & KPIs
python src/analysis.py

# Step 4: Generate all 8 publication visualizations
python src/visualizations.py

# Step 5: Run automated test suite (12 tests)
# From inside DataScience-Task2-UnemploymentAnalysis/:
python -m unittest tests/test_pipeline.py
# Or from OIBSIP root:
python -m unittest DataScience-Task2-UnemploymentAnalysis/tests/test_pipeline.py

# Step 6: Launch Streamlit Dashboard
python -m streamlit run dashboard/app.py
```

---

## 💼 Policy & Strategic Recommendations
1. **Urban Employment Guarantee:** Implement an urban equivalent to the rural MGNREGA scheme to cushion informal daily-wage earners against urban economic freezes.
2. **Universal Social Security Portability:** Expand portable ration (One Nation One Ration Card) and affordable rental housing schemes to safeguard migrant workers during inter-state dislocations.
3. **High-Frequency Labor Market Monitoring:** Establish municipal-level labor observatories to deploy targeted stimulus before broad macroeconomic metrics deteriorate.

---

## ⚠️ Analytical Limitations & Future Scope
* **Temporal Boundary:** CMIE dataset spans May 2019 to June 2020. Incorporating subsequent years (2021–2024) would enable long-term post-pandemic recovery modeling.
* **Informal Sector Measurement:** Self-employed and seasonal agricultural laborers may experience underemployment rather than outright unemployment, which monthly survey questionnaires can partially undercount.
* **Future Extension:** Implement ARIMA / Prophet time-series forecasting models to predict labor recovery trajectories.

---

## 👤 Author & Acknowledgments
* **Project:** Unemployment Analysis with Python – India
* **Internship Program:** OASIS INFOBYTE Internship in Data Science (Task 2)
* **Author:** Data Science Intern
* **Data Attribution:** Centre for Monitoring Indian Economy (CMIE)
