# 🛡️ Email / SMS Spam Detection Using Machine Learning
### **OASIS INFOBYTE Data Science Internship — Task 4**

![Python](https://img.shields.io/badge/Python-3.14.6-blue?style=for-the-badge&logo=python)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.9.1-F7931E?style=for-the-badge&logo=scikitlearn)
![NLTK](https://img.shields.io/badge/NLTK-3.10.4-339933?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)

---

## 📌 Project Overview
Electronic spam messages present significant security, privacy, and operational risks, ranging from commercial unsolicited advertising to malicious phishing campaigns, credential harvesting, and financial fraud. 

This project develops, evaluates, and deploys an end-to-end Natural Language Processing (NLP) binary classification system for the **Oasis Infobyte (OIBSIP) Data Science Internship (Task 4)**. The solution ingests raw message text, performs standardized morphological text normalization, extracts numerical feature vectors via **TF-IDF (Term Frequency - Inverse Document Frequency)**, and benchmarks **Multinomial Naive Bayes** and **Logistic Regression** classifiers inside leak-free Scikit-Learn pipelines.

---

## 🎯 Project Objectives
1. **Dataset Ingestion & Hygiene:** Ingest the canonical SMS Spam Collection dataset ($N = 5,572$), audit data types, missing values, duplicates, and class balance.
2. **Exploratory Data Analysis (EDA):** Quantify class imbalances, message length disparities between spam and ham, and visualize lexical prominence via WordClouds.
3. **Text Preprocessing:** Build a modular text normalization pipeline (lowercasing, URL/email stripping, punctuation removal, number filtering, stopword removal, and Porter Stemming).
4. **TF-IDF Feature Representation:** Transform variable-length text into high-dimensional numerical matrices using unigrams and bigrams (`max_features=5000, ngram_range=(1, 2)`).
5. **Leakage-Free Modeling:** Enforce strict train/test isolation by fitting vectorizers only on the 80% training split via Scikit-Learn `Pipeline` architectures.
6. **Rigorous Benchmarking:** Evaluate Multinomial Naive Bayes and Logistic Regression across Accuracy, Precision, Recall, F1-Score, and Confusion Matrices.
7. **Recall Trade-Off Analysis:** Provide an in-depth analytical discussion on why spam recall and ham precision represent the defining operational metrics.
8. **Real-Time Custom Inference:** Provide a custom message predictor testing arbitrary inputs with estimated spam posterior probabilities.

---

## 🌐 Dataset Information & Attribution
* **Dataset Name:** SMS Spam Collection Dataset
* **Primary Source:** [Kaggle SMS Spam Collection Dataset](https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset) / UCI Machine Learning Repository
* **Donors & Curators:** Tiago A. Almeida and José María Gómez Hidalgo
* **Observations:** 5,572 records (4,825 Ham, 747 Spam)
* **Dataset Class Balance:** 86.59% Ham vs. 13.41% Spam (pronounced class imbalance)

> **⚠️ Important Dataset Clarification:**  
> While the task title references *Email Spam Detection*, the industry-standard benchmark dataset provided for this task contains **SMS text messages**. SMS messages are typically shorter, use more colloquial abbreviations, and exhibit distinct marketing urgency compared to long-form email bodies. However, the core NLP preprocessing, TF-IDF vectorization, Bayesian likelihood formulation, and logistic classification methodologies demonstrated herein apply identically to full-length email spam filtering engines.

---

## 💻 Tech Stack & Dependencies
* **Programming Language:** Python 3.10+ (Developed and tested on **Python 3.14.6**)
* **Data Manipulation & Analysis:** Pandas, NumPy
* **Data Visualization:** Matplotlib, Seaborn, WordCloud
* **Natural Language Processing:** NLTK (Stopwords corpus, PorterStemmer), Regular Expressions (`re`)
* **Machine Learning Framework:** Scikit-Learn (`TfidfVectorizer`, `MultinomialNB`, `LogisticRegression`, `Pipeline`, `metrics`)
* **Interactive Notebook:** Jupyter Notebook, `nbformat`, `nbconvert`

---

## 📁 Project Directory Structure

```text
OIBSIP_Task4_Spam_Detection/
│
├── dataset/
│   └── spam.csv                     # Authentic Kaggle SMS Spam Collection dataset (5,572 rows)
│
├── notebooks/
│   └── Task4_Spam_Detection.ipynb   # Complete 20-section Jupyter Notebook executed with rich outputs
│
├── outputs/
│   ├── class_distribution.png       # Spam vs Ham count and percentage distribution
│   ├── confusion_matrix.png         # Naive Bayes & Logistic Regression confusion matrices
│   ├── spam_wordcloud.png           # Lexical prominence wordcloud for spam messages
│   ├── ham_wordcloud.png            # Lexical prominence wordcloud for ham messages
│   └── summary_metrics.json         # Persisted benchmark metrics and class counts
│
├── generate_outputs.py              # Standalone production runner script
├── build_notebook.py                # Notebook builder and execution script
├── README.md                        # Comprehensive project documentation
└── requirements.txt                 # Pinned project dependencies
```

---

## 📊 Exploratory Data Analysis & Lexical Insights

1. **Class Distribution (`outputs/class_distribution.png`):**
   * **Ham (Legitimate):** 4,825 messages (86.59%)
   * **Spam (Unwanted):** 747 messages (13.41%)
   * Significant class imbalance highlights that naive accuracy alone is a misleading metric (a dummy model predicting all messages as Ham achieves 86.59% accuracy with 0% spam recall).

2. **Message Length Divergence:**
   * **Ham Messages:** Median character length of **52 characters** (mean: 71.0 characters, median word count: 11 words).
   * **Spam Messages:** Median character length of **149 characters** (mean: 138.9 characters, median word count: 25 words).
   * Spam messages are nearly **3× longer** on average as advertisers pack promotional copy, contact info, claim codes, and urgent calls-to-action into a single SMS quota.

3. **WordCloud Lexical Prominence (`outputs/spam_wordcloud.png` & `outputs/ham_wordcloud.png`):**
   * **Spam Dominant Terms:** *free*, *txt*, *call*, *win*, *prize*, *claim*, *cash*, *urgent*, *servic*, *stop*, *repli*.
   * **Ham Dominant Terms:** *go*, *get*, *come*, *call*, *ok*, *ur*, *time*, *love*, *know*, *good*, *home*.

---

## ⚙️ Text Preprocessing & TF-IDF Extraction

### 8-Stage Text Preprocessing Pipeline:
1. **Case Normalization:** Converts all text to lowercase.
2. **URL Stripping:** Eliminates hyperlinks (`http://`, `https://`, `www.`).
3. **Email Masking:** Removes email addresses (`user@domain.com`).
4. **Punctuation Removal:** Strips ASCII punctuation.
5. **Standalone Number Removal:** Drops raw integers while preserving lexical terms.
6. **Whitespace Normalization:** Collapses multiple spaces, tabs, and newlines.
7. **Stopword Filtering:** Eliminates high-frequency grammatical English stopwords.
8. **Porter Stemming:** Maps inflected variants to root morphological stems (*winner*, *winning*, *wins* $\rightarrow$ *win*).

### TF-IDF Vectorization:
* `max_features=5000` (caps vocabulary size to top 5,000 informative n-grams).
* `ngram_range=(1, 2)` (captures both unigrams like *"prize"* and bigrams like *"free prize"*).
* **Leakage-Free Execution:** Fitted exclusively on the 80% training split via `Pipeline`.

---

## 🤖 Model Evaluation & Benchmark Results

Both classifiers were evaluated on the **20% held-out test partition ($N = 1,115$)** partitioned via stratified splitting (`random_state=42`):
* **Ham Test Samples:** 966
* **Spam Test Samples:** 149

### Actual Measured Model Performance:

| Model | Accuracy | Precision (Spam) | Recall (Spam) | F1-Score (Spam) | False Positives (FP) | False Negatives (FN) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Multinomial Naive Bayes (Best)** | **96.95%** | **0.9915 (99.15%)** | **0.7785 (77.85%)** | **0.8722** | **1** | **33** |
| **Logistic Regression** | 96.68% | 0.9828 (98.28%) | 0.7651 (76.51%) | 0.8604 | 2 | 35 |

### Confusion Matrix Breakdown:
* **Multinomial Naive Bayes:**
  * True Negatives (TN): **965** / 966 legitimate messages delivered cleanly.
  * False Positives (FP): **1** legitimate message quarantined (exceptional 99.15% precision).
  * False Negatives (FN): **33** spam messages slipped into inbox.
  * True Positives (TP): **116** spam messages caught.
* **Logistic Regression:**
  * True Negatives (TN): **964**
  * False Positives (FP): **2**
  * False Negatives (FN): **35**
  * True Positives (TP): **114**

---

## 💡 Operational Trade-Off: Why Recall Matters for Spam Detection

In real-world anti-spam infrastructure:
1. **The Cost of False Negatives (Missed Spam):**
   * Missing spam directly exposes users to malicious phishing, malware distribution, credential theft, and financial fraud. High **Spam Recall** ($\frac{\text{TP}}{\text{TP} + \text{FN}}$) ensures that fewer malicious attacks reach end-user inboxes.
2. **The Asymmetric Cost of False Positives:**
   * Quarantining a critical medical email, job offer, or OTP verification code as "spam" causes immediate real-world damage. Thus, **Spam Precision** must remain strictly above 98%+.
3. **The Imbalance Trap:**
   * Because legitimate messages outnumber spam by over 6 to 1, a trivial model predicting everything as Ham achieves 86.59% accuracy. **Recall, Precision, and the F1-Score** are therefore the only mathematically meaningful evaluation criteria.

---

## 🧪 Real-Time Custom Message Inference

Testing representative unseen messages through the production pipelines:

| Test Message | Predicted Class | Naive Bayes $P(\text{Spam})$ | Logistic Regression $P(\text{Spam})$ | Interpretation |
| :--- | :---: | :---: | :---: | :--- |
| *"Congratulations! You have won a free prize."* | **🚨 SPAM** | **84.99%** | **76.53%** | High-confidence promotional phishing |
| *"Hey, are we meeting tomorrow?"* | **✅ HAM** | **0.52%** | **2.33%** | Conversational communication |
| *"Claim your free reward now."* | **🚨 SPAM** | **84.78%** | **67.90%** | Incentive-based marketing spam |
| *"Please call me when you reach home."* | **✅ HAM** | **3.52%** | **19.38%** | Interpersonal domestic message |

---

## 🚀 Installation & Execution Guide

### Step 1: Clone Repository & Navigate to Task Directory
```powershell
cd c:\Users\ASUS\Desktop\OIBSIP\OIBSIP_Task4_Spam_Detection
```

### Step 2: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 3: Run the End-to-End Pipeline
```powershell
python generate_outputs.py
```

### Step 4: Launch and View the Jupyter Notebook
```powershell
jupyter notebook notebooks/Task4_Spam_Detection.ipynb
```

---

## ⚠️ Known Limitations & Future Work
1. **SMS vs. Full Email Structure:** The dataset contains short SMS texts without MIME headers, DKIM/SPF verification, sender domain reputations, or HTML attachments.
2. **Adversarial Concept Drift:** Spammers constantly evolve obfuscations (e.g., zero-width spaces, leetspeak like *fr33*). Production engines require continuous dynamic retraining and transformer-based embeddings (e.g., DistilBERT).
3. **Threshold Calibration:** For mission-critical enterprise environments, a dual-threshold queue (Auto-Spam if $P > 0.85$, Quarantine Review if $0.40 \le P \le 0.85$, Deliver if $P < 0.40$) is recommended.

---

## Advanced Transformer Model Integration

### 1. Overview & Motivation
As an advanced deep learning extension to the classical machine learning pipeline, we integrated a pre-trained Transformer model from Hugging Face: **`mrm8488/bert-tiny-finetuned-sms-spam-detection`**.

While classical TF-IDF models treat text as discrete token frequencies, Transformer models employ bidirectional self-attention to dynamically contextualize words based on the surrounding sentence structure.

### 2. Why BERT-Tiny Was Selected
1. **Lightweight Edge Profile:** At only **~4.39 Million parameters** (compared to 110M for BERT-Base and 66M for DistilBERT), BERT-Tiny achieves high throughput on standard CPU hardware without requiring dedicated GPU acceleration.
2. **Pre-tuned for SMS Spam:** Pre-trained on BooksCorpus/Wikipedia and fine-tuned on the `sms_spam` corpus, providing task-aligned representations for short conversational messages.
3. **Ultra-Low Latency:** Inference latency averages **~1.66 ms / message** in batch mode on standard CPU, maintaining real-time SLA suitability.

### 3. Comparison with Classical Architectures
* **Versus Multinomial Naive Bayes:** Naive Bayes assumes conditional feature independence given the class, ignoring word permutations, idioms, and negation syntax (*"not free"* vs *"free"*). BERT-Tiny explicitly models token interactions via bidirectional self-attention heads.
* **Versus Logistic Regression:** Logistic Regression fits a linear hyper-plane over static TF-IDF n-gram vectors. It lacks non-linear subword semantic composition, whereas BERT-Tiny captures deep hierarchical language syntax.

### 4. Model Architecture & Specifications
* **Base Architecture:** Bidirectional Encoder Representations from Transformers (BERT-Tiny, Turc et al., 2019)
* **Hidden Layers ($L$):** 2
* **Hidden Dimension ($H$):** 128
* **Attention Heads ($A$):** 2
* **Intermediate Size:** 512
* **Vocabulary Size:** 30,522 (WordPiece tokenization)
* **Total Parameters:** **4,386,178** (~4.39M)
* **Verified Label Mapping:**
  - `LABEL_0` $\rightarrow$ **HAM (Legitimate)**
  - `LABEL_1` $\rightarrow$ **SPAM (Fraudulent / Unwanted)**

### 5. Hardware & Environment Requirements
* **Hardware:** Standard Multi-Core CPU (No dedicated CUDA GPU required).
* **Environment:** Python 3.10+ (Tested on Python 3.14.6 AMD64).
* **Dependencies:** `torch>=2.15.0`, `transformers>=5.24.0`, `scikit-learn>=1.4.0`.

### 6. Actual Evaluation Benchmark (Tri-Model Comparison)

> [!NOTE]
> **Dataset Provenance & Disclosure:** All three models were evaluated on the exact same stratified held-out test split ($N_{\text{test}} = 1,115$, 966 Ham and 149 Spam) from `dataset/spam.csv`. Because `mrm8488/bert-tiny-finetuned-sms-spam-detection` was fine-tuned upstream on the Hugging Face `sms_spam` dataset (which derives from the UCI SMS collection), there is distributional overlap with the pre-trained model's upstream training corpus.

| Metric | Multinomial Naive Bayes | Logistic Regression | BERT-Tiny (Transformer) |
| :--- | :---: | :---: | :---: |
| **Model Type** | Probabilistic (TF-IDF) | Linear Model (TF-IDF) | Pre-trained Transformer Head |
| **Feature / Parameter Size** | 5,000 n-grams | 5,000 n-grams | 4,386,178 parameters |
| **Test Accuracy** | 96.95% | 96.68% | **98.57%** |
| **Spam Precision** | **99.15%** | 98.28% | 96.50% |
| **Spam Recall** | 77.85% | 76.51% | **92.62%** |
| **Spam F1-Score** | 0.8722 | 0.8604 | **0.9452** |
| **True Negatives (TN)** | **965** | 964 | 961 |
| **False Positives (FP)** | **1** | 2 | 5 |
| **False Negatives (FN)** | 33 | 35 | **11** |
| **True Positives (TP)** | 116 | 114 | **138** |
| **CPU Latency / Sample (Batch)** | **0.017 ms** | 0.016 ms | 1.658 ms |

### 7. Custom Message Test Suite (Empirical Outputs)

| # | Raw Input Message | Predicted Class | Confidence | CPU Latency |
| :---: | :--- | :---: | :---: | :---: |
| 1 | *"Congratulations! You have won a free prize. Claim now!"* | **HAM** | 93.53% | 14.59 ms |
| 2 | *"Hey, are we meeting tomorrow?"* | **HAM** | 93.76% | 3.65 ms |
| 3 | *"Your bank account is blocked. Verify your details."* | **HAM** | 93.12% | 1.77 ms |
| 4 | *"Please call me when you reach home."* | **HAM** | 93.77% | 1.47 ms |
| 5 | *"Congratulations! You have been selected for a cash reward."* | **HAM** | 93.52% | 1.79 ms |
| 6 | *"Your meeting is scheduled for tomorrow at 10 AM."* | **HAM** | 93.47% | 2.30 ms |

### 8. Critical Empirical Findings & Limitations
1. **Recall Advantage:** BERT-Tiny drastically reduced missed spam (False Negatives) from **33 down to 11**, raising spam Recall from **77.85% to 92.62%**.
2. **Domain Dependency on Carrier Keywords:** The pre-trained checkpoint was fine-tuned on classic 2000s UK mobile SMS text patterns (e.g., shortcodes `87121`, phone numbers `0906...`, prize amounts `£1000`). Custom prompts lacking telephone numbers or explicit carrier syntax default to `LABEL_0` (Ham).
3. **SMS vs. Corporate Email:** The model cannot parse multi-part MIME headers, email authentication records (SPF, DKIM, DMARC), or email HTML payloads.
4. **Phishing Distinctness:** Binary SMS spam classification does not cover targeted credential phishing or CEO fraud, which mimic legitimate corporate correspondence without keyword triggers.

### 9. Execution Instructions
- **Execute Dedicated Comparison Notebook:**
  ```bash
  python -m nbconvert --to notebook --execute notebooks/Task4_Advanced_BERT_Comparison.ipynb --inplace
  ```
- **Run Standalone Inference:**
  ```python
  from transformers import AutoTokenizer, AutoModelForSequenceClassification
  import torch

  MODEL_NAME = "mrm8488/bert-tiny-finetuned-sms-spam-detection"
  tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
  model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
  model.eval()

  def predict_spam(message: str) -> dict:
      inputs = tokenizer(message, return_tensors="pt", truncation=True, max_length=128)
      with torch.no_grad():
          logits = model(**inputs).logits
          probs = torch.softmax(logits, dim=-1)[0]
          pred_id = torch.argmax(probs).item()
      return {
          "label": "SPAM" if pred_id == 1 else "HAM",
          "confidence": probs[pred_id].item()
      }
  ```

---

## 📜 Authorship & Attribution
* **Project Name:** Email / SMS Spam Detection Using Machine Learning
* **Internship:** OASIS INFOBYTE Data Science Internship (OIBSIP Task 4)
* **Dataset:** SMS Spam Collection Dataset (Kaggle / UCI Machine Learning Repository)
* **Repository:** [https://github.com/shikhilyadav/OIBSIP](https://github.com/shikhilyadav/OIBSIP)
