"""
Pydantic Schemas
"""

from datetime import datetime
from typing import Dict
from typing import List
from typing import Optional

from pydantic import BaseModel


class DatasetCreate(BaseModel):

    name: str

    source: str

    meta_features: Dict


class DatasetResponse(BaseModel):

    id: int

    name: str

    source: str

    meta_features: Dict

    created_at: datetime

    class Config:

        from_attributes = True


class RecommendationResponse(BaseModel):

    recommendations: List[Dict]

    reasoning: str


class RunResponse(BaseModel):

    model_name: str

    hyperparameters: Dict

    score: float

    metric_type: str


class HistoryResponse(BaseModel):

    dataset: str

    model: str

    score: float

    created_at: datetime