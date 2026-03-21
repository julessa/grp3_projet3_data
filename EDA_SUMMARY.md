# Analyse Exploratoire - Dataset Fake News LIAR

## 📊 Vue d'Ensemble

**Dataset LIAR** (Liar, Liar Pants on Fire) - Détection de Fake News Politiques

### Structure des Données
- **Total**: 12,791 déclarations politiques
- **TRAIN**: 10,240 (80.1%)
- **TEST**: 1,267 (9.9%)
- **VALID**: 1,284 (10.0%)

---

## 🏷️ Labels (Classification Multi-classe)

| Label | Nombre | Pourcentage | Description |
|-------|--------|-------------|-------------|
| half-true | 2,627 | 20.5% | Partiellement vrai |
| false | 2,507 | 19.6% | Faux |
| mostly-true | 2,454 | 19.2% | Principalement vrai |
| barely-true | 2,103 | 16.4% | À peine vrai |
| true | 2,053 | 16.1% | Vrai |
| pants-fire | 1,047 | 8.2% | Complètement faux |

### ⚠️ Équilibre des Classes
- **Ratio Min/Max**: 0.39 (DÉSÉQUILIBRÉ)
- Classe majoritaire: `half-true` (20.5%)
- Classe minoritaire: `pants-fire` (8.2%)

**Action**: Utiliser weighted cross-entropy ou techniques de résampling

---

## 📝 Caractéristiques Textuelles

### Longueur des Déclarations
- **Moyenne**: 18.0 mots
- **Médiane**: 17.0 mots
- **Min**: 2 mots
- **Max**: 467 mots
- **Écart-type**: 9.7 mots

**Observation**: Textes courts et concis, variation importante

### Longueur par Label
```
half-true:    18.96 mots (±11.42)
mostly-true:  18.50 mots (±11.90)
barely-true:  18.15 mots (±7.79)
true:         18.03 mots (±9.83)
false:        16.87 mots (±9.60)
pants-fire:   17.24 mots (±7.48)
```

---

## 🏷️ Features POS (Part-of-Speech)

### Top 15 POS Tags
1. **NN** (Noun): 16.10% - Noms
2. **IN** (Preposition): 12.78% - Prépositions
3. **NNP** (Proper Noun): 12.50% - Noms propres
4. **DT** (Determiner): 8.75% - Déterminants
5. **NNS** (Plural Noun): 7.06% - Noms pluriels
6. **JJ** (Adjective): 5.76% - Adjectifs
7. **CD** (Cardinal Digit): 5.22% - Nombres
8. **VBZ** (Verb, 3rd person singular): 3.87%
9. **VBD** (Verb, past tense): 3.53%
10. **RB** (Adverb): 2.98%

**Observation**: Domination des noms et prépositions (structure grammaticale)

---

## 🗳️ Analyse Politique

### Distribution par Parti

#### DÉMOCRATES (4,137 déclarations - 32.3%)
- Taux de mensonges: **19.8%** (false + pants-fire)
- Taux de vérité: **43.6%** (true + mostly-true)
- **Plus honnêtes** selon le dataset

#### RÉPUBLICAINS (5,665 déclarations - 44.3%)
- Taux de mensonges: **31.1%** ⚠️ **SIGNIFICATIVEMENT PLUS HAUT**
- Taux de vérité: **30.2%**
- Plus représentés dans le dataset

### ⚠️ Biais Potentiel
- Les républicains ont un taux de mensonges 1.57x plus élevé
- Surreprésentation des républicains (44.3% vs 32.3%)
- À considérer lors de l'évaluation du modèle

---

## 👥 Top Orateurs

### Top 10 par Activité
1. Hillary Clinton
2. Barack Obama
3. Marco Rubio
4. Rick Scott
5. John McCain
6. Mitt Romney
7. Rick Perry
8. Scott Walker
9. Donald Trump
10. Chain-email

