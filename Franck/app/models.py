import joblib
from pathlib import Path
from typing import Tuple
from config import MODEL_PATH
from preprocessing import preprocess_text

class FakeNewsModel:
    def __init__(self, model_path: Path = MODEL_PATH):
        self.model_path = model_path
        self.pipeline = None

    def load(self):
        """Charge le pipeline depuis le disque."""
        if not self.model_path.exists():
            raise FileNotFoundError(f"⚠️ Modèle introuvable ({self.model_path}). Veuillez l'entraîner.")
        self.pipeline = joblib.load(self.model_path)


def predict_news(text: str, model_instance: FakeNewsModel) -> Tuple[str, float, float]:
    """
    Inférence : Prédit si le texte est Fake ou Real.
    Retourne : (label: str, proba_fake: float, proba_real: float)
    """
    if model_instance.pipeline is None:
        model_instance.load()
        
    # Appeler le prétraitement NLP
    cleaned_text = preprocess_text(text)
    
    # Prédiction des probabilités via la pipeline scikit-learn
    # Mapping binaire classique du modèle (0 = Fake, 1 = Real)
    probas = model_instance.pipeline.predict_proba([cleaned_text])[0]
    
    proba_fake = float(probas[0])
    proba_real = float(probas[1])
    
    # Règle d'attribution
    label = "Real News" if proba_real > 0.5 else "Fake News"
    
    return label, proba_fake, proba_real
