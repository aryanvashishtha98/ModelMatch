"""
History Service

Responsibilities
----------------
Return previous recommendations and
verified tuning runs.
"""

from sqlalchemy.orm import Session

from backend.models import Dataset
from backend.models import Run


class HistoryService:

    def __init__(self, db: Session):

        self.db = db

    def get_history(self):

        rows = (

            self.db.query(
                Dataset,
                Run
            )

            .join(
                Run,
                Dataset.id == Run.dataset_id
            )

            .order_by(
                Run.created_at.desc()
            )

            .all()

        )

        history = []

        for dataset, run in rows:

            history.append(

                {

                    "dataset_id": dataset.id,

                    "dataset_name": dataset.name,

                    "model": run.model_name,

                    "score": run.score,

                    "metric": run.metric_type,

                    "hyperparameters":
                    run.hyperparameters,

                    "created_at":
                    run.created_at

                }

            )

        return history

    def get_dataset_history(
        self,
        dataset_id
    ):

        rows = (

            self.db.query(Run)

            .filter(
                Run.dataset_id == dataset_id
            )

            .order_by(
                Run.score.desc()
            )

            .all()

        )

        response = []

        for run in rows:

            response.append(

                {

                    "model": run.model_name,

                    "score": run.score,

                    "metric": run.metric_type,

                    "hyperparameters":
                    run.hyperparameters,

                    "created_at":
                    run.created_at

                }

            )

        return response