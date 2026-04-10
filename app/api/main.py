"""
API FastAPI pour la détection de fake news politiques.

Modèle final : **DistilBERT + XGBoost**
- Backbone DistilBERT fine-tuné (mean pooling embeddings)
- XGBoost sur embeddings (768d) + metadata (5d)

Modèles legacy disponibles : TF-IDF + LogReg / LinearSVC (pour comparaison)

Entraîné sur le dataset LIAR (binaire : Fake=0 / Real=1)
"""
from pathlib import Path
import json
import math
import numpy as np
import joblib
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# ── Chemins ──────────────────────────────────────────────────────────────────
BASE_DIR   = Path(__file__).resolve().parent.parent.parent
MODELS_DIR = Path(__file__).resolve().parent / "models"
if not MODELS_DIR.exists():
    MODELS_DIR = BASE_DIR / "models"

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"[startup] device = {DEVICE}")
print(f"[startup] models dir = {MODELS_DIR}")

# ── Chargement modèles legacy (TF-IDF) ───────────────────────────────────────
LEGACY_MODELS = {
    "logreg-tfidf":    joblib.load(MODELS_DIR / "liar_tfidf_smote_logreg_label_binary.joblib"),
    "linearsvc-tfidf": joblib.load(MODELS_DIR / "liar_tfidf_smote_linearsvc_label_binary.joblib"),
}
print(f"[startup] legacy modeles charges : {list(LEGACY_MODELS.keys())}")

# ── Chargement modèle final DistilBERT + XGBoost ────────────────────────────
DBXGB = None
try:
    xgb_model = joblib.load(MODELS_DIR / "distilbert_xgboost.joblib")
    with open(MODELS_DIR / "distilbert_xgboost_meta.json") as f:
        meta_bundle = json.load(f)
    tokenizer_db = AutoTokenizer.from_pretrained(str(MODELS_DIR / "distilbert_best"))
    model_db = AutoModelForSequenceClassification.from_pretrained(str(MODELS_DIR / "distilbert_best"))
    model_db.to(DEVICE)
    model_db.eval()
    DBXGB = {
        "xgb": xgb_model,
        "meta": meta_bundle,
        "tokenizer": tokenizer_db,
        "model": model_db,
    }
    print(f"[startup] DistilBERT + XGBoost charge (test_acc={meta_bundle['test_acc']:.4f})")
except Exception as e:
    print(f"[startup] DistilBERT + XGBoost non disponible : {e}")

