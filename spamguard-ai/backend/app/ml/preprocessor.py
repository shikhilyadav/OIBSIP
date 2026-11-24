"""
Standardized Preprocessing Pipeline
Preserves exact text preprocessing logic from OIBSIP Task 4.
"""

import re
import string
from pathlib import Path
from ..config import TASK4_DIR

try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.stem import PorterStemmer
    nltk_path = TASK4_DIR / "nltk_data"
    if nltk_path.exists():
        nltk.data.path.insert(0, str(nltk_path.resolve()))
    STOP_WORDS = set(stopwords.words("english"))
except Exception:
    from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
    STOP_WORDS = set(ENGLISH_STOP_WORDS)
    from nltk.stem import PorterStemmer

stemmer = PorterStemmer()

def preprocess_text(text: str) -> str:
    """Standardized text preprocessing matching Task 4 pipeline."""
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