### Taux de Mensonges des Top 10
- Range: 10% à 87%
- Variation importante selon l'orateur

---

## 📍 Distribution Géographique

### Top 10 États
| État | Nombre | Pourcentage |
|------|--------|-------------|
| Texas | 1,241 | 9.7% |
| Florida | 806 | 6.3% |
| New York | 776 | 6.1% |
| Wisconsin | 757 | 5.9% |
| Illinois | 657 | 5.1% |
| Ohio | 579 | 4.5% |
| Georgia | 571 | 4.5% |
| Virginia | 505 | 3.9% |
| Rhode Island | 466 | 3.6% |
| Oregon | 442 | 3.5% |

---

## 🎯 Insights Clés

### ✅ Points Positifs
1. **Dataset complet**: 12,791 examples suffisants pour ML
2. **Bien structuré**: 14 colonnes avec métadonnées riches
3. **Features pré-calculées**: POS tags disponibles
4. **Distribution train/test/valid appropriée**: 80/10/10
5. **Métadonnées exploitables**: speaker, party, state, context

### ⚠️ Points d'Attention
1. **Classes déséquilibrées**: Ratio 0.39 (mineur/majeur)
2. **Biais politique**: Républicains surreprésents avec + mensonges
3. **Textes courts**: Moyenne 18 mots (moins de contexte)
4. **Variation importante**: Longueur 2-467 mots
5. **Data leakage potentiel**: Plusieurs déclarations du même speaker

---

## 🔬 Recommandations pour la Modélisation

### 1. Choix du Modèle
- **Multiclasse (6 labels)**: BERT, RoBERTa, DistilBERT
- **Binaire (True/False)**: Peut donner meilleurs résultats

### 2. Gestion du Déséquilibre
- ✓ Class weights dans loss function
- ✓ Stratified train/test split
- ✓ Oversampling/Undersampling
- ✓ SMOTE ou techniques synthétiques

### 3. Features à Utiliser
- Texte principal (TF-IDF ou embeddings)
- POS tag ratios
- Métadonnées: party, speaker, state, context
- Historique de vérité du speaker

### 4. Hyperparamètres
```
Learning rate: 2e-5 à 5e-5
Batch size: 16-32
Epochs: 3-5
Dropout: 0.1-0.3
Warmup steps: 10%
```

### 5. Métriques d'Évaluation
- **Macro F1-score** (important pour déséquilibre)
- Precision/Recall par classe
- Confusion matrix
- ROC-AUC
- Per-class accuracy

### 6. Validation
- Stratified K-Fold
- Cross-validation par speaker (avoid data leakage)
- Hold-out test set stratifié

### 7. Analyse d'Erreurs
- Vérifier confusion entre labels proches
- Analyse de fairness par parti
- Pattern d'erreurs par speaker

---

## 📊 Fichiers Disponibles

### Dans le dataset LIAR
- `train.tsv`: 10,240 déclarations d'entraînement
- `test.tsv`: 1,267 déclarations de test
- `valid.tsv`: 1,284 déclarations de validation
- `train_pos.csv`: Features POS pour TRAIN
- `test_pos.csv`: Features POS pour TEST
- `valid_pos.csv`: Features POS pour VALID

### Fichiers Créés
- `Eda_Val-1.ipynb`: Notebook d'analyse exploratoire complète
- `EDA_SUMMARY.md`: Ce fichier (résumé)

---

## 🚀 Prochaines Étapes

1. ✅ EDA complétée
2. ⏳ Prétraitement et nettoyage des données
3. ⏳ Feature engineering
4. ⏳ Entraînement des modèles
5. ⏳ Évaluation et comparaison
6. ⏳ Fine-tuning et optimisation
7. ⏳ Analyse de fairness et biais
8. ⏳ Déploiement et inférence

---

**Dernière mise à jour**: 20 Mars 2026
**Status**: ✅ Analyse Exploratoire Complétée
