"""
Model Service: Singleton model loader and inference engine.
Initializes models once on startup; runs CPU-optimized inference.
"""

import time
from pathlib import Path
from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np
import torch
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from ..config import TASK4_DATASET, BERT_MODEL_NAME
from .preprocessor import preprocess_text

class ModelService:
    _instance = None

    def __init__(self):
        self.nb_pipeline = None
        self.lr_pipeline = None
        self.bert_tokenizer = None
        self.bert_model = None
        self.is_initialized = False

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def initialize(self):
        if self.is_initialized:
            return

        print("[ModelService] Initializing models...")

        # 1. Load dataset & train classical baselines on Task 4 split (reproducing exact historical models)
        if TASK4_DATASET.exists():
            df = pd.read_csv(TASK4_DATASET, encoding="latin-1")[["v1", "v2"]].rename(columns={"v1": "label", "v2": "msg"}).dropna()
            df["clean"] = df["msg"].apply(preprocess_text)
            df["y"] = df["label"].map({"ham": 0, "spam": 1})

            X_train, _, y_train, _ = train_test_split(
                df["clean"], df["y"], test_size=0.20, random_state=42, stratify=df["y"]
            )

            # Fit Naive Bayes Pipeline
            self.nb_pipeline = Pipeline([
                ("tfidf", TfidfVectorizer(max_features=5000, ngram_range=(1, 2))),
                ("clf", MultinomialNB(alpha=1.0))
            ])
            self.nb_pipeline.fit(X_train, y_train)

            # Fit Logistic Regression Pipeline
            self.lr_pipeline = Pipeline([
                ("tfidf", TfidfVectorizer(max_features=5000, ngram_range=(1, 2))),
                ("clf", LogisticRegression(max_iter=1000, random_state=42))
            ])
            self.lr_pipeline.fit(X_train, y_train)
            print("[ModelService] Classical models (Naive Bayes & Logistic Regression) loaded.")

        # 2. Load pre-trained BERT-Tiny
        try:
            self.bert_tokenizer = AutoTokenizer.from_pretrained(BERT_MODEL_NAME, local_files_only=True)
            self.bert_model = AutoModelForSequenceClassification.from_pretrained(BERT_MODEL_NAME, local_files_only=True)
            self.bert_model.eval()
            print("[ModelService] BERT-Tiny transformer loaded in CPU eval mode.")
        except Exception as e:
            print(f"[ModelService] Warning: Failed to load cached BERT-Tiny ({e}). Attempting remote load...")
            try:
                self.bert_tokenizer = AutoTokenizer.from_pretrained(BERT_MODEL_NAME)
                self.bert_model = AutoModelForSequenceClassification.from_pretrained(BERT_MODEL_NAME)
                self.bert_model.eval()
            except Exception as e2:
                print(f"[ModelService] Error: Could not initialize BERT-Tiny: {e2}")

        self.is_initialized = True

    def predict_naive_bayes(self, raw_text: str) -> Dict[str, Any]:
        """Runs Naive Bayes prediction on preprocessed text."""
        t0 = time.perf_counter()
        clean = preprocess_text(raw_text)
        probs = self.nb_pipeline.predict_proba([clean])[0]
        latency = (time.perf_counter() - t0) * 1000
        spam_p = float(probs[1])
        return {
            "model_name": "naive_bayes",
            "display_name": "Multinomial Naive Bayes",
            "architecture": "TF-IDF + Multinomial NB",
            "predicted_label": "SPAM" if spam_p >= 0.5 else "HAM",
            "spam_probability": round(spam_p, 4),
            "ham_confidence": round(float(probs[0]), 4),
            "latency_ms": round(latency, 2),
            "raw_logits": None
        }

    def predict_logistic_regression(self, raw_text: str) -> Dict[str, Any]:
        """Runs Logistic Regression prediction on preprocessed text."""
        t0 = time.perf_counter()
        clean = preprocess_text(raw_text)
        probs = self.lr_pipeline.predict_proba([clean])[0]
        latency = (time.perf_counter() - t0) * 1000
        spam_p = float(probs[1])
        return {
            "model_name": "logistic_regression",
            "display_name": "Logistic Regression",
            "architecture": "TF-IDF + L2 Logistic Regression",
            "predicted_label": "SPAM" if spam_p >= 0.5 else "HAM",
            "spam_probability": round(spam_p, 4),
            "ham_confidence": round(float(probs[0]), 4),
            "latency_ms": round(latency, 2),
            "raw_logits": None
        }

    def predict_bert_tiny(self, raw_text: str) -> Dict[str, Any]:
        """Runs BERT-Tiny transformer prediction on raw text."""
        if self.bert_model is None or self.bert_tokenizer is None:
            return {
                "model_name": "bert_tiny",
                "display_name": "BERT-Tiny Transformer",
                "architecture": "2-Layer Distilled Transformer",
                "predicted_label": "UNAVAILABLE",
                "spam_probability": 0.0,
                "ham_confidence": 0.0,
                "latency_ms": 0.0,
                "raw_logits": None
            }

        t0 = time.perf_counter()
        inputs = self.bert_tokenizer(raw_text, return_tensors="pt", truncation=True, max_length=128)
        with torch.no_grad():
            outputs = self.bert_model(**inputs)
            logits = outputs.logits[0]
            probs = torch.softmax(logits, dim=-1)
            raw_logits = [round(float(l), 3) for l in logits.tolist()]
            spam_p = float(probs[1].item())
            ham_p = float(probs[0].item())

        latency = (time.perf_counter() - t0) * 1000
        return {
            "model_name": "bert_tiny",
            "display_name": "BERT-Tiny Transformer",
            "architecture": "2-Layer Distilled Transformer (4.39M params)",
            "predicted_label": "SPAM" if spam_p >= 0.5 else "HAM",
            "spam_probability": round(spam_p, 4),
            "ham_confidence": round(ham_p, 4),
            "latency_ms": round(latency, 2),
            "raw_logits": raw_logits
        }

    def predict_all(self, raw_text: str) -> Dict[str, Any]:
        """Runs all three models on input text."""
        return {
            "naive_bayes": self.predict_naive_bayes(raw_text),
            "logistic_regression": self.predict_logistic_regression(raw_text),
            "bert_tiny": self.predict_bert_tiny(raw_text)
        }


def get_model_service() -> ModelService:
    """Convenience getter for singleton instance."""
    return ModelService.get_instance()

