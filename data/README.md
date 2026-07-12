# Data Collection

## Data Source

ModelMatch uses **OpenML**, a publicly available machine learning repository containing thousands of benchmark datasets and experiment records.

Official Website:

https://www.openml.org

---

## Why OpenML?

The objective of ModelMatch is to recommend machine learning models based on **real historical evidence** rather than synthetic examples or manually created rules.

OpenML provides:

- Real benchmark datasets
- Standardized machine learning tasks
- Historical experiment results
- Dataset metadata
- Community-verified evaluations

This makes it an ideal knowledge source for meta-learning.

---

## Data Pipeline

The ingestion pipeline performs the following steps:

1. Download classification tasks.
2. Retrieve associated datasets.
3. Load feature matrix and target labels.
4. Clean missing values.
5. Extract statistical meta-features using **PyMFE**.
6. Save processed metadata for recommendation.
7. Store future experiment results in PostgreSQL.

---

## Meta-Features Extracted

Examples include:

- Number of rows
- Number of columns
- Missing value percentage
- Numerical feature ratio
- Categorical feature ratio
- Correlation statistics
- Class imbalance
- Entropy
- Skewness
- Kurtosis
- Landmarking measures
- Information-theoretic measures

These characteristics describe datasets independently of their domain.

---

## Why These Features?

Instead of comparing raw datasets, ModelMatch compares **dataset characteristics**.

Datasets with similar statistical properties often exhibit similar machine learning behavior.

This enables recommendation through historical similarity.

---

## Data Cleaning

Before feature extraction:

- Missing numerical values → median imputation
- Missing categorical values → "missing"
- Invalid datasets skipped
- Corrupted tasks ignored
- Exceptions logged

---

## Output Files

```
processed/
│
├── openml_meta_features.csv
└── openml_meta_features.json
```

These files are later inserted into the PostgreSQL database and queried by the recommendation engine.

---

## Why This Data Fits the Problem

ModelMatch is designed to recommend machine learning models using **historical performance evidence**.

OpenML provides exactly this:

- Real datasets
- Real benchmark experiments
- Real evaluation metrics

Unlike synthetic datasets or manually generated rules, OpenML reflects how algorithms actually perform across diverse real-world problems.

This historical grounding allows ModelMatch to make transparent, evidence-based recommendations rather than relying on heuristic guesses.