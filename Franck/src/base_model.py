"""
module base_model.py

Fournit les utilitaires pour entraîner, évaluer et sauvegarder les baselines 
linéaires (TF-IDF + LogisticRegression / LinearSVC) sur le dataset LIAR binaire.
"""

import pandas as pd
import joblib
from pathlib import Path
from typing import Tuple, Dict, Union, Any

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix

def train_baseline_models(
    X_train: pd.Series, 
    y_train: pd.Series
) -> Tuple[Pipeline, Pipeline, Dict[str, Any]]:
    """
    Entraîne les pipelines LogisticRegression et LinearSVC via GridSearchCV
    avec optimisation du F1 pondéré, et retourne les meilleurs modèles.
    """
    # Espace de recherche raisonnable
    param_grid = {
        'tfidf__ngram_range': [(1, 1), (1, 2)],
        'tfidf__min_df': [2, 5],
        'tfidf__max_df': [0.9, 1.0],
        'clf__C': [0.1, 1.0, 10.0]
    }
    
    # 1. Pipeline LogisticRegression
    pipe_lr = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42))
    ])
    
    print("\n[LogisticRegression] Lancement du GridSearchCV (3-fold CV)...")
    grid_lr = GridSearchCV(
        pipe_lr, param_grid, cv=3, scoring='f1_weighted', n_jobs=-1, verbose=1
    )
    grid_lr.fit(X_train, y_train)
    best_lr = grid_lr.best_estimator_
    print(f"Meilleurs paramètres LR : {grid_lr.best_params_}")
    
    # 2. Pipeline LinearSVC
    pipe_svc = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', LinearSVC(class_weight='balanced', max_iter=2000, random_state=42))
    ])
    
    print("\n[LinearSVC] Lancement du GridSearchCV (3-fold CV)...")
    grid_svc = GridSearchCV(
        pipe_svc, param_grid, cv=3, scoring='f1_weighted', n_jobs=-1, verbose=1
    )
    grid_svc.fit(X_train, y_train)
    best_svc = grid_svc.best_estimator_
    print(f"Meilleurs paramètres SVC : {grid_svc.best_params_}")
    
    metrics = {
        'LogisticRegression_best_params': grid_lr.best_params_,
        'LinearSVC_best_params': grid_svc.best_params_
    }
    
    return best_lr, best_svc, metrics

def evaluate_model(
    model: Pipeline, 
    X_train: pd.Series, 
    y_train: pd.Series, 
    X_test: pd.Series, 
    y_test: pd.Series
) -> Dict[str, Any]:
    """
    Évalue le modèle sur l'ensemble d'entraînement et de test.
    Calcule l'Accuracy, le F1-Score pondéré (train et test), l'écart de généralisation (gap),
    et retourne un rapport global de classification.
    """
    # Prédictions
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    
    # Métriques Train
    acc_train = accuracy_score(y_train, y_train_pred)
    f1_train = f1_score(y_train, y_train_pred, average='weighted')
    
    # Métriques Test
    acc_test = accuracy_score(y_test, y_test_pred)
    f1_test = f1_score(y_test, y_test_pred, average='weighted')
    
    # Generalization gap (Δ Accuracy)
    gap_acc = acc_train - acc_test
    
    metrics = {
        "train_accuracy": acc_train,
        "train_f1_weighted": f1_train,
        "test_accuracy": acc_test,
        "test_f1_weighted": f1_test,
        "generalization_gap_accuracy": gap_acc,
        "classification_report_test": classification_report(y_test, y_test_pred, output_dict=True),
        "confusion_matrix_test": confusion_matrix(y_test, y_test_pred).tolist()
    }
    
    print(f"--- Résultats d'Évaluation ---")
    print(f"Train Acc: {acc_train:.4f} | Train F1 (Weigh): {f1_train:.4f}")
    print(f"Test Acc:  {acc_test:.4f} | Test F1 (Weigh):  {f1_test:.4f}")
    print(f"Generalization Gap (Delta Acc): {gap_acc:.4f}")
    print(f"\nClassification Report (Test):\n{classification_report(y_test, y_test_pred)}")
    
    return metrics

def save_model(model: Pipeline, path: Union[str, Path]) -> None:
    """Sauvegarde le modèle sérialisé sur le disque (joblib)."""
    out_path = Path(path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, out_path)
    print(f"Modèle sauvegardé -> {out_path}")

def load_model(path: Union[str, Path]) -> Pipeline:
    """Charge et retourne un modèle sérialisé par joblib."""
    in_path = Path(path)
    if not in_path.exists():
        raise FileNotFoundError(f"Modèle introuvable au chemin : {in_path}")
    return joblib.load(in_path)

def main():
    """
    Script d'exécution principal : charge les données, exécute l'entraînement, 
    l'évaluation, et sauvegarde les modèles finaux de Baseline.
    """
    import json
    
    # Optionnel: on utilise le dossier de root (cwd courant)
    DATA_DIR = Path("data")
    TRAITEES_DIR = DATA_DIR / "traitees"
    MODELS_DIR = Path("models")
    
    train_path = TRAITEES_DIR / "liar_train.parquet"
    test_path = TRAITEES_DIR / "liar_test.parquet"
    
    if not train_path.exists() or not test_path.exists():
        print(f"Attention: {train_path} ou {test_path} introuvable.")
        print("Assurez-vous que l'exploration de données (EDA) a bien généré les splits.")
        return
        
    print(f"=== Chargement des données d'entraînement et de test ===")
    df_train = pd.read_parquet(train_path)
    df_test = pd.read_parquet(test_path)
    
    X_train, y_train = df_train["statement"], df_train["label_binary"]
    X_test, y_test = df_test["statement"], df_test["label_binary"]
    
    print("\n=== Entraînement des baselines (Validation Croisée) ===")
    best_lr, best_svc, grid_metrics = train_baseline_models(X_train, y_train)
    
    print("\n=== Évaluation du modèle LogisticRegression ===")
    metrics_lr = evaluate_model(best_lr, X_train, y_train, X_test, y_test)
    
    print("\n=== Évaluation du modèle LinearSVC ===")
    metrics_svc = evaluate_model(best_svc, X_train, y_train, X_test, y_test)
    
    print("\n=== Sauvegarde des modèles finaux ===")
    save_model(best_lr, MODELS_DIR / "liar_tfidf_logreg_label_binary.joblib")
    save_model(best_svc, MODELS_DIR / "liar_tfidf_linearsvc_label_binary.joblib")
    
    # Historique métriques optionnel
    with open(MODELS_DIR / "baselines_gap_metrics.json", "w", encoding="utf-8") as f:
        json.dump({
            "LogisticRegression": metrics_lr, 
            "LinearSVC": metrics_svc,
            "GridSearch": grid_metrics
        }, f, indent=4)
        
    print("\n✅ Opération terminée avec succès.")

if __name__ == "__main__":
    main()
