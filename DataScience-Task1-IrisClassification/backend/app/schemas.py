from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any

class PredictionInput(BaseModel):
    sepal_length: float = Field(..., ge=0.1, le=15.0, description="Sepal length in cm")
    sepal_width: float = Field(..., ge=0.1, le=10.0, description="Sepal width in cm")
    petal_length: float = Field(..., ge=0.1, le=15.0, description="Petal length in cm")
    petal_width: float = Field(..., ge=0.01, le=10.0, description="Petal width in cm")

class PredictionResult(BaseModel):
    class_id: int
    species: str
    confidence: float
    probabilities: Dict[str, float]

class PredictionResponse(BaseModel):
    success: bool
    prediction: PredictionResult
    input: Dict[str, float]
    model_name: str

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    dataset_loaded: bool
    version: str
    model_name: str

class DatasetSummary(BaseModel):
    total_specimens: int
    distinct_species: int
    species_names: List[str]
    feature_names: List[str]
    class_distribution: Dict[str, int]
    descriptive_statistics: Dict[str, Dict[str, float]]

class SpeciesInsightsResponse(BaseModel):
    insights: Dict[str, Dict[str, Any]]
