"""
SpamGuard AI - Main FastAPI Application
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import CORS_ORIGINS
from app.ml.model_service import ModelService
from app.routers import analyze, models, metrics, history, threat_intel, dataset


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager: loads ML models into memory on startup."""
    print(">>> Initializing SpamGuard AI ML Engines...")
    service = ModelService.get_instance()
    service.initialize()
    print(">>> All models loaded successfully into CPU memory.")
    yield
    print(">>> Shutting down SpamGuard AI.")


app = FastAPI(
    title="SpamGuard AI - Enterprise Threat Intelligence API",
    description="Full-stack NLP and Transformer-based cybersecurity API for SMS and messaging threat detection.",
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

# Register routers
app.include_router(analyze.router, prefix="/api")
app.include_router(models.router, prefix="/api")
app.include_router(metrics.router, prefix="/api")
app.include_router(history.router, prefix="/api")
app.include_router(threat_intel.router, prefix="/api")
app.include_router(dataset.router, prefix="/api")


@app.get("/api/health", tags=["Health"])
def health_check():
    """Health check endpoint reporting system status and active models."""
    service = ModelService.get_instance()
    ready = service.is_initialized
    return {
        "status": "healthy" if ready else "initializing",
        "version": "2.0.0",
        "models_ready": ready,
        "engines": {
            "naive_bayes": service.nb_pipeline is not None,
            "logistic_regression": service.lr_pipeline is not None,
            "bert_tiny": service.bert_model is not None
        }
    }
