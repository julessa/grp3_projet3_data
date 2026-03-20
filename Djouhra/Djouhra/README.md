# 🕵️ Projet 3 — Détection automatique de Fake News politiques
**Module Data Business Intelligence — Epitech Digital School**

---

## 📁 Structure du projet

```
GRP3_PROJET3_DATA/
│
├── notebook/
│   ├── EDA_LIAR.ipynb                ← Exploration des données
│   ├── Modeles_de_Base.ipynb         ← TF-IDF + LR / SVC / XGBoost
│   ├── Modeles_Avances.ipynb         ← Sentence-BERT embeddings
│   ├── Evaluation_Hors_Domaine.ipynb ← Domain shift BuzzFeed
│   └── Interpretabilite_Biais.ipynb  ← LIME + analyse des biais
│
├── data/
│   ├── brutes/          ← Fichiers TSV originaux (train/valid/test)
│   ├── fusionnes/       ← liar_unifie.csv (tous splits fusionnés)
│   ├── modeles/         ← Modèles .joblib + métriques .json
│   └── traitees/        ← Fichiers .parquet prétraités
│
├── Doc/                 ← Tous les graphiques générés (.png, .html)
├── src/                 ← Code utilitaire (si besoin)
├── main.py              ← Lance tous les notebooks dans l'ordre
├── pyproject.toml       ← Dépendances du projet
├── .python-version      ← Version Python cible (3.11)
└── README.md
```

---

## 🚀 Démarrage rapide

### 1. Installation
```bash
pip install pandas numpy matplotlib seaborn scikit-learn nltk wordcloud lime xgboost sentence-transformers jupyter nbconvert joblib pyarrow
```

### 2. Lancer les notebooks dans VS Code / PyCharm / Jupyter
Ouvre chaque notebook dans l'ordre et exécute toutes les cellules :

| Ordre | Notebook | Durée |
|-------|----------|-------|
| 1 | `EDA_LIAR.ipynb` | ~2 min |
| 2 | `Modeles_de_Base.ipynb` | ~5 min |
| 3 | `Modeles_Avances.ipynb` | **~10 min** (SBERT) |
| 4 | `Evaluation_Hors_Domaine.ipynb` | ~3 min |
| 5 | `Interpretabilite_Biais.ipynb` | ~5 min |

### 3. Ou lancer tout d'un coup
```bash
python main.py
```

---

## 📊 Fichiers générés dans `Doc/`

| Fichier | Contenu |
|---------|---------|
| `EDA_01_distribution_labels.png` | Distribution des 6 labels |
| `EDA_02_distribution_binaire.png` | Distribution binaire |
| `EDA_03_top_speakers.png` | Top 15 speakers |
| `EDA_04_labels_by_party.png` | Labels par parti |
| `EDA_05_text_length.png` | Longueur des déclarations |
| `BASE_01_confusion_matrices.png` | Matrices de confusion baselines |
| `BASE_02_models_comparison.png` | Comparaison TF-IDF |
| `BASE_03_top_features.png` | Features discriminants |
| `ADV_01_sbert_comparison.png` | TF-IDF vs SBERT |
| `OOD_01_domain_shift.png` | Analyse domain shift |
| `OOD_02_liar_vs_buzzfeed.png` | Comparaison datasets |
| `BIAS_01_top_features.png` | Features globaux |
| `BIAS_02_party_bias.png` | Biais partisans |
| `BIAS_03_speaker_bias.png` | Biais par speaker |
| `BIAS_04_error_analysis.png` | Analyse des erreurs |
| `LIME_*.html` | Explications interactives LIME |

---

## 📚 Références
- Wang, W. Y. (2017). "Liar, Liar Pants on Fire". *ACL 2017*.
- Reimers & Gurevych (2019). Sentence-BERT. *EMNLP 2019*.
- BuzzFeed News (2016). Facebook Fact-Check Dataset.
