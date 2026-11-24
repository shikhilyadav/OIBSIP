import json
import joblib
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
from app.config import MODEL_PATH, METADATA_PATH, DATA_PATH

class IrisService:
    _instance = None

    def __init__(self):
        self.artifact: Optional[Dict[str, Any]] = None
        self.pipeline = None
        self.model_name = "Random Forest Classifier"
        self.feature_names = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
        self.target_names = ["Setosa", "Versicolor", "Virginica"]
        self.metadata: Optional[Dict[str, Any]] = None
        self.df: Optional[pd.DataFrame] = None
        self.is_initialized = False

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def initialize(self):
        if self.is_initialized:
            return

        # 1. Load Model Artifact
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Model artifact not found at: {MODEL_PATH}")

        self.artifact = joblib.load(MODEL_PATH)
        self.pipeline = self.artifact["pipeline"]
        self.model_name = self.artifact.get("model_name", "Random Forest Classifier")
        self.feature_names = self.artifact.get("feature_names", self.feature_names)
        self.target_names = self.artifact.get("target_names", self.target_names)

        # 2. Load Metadata
        if METADATA_PATH.exists():
            with open(METADATA_PATH, "r", encoding="utf-8") as f:
                self.metadata = json.load(f)

        # 3. Load Dataset
        if DATA_PATH.exists():
            df = pd.read_csv(DATA_PATH)
            col_map = {
                "SepalLengthCm": "sepal_length",
                "SepalWidthCm": "sepal_width",
                "PetalLengthCm": "petal_length",
                "PetalWidthCm": "petal_width",
                "Species": "species"
            }
            df = df.rename(columns=col_map)
            if "Id" in df.columns:
                df = df.drop(columns=["Id"])
            df["species"] = df["species"].astype(str).str.replace("Iris-", "")
            self.df = df

        self.is_initialized = True

    def predict(self, sepal_length: float, sepal_width: float, petal_length: float, petal_width: float) -> Dict[str, Any]:
        """
        Executes prediction on input features using the exact serialized scikit-learn pipeline.
        Features must be ordered: ['sepal_length', 'sepal_width', 'petal_length', 'petal_width'].
        """
        if not self.is_initialized:
            self.initialize()

        # Build feature DataFrame matching trained column names
        X = pd.DataFrame([{
            "sepal_length": float(sepal_length),
            "sepal_width": float(sepal_width),
            "petal_length": float(petal_length),
            "petal_width": float(petal_width)
        }])[self.feature_names]

        # Raw pipeline prediction and predict_proba
        pred_class_id = int(self.pipeline.predict(X)[0])
        raw_probs = self.pipeline.predict_proba(X)[0]

        # Map to species names based on target_names: [0: Setosa, 1: Versicolor, 2: Virginica]
        species_label = self.target_names[pred_class_id]

        # Map classes to probabilities explicitly
        probs_dict = {
            self.target_names[i].lower(): round(float(raw_probs[i]), 4)
            for i in range(len(self.target_names))
        }

        confidence = round(float(raw_probs[pred_class_id]), 4)

        return {
            "class_id": pred_class_id,
            "species": f"Iris {species_label}",
            "confidence": confidence,
            "probabilities": probs_dict
        }

    def get_dataset_summary(self) -> Dict[str, Any]:
        if not self.is_initialized:
            self.initialize()

        df = self.df
        counts = df["species"].value_counts().to_dict()
        desc = df[self.feature_names].describe().round(3).to_dict()

        return {
            "total_specimens": len(df),
            "distinct_species": df["species"].nunique(),
            "species_names": sorted(df["species"].unique().tolist()),
            "feature_names": self.feature_names,
            "class_distribution": counts,
            "descriptive_statistics": desc
        }

    def get_records(self, species: Optional[str] = None, search: Optional[str] = None, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        if not self.is_initialized:
            self.initialize()

        filtered = self.df.copy()
        if species and species.lower() != "all":
            filtered = filtered[filtered["species"].str.lower() == species.lower()]

        if search:
            q = search.lower()
            filtered = filtered[
                filtered.apply(lambda r: q in str(r.to_dict()).lower(), axis=1)
            ]

        total = len(filtered)
        start = (page - 1) * page_size
        end = start + page_size
        records = filtered.iloc[start:end].to_dict(orient="records")

        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "records": records
        }

    def get_species_insights(self) -> Dict[str, Any]:
        if not self.is_initialized:
            self.initialize()

        insights = {}
        for sp in self.target_names:
            sub = self.df[self.df["species"] == sp]
            means = sub[self.feature_names].mean().round(2).to_dict()
            stds = sub[self.feature_names].std().round(2).to_dict()
            mins = sub[self.feature_names].min().round(2).to_dict()
            maxs = sub[self.feature_names].max().round(2).to_dict()

            notes = {
                "Setosa": {
                    "tagline": "Linear Separability & Arctic Origin",
                    "accent": "#76649D",
                    "description": "Exhibits compact petal structures (< 2 cm) combined with prominent sepal width. Linearly separable in petal feature space.",
                    "morphology": "Diminutive petals, robust broad sepals."
                },
                "Versicolor": {
                    "tagline": "Intermediate Harmonic Manifold",
                    "accent": "#C18E61",
                    "description": "Known as the Blue Flag iris. Occupies balanced intermediate coordinates between Setosa and Virginica across both sepal and petal axes.",
                    "morphology": "Moderate petal length (3.0-5.1 cm), slender sepals."
                },
                "Virginica": {
                    "tagline": "Maximum Structural Dimensions",
                    "accent": "#2C6A50",
                    "description": "Known as the Southern Blue Flag. Demonstrates the greatest overall structural scale with petal lengths exceeding 5.5 cm.",
                    "morphology": "Elongated petals (up to 6.9 cm), robust petal width."
                }
            }

            insights[sp] = {
                "species": sp,
                "count": len(sub),
                "means": means,
                "stds": stds,
                "mins": mins,
                "maxs": maxs,
                "profile": notes.get(sp, {})
            }

        return {"insights": insights}

    def get_metrics(self) -> Dict[str, Any]:
        if not self.is_initialized:
            self.initialize()

        return self.metadata if self.metadata else {}
