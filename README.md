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
**Franck** **Jules** **Valentine** **Djouhra** **Laura** 
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


### Référence bibliographique

Wang, W. Y. (2017). *"Liar, Liar Pants on Fire": A New Benchmark Dataset for Fake News Detection*. ACL 2017.

---

*Projet académique — Master Data & BI, 2025–2026.*
