"""
Exemple de pipeline complet : Entraînement et Sauvegarde d'un modèle NLP
-------------------------------------------------------------------------
Ce script illustre la logique "Backend" du workflow ML pour le Fake News.
(Il reproduit la logique conceptuelle de Modeles_de_Base.ipynb).
"""

import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib

def main():
    print("1. Collecte et Chargement des données...")
    # Remplacez ce chemin par votre vrai dataset (ex: liar_unifie.csv)
    # df = pd.read_csv("../data/fusionnes/liar_unifie.csv")
    
    # Dataset fictif (mock) pour illustration locale
    data = {
        "statement": [
            "La terre est clairement plate et les images satellites sont fausses.", 
            "L'eau bout à environ 100 degrés Celsius.", 
            "Les extraterrestres contrôlent les esprits via les ondes radio.", 
            "La population de la France dépasse les 60 millions d'habitants."
        ],
        "label_binary": [0, 1, 0, 1]  # 0 = Fake, 1 = Real
    }
    df = pd.DataFrame(data)
    
    X = df["statement"]
    y = df["label_binary"]
    
    # Séparation Stratifiée Train/Test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    
    print("2. Création de la pipeline (Prétraitement TF-IDF + Classifier)...")
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(min_df=1, max_df=1.0)), 
        ('clf', LogisticRegression(class_weight='balanced', max_iter=1000))
    ])
    
    print("3. Entraînement en cours...")
    pipeline.fit(X_train, y_train)
    
    print("4. Évaluation des performances...")
    acc = pipeline.score(X_test, y_test)
    print(f"Accuracy de base : {acc * 100:.2f} %")
    
    print("5. Sérialisation du pipeline pour l'interface Streamlit...")
    target_dir = Path("../data/modeles")
    target_dir.mkdir(parents=True, exist_ok=True)
    
    model_path = target_dir / "baseline_logreg.joblib"
    joblib.dump(pipeline, model_path)
    print(f"✅ Terminé ! Le modèle est disponible sous : {model_path}")

if __name__ == "__main__":
    main()
