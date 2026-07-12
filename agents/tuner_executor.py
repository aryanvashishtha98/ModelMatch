import warnings
warnings.filterwarnings("ignore")

import optuna
import pandas as pd
import numpy as np

from pathlib import Path

from sklearn.model_selection import (
    StratifiedKFold,
    cross_val_score,
    train_test_split,
)

from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

from lightgbm import LGBMClassifier


class ModelExecutor:

    def __init__(self, csv_path):

        self.csv_path = csv_path

        self.df = pd.read_csv(csv_path)

        self.target_column = self.df.columns[-1]

        self.X = self.df.drop(columns=[self.target_column])

        self.y = self.df[self.target_column]

        # -----------------------------
        # Encode target if needed
        # -----------------------------
        if self.y.dtype == object:

            from sklearn.preprocessing import LabelEncoder

            encoder = LabelEncoder()

            self.y = encoder.fit_transform(self.y)

        # -----------------------------
        # Convert categorical columns
        # -----------------------------
        self.X = pd.get_dummies(self.X)

        # -----------------------------
        # Missing values
        # -----------------------------
        self.X = self.X.replace([np.inf, -np.inf], np.nan)

        imputer = SimpleImputer(strategy="median")

        self.X = pd.DataFrame(
            imputer.fit_transform(self.X),
            columns=self.X.columns,
        )

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X,
            self.y,
            test_size=0.20,
            random_state=42,
            stratify=self.y,
        )

        self.cv = StratifiedKFold(
            n_splits=5,
            shuffle=True,
            random_state=42,
        )

    # ==========================================================
    # Random Forest Objective
    # ==========================================================

    def rf_objective(self, trial):

        params = {

            "n_estimators": trial.suggest_int(
                "n_estimators",
                100,
                300,
            ),

            "max_depth": trial.suggest_int(
                "max_depth",
                3,
                20,
            ),

            "min_samples_split": trial.suggest_int(
                "min_samples_split",
                2,
                10,
            ),

            "min_samples_leaf": trial.suggest_int(
                "min_samples_leaf",
                1,
                5,
            ),

            "random_state": 42,
        }

        model = RandomForestClassifier(**params)

        score = cross_val_score(
            model,
            self.X_train,
            self.y_train,
            cv=self.cv,
            scoring="accuracy",
        ).mean()

        return score

    # ==========================================================
    # SVM Objective
    # ==========================================================

    def svm_objective(self, trial):

        params = {

            "C": trial.suggest_float(
                "C",
                0.01,
                100,
                log=True,
            ),

            "kernel": trial.suggest_categorical(
                "kernel",
                [
                    "linear",
                    "rbf",
                    "poly",
                ],
            ),

            "gamma": trial.suggest_categorical(
                "gamma",
                [
                    "scale",
                    "auto",
                ],
            ),
        }

        pipeline = Pipeline(

            [

                ("scaler", StandardScaler()),

                ("svm", SVC(**params)),
            ]

        )

        score = cross_val_score(

            pipeline,

            self.X_train,

            self.y_train,

            cv=self.cv,

            scoring="accuracy",

        ).mean()

        return score

    # ==========================================================
    # LightGBM Objective
    # ==========================================================

    def lgbm_objective(self, trial):

        params = {

            "n_estimators": trial.suggest_int(
                "n_estimators",
                100,
                300,
            ),

            "learning_rate": trial.suggest_float(
                "learning_rate",
                0.01,
                0.30,
            ),

            "num_leaves": trial.suggest_int(
                "num_leaves",
                20,
                80,
            ),

            "max_depth": trial.suggest_int(
                "max_depth",
                3,
                15,
            ),

            "random_state": 42,

            "verbosity": -1,
        }

        model = LGBMClassifier(**params)

        score = cross_val_score(

            model,

            self.X_train,

            self.y_train,

            cv=self.cv,

            scoring="accuracy",

        ).mean()

        return score
            # ==========================================================
    # Random Forest Tuning
    # ==========================================================

    def tune_random_forest(self):

        study = optuna.create_study(direction="maximize")

        study.optimize(self.rf_objective, n_trials=20, show_progress_bar=False)

        best_params = study.best_params

        model = RandomForestClassifier(

            **best_params,

            random_state=42,

        )

        model.fit(self.X_train, self.y_train)

        score = model.score(self.X_test, self.y_test)

        return {

            "model": "Random Forest",

            "best_score": float(score),

            "parameters": best_params,

        }

    # ==========================================================
    # SVM Tuning
    # ==========================================================

    def tune_svm(self):

        study = optuna.create_study(direction="maximize")

        study.optimize(self.svm_objective, n_trials=20, show_progress_bar=False)

        best_params = study.best_params

        pipeline = Pipeline(

            [

                ("scaler", StandardScaler()),

                ("svm", SVC(**best_params)),

            ]

        )

        pipeline.fit(self.X_train, self.y_train)

        score = pipeline.score(self.X_test, self.y_test)

        return {

            "model": "SVM",

            "best_score": float(score),

            "parameters": best_params,

        }

    # ==========================================================
    # LightGBM Tuning
    # ==========================================================

    def tune_lightgbm(self):

        study = optuna.create_study(direction="maximize")

        study.optimize(self.lgbm_objective, n_trials=20, show_progress_bar=False)

        best_params = study.best_params

        model = LGBMClassifier(

            **best_params,

            random_state=42,

            verbosity=-1,

        )

        model.fit(self.X_train, self.y_train)

        score = model.score(self.X_test, self.y_test)

        return {

            "model": "LightGBM",

            "best_score": float(score),

            "parameters": best_params,

        }
            # ==========================================================
    # Execute Complete AutoML Pipeline
    # ==========================================================

    def execute(self):

        print("\n========================================")
        print("Running AutoML Hyperparameter Tuning")
        print("========================================")

        rf_result = self.tune_random_forest()

        print(
            f"✓ Random Forest tuned | Accuracy = {rf_result['best_score']:.4f}"
        )

        svm_result = self.tune_svm()

        print(
            f"✓ SVM tuned | Accuracy = {svm_result['best_score']:.4f}"
        )

        lgbm_result = self.tune_lightgbm()

        print(
            f"✓ LightGBM tuned | Accuracy = {lgbm_result['best_score']:.4f}"
        )

        results = [

            rf_result,

            lgbm_result,

            svm_result,

        ]

        results = sorted(

            results,

            key=lambda x: x["best_score"],

            reverse=True,

        )

        print("\n========================================")
        print("Final Ranking")
        print("========================================")

        for i, model in enumerate(results, start=1):

            print(

                f"{i}. {model['model']}  "

                f"Accuracy = {model['best_score']:.4f}"

            )

        print("========================================\n")

        return results