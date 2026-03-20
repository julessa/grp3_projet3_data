# Détection Automatique de Fake News Politiques

Ce projet vise à entraîner un modèle de classification de déclarations politiques basé sur le [LIAR Dataset](https://huggingface.co/datasets/liar), et à évaluer sa robustesse et sa capacité de généralisation sur un second jeu de données externe (BuzzFeed - facebook-fact-check) pour observer le phénomène de *domain shift*.

L'environnement et la gestion des dépendances sont assurés par `uv`. Tous les graphiques sont générés via `plotly`.

## Structure du Projet

- `data/` : Dossier contenant les données.
  - `brutes/` : Contient les jeux de données originaux téléchargés (LIAR, FakeNewsNet, BuzzFeed).
  - `fusionnes/` : Contient le jeu de données LIAR unifié (`liar_unifie.csv`, 12 791 lignes).
  - `traitees/` : Contient le jeu de données traitées
- `notebook/` :
  - **`EDA_LIAR.ipynb`** : Exploration de données (distribution, longueur, partis) sur le jeu de données unifié.
  - **`Modeles_de_Base.ipynb`** : Modèles de base TF-IDF avec Régression Logistique et LinearSVC.
  - **`Modeles_Avances.ipynb`** : Fine-Tuning de `distilbert-base-uncased` ou `roberta-base` pour la classification riche en contexte.
  - **`Evaluation_Hors_Domaine.ipynb`** : Évaluation sur un dataset externe (BuzzFeed/facebook-fact-check) et analyse de la baisse de performance (*domain shift*).
  - **`Interpretabilite_Biais.ipynb`** : Interprétabilité locale (LIME) et globale, ainsi qu'une analyse des biais par affiliation.
- `src/` : Scripts python auxiliaires.
- `pyproject.toml` : Dépendances gérées par uv.

   ```
