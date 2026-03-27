import os
from pathlib import Path

# Chemins de base dynamiques
BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"
EMBEDDINGS_DIR = BASE_DIR / "data" / "embeddings"

# Dictionnaire des modèles disponibles
MODELS_CONFIG = {
    "TF-IDF + LogReg (SMOTE)": {
        "path": MODELS_DIR / "liar_tfidf_smote_logreg_label_binary.joblib",
        "type": "tfidf",
        "desc": "Baseline robuste utilisant TF-IDF et régression logistique avec rééquilibrage SMOTE."
    },
    "TF-IDF + LinearSVC (SMOTE)": {
        "path": MODELS_DIR / "liar_tfidf_smote_linearsvc_label_binary.joblib",
        "type": "tfidf",
        "desc": "Modèle performant utilisant des vecteurs de support (SVM) et SMOTE."
    },
    "GloVe + LogReg (300d)": {
        "path": MODELS_DIR / "liar_glove_logreg_label_binary.joblib",
        "type": "glove",
        "desc": "Modèle sémantique utilisant les embeddings Dolma (300 dimensions)."
    }
}

# Chemin par défaut
DEFAULT_MODEL = "TF-IDF + LogReg (SMOTE)"
GLOVE_PATH = EMBEDDINGS_DIR / "dolma_300_2024_1.2M.100_combined.txt"

# Méta-données de l'application
APP_NAME = "AI-based Fake News Detection System"
APP_DESC = "Cette application utilise l'IA (NLP) pour analyser les déclarations politiques et estimer la probabilité qu'elles soient authentiques (Real) ou trompeuses (Fake)."
