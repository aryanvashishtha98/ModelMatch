"""
ModelMatch Agent 4
==================

Evolver / Validator

Responsibility
--------------
Store newly verified model results into the
knowledge base so future recommendations
improve continuously.

Input:
    Dataset information
    Model results

Output:
    Database record
"""

from datetime import datetime

from sqlalchemy.orm import Session

from backend.models import Run


class EvolverValidator:

    def __init__(self, db: Session):

        self.db = db

    def log_result(
        self,
        dataset_id,
        result
    ):

        run = Run(

            dataset_id=dataset_id,

            model_name=result["model"],

            hyperparameters=result["parameters"],

            score=result["best_score"],

            metric_type="accuracy",

            created_at=datetime.utcnow()

        )

        self.db.add(run)

        self.db.commit()

        self.db.refresh(run)

        return run

    def log_multiple(
        self,
        dataset_id,
        results
    ):

        stored = []

        for result in results:

            stored.append(
                self.log_result(
                    dataset_id,
                    result
                )
            )

        return stored