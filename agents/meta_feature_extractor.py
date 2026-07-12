"""
ModelMatch Agent 1
==================

Meta Feature Extractor (Retriever)

Responsibility
--------------
Accepts a user uploaded dataset and computes statistical
meta-features using PyMFE.

Input:
    CSV Dataset

Output:
    Dictionary containing dataset meta-features.
"""

from pathlib import Path

import pandas as pd
from pymfe.mfe import MFE


class MetaFeatureExtractor:

    def __init__(self):
        pass

    def _clean_dataframe(self, df: pd.DataFrame):

        df = df.copy()

        for column in df.columns:

            if df[column].dtype == object:
                df[column] = df[column].fillna("missing")
            else:
                df[column] = df[column].fillna(df[column].median())

        return df

    def _separate_target(self, df):

        target = df.columns[-1]

        X = df.drop(columns=[target])

        y = df[target]

        return X, y

    def extract(self, csv_path: str):

        csv_path = Path(csv_path)

        if not csv_path.exists():
            raise FileNotFoundError(csv_path)

        df = pd.read_csv(csv_path)

        import numpy as np

        X, y = self._separate_target(df)

        X = self._clean_dataframe(X)

        # Convert to NumPy arrays explicitly
        X = np.asarray(X.to_numpy(), dtype=float)
        y = np.asarray(y.to_numpy()).ravel()

        mfe = MFE()

        mfe.fit(X, y)

        names, values = mfe.extract()
        

        meta = {}

        import math

        for n, v in zip(names, values):

            try:
               value = float(v)

               # PostgreSQL JSONB doesn't support NaN or Infinity
               if math.isnan(value) or math.isinf(value):
                  value = None

               meta[n] = value

            except Exception:
               meta[n] = None if str(v).lower() == "nan" else str(v)

        meta["rows"] = len(df)
        meta["columns"] = len(df.columns)
        meta["missing_percentage"] = (
            df.isnull().sum().sum()
            /
            (df.shape[0] * df.shape[1])
        ) * 100

        return meta