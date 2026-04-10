"""
Vercel Serverless — API de detection de fake news (FastAPI).
"""
from pathlib import Path
import math
import joblib
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

API_DIR = Path(__file__).resolve().parent
MODELS = {
    "logreg-tfidf": joblib.load(API_DIR / "liar_tfidf_smote_logreg_label_binary.joblib"),
    "linearsvc-tfidf": joblib.load(API_DIR / "liar_tfidf_smote_linearsvc_label_binary.joblib"),
}

app = FastAPI(title="The Sentinel API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class PredictRequest(BaseModel):
    texte: str
    modele: str = "logreg-tfidf"


class Facteur(BaseModel):
    mot: str
    poids: float


class PredictResponse(BaseModel):
    label: str
    proba_faux: float
    proba_reel: float
    confiance: int
    facteurs_cles: list[Facteur]


def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def extraire_facteurs(pipeline, texte_clean, modele_id):
    try:
        tfidf = pipeline.named_steps["tfidf"]
        clf = pipeline.named_steps["clf"]
        vec = tfidf.transform([texte_clean])
        indices = vec.nonzero()[1]
        coefs = clf.coef_[0]
        facteurs = []
        for idx in indices:
            tfidf_val = vec[0, idx]
            poids = float(tfidf_val * coefs[idx])
            mot = tfidf.get_feature_names_out()[idx]
            facteurs.append(Facteur(mot=mot, poids=round(poids, 4)))
        facteurs.sort(key=lambda f: abs(f.poids), reverse=True)
        return facteurs[:5]
    except Exception:
        return []


@app.post("/predict", response_model=PredictResponse)
@app.post("/api/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    if not req.texte.strip():
        raise HTTPException(422, "Le texte ne peut pas etre vide.")
    pipeline = MODELS.get(req.modele)
    if pipeline is None:
        raise HTTPException(404, f"Modele '{req.modele}' introuvable.")

    texte_clean = req.texte.strip().lower()

    if req.modele == "logreg-tfidf":
        probas = pipeline.predict_proba([texte_clean])[0]
        proba_faux, proba_reel = float(probas[0]), float(probas[1])
    else:
        score = float(pipeline.decision_function([texte_clean])[0])
        proba_reel = sigmoid(score)
        proba_faux = 1.0 - proba_reel

    label = "Réel" if proba_reel >= 0.5 else "Faux"
    confiance = int(max(proba_faux, proba_reel) * 100)
    facteurs = extraire_facteurs(pipeline, texte_clean, req.modele)

    return PredictResponse(
        label=label,
        proba_faux=round(proba_faux, 4),
        proba_reel=round(proba_reel, 4),
        confiance=confiance,
        facteurs_cles=facteurs,
    )


@app.get("/")
@app.get("/predict")
@app.get("/api/predict")
def health():
    return {"status": "ok", "modeles": list(MODELS.keys())}
