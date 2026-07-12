"""
Recommendation Service

Responsibilities
----------------
1. Load uploaded dataset.
2. Query historical OpenML meta-features.
3. Run KNN similarity.
4. Store recommendation history.
"""

import json

from sqlalchemy.orm import Session

from agents.recommender import ModelRecommender
from backend.models import Dataset
from backend.models import Recommendation


class RecommendationService:

    def __init__(self, db: Session):

        self.db = db

        self.recommender = ModelRecommender(
            "data/processed/openml_meta_features.csv"
        )

    def recommend(self, dataset_id):

        dataset = (
            self.db.query(Dataset)
            .filter(Dataset.id == dataset_id)
            .first()
        )

        if dataset is None:
            raise Exception("Dataset not found.")

        result = self.recommender.recommend(
            dataset.meta_features
        )

        recommendation = Recommendation(

            dataset_id=dataset.id,

            ranked_shortlist=result["recommendations"],

            reasoning=result["reasoning"]

        )

        self.db.add(recommendation)

        self.db.commit()

        self.db.refresh(recommendation)

        return {

            "dataset_id": dataset.id,

            "recommendations":
            result["recommendations"],

            "reasoning":
            result["reasoning"]

        }

    def history(self, dataset_id):

        rows = (

            self.db.query(Recommendation)

            .filter(
                Recommendation.dataset_id == dataset_id
            )

            .all()

        )

        history = []

        for row in rows:

            history.append({

                "id": row.id,

                "recommendations": row.ranked_shortlist,

                "reasoning": row.reasoning,

                "created_at": row.created_at

            })

        return history