"""
ModelMatch Backend

FastAPI Application Entry Point

Endpoints
---------
POST    /upload-dataset
GET     /get-recommendation/{dataset_id}
POST    /run-tuning/{dataset_id}
GET     /get-history

Swagger
--------
/docs

ReDoc
------
/redoc
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import settings
from backend.database import Base
from backend.database import engine

from backend.routers.upload import router as upload_router
from backend.routers.recommendation import router as recommendation_router
from backend.routers.tuning import router as tuning_router
from backend.routers.history import router as history_router


# --------------------------------------------------
# Create Database Tables
# --------------------------------------------------

Base.metadata.create_all(bind=engine)


# --------------------------------------------------
# FastAPI App
# --------------------------------------------------

app = FastAPI(

    title=settings.APP_NAME,

    version=settings.APP_VERSION,

    description="""
ModelMatch

Meta-Learning Powered Model Recommendation Engine

Workflow

1 Upload Dataset

2 Extract Meta Features

3 Recommend Models

4 Hyperparameter Tuning

5 Store Verified Results

6 Improve Future Recommendations
""",

    docs_url="/docs",

    redoc_url="/redoc"

)


# --------------------------------------------------
# Enable CORS
# --------------------------------------------------

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)


# --------------------------------------------------
# Register Routers
# --------------------------------------------------

app.include_router(upload_router)

app.include_router(recommendation_router)

app.include_router(tuning_router)

app.include_router(history_router)


# --------------------------------------------------
# Root Endpoint
# --------------------------------------------------

@app.get("/")

def root():

    return {

        "application": settings.APP_NAME,

        "version": settings.APP_VERSION,

        "status": "running",

        "documentation": "/docs"

    }


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/health")

def health():

    return {

        "status": "healthy"

    }


# --------------------------------------------------
# Startup Event
# --------------------------------------------------

@app.on_event("startup")

def startup():

    print("=" * 60)

    print("ModelMatch Backend Started")

    print("=" * 60)

    print("Swagger Docs")

    print("http://localhost:8000/docs")

    print()

    print("ReDoc")

    print("http://localhost:8000/redoc")

    print("=" * 60)


# --------------------------------------------------
# Shutdown Event
# --------------------------------------------------

@app.on_event("shutdown")

def shutdown():

    print()

    print("Stopping ModelMatch Backend...")

    print("Goodbye!")

    print()