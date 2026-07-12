"""
ModelMatch
-----------

Fetch historical ML experiment information from OpenML.

Responsibilities
----------------
1. Download classification datasets.
2. Extract meta-features using pymfe.
3. Store cleaned information for recommendation.
"""

import json
import warnings
from pathlib import Path

import openml
import pandas as pd
from pymfe.mfe import MFE

warnings.filterwarnings("ignore")

OUTPUT_DIR = Path("processed")
OUTPUT_DIR.mkdir(exist_ok=True)


# ---------------------------------------------------
# Configuration
# ---------------------------------------------------

MAX_DATASETS = 25


# ---------------------------------------------------
# Utility Functions
# ---------------------------------------------------

def clean_dataframe(df):
    """
    Replace missing values for meta-feature extraction.
    """

    for column in df.columns:

        if df[column].dtype == object:
            df[column] = df[column].fillna("missing")
        else:
            df[column] = df[column].fillna(df[column].median())

    return df


def extract_meta_features(X, y):
    """
    Extract statistical meta-features using pymfe.
    """

    mfe = MFE()

    mfe.fit(X.values, y.values)

    names, values = mfe.extract()

    meta = {}

    for name, value in zip(names, values):

        try:
            meta[name] = float(value)

        except Exception:
            meta[name] = str(value)

    return meta


# ---------------------------------------------------
# OpenML Processing
# ---------------------------------------------------

def fetch_classification_tasks():

    print("\nDownloading OpenML task list...\n")

    tasks = openml.tasks.list_tasks(
        task_type_id=1,
        output_format="dataframe"
    )

    tasks = tasks.head(MAX_DATASETS)

    print(f"Found {len(tasks)} tasks.\n")

    return tasks


def process_task(task_id):

    print(f"Processing Task {task_id}")

    task = openml.tasks.get_task(task_id)

    dataset = task.get_dataset()

    X, y, categorical, attribute_names = dataset.get_data(
        target=dataset.default_target_attribute
    )

    X = clean_dataframe(X)

    meta_features = extract_meta_features(X, y)

    info = {

        "task_id": task_id,

        "dataset_id": dataset.dataset_id,

        "dataset_name": dataset.name,

        "instances": len(X),

        "features": len(X.columns),

        "target": dataset.default_target_attribute,

        "meta_features": meta_features

    }

    return info


def main():

    tasks = fetch_classification_tasks()

    all_results = []

    for task_id in tasks.task_id.tolist():

        try:

            result = process_task(task_id)

            all_results.append(result)

        except Exception as e:

            print(f"Skipping Task {task_id}: {e}")

    output_file = OUTPUT_DIR / "openml_meta_features.json"

    with open(output_file, "w") as f:

        json.dump(all_results, f, indent=4)

    pd.DataFrame(all_results).to_csv(
        OUTPUT_DIR / "openml_meta_features.csv",
        index=False
    )

    print("\nCompleted Successfully.")
    print(f"Saved {len(all_results)} datasets.")


if __name__ == "__main__":
    main()