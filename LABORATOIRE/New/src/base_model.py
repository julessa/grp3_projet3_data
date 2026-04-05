"""
module base_model.py

Utilitaires pour entrainer, evaluer et sauvegarder les baselines
lineaires (TF-IDF + LogisticRegression / LinearSVC) sur le dataset LIAR binaire.
"""

import json
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from typing import Tuple, Dict, Union, Any

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import (
    accuracy_score, f1_score, precision_score, recall_score,
    classification_report, confusion_matrix
)


# ---------------------------------------------------------------------------
# Entrainement
# ---------------------------------------------------------------------------

def build_tfidf_pipeline(clf_name: str = "logreg") -> Pipeline:
    """Construit un pipeline TF-IDF + classifieur."""
    if clf_name == "logreg":
        clf = LogisticRegression(
            class_weight="balanced", max_iter=1000, random_state=42
        )
    elif clf_name == "svc":
        clf = LinearSVC(
            class_weight="balanced", max_iter=2000, random_state=42
        )
    else:
        raise ValueError(f"Classifieur inconnu: {clf_name}")

    return Pipeline([
        ("tfidf", TfidfVectorizer(sublinear_tf=True)),
        ("clf", clf),
    ])


def train_baseline_models(
    X_train: pd.Series,
    y_train: pd.Series,
    cv: int = 3,
) -> Tuple[Pipeline, Pipeline, Dict[str, Any]]:
    """
    Entraine LogisticRegression et LinearSVC via GridSearchCV
    (optimisation F1 pondere) et retourne les meilleurs modeles.
    """
    param_grid = {
        "tfidf__ngram_range": [(1, 1), (1, 2)],
        "tfidf__min_df": [2, 5],
        "tfidf__max_df": [0.9, 1.0],
        "clf__C": [0.1, 1.0, 10.0],
    }

    results = {}
    best_models = {}

    for name, clf_key in [("LogisticRegression", "logreg"), ("LinearSVC", "svc")]:
        pipe = build_tfidf_pipeline(clf_key)
        print(f"\n[{name}] GridSearchCV ({cv}-fold)...")
        grid = GridSearchCV(
            pipe, param_grid, cv=cv,
            scoring="f1_weighted", n_jobs=-1, verbose=1,
        )
        grid.fit(X_train, y_train)
        best_models[name] = grid.best_estimator_
        results[f"{name}_best_params"] = grid.best_params_
        results[f"{name}_best_score"] = grid.best_score_
        print(f"  Meilleurs params : {grid.best_params_}")
        print(f"  Meilleur F1 CV   : {grid.best_score_:.4f}")

    return best_models["LogisticRegression"], best_models["LinearSVC"], results


# ---------------------------------------------------------------------------
# Evaluation
# ---------------------------------------------------------------------------

def evaluate_model(
    model: Pipeline,
    X_train: pd.Series,
    y_train: pd.Series,
    X_test: pd.Series,
    y_test: pd.Series,
) -> Dict[str, Any]:
    """
    Evalue un modele sur train et test.
    Retourne accuracy, F1, precision, recall, gap de generalisation,
    classification report et matrice de confusion.
    """
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    acc_train = accuracy_score(y_train, y_train_pred)
    f1_train = f1_score(y_train, y_train_pred, average="weighted")
    acc_test = accuracy_score(y_test, y_test_pred)
    f1_test = f1_score(y_test, y_test_pred, average="weighted")

    metrics = {
        "train_accuracy": round(acc_train, 4),
        "train_f1_weighted": round(f1_train, 4),
        "test_accuracy": round(acc_test, 4),
        "test_f1_weighted": round(f1_test, 4),
        "test_precision_weighted": round(
            precision_score(y_test, y_test_pred, average="weighted"), 4
        ),
        "test_recall_weighted": round(
            recall_score(y_test, y_test_pred, average="weighted"), 4
        ),
        "generalization_gap_accuracy": round(acc_train - acc_test, 4),
        "classification_report_test": classification_report(
            y_test, y_test_pred, output_dict=True
        ),
        "confusion_matrix_test": confusion_matrix(y_test, y_test_pred).tolist(),
    }

    print(f"  Train  — Acc: {acc_train:.4f}  F1: {f1_train:.4f}")
    print(f"  Test   — Acc: {acc_test:.4f}  F1: {f1_test:.4f}")
    print(f"  Gap Acc: {acc_train - acc_test:.4f}")
    print(f"\n{classification_report(y_test, y_test_pred)}")

    return metrics


# ---------------------------------------------------------------------------
# Persistance
# ---------------------------------------------------------------------------

def save_model(model: Pipeline, path: Union[str, Path]) -> None:
    """Sauvegarde le modele (joblib)."""
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, out)
    print(f"  Modele sauvegarde -> {out}")


def load_model(path: Union[str, Path]) -> Pipeline:
    """Charge un modele sauvegarde."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Modele introuvable : {p}")
    return joblib.load(p)


# ---------------------------------------------------------------------------
# Script principal
# ---------------------------------------------------------------------------

def main():
    """Charge les donnees, entraine les baselines, evalue et sauvegarde."""
    DATA_DIR = Path("data/Traitees")
    MODELS_DIR = Path("models")

    train_path = DATA_DIR / "liar_train.parquet"
    test_path = DATA_DIR / "liar_test.parquet"

    if not train_path.exists() or not test_path.exists():
        print(f"Fichiers manquants: {train_path} ou {test_path}")
        print("Executez d'abord le notebook EDA pour generer les splits.")
        return

    print("=== Chargement des donnees ===")
    df_train = pd.read_parquet(train_path)
    df_test = pd.read_parquet(test_path)

    X_train, y_train = df_train["statement"], df_train["label_binary"]
    X_test, y_test = df_test["statement"], df_test["label_binary"]

    print("\n=== Entrainement des baselines ===")
    best_lr, best_svc, grid_metrics = train_baseline_models(X_train, y_train)

    print("\n=== Evaluation LogisticRegression ===")
    metrics_lr = evaluate_model(best_lr, X_train, y_train, X_test, y_test)

    print("\n=== Evaluation LinearSVC ===")
    metrics_svc = evaluate_model(best_svc, X_train, y_train, X_test, y_test)

    print("\n=== Sauvegarde ===")
    save_model(best_lr, MODELS_DIR / "liar_tfidf_logreg_binary.joblib")
    save_model(best_svc, MODELS_DIR / "liar_tfidf_linearsvc_binary.joblib")

    with open(MODELS_DIR / "baselines_metrics.json", "w", encoding="utf-8") as f:
        json.dump({
            "LogisticRegression": metrics_lr,
            "LinearSVC": metrics_svc,
            "GridSearch": grid_metrics,
        }, f, indent=2, default=str)

    print("\nTermine.")


if __name__ == "__main__":
    main()
