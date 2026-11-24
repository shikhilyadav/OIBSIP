"""
generate_outputs.py
===================
End-to-end execution script for Task 4: Email/SMS Spam Detection.
Generates:
1. Class distribution visualization (outputs/class_distribution.png)
2. Confusion matrix comparison visualization (outputs/confusion_matrix.png)
3. Spam WordCloud (outputs/spam_wordcloud.png)
4. Ham WordCloud (outputs/ham_wordcloud.png)
5. Model metrics and evaluation logs.
"""

import os
import re
import string
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)
import nltk

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "dataset", "spam.csv")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
NLTK_DATA_DIR = os.path.join(BASE_DIR, "nltk_data")

os.makedirs(OUTPUTS_DIR, exist_ok=True)

if os.path.exists(NLTK_DATA_DIR):
    nltk.data.path.append(NLTK_DATA_DIR)

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from wordcloud import WordCloud

# Set plot aesthetics
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cbd5e1'
plt.rcParams['axes.linewidth'] = 0.8


def run():
    print("[1/6] Loading authentic SMS Spam Collection dataset...")
    df_raw = pd.read_csv(DATA_PATH, encoding="latin-1")
    print(f"Raw shape: {df_raw.shape}")

    # Keep only primary columns and rename
    df = df_raw[["v1", "v2"]].copy()
    df.rename(columns={"v1": "label", "v2": "message"}, inplace=True)
    df["target"] = df["label"].map({"ham": 0, "spam": 1})

    print(f"Cleaned columns: {df.columns.tolist()}")
    print("Class counts:")
    print(df["label"].value_counts())
    print("Class percentages:")
    print((df["label"].value_counts(normalize=True) * 100).round(2))

    # -------------------------------------------------------------
    # Visualization 1: Class Distribution
    # -------------------------------------------------------------
    print("[2/6] Generating Class Distribution plot...")
    fig, axes = plt.subplots(1, 2, figsize=(13, 5), dpi=300)
    
    # Bar plot
    palette = {"ham": "#2563eb", "spam": "#dc2626"}
    counts = df["label"].value_counts()
    sns.barplot(x=counts.index, y=counts.values, hue=counts.index, palette=palette, ax=axes[0], legend=False)
    axes[0].set_title("SMS Message Class Distribution (Counts)", fontsize=13, fontweight="bold", pad=12)
    axes[0].set_xlabel("Class Label", fontsize=11, fontweight="600")
    axes[0].set_ylabel("Message Count", fontsize=11, fontweight="600")
    for i, v in enumerate(counts.values):
        axes[0].text(i, v + 60, f"{v:,d}\n({v/len(df)*100:.1f}%)", ha="center", fontsize=10, fontweight="bold")
    axes[0].set_ylim(0, max(counts.values) * 1.15)

    # Pie chart
    axes[1].pie(
        counts.values,
        labels=[f"Ham ({counts['ham']:,d})", f"Spam ({counts['spam']:,d})"],
        autopct="%1.2f%%",
        startangle=140,
        colors=["#3b82f6", "#ef4444"],
        explode=(0, 0.1),
        textprops={"fontsize": 11, "fontweight": "600"},
        wedgeprops={"edgecolor": "white", "linewidth": 2}
    )
    axes[1].set_title("Spam vs. Ham Proportion (%)", fontsize=13, fontweight="bold", pad=12)

    plt.suptitle("OIBSIP Task 4: SMS Spam Collection Dataset Balance", fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    class_dist_path = os.path.join(OUTPUTS_DIR, "class_distribution.png")
    fig.savefig(class_dist_path, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {class_dist_path}")

    # -------------------------------------------------------------
    # Text Preprocessing
    # -------------------------------------------------------------
    print("[3/6] Preprocessing text messages...")
    try:
        stop_words = set(stopwords.words("english"))
    except Exception:
        from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
        stop_words = set(ENGLISH_STOP_WORDS)
    
    ps = PorterStemmer()

    def preprocess_text(text):
        if not isinstance(text, str):
            return ""
        # Lowercase
        text = text.lower()
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        # Remove emails
        text = re.sub(r'\S+@\S+', '', text)
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        # Remove standalone numbers
        text = re.sub(r'\b\d+\b', '', text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        # Tokenize, remove stopwords, and apply Porter Stemming
        tokens = [ps.stem(word) for word in text.split() if word not in stop_words and len(word) > 1]
        return ' '.join(tokens)

    df["clean_message"] = df["message"].apply(preprocess_text)

    # -------------------------------------------------------------
    # Visualizations 2 & 3: WordClouds
    # -------------------------------------------------------------
    print("[4/6] Generating WordClouds...")
    spam_text = " ".join(df[df["label"] == "spam"]["clean_message"])
    ham_text = " ".join(df[df["label"] == "ham"]["clean_message"])

    # Spam WordCloud
    wc_spam = WordCloud(
        width=800, height=450,
        background_color="white",
        colormap="Reds",
        max_words=150,
        random_state=42
    ).generate(spam_text)

    fig_wc_s, ax_s = plt.subplots(figsize=(10, 5), dpi=300)
    ax_s.imshow(wc_spam, interpolation="bilinear")
    ax_s.axis("off")
    ax_s.set_title("Most Prominent Keywords in Spam Messages (Stemmed)", fontsize=14, fontweight="bold", pad=12)
    spam_wc_path = os.path.join(OUTPUTS_DIR, "spam_wordcloud.png")
    fig_wc_s.savefig(spam_wc_path, bbox_inches="tight")
    plt.close(fig_wc_s)
    print(f"Saved: {spam_wc_path}")

    # Ham WordCloud
    wc_ham = WordCloud(
        width=800, height=450,
        background_color="white",
        colormap="Blues",
        max_words=150,
        random_state=42
    ).generate(ham_text)

    fig_wc_h, ax_h = plt.subplots(figsize=(10, 5), dpi=300)
    ax_h.imshow(wc_ham, interpolation="bilinear")
    ax_h.axis("off")
    ax_h.set_title("Most Prominent Keywords in Legitimate (Ham) Messages (Stemmed)", fontsize=14, fontweight="bold", pad=12)
    ham_wc_path = os.path.join(OUTPUTS_DIR, "ham_wordcloud.png")
    fig_wc_h.savefig(ham_wc_path, bbox_inches="tight")
    plt.close(fig_wc_h)
    print(f"Saved: {ham_wc_path}")

    # -------------------------------------------------------------
    # Train / Test Split (Stratified 80/20)
    # -------------------------------------------------------------
    print("[5/6] Performing Stratified Train/Test Split (80/20)...")
    X_train, X_test, y_train, y_test = train_test_split(
        df["clean_message"],
        df["target"],
        test_size=0.20,
        random_state=42,
        stratify=df["target"]
    )
    print(f"Train samples: {len(X_train)} (Ham: {(y_train == 0).sum()}, Spam: {(y_train == 1).sum()})")
    print(f"Test samples : {len(X_test)} (Ham: {(y_test == 0).sum()}, Spam: {(y_test == 1).sum()})")

    # -------------------------------------------------------------
    # Machine Learning Models: MultinomialNB & Logistic Regression
    # -------------------------------------------------------------
    print("Training Multinomial Naive Bayes Pipeline...")
    pipe_nb = Pipeline([
        ("tfidf", TfidfVectorizer(max_features=5000, ngram_range=(1, 2))),
        ("nb", MultinomialNB())
    ])
    pipe_nb.fit(X_train, y_train)
    y_pred_nb = pipe_nb.predict(X_test)
    y_prob_nb = pipe_nb.predict_proba(X_test)[:, 1]

    print("Training Logistic Regression Pipeline...")
    pipe_lr = Pipeline([
        ("tfidf", TfidfVectorizer(max_features=5000, ngram_range=(1, 2))),
        ("lr", LogisticRegression(random_state=42, max_iter=1000))
    ])
    pipe_lr.fit(X_train, y_train)
    y_pred_lr = pipe_lr.predict(X_test)
    y_prob_lr = pipe_lr.predict_proba(X_test)[:, 1]

    # Metrics
    metrics_nb = {
        "accuracy": float(accuracy_score(y_test, y_pred_nb)),
        "precision": float(precision_score(y_test, y_pred_nb)),
        "recall": float(recall_score(y_test, y_pred_nb)),
        "f1": float(f1_score(y_test, y_pred_nb)),
        "cm": confusion_matrix(y_test, y_pred_nb).tolist()
    }

    metrics_lr = {
        "accuracy": float(accuracy_score(y_test, y_pred_lr)),
        "precision": float(precision_score(y_test, y_pred_lr)),
        "recall": float(recall_score(y_test, y_pred_lr)),
        "f1": float(f1_score(y_test, y_pred_lr)),
        "cm": confusion_matrix(y_test, y_pred_lr).tolist()
    }

    print("\n" + "="*50)
    print("EVALUATION RESULTS")
    print("="*50)
    print(f"Multinomial Naive Bayes:")
    print(f"  Accuracy : {metrics_nb['accuracy']:.4f} ({metrics_nb['accuracy']*100:.2f}%)")
    print(f"  Precision: {metrics_nb['precision']:.4f}")
    print(f"  Recall   : {metrics_nb['recall']:.4f}")
    print(f"  F1-Score : {metrics_nb['f1']:.4f}")
    print("  Confusion Matrix:")
    print(f"    TN: {metrics_nb['cm'][0][0]}, FP: {metrics_nb['cm'][0][1]}")
    print(f"    FN: {metrics_nb['cm'][1][0]}, TP: {metrics_nb['cm'][1][1]}")

    print(f"\nLogistic Regression:")
    print(f"  Accuracy : {metrics_lr['accuracy']:.4f} ({metrics_lr['accuracy']*100:.2f}%)")
    print(f"  Precision: {metrics_lr['precision']:.4f}")
    print(f"  Recall   : {metrics_lr['recall']:.4f}")
    print(f"  F1-Score : {metrics_lr['f1']:.4f}")
    print("  Confusion Matrix:")
    print(f"    TN: {metrics_lr['cm'][0][0]}, FP: {metrics_lr['cm'][0][1]}")
    print(f"    FN: {metrics_lr['cm'][1][0]}, TP: {metrics_lr['cm'][1][1]}")

    # -------------------------------------------------------------
    # Visualization 4: Confusion Matrix Comparison
    # -------------------------------------------------------------
    print("[6/6] Generating Confusion Matrix comparison plot...")
    fig_cm, axes_cm = plt.subplots(1, 2, figsize=(13, 5), dpi=300)

    # NB Confusion Matrix
    cm_nb = np.array(metrics_nb["cm"])
    sns.heatmap(
        cm_nb, annot=True, fmt="d", cmap="Blues", cbar=False, ax=axes_cm[0],
        xticklabels=["Predicted Ham", "Predicted Spam"],
        yticklabels=["Actual Ham", "Actual Spam"],
        annot_kws={"size": 13, "fontweight": "bold"}
    )
    axes_cm[0].set_title(
        f"Multinomial Naive Bayes\nAcc: {metrics_nb['accuracy']*100:.2f}% | Precision: {metrics_nb['precision']:.4f} | Recall: {metrics_nb['recall']:.4f}",
        fontsize=11, fontweight="bold", pad=12
    )

    # LR Confusion Matrix
    cm_lr = np.array(metrics_lr["cm"])
    sns.heatmap(
        cm_lr, annot=True, fmt="d", cmap="Greens", cbar=False, ax=axes_cm[1],
        xticklabels=["Predicted Ham", "Predicted Spam"],
        yticklabels=["Actual Ham", "Actual Spam"],
        annot_kws={"size": 13, "fontweight": "bold"}
    )
    axes_cm[1].set_title(
        f"Logistic Regression\nAcc: {metrics_lr['accuracy']*100:.2f}% | Precision: {metrics_lr['precision']:.4f} | Recall: {metrics_lr['recall']:.4f}",
        fontsize=11, fontweight="bold", pad=12
    )

    plt.suptitle("Model Confusion Matrix Comparison (Test Set $N=1,115$)", fontsize=14, fontweight="bold", y=1.03)
    plt.tight_layout()
    cm_path = os.path.join(OUTPUTS_DIR, "confusion_matrix.png")
    fig_cm.savefig(cm_path, bbox_inches="tight")
    plt.close(fig_cm)
    print(f"Saved: {cm_path}")

    # -------------------------------------------------------------
    # Custom Message Predictions
    # -------------------------------------------------------------
    print("\n" + "="*50)
    print("CUSTOM MESSAGE PREDICTIONS")
    print("="*50)
    test_messages = [
        "Congratulations! You have won a free prize.",
        "Hey, are we meeting tomorrow?",
        "Claim your free reward now.",
        "Please call me when you reach home."
    ]
    for msg in test_messages:
        cleaned = preprocess_text(msg)
        pred_nb = pipe_nb.predict([cleaned])[0]
        prob_nb = pipe_nb.predict_proba([cleaned])[0][1]
        pred_lr = pipe_lr.predict([cleaned])[0]
        prob_lr = pipe_lr.predict_proba([cleaned])[0][1]

        lbl_nb = "SPAM" if pred_nb == 1 else "HAM"
        lbl_lr = "SPAM" if pred_lr == 1 else "HAM"
        print(f"\nMessage: '{msg}'")
        print(f"  Naive Bayes        -> {lbl_nb:<4} (P(Spam) = {prob_nb:.4f})")
        print(f"  Logistic Regression-> {lbl_lr:<4} (P(Spam) = {prob_lr:.4f})")

    # Save summary json
    summary_data = {
        "dataset": {
            "total_records": len(df),
            "ham_count": int(counts["ham"]),
            "spam_count": int(counts["spam"]),
            "ham_pct": float(counts["ham"] / len(df) * 100),
            "spam_pct": float(counts["spam"] / len(df) * 100)
        },
        "naive_bayes": metrics_nb,
        "logistic_regression": metrics_lr
    }
    with open(os.path.join(OUTPUTS_DIR, "summary_metrics.json"), "w", encoding="utf-8") as f:
        json.dump(summary_data, f, indent=2)
    print("\nSummary metrics saved to outputs/summary_metrics.json")


if __name__ == "__main__":
    run()
