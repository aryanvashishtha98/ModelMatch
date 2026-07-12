"""
Upload Service

Responsibilities
----------------
1. Validate uploaded CSV.
2. Extract meta-features.
3. Store dataset information.
4. Return dataset_id + extracted features.
"""

import os

from sqlalchemy.orm import Session

from agents.meta_feature_extractor import MetaFeatureExtractor
from backend.models import Dataset
from backend.utils import save_uploaded_file
from backend.utils import validate_csv
from backend.utils import file_size_ok


class UploadService:

    def __init__(self, db: Session):
        self.db = db
        self.extractor = MetaFeatureExtractor()

    def upload_dataset(self, upload_file):

        # Validate extension
        validate_csv(upload_file)

        # Save file
        filepath = save_uploaded_file(upload_file)

        # Validate file size
        if not file_size_ok(filepath):
            os.remove(filepath)
            raise Exception("Uploaded file exceeds allowed size.")

        # Extract meta-features
        try:
           meta_features = self.extractor.extract(filepath)
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise

        # Store dataset
        dataset = Dataset(
            name=upload_file.filename,
            source="user-upload",
            meta_features=meta_features
        )

        self.db.add(dataset)
        self.db.commit()
        self.db.refresh(dataset)

        return {
            "dataset_id": dataset.id,
            "dataset_name": dataset.name,
            "meta_features": meta_features
        }

    def get_dataset(self, dataset_id):

        dataset = (
            self.db.query(Dataset)
            .filter(Dataset.id == dataset_id)
            .first()
        )

        if dataset is None:
            raise Exception("Dataset not found.")

        return dataset