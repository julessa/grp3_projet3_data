import os
from pathlib import Path

# Chemins de base dynamiques (s'adaptent automatiquement à l'environnement)
BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "data" / "modeles"

# Le modèle TF-IDF + LogReg entraîné dans le notebook Modeles_de_Base.ipynb
MODEL_PATH = MODELS_DIR / "baseline_logreg.joblib"

# Méta-données de l'application
APP_NAME = "AI-based Fake News Detection System"
APP_DESC = "Cette application utilise l'IA (Traitement du Langage Naturel) pour analyser les déclarations politiques et estimer la probabilité qu'elles soient authentiques (Real) ou trompeuses (Fake)."
