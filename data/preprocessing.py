"""
===========================================================
ModelMatch
Preprocessing Pipeline
===========================================================

This script builds the historical metadata database used
by the recommendation engine.

Output:
data/processed/openml_meta_features.csv
"""
import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import os
import warnings

import numpy as np
import pandas as pd

from sklearn.base import clone
from sklearn.datasets import (
    load_iris,
    load_wine,
    load_breast_cancer,
    load_digits,
    load_diabetes,
    load_linnerud,
)

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from sklearn.metrics import (
    accuracy_score,
    r2_score,
)

from sklearn.linear_model import (
    LogisticRegression,
    LinearRegression,
)

from sklearn.tree import DecisionTreeClassifier

from sklearn.ensemble import (
    RandomForestClassifier,
)

from sklearn.svm import (
    SVC,
)

from sklearn.neighbors import (
    KNeighborsClassifier,
)

from sklearn.naive_bayes import GaussianNB

from sklearn.utils import shuffle

warnings.filterwarnings("ignore")

# ---------------------------------------------------
# OUTPUT LOCATION
# ---------------------------------------------------

OUTPUT_DIR = "data/processed"
OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "openml_meta_features.csv",
)

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------------------------------------------
# CLASSIFICATION MODELS
# ---------------------------------------------------

CLASSIFICATION_MODELS = {

    "LogisticRegression":
        LogisticRegression(max_iter=500),

    "RandomForest":
        RandomForestClassifier(
            n_estimators=200,
            random_state=42,
        ),

    "DecisionTree":
        DecisionTreeClassifier(
            random_state=42,
        ),

    "SVM":
        SVC(),

    "KNN":
        KNeighborsClassifier(),

    "NaiveBayes":
        GaussianNB(),
}

# ---------------------------------------------------
# REGRESSION MODELS
# ---------------------------------------------------

REGRESSION_MODELS = {

    "LinearRegression":
        LinearRegression(),
}

# ---------------------------------------------------
# LOAD DATASETS
# ---------------------------------------------------

def load_all_datasets():

    datasets = []

    iris = load_iris(as_frame=True)
    datasets.append(
        (
            "iris",
            iris.frame,
            True,
        )
    )

    wine = load_wine(as_frame=True)
    datasets.append(
        (
            "wine",
            wine.frame,
            True,
        )
    )

    cancer = load_breast_cancer(as_frame=True)
    datasets.append(
        (
            "breast_cancer",
            cancer.frame,
            True,
        )
    )

    digits = load_digits(as_frame=True)
    datasets.append(
        (
            "digits",
            digits.frame,
            True,
        )
    )

    diabetes = load_diabetes(as_frame=True)

    diabetes_df = diabetes.frame.copy()

    diabetes_df.rename(
        columns={
            "target": "class"
        },
        inplace=True,
    )

    datasets.append(
        (
            "diabetes",
            diabetes_df,
            False,
        )
    )

    linnerud = load_linnerud(as_frame=True)

    linnerud_df = linnerud.data.copy()

    linnerud_df["class"] = (
        linnerud.target.iloc[:, 0]
    )

    datasets.append(
        (
            "linnerud",
            linnerud_df,
            False,
        )
    )

    return datasets

# ---------------------------------------------------
# CREATE VARIATIONS
# ---------------------------------------------------

def generate_variants(name, df, classification):

    variants = []

    variants.append(
        (
            f"{name}_original",
            df.copy(),
            classification,
        )
    )

    shuffled = shuffle(
        df,
        random_state=42,
    )

    variants.append(
        (
            f"{name}_shuffled",
            shuffled,
            classification,
        )
    )

    sampled = df.sample(
        frac=0.8,
        random_state=42,
    )

    variants.append(
        (
            f"{name}_sampled",
            sampled,
            classification,
        )
    )

    noisy = df.copy()

    feature_columns = noisy.columns[:-1]

    noise = np.random.normal(
        0,
        0.01,
        size=noisy[feature_columns].shape,
    )

    noisy[feature_columns] += noise

    variants.append(
        (
            f"{name}_noisy",
            noisy,
            classification,
        )
    )

    return variants
    # ---------------------------------------------------
# TRAINING UTILITIES
# ---------------------------------------------------

def evaluate_classification(df):

    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    best_model = None
    best_score = -1

    for model_name, model in CLASSIFICATION_MODELS.items():

        pipeline = Pipeline(
            [
                ("scaler", StandardScaler()),
                ("model", clone(model)),
            ]
        )

        pipeline.fit(X_train, y_train)

        predictions = pipeline.predict(X_test)

        score = accuracy_score(
            y_test,
            predictions,
        )

        if score > best_score:

            best_score = score
            best_model = model_name

    return best_model, round(best_score, 4)