# ── Application ───────────────────────────────────────────────────────────────
app = FastAPI(title="The Sentinel – Fake News API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)


# ── Schémas ───────────────────────────────────────────────────────────────────
class PredictRequest(BaseModel):
    texte:  str
    modele: str = "distilbert-xgboost"   # default = modele final


class Facteur(BaseModel):
    mot:   str
    poids: float


class PredictResponse(BaseModel):
    label:         str          # "Réel" | "Faux"
    proba_faux:    float
    proba_reel:    float
    confiance:     int
    facteurs_cles: list[Facteur]
    modele_utilise: str


# ── Helpers ───────────────────────────────────────────────────────────────────
def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def extract_embedding_dbxgb(texte: str) -> np.ndarray:
    """Mean-pooling embedding (1 x 768) depuis le backbone DistilBERT."""
    tokenizer = DBXGB["tokenizer"]
    model = DBXGB["model"]
    backbone = model.distilbert if hasattr(model, "distilbert") else model.base_model
    enc = tokenizer([texte], return_tensors="pt", truncation=True,
                    padding=True, max_length=256).to(DEVICE)
    with torch.no_grad():
        out = backbone(**enc)
        mask = enc["attention_mask"].unsqueeze(-1).float()
        mean = (out.last_hidden_state * mask).sum(dim=1) / mask.sum(dim=1)
    return mean.cpu().numpy()  # (1, 768)


def build_default_meta(texte: str) -> np.ndarray:
    """Metadata avec valeurs par defaut (speaker/party/credibility inconnus)."""
    gm = DBXGB["meta"]["global_mean"]
    return np.array([[
        0.5,                 # credibility_score (inconnu)
        gm,                  # speaker_cred (defaut moyenne globale)
        0.0,                 # log(speaker_count+1)
        gm,                  # party_cred
        len(texte.split()),  # n_words
    ]])


def predict_dbxgb(texte: str) -> tuple[float, float]:
    """Prediction (proba_faux, proba_reel) avec DistilBERT + XGBoost."""
    emb = extract_embedding_dbxgb(texte)
    meta = build_default_meta(texte)
    X = np.hstack([emb, meta])
    probas = DBXGB["xgb"].predict_proba(X)[0]
    return float(probas[0]), float(probas[1])


def extraire_facteurs_tfidf(pipeline, texte_clean: str) -> list[Facteur]:
    """Top tokens TF-IDF avec le plus fort impact (LogReg/LinearSVC)."""
    try:
        tfidf   = pipeline.named_steps["tfidf"]
        clf     = pipeline.named_steps["clf"]
        vec     = tfidf.transform([texte_clean])
        indices = vec.nonzero()[1]
        coefs   = clf.coef_[0]

        facteurs = []
        for idx in indices:
            tfidf_val = vec[0, idx]
            poids     = float(tfidf_val * coefs[idx])
            mot       = tfidf.get_feature_names_out()[idx]
            facteurs.append(Facteur(mot=mot, poids=round(poids, 4)))

        facteurs.sort(key=lambda f: abs(f.poids), reverse=True)
        return facteurs[:5]
    except Exception:
        return []


# ── Route principale ──────────────────────────────────────────────────────────
@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    if not req.texte.strip():
        raise HTTPException(status_code=422, detail="Le texte ne peut pas être vide.")

    texte_clean = req.texte.strip().lower()

    # === Modele final : DistilBERT + XGBoost ===
    if req.modele == "distilbert-xgboost":
        if DBXGB is None:
            raise HTTPException(status_code=503, detail="DistilBERT + XGBoost indisponible (modeles non charges).")
        proba_faux, proba_reel = predict_dbxgb(req.texte)
        label     = "Réel" if proba_reel >= 0.5 else "Faux"
        confiance = int(max(proba_faux, proba_reel) * 100)
        # Pas de facteurs cles "mots" pour ce modele (les features sont des embeddings 768d)
        return PredictResponse(
            label=label,
            proba_faux=round(proba_faux, 4),
            proba_reel=round(proba_reel, 4),
            confiance=confiance,
            facteurs_cles=[],
            modele_utilise="distilbert-xgboost",
        )

    # === Modeles legacy TF-IDF ===
    pipeline = LEGACY_MODELS.get(req.modele)
    if pipeline is None:
        raise HTTPException(
            status_code=404,
            detail=f"Modele '{req.modele}' introuvable. Disponibles : distilbert-xgboost, logreg-tfidf, linearsvc-tfidf",
        )

    if req.modele == "logreg-tfidf":
        probas     = pipeline.predict_proba([texte_clean])[0]
        proba_faux = float(probas[0])
        proba_reel = float(probas[1])
    else:
        score      = float(pipeline.decision_function([texte_clean])[0])
        proba_reel = sigmoid(score)
        proba_faux = 1.0 - proba_reel

    label     = "Réel" if proba_reel >= 0.5 else "Faux"
    confiance = int(max(proba_faux, proba_reel) * 100)
    facteurs  = extraire_facteurs_tfidf(pipeline, texte_clean)

    return PredictResponse(
        label=label,
        proba_faux=round(proba_faux, 4),
        proba_reel=round(proba_reel, 4),
        confiance=confiance,
        facteurs_cles=facteurs,
        modele_utilise=req.modele,
    )


@app.get("/health")
def health():
    available = list(LEGACY_MODELS.keys())
    if DBXGB is not None:
        available.insert(0, "distilbert-xgboost")
    return {
        "status": "ok",
        "device": DEVICE,
        "modele_par_defaut": "distilbert-xgboost",
        "modeles_disponibles": available,
    }
