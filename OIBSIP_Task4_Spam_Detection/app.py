"""
OIBSIP Task 4: Email / SMS Spam Detection Interactive Web Application
Built with Streamlit, Scikit-learn, and NLTK.
"""

import re
import string
from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# NLTK Stopwords with offline fallback
try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.stem import PorterStemmer
    nltk_path = Path(__file__).resolve().parent / "nltk_data"
    if nltk_path.exists():
        nltk.data.path.insert(0, str(nltk_path))
    STOP_WORDS = set(stopwords.words("english"))
except Exception:
    from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
    STOP_WORDS = set(ENGLISH_STOP_WORDS)
    from nltk.stem import PorterStemmer

stemmer = PorterStemmer()

def preprocess_text(text: str) -> str:
    """Standardized text preprocessing pipeline."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    text = re.sub(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", " ", text)
    text = re.sub(f"[{re.escape(string.punctuation)}]", " ", text)
    text = re.sub(r"\b\d+\b", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    tokens = [stemmer.stem(w) for w in text.split() if w not in STOP_WORDS and len(w) > 1]
    return " ".join(tokens)

@st.cache_resource(show_spinner="Training production spam models...")
def load_models_and_data():
    data_path = Path(__file__).resolve().parent / "dataset" / "spam.csv"
    df = pd.read_csv(data_path, encoding="latin-1")
    df = df[["v1", "v2"]].rename(columns={"v1": "label", "v2": "message"}).dropna()
    df["clean_message"] = df["message"].apply(preprocess_text)
    
    y = df["label"].map({"ham": 0, "spam": 1})
    X = df["clean_message"]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    
    # Model 1: Multinomial Naive Bayes
    nb_pipe = Pipeline([
        ("tfidf", TfidfVectorizer(max_features=5000, ngram_range=(1, 2))),
        ("clf", MultinomialNB(alpha=1.0))
    ])
    nb_pipe.fit(X_train, y_train)
    
    # Model 2: Logistic Regression
    lr_pipe = Pipeline([
        ("tfidf", TfidfVectorizer(max_features=5000, ngram_range=(1, 2))),
        ("clf", LogisticRegression(max_iter=1000, random_state=42))
    ])
    lr_pipe.fit(X_train, y_train)
    
    # Model 3: Pre-trained Transformer (BERT-Tiny)
    try:
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
        import torch
        bert_name = "mrm8488/bert-tiny-finetuned-sms-spam-detection"
        bert_tok = AutoTokenizer.from_pretrained(bert_name)
        bert_mod = AutoModelForSequenceClassification.from_pretrained(bert_name)
        bert_mod.eval()
    except Exception:
        bert_tok, bert_mod = None, None
    
    return nb_pipe, lr_pipe, (bert_tok, bert_mod), df

# Page config
st.set_page_config(
    page_title="SMS / Email Spam Detector | OIBSIP Task 4",
    page_icon="🛡️",
    layout="wide"
)

# Custom Styling
st.markdown("""
<style>
    .main-header { font-size: 2.2rem; font-weight: 700; color: #1E3A8A; margin-bottom: 0.2rem; }
    .sub-header { font-size: 1.05rem; color: #4B5563; margin-bottom: 1.5rem; }
    .card { background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 20px; margin-bottom: 20px; }
    .spam-badge { background-color: #FEE2E2; color: #991B1B; font-weight: 700; padding: 6px 14px; border-radius: 9999px; font-size: 1.1rem; }
    .ham-badge { background-color: #DCFCE7; color: #166534; font-weight: 700; padding: 6px 14px; border-radius: 9999px; font-size: 1.1rem; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🛡️ Email & SMS Spam Detection Portal</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Oasis Infobyte (OIBSIP) Data Science Internship — Task 4 | NLP Machine Learning System</div>', unsafe_allow_html=True)

nb_pipe, lr_pipe, (bert_tok, bert_mod), df = load_models_and_data()

# Sidebar
st.sidebar.header("⚙️ Configuration")
model_choice = st.sidebar.radio(
    "Choose Classifier Architecture:",
    [
        "Multinomial Naive Bayes (Fastest - 96.95% Acc, 99.15% Prec)",
        "Logistic Regression (96.68% Acc, 98.28% Prec)",
        "BERT-Tiny Transformer (Highest Recall - 98.57% Acc, 92.62% Rec)"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Dataset Overview")
st.sidebar.write(f"- **Total Corpus:** {len(df):,} messages")
st.sidebar.write(f"- **Ham (Legit):** {(df['label'] == 'ham').sum():,} (86.59%)")
st.sidebar.write(f"- **Spam:** {(df['label'] == 'spam').sum():,} (13.41%)")
st.sidebar.write("- **TF-IDF Specs:** 5,000 features, 1-2 n-grams")
st.sidebar.write("- **BERT Specs:** 2 layers, 128 dim, 4.39M params")

# Pre-defined test messages
st.subheader("📝 Try Sample Messages")
col1, col2, col3, col4, col5, col6 = st.columns(6)
sample_text = ""
if col1.button("🏆 Sample 1 (Prize)"):
    sample_text = "Congratulations! You have won a free prize. Claim now!"
if col2.button("💬 Sample 2 (Meeting)"):
    sample_text = "Hey, are we meeting tomorrow?"
if col3.button("🏦 Sample 3 (Bank Alert)"):
    sample_text = "Your bank account is blocked. Verify your details."
if col4.button("🏠 Sample 4 (Arrive)"):
    sample_text = "Please call me when you reach home."
if col5.button("💰 Sample 5 (Cash)"):
    sample_text = "Congratulations! You have been selected for a cash reward."
if col6.button("📅 Sample 6 (Schedule)"):
    sample_text = "Your meeting is scheduled for tomorrow at 10 AM."

user_input = st.text_area(
    "Enter message content to analyze for spam / phishing indicators:",
    value=sample_text,
    height=100,
    placeholder="Type or paste any SMS or email message here..."
)

if st.button("🚀 Analyze Message", type="primary") or user_input:
    if not user_input.strip():
        st.warning("Please enter or select a message to test.")
    else:
        clean = preprocess_text(user_input)
        
        # Determine prediction mode
        if "BERT-Tiny" in model_choice and bert_tok is not None and bert_mod is not None:
            import torch
            inp = bert_tok(user_input, return_tensors="pt", truncation=True, max_length=128)
            with torch.no_grad():
                logits = bert_mod(**inp).logits[0]
                probs = torch.softmax(logits, dim=-1)
                spam_prob = float(probs[1].item())
                is_spam = spam_prob >= 0.5
        elif "Logistic Regression" in model_choice:
            proba = lr_pipe.predict_proba([clean])[0]
            spam_prob = float(proba[1])
            is_spam = spam_prob >= 0.5
        else:
            proba = nb_pipe.predict_proba([clean])[0]
            spam_prob = float(proba[1])
            is_spam = spam_prob >= 0.5

        st.markdown("---")
        res_col1, res_col2 = st.columns([1, 2])
        
        with res_col1:
            st.markdown("### 🏷️ Classification Result")
            if is_spam:
                st.markdown('<span class="spam-badge">🚨 SPAM DETECTED</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="ham-badge">✅ LEGITIMATE (HAM)</span>', unsafe_allow_html=True)
            
            st.write("")
            st.metric("Spam Risk Score", f"{spam_prob * 100:.2f}%")
            st.metric("Ham Confidence", f"{(1 - spam_prob) * 100:.2f}%")

        with res_col2:
            st.markdown("### 🔍 Model Diagnostics")
            st.text_input("Preprocessed Tokens (Case-folded, Stemmed, Cleaned):", value=clean, disabled=True)
            st.progress(spam_prob)
            if spam_prob >= 0.7:
                st.error("High risk: Strong promotional or financial bait indicators detected.")
            elif spam_prob >= 0.5:
                st.warning("Moderate risk: Borderline spam tokens detected.")
            else:
                st.success("Clean message: Low spam likelihood.")

st.markdown("---")
st.markdown("### 📈 Visual Benchmarks & Evaluation")
tab1, tab2 = st.tabs(["📊 Tri-Model Comparison & BERT", "📉 Classical Model Baselines"])
with tab1:
    vcol1, vcol2 = st.columns(2)
    with vcol1:
        st.image(str(Path(__file__).resolve().parent / "outputs" / "three_model_comparison.png"), caption="Accuracy, Precision, Recall & F1-Score Comparison")
    with vcol2:
        st.image(str(Path(__file__).resolve().parent / "outputs" / "bert_confusion_matrix.png"), caption="BERT-Tiny Confusion Matrix (Held-out Test N=1,115)")
with tab2:
    vcol3, vcol4 = st.columns(2)
    with vcol3:
        st.image(str(Path(__file__).resolve().parent / "outputs" / "confusion_matrix.png"), caption="Classical Confusion Matrices (Naive Bayes vs Logistic Regression)")
    with vcol4:
        st.image(str(Path(__file__).resolve().parent / "outputs" / "class_distribution.png"), caption="Dataset Class Balance & Message Length Distribution")