# ---------------------------------------------------
# REGRESSION EVALUATION
# ---------------------------------------------------

def evaluate_regression(df):

    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
    )

    best_model = None
    best_score = -999999

    for model_name, model in REGRESSION_MODELS.items():

        pipeline = Pipeline(
            [
                ("scaler", StandardScaler()),
                ("model", clone(model)),
            ]
        )

        pipeline.fit(
            X_train,
            y_train,
        )

        predictions = pipeline.predict(
            X_test,
        )

        score = r2_score(
            y_test,
            predictions,
        )

        if score > best_score:

            best_score = score
            best_model = model_name

    return best_model, round(best_score, 4)


# ---------------------------------------------------
# SELECT BEST MODEL
# ---------------------------------------------------

def find_best_model(df, classification):

    if classification:

        return evaluate_classification(df)

    return evaluate_regression(df)


# ---------------------------------------------------
# META FEATURE EXTRACTION
# ---------------------------------------------------

from agents.meta_feature_extractor import MetaFeatureExtractor

extractor = MetaFeatureExtractor()


def extract_meta_features(temp_csv):

    meta = extractor.extract(temp_csv)

    return meta


# ---------------------------------------------------
# SAVE TEMP CSV
# ---------------------------------------------------

TEMP_FOLDER = "data/temp"

os.makedirs(
    TEMP_FOLDER,
    exist_ok=True,
)


def save_temp_dataset(dataset_name, dataframe):

    filepath = os.path.join(
        TEMP_FOLDER,
        dataset_name + ".csv",
    )

    dataframe.to_csv(
        filepath,
        index=False,
    )

    return filepath
    # ---------------------------------------------------
# BUILD HISTORICAL METADATA
# ---------------------------------------------------

def build_metadata():

    rows = []

    datasets = load_all_datasets()

    print("=" * 60)
    print("Generating historical metadata...")
    print("=" * 60)

    for dataset_name, dataframe, classification in datasets:

        print(f"\nProcessing {dataset_name}")

        variants = generate_variants(
            dataset_name,
            dataframe,
            classification,
        )

        for variant_name, variant_df, variant_classification in variants:

            print(f"   -> {variant_name}")

            try:

                # ------------------------------------
                # Save temporary CSV
                # ------------------------------------

                temp_csv = save_temp_dataset(
                    variant_name,
                    variant_df,
                )

                # ------------------------------------
                # Extract meta-features
                # ------------------------------------

                meta = extract_meta_features(
                    temp_csv,
                )

                # ------------------------------------
                # Train ML models
                # ------------------------------------

                best_model, score = find_best_model(
                    variant_df,
                    variant_classification,
                )

                # ------------------------------------
                # Build one metadata row
                # ------------------------------------

                row = {

                    "dataset_name": variant_name,

                    "best_model": best_model,

                    "score": score,

                }

                # add all extracted meta-features

                for key, value in meta.items():

                    row[key] = value

                rows.append(row)

            except Exception as e:

                print(
                    f"Failed on {variant_name}"
                )

                print(e)

    return pd.DataFrame(rows)
    # ---------------------------------------------------
# SAVE CSV
# ---------------------------------------------------

def save_metadata(df):

    # Remove duplicate datasets if any
    df = df.drop_duplicates(
        subset=["dataset_name"]
    )

    # Replace NaN/Inf because PostgreSQL JSON
    df = df.replace(
        [np.inf, -np.inf],
        np.nan,
    )

    df = df.fillna(0)

    # Sort alphabetically
    df = df.sort_values(
        by="dataset_name"
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    print("\n")
    print("=" * 60)
    print("Metadata successfully generated.")
    print("=" * 60)
    print(OUTPUT_FILE)
    print(f"Rows : {len(df)}")
    print(f"Columns : {len(df.columns)}")
    print("=" * 60)


# ---------------------------------------------------
# CLEAN TEMP FILES
# ---------------------------------------------------

def cleanup():

    if not os.path.exists(TEMP_FOLDER):
        return

    for file in os.listdir(TEMP_FOLDER):

        path = os.path.join(
            TEMP_FOLDER,
            file,
        )

        try:
            os.remove(path)
        except Exception:
            pass


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------

def main():

    print("\n")
    print("=" * 60)
    print("ModelMatch Historical Metadata Builder")
    print("=" * 60)

    dataframe = build_metadata()

    save_metadata(dataframe)

    cleanup()

    print("\nDone.")


# ---------------------------------------------------

if __name__ == "__main__":
    main()