"""
Tuning Service

Responsibilities
----------------
1. Load uploaded dataset.
2. Execute recommended models.
3. Perform Optuna tuning.
4. Store verified results.
5. Return ranked scores.
"""

import os

from sqlalchemy.orm import Session

from agents.tuner_executor import ModelExecutor
from agents.evolver_validator import EvolverValidator

from backend.models import Dataset
from backend.models import Recommendation


class TuningService:

    def __init__(self, db: Session):

        self.db = db

        self.validator = EvolverValidator(db)

    def run(self, dataset_id):

        dataset = (

            self.db.query(Dataset)

            .filter(Dataset.id == dataset_id)

            .first()

        )

        if dataset is None:

            raise Exception("Dataset not found.")

        csv_path = os.path.join(
            "backend",
            "uploads",
            dataset.name
        )

        if not os.path.exists(csv_path):

            raise FileNotFoundError(csv_path)

        executor = ModelExecutor(csv_path)

        results = executor.execute()

        self.validator.log_multiple(
            dataset.id,
            results
        )

        recommendation = (

            self.db.query(Recommendation)

            .filter(
                Recommendation.dataset_id == dataset.id
            )

            .order_by(
                Recommendation.created_at.desc()
            )

            .first()

        )

        return {

            "dataset_id": dataset.id,

            "recommendation": recommendation.ranked_shortlist
            if recommendation
            else [],

            "verified_results": results

        }