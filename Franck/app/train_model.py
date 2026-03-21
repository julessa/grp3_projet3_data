"""
Script d'entraînement du modèle Fake News.
Implémente le workflow demandé : load_data, preprocess, split, train_model, save_model.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib

from preprocessing import preprocess_text

def load_data(path: str) -> pd.DataFrame:
    """Charge les données étiquetées."""
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        print(f"Dataset {path} introuvable. Création d'un dataset factice LIAR-like pour la démo.")
        return pd.DataFrame({
            "statement": [
                "The earth is completely flat.", 
                "Water boils at 100 degrees Celsius.", 
                "Politicians are hiding alien contact.", 
                "France is a country in Europe."
            ],
            "label_binary": [0, 1, 0, 1]
        })

def preprocess(texts: pd.Series) -> pd.Series:
    """Applique le NLP (NLTK Tokenize, lemmatize, etc) sur la série pandas."""
    print("Application du NLP (cela peut prendre du temps sur de gros datasets)...")
    return texts.apply(preprocess_text)

def train_model(X_train: pd.Series, y_train: pd.Series) -> Pipeline:
    """Crée le pipeline vectorisation (TF-IDF) + Modèle scikit-learn."""
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=5000)),
        ('clf', LogisticRegression(class_weight='balanced'))
    ])
    pipeline.fit(X_train, y_train)
    return pipeline

def save_model(model: Pipeline, path: str):
    """Sérialise le pipeline complet en fichier .joblib."""
    joblib.dump(model, path)
    print(f"Modèle sauvegardé : {path}")

def main():
    # 1. Collecte / Chargement
    df = load_data("../data/fusionnes/liar_unifie.csv")
    
    # 2. Prétraitement du texte
    # Note : Sur un vrai workflow, on applique preprocess(df["statement"]). 
    # Le TF-IDF peut parfois s'en charger si configuré, mais ici on respecte la consigne strict NLTK.
    X_clean = preprocess(df["statement"])
    y = df["label_binary"]
    
    # 3. Split train/validation/test
    # (Par simplicité, on fait un 80/20 train/test classique)
    X_train, X_test, y_train, y_test = train_test_split(X_clean, y, test_size=0.2, random_state=42)
    
    # 4. Entraînement
    model = train_model(X_train, y_train)
    
    # 5. Évaluation des métriques
    y_pred = model.predict(X_test)
    print("=== Métriques d'Évaluation ===")
    print(f"Accuracy  : {accuracy_score(y_test, y_pred):.3f}")
    print(f"Precision : {precision_score(y_test, y_pred):.3f}")
    print(f"Recall    : {recall_score(y_test, y_pred):.3f}")
    print(f"F1-Score  : {f1_score(y_test, y_pred):.3f}")
    
    # 6. Sauvegarde
    save_model(model, "../data/modeles/baseline_logreg.joblib")

if __name__ == "__main__":
    main()
