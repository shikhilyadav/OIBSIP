"""
Independent Validation Benchmark Script
OIBSIP Task 5: Independent Evaluation of BERT-Tiny & Naive Bayes on Unseen Modern SMS Data
"""

import time
import json
import urllib.request
import io
import re
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import torch
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# NLTK Stopwords fallback
try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.stem import PorterStemmer
    nltk_path = Path("OIBSIP_Task4_Spam_Detection/nltk_data")
    if nltk_path.exists():
        nltk.data.path.insert(0, str(nltk_path.resolve()))
    STOP_WORDS = set(stopwords.words("english"))
except Exception:
    from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
    STOP_WORDS = set(ENGLISH_STOP_WORDS)

stemmer = PorterStemmer()

def preprocess_text(text: str) -> str:
    """Exact preprocessing pipeline from Task 4."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    text = re.sub(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", " ", text)
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\b\d+\b", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    tokens = [stemmer.stem(w) for w in text.split() if w not in STOP_WORDS and len(w) > 1]
    return " ".join(tokens)

print("=== Step 1: Downloading & Verifying Independent Dataset ===")
# Load original Task 4 training dataset to ensure exact zero overlap
orig_df = pd.read_csv("OIBSIP_Task4_Spam_Detection/dataset/spam.csv", encoding="latin-1")
orig_df = orig_df[["v1", "v2"]].rename(columns={"v1": "label", "v2": "message"}).dropna()
orig_df["clean"] = orig_df["message"].apply(preprocess_text)
orig_df["y"] = orig_df["label"].map({"ham": 0, "spam": 1})

# Train unchanged Naive Bayes model on Task 4 training split (80:20 split, seed 42)
X_train_orig, _, y_train_orig, _ = train_test_split(
    orig_df["clean"], orig_df["y"], test_size=0.20, random_state=42, stratify=orig_df["y"]
)
nb_pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(max_features=5000, ngram_range=(1, 2))),
    ("clf", MultinomialNB(alpha=1.0))
])
nb_pipeline.fit(X_train_orig, y_train_orig)
print("Trained reference Naive Bayes on Task 4 training data (zero leakage from independent data).")

# Download Shaghayegh-hp Smishing Dataset
url = "https://raw.githubusercontent.com/shaghayegh-hp/Smishing_Dataset/main/Combined-Labeled-Dataset.csv"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    raw_content = resp.read()

df_remote = pd.read_csv(io.BytesIO(raw_content))
print(f"Downloaded remote candidate dataset with {len(df_remote):,} rows.")

# Provenance verification & overlap filtering
uci_lower_msgs = set(orig_df["message"].str.strip().str.lower())
df_remote["msg_clean"] = df_remote["message"].astype(str).str.strip()
df_remote["msg_lower"] = df_remote["msg_clean"].str.lower()

# Filter out rows with exact or lowercased overlap with UCI corpus
df_no_overlap = df_remote[~df_remote["msg_lower"].isin(uci_lower_msgs)].copy()
df_no_overlap = df_no_overlap.drop_duplicates(subset=["msg_lower"])

# Retain only valid binary spam labels (0 and 1)
df_no_overlap["spam_bin"] = df_no_overlap["spam label"].astype(str).str.strip()
df_no_overlap = df_no_overlap[df_no_overlap["spam_bin"].isin(["0", "1"])].copy()
df_no_overlap["y"] = df_no_overlap["spam_bin"].astype(int)

# Length filter: ensure non-trivial SMS text (at least 5 characters)
df_no_overlap = df_no_overlap[df_no_overlap["msg_clean"].str.len() >= 5]

print(f"Total non-overlapping independent candidates: {len(df_no_overlap):,}")
print(f"  - Independent Ham: {(df_no_overlap['y']==0).sum():,}")
print(f"  - Independent Spam: {(df_no_overlap['y']==1).sum():,}")

# Sample balanced benchmark dataset (1,000 Ham, 1,000 Spam)
ham_sample = df_no_overlap[df_no_overlap['y'] == 0].sample(n=1000, random_state=42)
spam_sample = df_no_overlap[df_no_overlap['y'] == 1].sample(n=1000, random_state=42)
benchmark_df = pd.concat([ham_sample, spam_sample]).sample(frac=1.0, random_state=42).reset_index(drop=True)

# Save benchmark dataset
bench_path = Path("independent_validation/dataset/independent_sms_benchmark.csv")
benchmark_df[["msg_clean", "y"]].rename(columns={"msg_clean": "message", "y": "label"}).to_csv(bench_path, index=False)
print(f"Saved independent benchmark dataset to {bench_path} (N={len(benchmark_df):,}, 50% Ham / 50% Spam).")

# Split 50:50 into validation set (threshold tuning) and held-out test set (final evaluation)
val_df, test_df = train_test_split(
    benchmark_df, test_size=0.50, random_state=42, stratify=benchmark_df["y"]
)
val_df = val_df.reset_index(drop=True)
test_df = test_df.reset_index(drop=True)
print(f"Validation subset size: {len(val_df):,} (for decision threshold tuning)")
print(f"Test subset size: {len(test_df):,} (strictly held-out for final reporting)")

# Load BERT-Tiny model (unchanged)
model_name = "mrm8488/bert-tiny-finetuned-sms-spam-detection"
tok = AutoTokenizer.from_pretrained(model_name, local_files_only=True)
mod = AutoModelForSequenceClassification.from_pretrained(model_name, local_files_only=True)
mod.eval()

def get_predictions(df_split):
    messages = df_split["msg_clean"].tolist()
    y_true = df_split["y"].values
    
    # 1. Naive Bayes predictions
    clean_messages = [preprocess_text(m) for m in messages]
    nb_probs = nb_pipeline.predict_proba(clean_messages)[:, 1]
    nb_preds = (nb_probs >= 0.5).astype(int)
    
    # 2. BERT-Tiny predictions (batched)
    bert_probs = []
    batch_size = 32
    for i in range(0, len(messages), batch_size):
        batch = messages[i:i+batch_size]
        inps = tok(batch, padding=True, truncation=True, max_length=128, return_tensors="pt")
        with torch.no_grad():
            logits = mod(**inps).logits
            probs = torch.softmax(logits, dim=-1)[:, 1].cpu().numpy()
            bert_probs.extend(probs)
    bert_probs = np.array(bert_probs)
    bert_preds = (bert_probs >= 0.5).astype(int)
    
    return y_true, nb_probs, nb_preds, bert_probs, bert_preds

print("\n=== Step 2: Evaluating on Validation Subset & Calibrating Hybrid Layer ===")
y_val, nb_val_probs, nb_val_preds, bert_val_probs, bert_val_preds = get_predictions(val_df)

# Threshold Grid Search on Validation Set
# Hybrid Decision Logic:
# If P_NB >= theta_spam or P_BERT >= theta_spam -> SPAM
# If P_NB <= theta_ham and P_BERT <= theta_ham -> HAM
# Else -> SUSPICIOUS / REVIEW

best_config = None
best_score = -1.0

# Search space for thresholds
for th_spam in [0.60, 0.70, 0.75, 0.80, 0.85]:
    for th_ham in [0.10, 0.15, 0.20, 0.25]:
        # Formulate predictions on validation subset
        # When evaluating binary metrics for comparison, map SUSPICIOUS based on argmax or review queue
        hybrid_decisions = []
        for p_nb, p_bert in zip(nb_val_probs, bert_val_probs):
            if p_nb >= th_spam or p_bert >= th_spam:
                hybrid_decisions.append("SPAM")
            elif p_nb <= th_ham and p_bert <= th_ham:
                hybrid_decisions.append("HAM")
            else:
                hybrid_decisions.append("REVIEW")
        
        # Calculate auto-decided metrics (samples not sent to review)
        auto_mask = [d != "REVIEW" for d in hybrid_decisions]
        if sum(auto_mask) < 0.6 * len(y_val):
            continue
            
        auto_true = y_val[auto_mask]
        auto_pred = [1 if hybrid_decisions[i] == "SPAM" else 0 for i, is_auto in enumerate(auto_mask) if is_auto]
        
        acc = accuracy_score(auto_true, auto_pred)
        rec = recall_score(auto_true, auto_pred)
        prec = precision_score(auto_true, auto_pred, zero_division=0)
        f1 = f1_score(auto_true, auto_pred, zero_division=0)
        
        # Optimization objective: High recall + High precision on automated decisions
        score = f1 + 0.5 * rec - 0.2 * (1 - sum(auto_mask)/len(y_val))
        if score > best_score:
            best_score = score
            best_config = {
                "th_spam": th_spam,
                "th_ham": th_ham,
                "review_pct": (1 - sum(auto_mask)/len(y_val)) * 100,
                "val_accuracy": acc,
                "val_f1": f1
            }

print(f"Optimal Hybrid Thresholds Selected via Validation Tuning:")
print(f"  - Spam Threshold (Theta_Spam):  {best_config['th_spam']}")
print(f"  - Ham Threshold (Theta_Ham):    {best_config['th_ham']}")
print(f"  - Validation Auto-Accuracy:     {best_config['val_accuracy']*100:.2f}%")
print(f"  - Validation Review Rate:       {best_config['review_pct']:.2f}%")

print("\n=== Step 3: Strictly Held-out Independent Test Set Evaluation ===")
y_test, nb_test_probs, nb_test_preds, bert_test_probs, bert_test_preds = get_predictions(test_df)

# Evaluate Naive Bayes Alone
acc_nb = accuracy_score(y_test, nb_test_preds)
prec_nb = precision_score(y_test, nb_test_preds)
rec_nb = recall_score(y_test, nb_test_preds)
f1_nb = f1_score(y_test, nb_test_preds)
macro_f1_nb = f1_score(y_test, nb_test_preds, average="macro")
cm_nb = confusion_matrix(y_test, nb_test_preds)
tn_nb, fp_nb, fn_nb, tp_nb = cm_nb.ravel()

# Evaluate BERT-Tiny Alone
acc_bert = accuracy_score(y_test, bert_test_preds)
prec_bert = precision_score(y_test, bert_test_preds, zero_division=0)
rec_bert = recall_score(y_test, bert_test_preds)
f1_bert = f1_score(y_test, bert_test_preds, zero_division=0)
macro_f1_bert = f1_score(y_test, bert_test_preds, average="macro")
cm_bert = confusion_matrix(y_test, bert_test_preds)
tn_bert, fp_bert, fn_bert, tp_bert = cm_bert.ravel()

# Evaluate Hybrid Decision Layer on Held-out Test Set
th_s = best_config["th_spam"]
th_h = best_config["th_ham"]

hybrid_test_outcomes = []
for p_nb, p_bert in zip(nb_test_probs, bert_test_probs):
    if p_nb >= th_s or p_bert >= th_s:
        hybrid_test_outcomes.append("SPAM")
    elif p_nb <= th_h and p_bert <= th_h:
        hybrid_test_outcomes.append("HAM")
    else:
        hybrid_test_outcomes.append("SUSPICIOUS_REVIEW")

# Metrics for Hybrid (considering automated decisions vs full triage)
hybrid_test_df = pd.DataFrame({
    "y_true": y_test,
    "decision": hybrid_test_outcomes,
    "p_nb": nb_test_probs,
    "p_bert": bert_test_probs
})

total_test = len(hybrid_test_df)
count_ham = (hybrid_test_df["decision"] == "HAM").sum()
count_spam = (hybrid_test_df["decision"] == "SPAM").sum()
count_review = (hybrid_test_df["decision"] == "SUSPICIOUS_REVIEW").sum()

# Triage distribution breakdown
spam_in_review = ((hybrid_test_df["decision"] == "SUSPICIOUS_REVIEW") & (hybrid_test_df["y_true"] == 1)).sum()
ham_in_review = ((hybrid_test_df["decision"] == "SUSPICIOUS_REVIEW") & (hybrid_test_df["y_true"] == 0)).sum()

auto_df = hybrid_test_df[hybrid_test_df["decision"] != "SUSPICIOUS_REVIEW"].copy()
auto_df["y_pred"] = (auto_df["decision"] == "SPAM").astype(int)

acc_hybrid_auto = accuracy_score(auto_df["y_true"], auto_df["y_pred"])
prec_hybrid_auto = precision_score(auto_df["y_true"], auto_df["y_pred"])
rec_hybrid_auto = recall_score(auto_df["y_true"], auto_df["y_pred"])
f1_hybrid_auto = f1_score(auto_df["y_true"], auto_df["y_pred"])
macro_f1_hybrid_auto = f1_score(auto_df["y_true"], auto_df["y_pred"], average="macro")
cm_hybrid_auto = confusion_matrix(auto_df["y_true"], auto_df["y_pred"])
tn_h, fp_h, fn_h, tp_h = cm_hybrid_auto.ravel()

# Binary fallback for Hybrid (if review is forced to decision by max probability)
fallback_preds = []
for p_nb, p_bert in zip(nb_test_probs, bert_test_probs):
    combined_prob = 0.5 * p_nb + 0.5 * p_bert
    fallback_preds.append(1 if combined_prob >= 0.5 else 0)

acc_hybrid_all = accuracy_score(y_test, fallback_preds)
prec_hybrid_all = precision_score(y_test, fallback_preds)
rec_hybrid_all = recall_score(y_test, fallback_preds)
f1_hybrid_all = f1_score(y_test, fallback_preds)
macro_f1_hybrid_all = f1_score(y_test, fallback_preds, average="macro")

print("\n--- Unchanged Naive Bayes Performance (Independent Test N=1,000) ---")
print(f"Accuracy:        {acc_nb*100:.2f}%")
print(f"Spam Precision:  {prec_nb*100:.2f}%")
print(f"Spam Recall:     {rec_nb*100:.2f}%")
print(f"Spam F1-Score:   {f1_nb:.4f}")
print(f"Macro F1-Score:  {macro_f1_nb:.4f}")
print(f"Confusion Matrix: TN={tn_nb}, FP={fp_nb}, FN={fn_nb}, TP={tp_nb}")

print("\n--- Unchanged BERT-Tiny Performance (Independent Test N=1,000) ---")
print(f"Accuracy:        {acc_bert*100:.2f}%")
print(f"Spam Precision:  {prec_bert*100:.2f}%")
print(f"Spam Recall:     {rec_bert*100:.2f}%")
print(f"Spam F1-Score:   {f1_bert:.4f}")
print(f"Macro F1-Score:  {macro_f1_bert:.4f}")
print(f"Confusion Matrix: TN={tn_bert}, FP={fp_bert}, FN={fn_bert}, TP={tp_bert}")

print("\n--- Hybrid Decision Layer Performance ---")
print(f"Triage Breakdown (N={total_test}):")
print(f"  - Auto-Classified as HAM:  {count_ham} ({count_ham/total_test*100:.1f}%)")
print(f"  - Auto-Classified as SPAM: {count_spam} ({count_spam/total_test*100:.1f}%)")
print(f"  - Routed to SUSPICIOUS/REVIEW: {count_review} ({count_review/total_test*100:.1f}%)")
print(f"    └─ Contains {spam_in_review} actual Spams and {ham_in_review} actual Hams")
print(f"Automated Decisions Accuracy: {acc_hybrid_auto*100:.2f}% (F1={f1_hybrid_auto:.4f})")
print(f"Full Fallback Accuracy:       {acc_hybrid_all*100:.2f}% (F1={f1_hybrid_all:.4f})")

print("\n=== Step 4: Diagnostic Logit & Feature Stress-Testing ===")
stress_suite = [
    # Legitimate Conversational & Transactional
    ("Hey mom, are we having lunch together today?", "Legit Family"),
    ("Your appointment with Dr. Smith is confirmed for tomorrow at 2 PM.", "Legit Appointment"),
    ("Acct 4921: Deposited $500.00. Current balance is $1,245.80.", "Legit Bank Alert"),
    
    # Generic Promotional Bait (No telephony numbers)
    ("Congratulations! You have won a free prize. Claim now!", "Promo Unprompted Prize"),
    ("Exclusive offer: Get 50% discount on your next online purchase.", "Promo E-Commerce"),
    ("You are selected for an instant cash reward of $10,000.", "Promo Cash Reward"),
    
    # Modern Phishing & Suspicious URLs
    ("Urgent: Your Chase bank account has been suspended. Verify at https://chase-login-auth.com", "Phishing Bank Link"),
    ("USPS: Your package could not be delivered. Update address at https://postal-track-delivery.xyz", "Phishing Package Link"),
    ("Your Netflix account is on hold. Update billing information immediately.", "Phishing Account Hold"),
    
    # Traditional 2003 UK SMS Carrier Spam (Phone & Shortcode)
    ("WINNER!! Claim your £1000 cash prize now! Call 09061701461 to claim.", "Traditional UK Phone"),
    ("URGENT! You have won a 1 week free holiday. Text CLAIM to 87121", "Traditional UK Shortcode"),
    ("Free entry in 2 a weekly competition. Call 0800123456 immediately.", "Traditional 0800 Call")
]

stress_records = []
for text, category in stress_suite:
    inp = tok(text, return_tensors="pt", truncation=True, max_length=128)
    with torch.no_grad():
        out = mod(**inp)
        logits = out.logits[0].tolist()
        probs = torch.softmax(out.logits[0], dim=-1).tolist()
    
    p_nb = nb_pipeline.predict_proba([preprocess_text(text)])[0][1]
    
    stress_records.append({
        "Category": category,
        "Message": text,
        "BERT Logits [Ham, Spam]": [round(l, 3) for l in logits],
        "Logit Diff (L0 - L1)": round(logits[0] - logits[1], 3),
        "BERT Spam Prob (%)": round(probs[1] * 100, 2),
        "BERT Label": "SPAM" if probs[1] >= 0.5 else "HAM",
        "NB Spam Prob (%)": round(p_nb * 100, 2),
        "NB Label": "SPAM" if p_nb >= 0.5 else "HAM"
    })

print(f"Tested {len(stress_suite)} targeted stress messages.")

# Save metrics to json
metrics_dict = {
    "dataset_provenance": {
        "candidate_source": "shaghayegh-hp/Smishing_Dataset (ACM 2025)",
        "total_remote_records": int(len(df_remote)),
        "uci_overlap_records_filtered": int(len(orig_df)),
        "independent_unseen_candidates": int(len(df_no_overlap)),
        "benchmark_sample_size": int(len(benchmark_df)),
        "validation_subset_size": int(len(val_df)),
        "held_out_test_subset_size": int(len(test_df)),
        "class_balance": "50% Ham / 50% Spam (Balanced)"
    },
    "naive_bayes_test": {
        "accuracy": float(acc_nb),
        "precision": float(prec_nb),
        "recall": float(rec_nb),
        "f1": float(f1_nb),
        "macro_f1": float(macro_f1_nb),
        "confusion_matrix": cm_nb.tolist(),
        "tn": int(tn_nb),
        "fp": int(fp_nb),
        "fn": int(fn_nb),
        "tp": int(tp_nb)
    },
    "bert_tiny_test": {
        "accuracy": float(acc_bert),
        "precision": float(prec_bert),
        "recall": float(rec_bert),
        "f1": float(f1_bert),
        "macro_f1": float(macro_f1_bert),
        "confusion_matrix": cm_bert.tolist(),
        "tn": int(tn_bert),
        "fp": int(fp_bert),
        "fn": int(fn_bert),
        "tp": int(tp_bert)
    },
    "hybrid_decision_layer": {
        "threshold_spam": float(th_s),
        "threshold_ham": float(th_h),
        "total_test_samples": int(total_test),
        "auto_ham_count": int(count_ham),
        "auto_spam_count": int(count_spam),
        "suspicious_review_count": int(count_review),
        "review_rate_pct": float(count_review / total_test * 100),
        "spams_in_review": int(spam_in_review),
        "hams_in_review": int(ham_in_review),
        "automated_decisions": {
            "accuracy": float(acc_hybrid_auto),
            "precision": float(prec_hybrid_auto),
            "recall": float(rec_hybrid_auto),
            "f1": float(f1_hybrid_auto),
            "macro_f1": float(macro_f1_hybrid_auto),
            "confusion_matrix": cm_hybrid_auto.tolist(),
            "tn": int(tn_h),
            "fp": int(fp_h),
            "fn": int(fn_h),
            "tp": int(tp_h)
        },
        "full_triage_fallback": {
            "accuracy": float(acc_hybrid_all),
            "precision": float(prec_hybrid_all),
            "recall": float(rec_hybrid_all),
            "f1": float(f1_hybrid_all),
            "macro_f1": float(macro_f1_hybrid_all)
        }
    },
    "stress_testing": stress_records
}

metrics_path = Path("independent_validation/metrics.json")
with open(metrics_path, "w") as f:
    json.dump(metrics_dict, f, indent=2)
print(f"Saved independent evaluation metrics to {metrics_path}.")

# Generate Visualizations
print("\n=== Step 5: Generating Visualizations ===")
plt.style.use("seaborn-v0_8-whitegrid")

# 1. confusion_matrices.png
fig, axes = plt.subplots(1, 3, figsize=(18, 5), dpi=300)

sns.heatmap(cm_nb, annot=True, fmt="d", cmap="Blues", cbar=False,
            xticklabels=["Pred Ham", "Pred Spam"], yticklabels=["Actual Ham", "Actual Spam"],
            annot_kws={"size": 13, "weight": "bold"}, ax=axes[0])
axes[0].set_title(f"Multinomial Naive Bayes\nAcc: {acc_nb*100:.1f}% | Rec: {rec_nb*100:.1f}%", fontsize=12, weight="bold")

sns.heatmap(cm_bert, annot=True, fmt="d", cmap="Purples", cbar=False,
            xticklabels=["Pred Ham", "Pred Spam"], yticklabels=["Actual Ham", "Actual Spam"],
            annot_kws={"size": 13, "weight": "bold"}, ax=axes[1])
axes[1].set_title(f"BERT-Tiny (Unchanged)\nAcc: {acc_bert*100:.1f}% | Rec: {rec_bert*100:.1f}%", fontsize=12, weight="bold")

sns.heatmap(cm_hybrid_auto, annot=True, fmt="d", cmap="Greens", cbar=False,
            xticklabels=["Pred Ham", "Pred Spam"], yticklabels=["Actual Ham", "Actual Spam"],
            annot_kws={"size": 13, "weight": "bold"}, ax=axes[2])
axes[2].set_title(f"Hybrid Decision Layer (Automated Tier)\nAcc: {acc_hybrid_auto*100:.1f}% | F1: {f1_hybrid_auto:.4f}", fontsize=12, weight="bold")

plt.tight_layout()
cm_out = Path("independent_validation/confusion_matrices.png")
plt.savefig(cm_out, bbox_inches="tight")
plt.close()
print(f"Saved confusion matrices to {cm_out}.")

# 2. model_comparison.png
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)

models = ["Multinomial NB", "BERT-Tiny", "Hybrid (Automated)"]
accs = [acc_nb * 100, acc_bert * 100, acc_hybrid_auto * 100]
colors = ["#3B82F6", "#8B5CF6", "#10B981"]

bars = ax1.bar(models, accs, color=colors, width=0.45, edgecolor="black", linewidth=1)
ax1.set_ylim(0, 105)
ax1.set_ylabel("Accuracy (%)", fontsize=11, weight="bold")
ax1.set_title("Independent Test Accuracy Comparison\n(Held-out Unseen Modern SMS N=1,000)", fontsize=12, weight="bold", pad=12)
for b in bars:
    y = b.get_height()
    ax1.text(b.get_x() + b.get_width()/2.0, y + 2, f"{y:.1f}%", ha="center", va="bottom", fontsize=11, weight="bold")

# Comparison across Precision, Recall & F1
comp_df = pd.DataFrame({
    "Model": ["Multinomial NB"] * 3 + ["BERT-Tiny"] * 3 + ["Hybrid (Auto)"] * 3,
    "Metric": ["Precision (Spam)", "Recall (Spam)", "F1-Score (Spam)"] * 3,
    "Score": [
        prec_nb, rec_nb, f1_nb,
        prec_bert, rec_bert, f1_bert,
        prec_hybrid_auto, rec_hybrid_auto, f1_hybrid_auto
    ]
})

sns.barplot(data=comp_df, x="Metric", y="Score", hue="Model", palette=colors, ax=ax2, edgecolor="black", linewidth=0.8)
ax2.set_ylim(0, 1.1)
ax2.set_ylabel("Score (0.0 – 1.0)", fontsize=11, weight="bold")
ax2.set_title("Independent Spam Detection Metrics\n(Precision vs. Recall vs. F1)", fontsize=12, weight="bold", pad=12)
ax2.legend(loc="lower right", frameon=True)

for p in ax2.patches:
    h = p.get_height()
    if h > 0:
        ax2.annotate(f"{h:.2f}", (p.get_x() + p.get_width() / 2., h + 0.02),
                     ha="center", va="bottom", fontsize=9, weight="bold")

plt.tight_layout()
comp_out = Path("independent_validation/model_comparison.png")
plt.savefig(comp_out, bbox_inches="tight")
plt.close()
print(f"Saved model comparison to {comp_out}.")

print("\n=== Benchmark Script Successfully Completed! ===")
