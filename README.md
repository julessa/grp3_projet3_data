# The Sentinel — Détection de Fake News Politiques

![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat-square&logo=python&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-16.2-black?style=flat-square&logo=next.js)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.8-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-2.10-EE4C2C?style=flat-square&logo=pytorch&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-v4-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white)
![Dataset](https://img.shields.io/badge/Dataset-LIAR_12791-6366F1?style=flat-square)
![License](https://img.shields.io/badge/License-Academic-lightgrey?style=flat-square)

Système de détection automatique de fausses déclarations politiques par apprentissage automatique. Le projet couvre l'intégralité du pipeline de data science — de l'analyse exploratoire au déploiement en production — sur le dataset **LIAR** (12 791 déclarations vérifiées par PolitiFact).

---

## Membres du groupe

| Membre | Périmètre principal |
|--------|---------------------|
| **Franck** | Modèles de base, modèles avancés, API FastAPI, application web Next.js |
| **Jules** | EDA, prétraitement des données, FakeNewsNet |
| **Valentine** | EDA FakeNewsNet, analyse hors-domaine |
| **Djouhra** | EDA LIAR, interprétabilité, analyse des biais |

---

## Table des matières

1. [Architecture du projet](#architecture-du-projet)
2. [Dataset](#dataset)
3. [Pipeline ML](#pipeline-ml)
4. [Modèles](#modèles)
5. [Applications](#applications)
6. [Installation](#installation)
7. [Lancement](#lancement)
8. [Structure des fichiers](#structure-des-fichiers)
9. [Résultats](#résultats)

---

## Architecture du projet

```
grp3_projet3_data/
├── Franck/                         # Périmètre principal ML + apps
│   ├── notebook/                   # Notebooks Jupyter (pipeline complet)
│   ├── models/                     # Modèles entraînés (.joblib, checkpoints)
│   ├── app/
│   │   ├── api/                    # Backend FastAPI (inférence)
│   │   ├── reactjs/                # Frontend Next.js "The Sentinel"
│   │   └── streamlit/              # Prototype Streamlit
│   ├── src/                        # Modules Python réutilisables
│   └── data/                       # Données brutes et traitées
├── jules/                          # EDA, prétraitement, FakeNewsNet
├── valentine/                      # EDA FakeNewsNet, évaluation hors-domaine
├── Djouhra/                        # EDA LIAR, interprétabilité, biais
└── pyproject.toml                  # Dépendances partagées (uv)
```

Le projet suit un pipeline en cinq étapes :

```
LIAR Dataset  →  EDA & Prétraitement  →  Feature Extraction  →  Entraînement  →  Déploiement
   (TSV)            (Parquet)            TF-IDF / GloVe /          Sklearn /        FastAPI +
                                         Transformers             HuggingFace       Next.js
```

---

## Dataset

**LIAR** — Wang, 2017. Déclarations politiques issues de PolitiFact, annotées sur 6 niveaux de véracité, remappés en classification binaire dans ce projet.

| Split | Taille |
|-------|--------|
| Train | 10 240 |
| Validation | 1 284 |
| Test | 1 267 |
| **Total** | **12 791** |

**Label binaire :**

| Classe | Labels LIAR originaux |
|--------|-----------------------|
| **Réel (1)** | `true`, `mostly-true`, `half-true` |
| **Faux (0)** | `mostly-false`, `barely-true`, `pants-on-fire`, `false` |

**Caractéristiques textuelles :** déclarations courtes (médiane 17 mots), forte variation (2–467 mots), classes légèrement déséquilibrées (ratio 0.39 dans la version 6-classes).

**Biais documenté :** les déclarations républicaines représentent 44.3 % du corpus avec un taux de faux de 31.1 %, contre 19.8 % pour les démocrates. Ces statistiques reflètent les biais du corpus PolitiFact et doivent être interprétées avec précaution.

---

## Pipeline ML

### 1. EDA — `EDA_LIAR.ipynb`

Analyse exploratoire complète : distribution des labels, longueur des textes, POS tags, distribution par parti/orateur/état, détection des déséquilibres de classes.

### 2. Prétraitement

Nettoyage minimal aligné avec les travaux de référence sur LIAR :
- Normalisation casse (lowercase)
- Suppression URLs, chiffres, ponctuation
- Création du label binaire (`label_binary`)
- Export Parquet (`data/traitees/`)

### 3. Modèles de base — `Modeles_de_Base.ipynb`

Branche lexicale (TF-IDF) et sémantique (GloVe 300d) avec optimisation par GridSearchCV (F1 pondéré, 3-fold CV) et rééquilibrage SMOTE.

### 4. Modèles avancés — `Modeles_Avances.ipynb`

Fine-tuning de modèles Transformers (DistilBERT, RoBERTa) sur LIAR. Exploration des hyperparamètres (learning rate, batch size, scheduler).

### 5. Évaluation hors-domaine — `Evaluation_Hors_Domaine.ipynb`

Test de généralisation sur FakeNewsNet (BuzzFeed). Analyse de la robustesse des modèles hors du domaine PolitiFact.

### 6. Interprétabilité & Biais — `Interpretabilite_Biais.ipynb`

Analyse LIME/SHAP des facteurs clés de prédiction. Audit des biais par parti, orateur et contexte géographique.

---

## Modèles

### Modèles déployés (classification binaire)

| Modèle | Fichier | Accuracy (test) | F1 pondéré | Gap train–test |
|--------|---------|:--------------:|:----------:|:--------------:|
| TF-IDF + SMOTE + LogReg | `liar_tfidf_smote_logreg_label_binary.joblib` | 63.2 % | 63.2 % | 21.2 % |
| TF-IDF + SMOTE + LinearSVC | `liar_tfidf_smote_linearsvc_label_binary.joblib` | 63.1 % | 63.2 % | 20.0 % |

Paramètres optimaux (GridSearch) : `ngram_range=(1,2)`, `min_df=2`, `max_df=0.9`, `C=1.0` (LogReg) / `C=0.1` (SVC).

### Modèles entraînés (non déployés)

| Modèle | Répertoire | Notes |
|--------|-----------|-------|
| GloVe 300d + LogReg | `liar_glove_logreg_label_binary.joblib` | Nécessite le fichier d'embeddings Dolma 300d (non inclus) |
| DistilBERT fine-tuné | `models/distilbert_A/` | Checkpoints 640–3200 steps |
| RoBERTa fine-tuné | `models/tuning/roberta_lr1e-05_sampler/` | lr=1e-5, weighted sampler |

**Interprétabilité réelle :** les modèles TF-IDF déployés exposent les poids des tokens (`tfidf_value × coeff_modèle`) comme facteurs d'influence, sans approximation post-hoc.

---

## Applications

### The Sentinel — Application web (Next.js + FastAPI)

Interface de production pour l'analyse de déclarations politiques en temps réel.

**Stack technique :**
- Frontend : Next.js 16.2 (App Router, Turbopack), Tailwind CSS v4, React Context API
- Backend : FastAPI + uvicorn, scikit-learn, joblib
- Communication : Next.js API route (`/api/predict`) proxie vers FastAPI (`localhost:8000`)

**Fonctionnalités :**
- Analyse d'une déclaration avec affichage du verdict (Réel/Faux), confiance, probabilités
- Facteurs clés d'influence (poids TF-IDF réels)
- Historique des analyses (localStorage, 50 entrées max)
- Sélection du modèle (Paramètres)
- Pages Statistiques et Analyse des biais avec données réelles du corpus LIAR

### Prototype Streamlit

Application de démonstration rapide (`app/streamlit/`). Même logique d'inférence, interface Streamlit.

---

## Installation

### Prérequis

- Python 3.13+
- Node.js 20+
- [uv](https://docs.astral.sh/uv/) (gestionnaire de paquets Python)

### Environnement Python

```bash
# Depuis la racine du projet ou depuis Franck/
uv sync
```

Les dépendances clés incluent : `scikit-learn`, `imbalanced-learn`, `joblib`, `torch`, `transformers`, `fastapi`, `uvicorn`, `pandas`, `numpy`, `lime`, `shap`.

### Dépendances Node.js

```bash
cd Franck/app/reactjs
npm install
```

---

## Lancement

Deux processus doivent tourner simultanément.

### Terminal 1 — API Python

```bash
cd Franck
.\.venv\Scripts\python.exe -m uvicorn app.api.main:app --port 8000
```

Le serveur charge les deux modèles `.joblib` au démarrage et expose :
- `POST /predict` — inférence (corps JSON : `{ "texte": "...", "modele": "logreg-tfidf" }`)
- `GET /health` — statut et liste des modèles disponibles

### Terminal 2 — Application web

```bash
cd Franck/app/reactjs
npm run dev
```

Accessible sur [http://localhost:3000](http://localhost:3000).

### Notebooks

```bash
cd Franck
uv run jupyter lab
```

Ordre d'exécution recommandé :
1. `EDA_LIAR.ipynb`
2. `Modeles_de_Base.ipynb`
3. `Modeles_Avances.ipynb`
4. `Evaluation_Hors_Domaine.ipynb`
5. `Interpretabilite_Biais.ipynb`

---

## Structure des fichiers

```
Franck/
├── notebook/
│   ├── EDA_LIAR.ipynb                      # Analyse exploratoire du dataset LIAR
│   ├── Modeles_de_Base.ipynb               # TF-IDF + GloVe + baselines linéaires
│   ├── Modeles_Avances.ipynb               # Fine-tuning DistilBERT / RoBERTa
│   ├── Evaluation_Hors_Domaine.ipynb       # Généralisation sur FakeNewsNet
│   └── Interpretabilite_Biais.ipynb        # LIME, SHAP, analyse des biais
│
├── models/
│   ├── liar_tfidf_smote_logreg_label_binary.joblib
│   ├── liar_tfidf_smote_linearsvc_label_binary.joblib
│   ├── liar_glove_logreg_label_binary.joblib
│   ├── liar_glove_smote_logreg_label_binary.joblib
│   ├── baselines_gap_metrics.json          # Métriques détaillées des baselines
│   ├── distilbert_A/                       # Checkpoints DistilBERT (640–3200 steps)
│   └── tuning/roberta_lr1e-05_sampler/     # Checkpoint RoBERTa
│
├── app/
│   ├── api/
│   │   └── main.py                         # API FastAPI (inférence + facteurs clés)
│   ├── reactjs/
│   │   └── src/
│   │       ├── app/                        # Pages Next.js (App Router)
│   │       │   ├── page.tsx                # Tableau de bord principal
│   │       │   ├── historique/             # Historique des analyses
│   │       │   ├── statistiques/           # Métriques des modèles
│   │       │   ├── biais/                  # Analyse des biais du corpus
│   │       │   ├── parametres/             # Sélection du modèle
│   │       │   └── api/predict/route.ts    # Proxy Next.js → FastAPI
│   │       ├── components/                 # Composants React
│   │       ├── context/AnalysisContext.tsx # État global (React Context)
│   │       └── lib/                        # Types, config modèles
│   └── streamlit/                          # Prototype Streamlit
│
├── src/
│   └── base_model.py                       # Utilitaires d'entraînement réutilisables
│
└── data/
    ├── brutes/liar_dataset/                # Fichiers TSV originaux LIAR
    └── traitees/                           # Splits Parquet nettoyés
```

---

## Résultats

### Performances sur le test set LIAR (classification binaire)

| Modèle | Accuracy | F1 pondéré | F1 classe Réel | F1 classe Faux |
|--------|:--------:|:----------:|:--------------:|:--------------:|
| TF-IDF + SMOTE + LogReg | 63.2 % | 63.2 % | 67.4 % | 57.9 % |
| TF-IDF + SMOTE + LinearSVC | 63.1 % | 63.2 % | 67.2 % | 58.0 % |
| GloVe 300d + LogReg | 59.9 % | 60.0 % | 63.6 % | 55.4 % |

Le gap train–test (~20 %) est cohérent avec la littérature sur LIAR (textes courts, bruit élevé, fort déséquilibre contextuel). Les modèles GloVe présentent un gap quasi nul (~3 %), indiquant de meilleures représentations pour la généralisation hors-domaine.

### Référence bibliographique

Wang, W. Y. (2017). *"Liar, Liar Pants on Fire": A New Benchmark Dataset for Fake News Detection*. ACL 2017.

---

*Projet académique — Master Data & BI, 2025–2026.*
