"""
AutoValue AI — FastAPI Backend Server.
Production REST endpoints for used car valuation, dataset exploration, and model telemetry.
"""
from contextlib import asynccontextmanager
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.config import CORS_ORIGINS
from app.services import CarPriceService


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(">>> Initializing AutoValue AI Regression Service...")
    service = CarPriceService.get_instance()
    service.initialize()
    print(">>> AutoValue AI Pipeline & Cleaned Dataset Loaded.")
    yield
    print(">>> Shutting down AutoValue AI Backend.")


app = FastAPI(
    title="AutoValue AI — Automotive Valuation API",
    description="Enterprise Machine Learning REST API for Automotive Used Car Price Estimation.",
    version="2.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PredictRequest(BaseModel):
    brand: str = Field(..., example="Maruti")
    year: int = Field(..., ge=1990, le=2024, example=2017)
    km_driven: float = Field(..., ge=0, example=45000)
    fuel: str = Field(..., example="Petrol")
    seller_type: str = Field(..., example="Individual")
    transmission: str = Field(..., example="Manual")
    owner: str = Field(..., example="First Owner")


class BatchPredictRequest(BaseModel):
    items: List[PredictRequest]


@app.get("/api/health", tags=["System"])
def health_check():
    service = CarPriceService.get_instance()
    if not service.is_initialized:
        service.initialize()
    return {
        "status": "healthy" if service.is_initialized else "initializing",
        "model_loaded": service.pipeline is not None,
        "dataset_loaded": service.df is not None,
        "version": "2.0.0",
        "algorithm": service.metadata.get("best_model_name", "Linear Regression")
    }


@app.post("/api/predict", tags=["Inference"])
def predict_car_price(req: PredictRequest):
    service = CarPriceService.get_instance()
    try:
        res = service.predict(
            brand=req.brand,
            year=req.year,
            km_driven=req.km_driven,
            fuel=req.fuel,
            seller_type=req.seller_type,
            transmission=req.transmission,
            owner=req.owner
        )
        return {"success": True, "data": res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Valuation error: {str(e)}")


@app.post("/api/predict/batch", tags=["Inference"])
def predict_batch(req: BatchPredictRequest):
    service = CarPriceService.get_instance()
    results = []
    for item in req.items[:100]:
        res = service.predict(
            brand=item.brand,
            year=item.year,
            km_driven=item.km_driven,
            fuel=item.fuel,
            seller_type=item.seller_type,
            transmission=item.transmission,
            owner=item.owner
        )
        results.append(res)
    return {"total": len(results), "results": results}


@app.get("/api/dataset/summary", tags=["Dataset"])
def get_dataset_summary():
    service = CarPriceService.get_instance()
    return service.get_summary()


@app.get("/api/dataset/records", tags=["Dataset"])
def get_dataset_records(
    brand: Optional[str] = Query(None),
    fuel: Optional[str] = Query(None),
    transmission: Optional[str] = Query(None),
    min_year: Optional[int] = Query(None),
    max_year: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    service = CarPriceService.get_instance()
    return service.get_records(
        brand=brand,
        fuel=fuel,
        transmission=transmission,
        min_year=min_year,
        max_year=max_year,
        search=search,
        page=page,
        page_size=page_size
    )


@app.get("/api/dataset/options", tags=["Dataset"])
def get_dataset_options():
    service = CarPriceService.get_instance()
    return service.get_options()


@app.get("/api/metrics", tags=["Model"])
def get_metrics():
    service = CarPriceService.get_instance()
    return service.get_metrics()


@app.get("/api/models/feature-importance", tags=["Model"])
def get_feature_importance():
    service = CarPriceService.get_instance()
    return service.get_feature_importance()


@app.get("/api/models/info", tags=["Model"])
def get_model_info():
    service = CarPriceService.get_instance()
    return {
        "model_name": service.metadata.get("best_model_name", "Linear Regression"),
        "features": service.metadata.get("feature_columns", []),
        "categorical_features": service.metadata.get("categorical_features", []),
        "numerical_features": service.metadata.get("numerical_features", []),
        "train_size": service.metadata.get("train_observations", 2861),
        "test_size": service.metadata.get("test_observations", 716),
        "test_r2": service.metadata.get("model_comparison", {}).get("Linear Regression", {}).get("test_r2", 0.712)
    }
