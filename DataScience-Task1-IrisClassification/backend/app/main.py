"""
FastAPI Application for IrisAI Botanical Intelligence Studio
"""
from contextlib import asynccontextmanager
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app.config import CORS_ORIGINS
from app.schemas import (
    PredictionInput,
    PredictionResponse,
    PredictionResult,
    HealthResponse,
    DatasetSummary,
    SpeciesInsightsResponse
)
from app.services import IrisService


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(">>> Initializing IrisAI Botanical Model Service...")
    service = IrisService.get_instance()
    service.initialize()
    print(">>> IrisAI Model & Dataset Loaded Successfully.")
    yield
    print(">>> Shutting down IrisAI Backend.")


app = FastAPI(
    title="IrisAI — Botanical Intelligence API",
    description="Enterprise Machine Learning REST API for Taxonomic Iris Classification.",
    version="2.0.0",
    lifespan=lifespan
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", response_model=HealthResponse, tags=["System"])
def health_check():
    service = IrisService.get_instance()
    if not service.is_initialized:
        service.initialize()
    return {
        "status": "healthy" if service.is_initialized else "initializing",
        "model_loaded": service.pipeline is not None,
        "dataset_loaded": service.df is not None,
        "version": "2.0.0",
        "model_name": service.model_name
    }


@app.post("/api/predict", response_model=PredictionResponse, tags=["Inference"])
def predict_specimen(req: PredictionInput):
    service = IrisService.get_instance()
    try:
        res = service.predict(
            sepal_length=req.sepal_length,
            sepal_width=req.sepal_width,
            petal_length=req.petal_length,
            petal_width=req.petal_width
        )
        return {
            "success": True,
            "prediction": res,
            "input": {
                "sepal_length": req.sepal_length,
                "sepal_width": req.sepal_width,
                "petal_length": req.petal_length,
                "petal_width": req.petal_width
            },
            "model_name": service.model_name
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.get("/api/dataset/summary", response_model=DatasetSummary, tags=["Dataset"])
def get_dataset_summary():
    service = IrisService.get_instance()
    return service.get_dataset_summary()


@app.get("/api/dataset/records", tags=["Dataset"])
def get_dataset_records(
    species: Optional[str] = Query(None, description="Filter by species: Setosa, Versicolor, Virginica"),
    search: Optional[str] = Query(None, description="Search keyword in records"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=150)
):
    service = IrisService.get_instance()
    return service.get_records(species=species, search=search, page=page, page_size=page_size)


@app.get("/api/species/insights", response_model=SpeciesInsightsResponse, tags=["Dataset"])
def get_species_insights():
    service = IrisService.get_instance()
    return service.get_species_insights()


@app.get("/api/metrics", tags=["Model"])
def get_metrics():
    service = IrisService.get_instance()
    return service.get_metrics()


@app.get("/api/model/info", tags=["Model"])
def get_model_info():
    service = IrisService.get_instance()
    if not service.is_initialized:
        service.initialize()
    return {
        "model_name": service.model_name,
        "model_type": service.model_name,
        "features": service.feature_names,
        "feature_names": service.feature_names,
        "classes": service.target_names,
        "target_names": service.target_names,
        "artifact_loaded": service.is_initialized
    }
