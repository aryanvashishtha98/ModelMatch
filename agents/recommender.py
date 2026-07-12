"""
===========================================================
ModelMatch Agent 2
===========================================================

Recommender (Planner)

Responsibility
--------------
Find similar historical datasets using KNN and recommend
the best-performing models.
"""

import numpy as np
import pandas as pd

from sklearn.impute import SimpleImputer
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler


class ModelRecommender:

    def __init__(self, metadata_file):

        self.metadata_file = metadata_file

        # -----------------------------
        # Load metadata
        # -----------------------------

        self.df = pd.read_csv(metadata_file)

        # Required columns
        required = [
            "dataset_name",
            "best_model",
            "score",
        ]

        for col in required:
            if col not in self.df.columns:
                raise ValueError(f"Missing required column: {col}")

        # -----------------------------
        # Meta-feature columns
        # -----------------------------

        self.meta_columns = [
            c
            for c in self.df.columns
            if c not in required
        ]

        # -----------------------------
        # Numeric conversion
        # -----------------------------

        X = self.df[self.meta_columns].copy()

        X = X.apply(
            pd.to_numeric,
            errors="coerce",
        )

        # Replace +/-inf
        X = X.replace(
            [np.inf, -np.inf],
            np.nan,
        )

        # -----------------------------
        # Impute missing values
        # -----------------------------

        self.imputer = SimpleImputer(
            strategy="constant",
            fill_value=0,
        )

        X = self.imputer.fit_transform(X)

        # -----------------------------
        # Feature scaling
        # -----------------------------

        self.scaler = StandardScaler()

        X = self.scaler.fit_transform(X)

        # -----------------------------
        # Train KNN
        # -----------------------------

        neighbors = min(5, len(self.df))

        self.knn = NearestNeighbors(
            n_neighbors=neighbors,
            metric="euclidean",
        )

        self.knn.fit(X)

    # =====================================================
    # Recommendation
    # =====================================================

    def recommend(self, meta_features):

        query = []

        for column in self.meta_columns:

            value = meta_features.get(column, 0)

            if value is None:
                value = 0

            try:
                value = float(value)
            except Exception:
                value = 0

            if np.isnan(value) or np.isinf(value):
                value = 0

            query.append(value)

        query = np.array(query).reshape(1, -1)

        # Apply same preprocessing
        query = self.imputer.transform(query)
        query = self.scaler.transform(query)

        distances, indices = self.knn.kneighbors(query)

        neighbors = self.df.iloc[indices[0]].copy()

        neighbors["distance"] = distances[0]

        neighbors = neighbors.sort_values(
            by=["score", "distance"],
            ascending=[False, True],
        )

        recommendations = []

        seen_models = set()

        for _, row in neighbors.iterrows():

            model = row["best_model"]

            if model in seen_models:
                continue

            seen_models.add(model)

            recommendations.append(
                {
                    "dataset": row["dataset_name"],
                    "model": model,
                    "score": float(row["score"]),
                    "distance": round(float(row["distance"]), 4),
                }
            )

        reasoning = (
            "Recommendations are based on the nearest historical "
            "datasets using meta-feature similarity (KNN). "
            "Missing values were automatically handled before "
            "similarity computation."
        )

        return {
            "recommendations": recommendations,
            "reasoning": reasoning,
        }