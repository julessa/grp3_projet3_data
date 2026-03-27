import joblib
import numpy as np
import re
import streamlit as st
from pathlib import Path
from typing import Tuple, Dict
from config import MODELS_CONFIG, GLOVE_PATH
from preprocessing import preprocess_text

# Regex pour tokenisation GloVe
TOKEN_PATTERN = re.compile(r"\w+")

@st.cache_resource
def load_glove_embeddings(path: Path, emb_dim: int = 300) -> Dict[str, np.ndarray]:
    """Charge les vecteurs GloVe en cache."""
    if not path.exists():
        return {}
    
    embeddings_index = {}
    with open(path, "r", encoding="utf8") as f:
        for line in f:
            values = line.rstrip().split(" ")
            word = values[0]
            coefs = np.asarray(values[1:], dtype="float32")
            if coefs.shape[0] == emb_dim:
                embeddings_index[word] = coefs
    return embeddings_index

class FakeNewsModel:
    def __init__(self, model_key: str):
        self.config = MODELS_CONFIG.get(model_key)
        self.model_path = self.config["path"]
        self.type = self.config["type"]
        self.pipeline = None
        self.glove_index = None

    def load(self):
        """Charge le modèle et les dépendances nécessaires."""
        if not self.model_path.exists():
            raise FileNotFoundError(f"⚠️ Modèle introuvable ({self.model_path.name}). Veuillez l'entraîner dans le notebook.")
        
        self.pipeline = joblib.load(self.model_path)
        
        if self.type == "glove":
            self.glove_index = load_glove_embeddings(GLOVE_PATH, 300)
            if not self.glove_index:
                st.warning("⚠️ Fichier GloVe introuvable. Les prédictions sémantiques seront basées sur des vecteurs nuls.")

    def _text_to_glove(self, text: str) -> np.ndarray:
        """Convertit un texte en vecteur moyen GloVe."""
        tokens = TOKEN_PATTERN.findall(text.lower())
        if not tokens or not self.glove_index:
            return np.zeros(300, dtype="float32")
        
        vecs = [self.glove_index[t] for t in tokens if t in self.glove_index]
        if not vecs:
            return np.zeros(300, dtype="float32")
        return np.mean(vecs, axis=0).reshape(1, -1)

    def predict(self, text: str) -> Tuple[str, float, float]:
        """Inférence selon le type de modèle."""
        cleaned_text = preprocess_text(text)
        
        if self.type == "tfidf":
            # Pipeline complet (TF-IDF + CLF)
            probas = self.pipeline.predict_proba([cleaned_text])[0]
        else:
            # GloVe : Vectorisation manuelle puis Classifier
            vec = self._text_to_glove(cleaned_text)
            probas = self.pipeline.predict_proba(vec)[0]
        
        proba_fake = float(probas[0])
        proba_real = float(probas[1])
        label = "Real News" if proba_real > 0.5 else "Fake News"
        
        return label, proba_fake, proba_real

def predict_news(text: str, model_instance: FakeNewsModel) -> Tuple[str, float, float]:
    """Interface de prédiction pour app.py."""
    return model_instance.predict(text)
