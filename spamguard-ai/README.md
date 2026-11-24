# 🛡️ SpamGuard AI
> **Enterprise Threat Intelligence & Hybrid NLP Security Platform**  
> *Intelligent Message Security. Powered by NLP & Transformer Abstention Routing.*

---

## 📌 Executive Overview

**SpamGuard AI** transforms the completed Oasis Infobyte (OIBSIP) Data Science Internship research into a production-grade cybersecurity SaaS web application. Built for enterprise Security Operations Center (SecOps) analysts, SpamGuard AI provides deep packet inspection of SMS and email messages, multi-model probability scoring, structural threat extraction, and calibrated human-in-the-loop triage routing.

All historical work, original Task 4 benchmarks, Task 5 independent audit metrics, notebooks, and models are strictly preserved without modification.

---

## 🏛️ System Architecture

```
                                 ┌─────────────────────────┐
                                 │   Incoming SMS / Msg    │
                                 └────────────┬────────────┘
                                              │
                      ┌───────────────────────┴───────────────────────┐
                      ▼                                               ▼
      ┌───────────────────────────────┐               ┌───────────────────────────────┐
      │   Structural Threat Engine    │               │    NLP Inference Pipeline     │
      │  (Regex Heuristics & MITRE)   │               │   (Tokenization & Ensembles)  │
      └───────────────┬───────────────┘               └───────────────┬───────────────┘
                      │                                               │
                      │   - Reverse Billing Shortcodes                ├─► Multinomial Naive Bayes (MNB)
                      │   - Dial-in Vishing Traps                     ├─► Logistic Regression (LR)
                      │   - Deceptive URL Obfuscation                 └─► BERT-Tiny Transformer (4.39M)
                      │                                               │
                      └───────────────────────┬───────────────────────┘
                                              ▼
                             ┌─────────────────────────────────┐
                             │    Calibrated Hybrid Triage     │
                             │  (Dual-Threshold Abstention)    │
                             └────────────────┬────────────────┘
                                              │
             ┌────────────────────────────────┼────────────────────────────────┐
             ▼                                ▼                                ▼
  [ p_spam >= 0.60 ]               [ 0.10 < p < 0.60 ]                [ p_spam <= 0.10 ]
  Automated SPAM Quarantine       Human Review Queue (19.1%)          Automated HAM Clearance
 (Selective Acc: 96.66%)          (70.68% Spam Concentration)        (Selective Acc: 96.66%)
```

---

## 📊 Audited Benchmark Results (Task 4 & Task 5)

SpamGuard AI transparently reports both **In-Distribution** (UCI SMS Collection) and **Out-of-Distribution Independent Test** (Task 5, $N=1,000$ modern unseen SMS) metrics:

| Model Architecture | In-Distribution Accuracy (UCI) | In-Distribution Recall | Independent Test Accuracy (Task 5) | Independent Test Recall (Task 5) | False Negatives (Task 5) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Multinomial Naive Bayes** | 96.95% | 77.85% | 53.50% | 7.20% | 464 / 500 |
| **Logistic Regression** | 96.68% | 76.51% | 54.10% | 8.40% | 458 / 500 |
| **BERT-Tiny Transformer** | 98.57% | 92.62% | 87.10% | 76.60% | 117 / 500 |
| **SpamGuard Hybrid Triage** | **98.57%** | **92.62%** | **96.66% (Selective)** | **95.89% (Selective)** | **15 (Automated)** |

### 🔍 Key Audited Takeaways
1. **Vocabulary Drift in Classical Models:** Naive Bayes experiences extreme recall collapse (7.20%) when presented with modern phishing and smishing templates, missing 464 out of 500 spam messages.
2. **Transformer Robustness:** BERT-Tiny's subword tokenization provides high generalization (87.10% accuracy, 76.60% recall).
3. **Hybrid Abstention Layer:** By abstaining when $0.10 < p_{\text{spam}} < 0.60$ (191 messages routed to human review), automated selective accuracy rises to **96.66%** with **80.90% coverage**. The review queue successfully captures 135 spam messages (70.68% spam concentration).

---

## 📁 Repository Structure

```
spamguard-ai/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                  # FastAPI server & lifespan model loading
│   │   ├── config.py                # Audited thresholds & CORS configuration
│   │   ├── models.py                # Pydantic schemas
│   │   ├── ml/
│   │   │   ├── preprocessor.py      # Case folding, URL/punctuation stripping, stemming
│   │   │   ├── model_service.py     # Singleton loader for MNB, LR, and BERT-Tiny
│   │   │   └── hybrid_engine.py     # Dual-threshold triage evaluation
│   │   ├── services/
│   │   │   ├── threat_detector.py   # Heuristic pattern extractor & MITRE mapping
│   │   │   └── history_store.py     # In-memory session audit trail
│   │   └── routers/
│   │       ├── analyze.py           # POST /api/analyze
│   │       ├── models.py            # GET /api/models
│   │       ├── metrics.py           # GET /api/metrics/benchmark, GET /api/metrics/analytics
│   │       ├── history.py           # GET /api/history, DELETE /api/history
│   │       └── threat_intel.py      # GET /api/threat-intel
│   ├── test_api.py                  # Automated backend validation suite
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   ├── api/client.js            # Fetch API client
    │   ├── components/
    │   │   ├── common/              # StatCard, ModelScoreCard, ThreatSignalsView
    │   │   └── layout/              # Sidebar, Topbar, Layout shell
    │   ├── pages/
    │   │   ├── OverviewPage.jsx             # KPI dashboard & detection trend
    │   │   ├── MessageAnalyzerPage.jsx      # Live inspection & forensic test payloads
    │   │   ├── ModelIntelligencePage.jsx    # Model registry & triage specifications
    │   │   ├── PerformanceAnalyticsPage.jsx # Audited confusion matrices & charts
    │   │   ├── ThreatIntelligencePage.jsx   # Heuristic indicators & MITRE ATT&CK
    │   │   ├── ScanHistoryPage.jsx          # Searchable, filterable session history
    │   │   └── SettingsPage.jsx             # Enforced parameters & privacy notice
    │   ├── App.jsx
    │   ├── main.jsx
    │   └── index.css                # Dark Cybersecurity theme (#080D18, #00F5A0)
    ├── package.json
    ├── vite.config.js
    └── tailwind.config.js
```

---

## 🚀 Quickstart Guide

### 1. Start the FastAPI Backend
```bash
cd spamguard-ai/backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
- API Documentation (Swagger): `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/api/health`

### 2. Start the React Frontend
```bash
cd spamguard-ai/frontend
npm.cmd run dev
```
- Web Application: `http://localhost:3000`

### 3. Run Backend Validation Test Suite
```bash
python spamguard-ai/backend/test_api.py
```

### 4. Build Production Frontend Bundle
```bash
cd spamguard-ai/frontend
npm.cmd run build
```

---

## 🔒 Privacy & Compliance
SpamGuard AI operates under a **zero-retention** model: raw payloads are processed exclusively in RAM during the lifetime of the inference request, and scan history is maintained only in transient session memory.
