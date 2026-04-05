"""
API FastAPI pour la détection de fake news politiques.
Modèles disponibles : TF-IDF + SMOTE + LogisticRegression / LinearSVC
Entraînés sur le dataset LIAR (binaire : Fake=0 / Real=1)
"""
from pathlib import Path
import math
import numpy as np
import joblib
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ── Chemins ──────────────────────────────────────────────────────────────────
BASE_DIR   = Path(__file__).resolve().parent.parent.parent
MODELS_DIR = BASE_DIR / "models"

# ── Chargement des modèles au démarrage ───────────────────────────────────────
MODELS = {
    "logreg-tfidf":    joblib.load(MODELS_DIR / "liar_tfidf_smote_logreg_label_binary.joblib"),
    "linearsvc-tfidf": joblib.load(MODELS_DIR / "liar_tfidf_smote_linearsvc_label_binary.joblib"),
}

# ── Application ───────────────────────────────────────────────────────────────
app = FastAPI(title="The Sentinel – Fake News API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)


# ── Schémas ───────────────────────────────────────────────────────────────────
class PredictRequest(BaseModel):
    texte:    str
    modele:   str = "logreg-tfidf"


class Facteur(BaseModel):
    mot:   str
    poids: float


class PredictResponse(BaseModel):
    label:        str          # "Réel" | "Faux"
    proba_faux:   float
    proba_reel:   float
    confiance:    int
    facteurs_cles: list[Facteur]


# ── Prétraitement (identique à celui du notebook d'entraînement) ──────────────
def preprocess(text: str) -> str:
    return text.strip().lower()


# ── Sigmoid (pour LinearSVC) ─────────────────────────────────────────────────
def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


# ── Extraction des facteurs clés depuis le pipeline TF-IDF ───────────────────
def extraire_facteurs(pipeline, texte_clean: str, modele_id: str) -> list[Facteur]:
    """
    Retourne les 5 tokens TF-IDF avec le plus fort impact absolu sur la prédiction.
    - LogReg   : poids = tfidf_val × coef_lr  (+ = vers Réel, - = vers Faux)
    - LinearSVC: poids = tfidf_val × coef_svc
    """
    try:
        tfidf   = pipeline.named_steps["tfidf"]
        clf     = pipeline.named_steps["clf"]
        vec     = tfidf.transform([texte_clean])   # sparse matrix 1×V
        indices = vec.nonzero()[1]                 # indices des tokens présents

        if modele_id == "logreg-tfidf":
            coefs = clf.coef_[0]   # shape (V,) — positif = classe 1 (Réel)
        else:
            coefs = clf.coef_[0]   # LinearSVC : même structure

        facteurs = []
        for idx in indices:
            tfidf_val = vec[0, idx]
            poids     = float(tfidf_val * coefs[idx])
            mot       = tfidf.get_feature_names_out()[idx]
            facteurs.append(Facteur(mot=mot, poids=round(poids, 4)))

        # Trier par importance absolue, garder top 5
        facteurs.sort(key=lambda f: abs(f.poids), reverse=True)
        return facteurs[:5]
    except Exception:
        return []


# ── Route principale ──────────────────────────────────────────────────────────
@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    if not req.texte.strip():
        raise HTTPException(status_code=422, detail="Le texte ne peut pas être vide.")

    pipeline = MODELS.get(req.modele)
    if pipeline is None:
        raise HTTPException(status_code=404, detail=f"Modèle '{req.modele}' introuvable.")

    texte_clean = preprocess(req.texte)

    # Probabilités
    if req.modele == "logreg-tfidf":
        probas     = pipeline.predict_proba([texte_clean])[0]
        proba_faux = float(probas[0])   # classe 0 = Fake
        proba_reel = float(probas[1])   # classe 1 = Real
    else:
        # LinearSVC → decision_function + sigmoid
        score      = float(pipeline.decision_function([texte_clean])[0])
        proba_reel = sigmoid(score)
        proba_faux = 1.0 - proba_reel

    label     = "Réel" if proba_reel >= 0.5 else "Faux"
    confiance = int(max(proba_faux, proba_reel) * 100)

    facteurs = extraire_facteurs(pipeline, texte_clean, req.modele)

    return PredictResponse(
        label=label,
        proba_faux=round(proba_faux, 4),
        proba_reel=round(proba_reel, 4),
        confiance=confiance,
        facteurs_cles=facteurs,
    )


@app.get("/health")
def health():
    return {"status": "ok", "modeles": list(MODELS.keys())}
