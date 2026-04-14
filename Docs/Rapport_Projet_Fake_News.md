# Détection automatique de fake news politiques et généralisation

**Projet de Spécialisation 3 — Rapport écrit**

**Groupe 3** : Franck Fambou, Valentine Martin, Laura Galindo, Djouhra Ould-Younes, Jules Saccomano

**Liens utiles** :
- GitHub : *Projet de spécialisation 3*
- Notion : *Gestion de projet*
- Canva : *Présentation*

---

## 1. Introduction

### 1.1 Contexte et enjeux de la détection de fake news

La diffusion de fausses informations dans le débat politique constitue désormais un enjeu structurel pour la qualité du débat démocratique, la confiance dans les médias et les institutions, et plus largement pour la capacité des citoyens à se forger une opinion éclairée. Une déclaration trompeuse peut atteindre des millions de personnes en quelques heures via les réseaux sociaux, ce qui rend la vérification manuelle à grande échelle illusoire.

C'est précisément dans ce contexte que le traitement automatique du langage (NLP) et l'apprentissage profond apportent une valeur réelle : ils permettent d'automatiser au moins une partie du travail de détection. Des jeux de données annotés comme **LIAR**, qui contient plusieurs milliers de déclarations politiques vérifiées manuellement, rendent possible l'entraînement de modèles supervisés capables de distinguer — imparfaitement, mais utilement — les énoncés véridiques des énoncés trompeurs.

### 1.2 Objectifs du projet

L'objectif central de ce projet est de concevoir une approche **robuste** de détection de fake news politiques à partir de texte brut. Par robuste, nous entendons un modèle qui ne se contente pas de bien performer sur son corpus d'entraînement, mais qui conserve une utilité lorsqu'il est confronté à des données issues d'autres sources. Pour cela, nous nous appuyons sur **LIAR** en entraînement et en évaluation in-domain, tandis que les corpus externes **ISOT Fake News** (~44k articles) et **WELFake** (~72k articles) servent exclusivement à mesurer la capacité de généralisation et le *domain shift*.

Trois ambitions structurent notre démarche. La première consiste à construire un **pipeline NLP complet**, depuis le nettoyage du texte jusqu'au déploiement applicatif. La deuxième est de **comparer rigoureusement plusieurs familles de modèles** — baselines lexicales (TF-IDF, GloVe), gradient boosting, transformers contextuels (DistilBERT, RoBERTa) — afin de mesurer l'apport réel de chaque approche. La troisième, enfin, est d'**analyser les biais et limites** du modèle retenu (par parti politique, locuteur et sujet), car un classifieur statistiquement performant mais éthiquement problématique ne peut être déployé en l'état.

### 1.3 Méthodologie et travail de groupe

L'organisation du travail s'est appuyée sur un **tableau Kanban Notion** pour la répartition et le suivi des tâches (EDA, modélisation, évaluation hors-domaine, rapport, slides), et sur un **dépôt GitHub** centralisant l'ensemble du code. Les notebooks Jupyter sont gérés via `uv` pour assurer la reproductibilité de l'environnement Python d'un poste à l'autre. Des points de synchronisation réguliers permettaient d'éviter les redondances et de coordonner les responsabilités, chaque membre ayant un domaine principal d'intervention (NLP et modèles, EDA, interprétabilité, rédaction, présentation).

---

## 2. Jeux de données et environnement technique

### 2.1 Dataset LIAR

LIAR regroupe environ **12 800 déclarations politiques** vérifiées individuellement par PolitiFact. Chaque déclaration est annotée sur 6 niveaux de véracité (de `pants-fire` à `true`) et accompagnée d'un ensemble de métadonnées particulièrement riches : locuteur, parti, sujet, État, contexte médiatique, et même un historique des déclarations passées de chaque locuteur. C'est précisément cette richesse qui fait l'intérêt de LIAR — nous disposons de bien plus que du texte brut.

Pour faciliter la phase d'EDA, nous avons fusionné les splits d'origine dans un fichier unifié `liar_unifie.csv`, tout en conservant la colonne `split` afin de respecter strictement la séparation canonique au moment de l'entraînement. Ce point est essentiel pour éviter toute fuite de données entre train et test.

Plusieurs difficultés caractérisent ce dataset. D'abord, les déclarations sont **très courtes** (médiane autour de 17 tokens), ce qui pénalise les représentations qui s'appuient sur la longueur du contexte. Ensuite, certains locuteurs et partis sont sur-représentés, ce qui crée un risque de mémorisation stylistique. Enfin, il faut trancher sur un *framing* — 6 classes, 3 classes ou binaire — qui reste cohérent avec les datasets externes utilisés en évaluation OOD.

### 2.2 Datasets ISOT Fake News et WELFake

Pour mesurer la capacité de généralisation, nous avons retenu deux corpus externes volontairement très différents de LIAR :

| Dataset | Taille | Type de contenu |
|---|---|---|
| **ISOT Fake News** | ~34k articles nettoyés | Articles politiques (Reuters vs sites de fake news) |
| **WELFake** | ~64k articles nettoyés | Mix hétérogène de sources d'actualités |

La comparaison avec LIAR fait immédiatement ressortir trois différences majeures : les **textes sont nettement plus longs** (articles complets plutôt que déclarations isolées), le **style est journalistique** plutôt que des citations directes de politiciens, et le **vocabulaire couvre une plus large variété** de sujets, de pays, d'époques et de médias. C'est exactement ce contraste qui rend ces corpus pertinents pour mesurer la robustesse de nos modèles.

### 2.3 Environnement technique

L'environnement repose sur des outils standards bien intégrés. Tout tourne en Python ≥ 3.10, et la gestion des dépendances passe par `uv` via un `pyproject.toml`, ce qui permet à chaque membre du groupe de réinstaller l'environnement en une seule commande. Les notebooks Jupyter sont organisés dans `notebooks/` : `EDA_*.ipynb` pour l'exploration, `Modeles_de_Base.ipynb` pour les baselines, `Modeles_Avances.ipynb` pour les transformers, `Evaluation_Hors_Domaine.ipynb` pour les tests cross-dataset, et `Interpretabilite_Biais.ipynb` pour les analyses LIME, SHAP et fairness.

Côté bibliothèques, nous utilisons **scikit-learn** pour les modèles classiques (TF-IDF, LogReg, LinearSVC, pipelines), **PyTorch et HuggingFace Transformers** pour DistilBERT et RoBERTa, **XGBoost** pour le modèle final hybride, et **Plotly** pour les visualisations interactives — ces dernières offrant une lecture bien plus parlante que des figures statiques. Le versioning des datasets et modèles volumineux passe par **GitHub LFS**, sans lequel le dépôt serait inutilisable. Enfin, pour la démonstration, nous avons déployé une application **Next.js + FastAPI** sur Vercel, qui permet de tester le modèle en direct sur de nouvelles déclarations.

---

## 3. Analyse exploratoire et pré-traitement

### 3.1 Pré-traitement

Nous avons opté pour un nettoyage **volontairement léger** plutôt qu'un pipeline lourd. Concrètement, nous supprimons les lignes sans `statement`, nous normalisons le texte (espaces, encodage), et surtout nous remplaçons les métadonnées manquantes par `unknown` au lieu de filtrer les lignes correspondantes. Ce dernier choix est important : un filtrage strict sur les NaN de `jobtitle` aurait fait perdre près de 30 % du dataset, alors qu'il suffit que ces colonnes restent utilisables pour les analyses de fairness ultérieures. Nous ajoutons également deux features simples (`n_chars` et `n_tokens`) qui servent à la caractérisation du corpus et à certaines visualisations.

Le pré-traitement plus spécifique dépend ensuite du type de modèle. Pour les baselines TF-IDF, nous passons en lowercase et supprimons la ponctuation. Pour les transformers, en revanche, nous conservons la casse et laissons le tokenizer officiel opérer — DistilBERT et RoBERTa disposent chacun de leur propre tokenizer (WordPiece, BPE) optimisé pour leurs représentations, et il est préférable de ne pas interférer avec ce traitement.

### 3.2 Distribution des classes dans LIAR

LIAR comporte six labels d'origine, mais pour assurer une cohérence avec ISOT et WELFake, nous devons basculer en classification binaire. Nous reprenons la **formulation binaire** de Hasan et al. (2025), qui regroupe les labels selon le schéma suivant :

- `0 = FAKE` : `pants-fire`, `false`, `barely-true`
- `1 = REAL` : `half-true`, `mostly-true`, `true`

Sur les 12 791 déclarations unifiées, cette binarisation produit **5 657 FAKE (44,2 %)** et **7 134 REAL (55,8 %)**. Le déséquilibre est réel mais reste modéré (ratio 0,79), ce qui justifie le recours à des techniques légères — `class_weight='balanced'` ou SMOTE — plutôt qu'à des approches plus invasives. L'inclusion de `barely-true` dans la classe FAKE a fait débat au sein du groupe : en théorie, une déclaration "à peine vraie" n'est pas un mensonge au sens strict. Cependant, l'examen des annotations PolitiFact montre que ces déclarations contiennent quasi systématiquement des omissions ou distorsions significatives. Le choix retenu est donc à la fois pragmatique et sémantiquement défendable.

### 3.3 Métadonnées et biais potentiels

L'exploration des métadonnées révèle plusieurs déséquilibres structurels qu'il est essentiel de connaître avant toute phase de modélisation.

**Parti politique.** La répartition compte environ 5 000 Républicains, 4 000 Démocrates et 2 000 locuteurs sans étiquette de parti. Le point critique se situe au niveau du taux de FAKE : **49,8 % chez les Républicains** contre **33,9 % chez les Démocrates**, soit un écart de près de 16 points. Cette disparité peut refléter une réalité factuelle de la période couverte par PolitiFact, mais elle constitue surtout un biais potentiel pour le modèle, qui peut apprendre à associer le parti républicain à une probabilité élevée de FAKE indépendamment du contenu textuel.

**Locuteurs.** Sur 3 309 locuteurs uniques pour 12 791 déclarations, la distribution est fortement concentrée. Les 15 locuteurs les plus fréquents (Obama, Trump, Clinton, etc.) représentent une part disproportionnée du corpus, ce qui crée un risque réel de mémorisation stylistique : le modèle pourrait apprendre à reconnaître un locuteur particulier plutôt que des patterns généralisables de désinformation.

**Sujets.** Le corpus couvre 144 sujets distincts, dominés par `health-care`, `taxes`, `education` et `immigration`. Les tables de contingence sujet × label montrent que la véracité varie fortement selon le sujet, ce qui crée des interactions complexes contenu × label difficiles à démêler pour des modèles purement lexicaux.

### 3.4 Comparaison LIAR vs ISOT/WELFake

L'EDA des datasets externes confirme un *domain shift* important. Trois différences structurelles ressortent particulièrement.

La première concerne **la longueur des textes**. LIAR présente une médiane d'environ 17 tokens par déclaration, alors qu'ISOT et WELFake dépassent largement les 200 tokens. Cette différence n'est pas anecdotique : les représentations par mean pooling (GloVe, Word2Vec) calculent un vecteur phrase comme la moyenne des vecteurs de tokens, et plus le texte est long, plus le signal pertinent est dilué par les tokens non-discriminants.

La deuxième concerne **le style**. Les articles ISOT/WELFake utilisent des phrases complexes, des attributions indirectes (« according to », « sources say »), et un vocabulaire de médias alternatifs ou de réseaux sociaux (Breitbart, InfoWars) qui n'apparaît presque jamais dans les déclarations LIAR.

La troisième concerne **la distribution des classes**. ISOT est quasi équilibré (50/50), tandis que WELFake penche vers FAKE (~55 %). Le seuil de décision optimal appris sur LIAR n'est donc pas directement transférable : un modèle calibré pour LIAR peut se retrouver à sur-prédire FAKE ou REAL selon le dataset cible.

---

## 4. Modélisation

### 4.1 Cadre expérimental

Nous avons respecté strictement les splits **train/validation/test** d'origine de LIAR. Le tuning des hyperparamètres est réalisé sur train + validation, et le test LIAR est réservé exclusivement au reporting final in-domain : toute fuite à ce niveau invaliderait les comparaisons. Les datasets ISOT et WELFake, quant à eux, ne servent **jamais** à l'entraînement et sont utilisés uniquement pour l'évaluation hors-domaine. Cette séparation est volontaire : nous voulons mesurer comment un modèle entraîné sur LIAR se comporte face à du texte qu'il n'a jamais vu.

Notre démarche a été **itérative et comparative**. Plutôt que de viser directement une architecture sophistiquée, nous avons testé une dizaine de combinaisons (représentation × classifieur), en conservant à chaque étape ce qui apportait de la valeur et en remettant en question ce qui décevait. Les sous-sections qui suivent décrivent **l'ensemble des modèles évalués**, y compris ceux qui ont été écartés — car expliquer pourquoi une approche ne fonctionne pas est souvent aussi instructif que de justifier celle qui marche.

### 4.2 Baselines lexicales et sémantiques

**Représentations testées** :

| Représentation | Description | Dimension |
|---|---|---|
| **TF-IDF** | Unigrammes + bigrammes, `min_df`/`max_df` contrôlés, GridSearchCV sur `ngram_range` et `C` | ~5 000 |
| **Word2Vec corpus** | Entraîné sur LIAR (`vector_size=100`, `window=5`, `min_count=2`), mean pooling | 100 |
| **GloVe pré-entraîné** | Wikipedia/Gigaword 100d via `gensim`, mean pooling phrase | 100 |
| **GloVe + Party** | GloVe + one-hot encoding du parti politique en concaténation | 102 |

**Classifieurs testés** sur ces features :

| Classifieur | Particularité |
|---|---|
| **Logistic Regression** | Régularisation L2, `class_weight='balanced'`, GridSearchCV sur `C` |
| **LinearSVC** | Régularisation L2, sigmoid pour probabilités, `class_weight='balanced'` |
| **LogReg + SMOTE** | Pipeline `imblearn` avec sur-échantillonnage de la classe minoritaire |
| **LinearSVC + SMOTE** | Idem avec LinearSVC |

Cela donne **7 baselines** au total dont les résultats sont reportés en section 5.1. Toutes utilisent la même séparation train/valid/test de LIAR.

### 4.3 Approches avancées : Transformers et hybrides

Une fois les baselines en place, nous sommes passés à des architectures plus ambitieuses. **Cinq approches avancées** ont été testées, et toutes n'ont pas été retenues.

#### 4.3.1 DistilBERT fine-tuné

DistilBERT (Sanh et al., 2019) est une version compressée de BERT — 6 couches au lieu de 12, 66 millions de paramètres, 60 % plus rapide à l'inférence. C'est typiquement le modèle de choix lorsqu'on souhaite bénéficier d'un transformer sans payer le coût complet de BERT-base. Nous avons tenté un fine-tuning via le `Trainer` HuggingFace, avec `max_length=128`, `learning_rate=5e-5`, batch size 32, label smoothing 0.1, scheduler cosine et early stopping. Le problème principal a été le **coût d'exécution sur CPU : plus de 9 heures pour 3 époques**, pour un gain marginal par rapport à l'extraction d'embeddings sans fine-tuning (de l'ordre de 1 à 2 points d'accuracy). Le ratio coût/bénéfice n'était pas favorable dans notre contexte.

#### 4.3.2 RoBERTa fine-tuné

La situation est similaire avec RoBERTa (Liu et al., 2019), version améliorée de BERT entraînée plus longtemps sur davantage de données. Nous avons testé `roberta-base` (125M paramètres) avec les mêmes hyperparamètres que DistilBERT, en abaissant simplement le `learning_rate` à 3e-5. Le coût CPU s'est révélé encore plus élevé (~20 heures pour 3 époques), ce qui nous a contraints à abandonner cette piste comme modèle final. L'architecture reste pertinente sur GPU, mais elle ne pouvait pas être validée dans notre contexte d'exécution.

#### 4.3.3 TF-IDF + XGBoost (texte enrichi)

Nous avons également cherché à pousser les baselines à leur maximum, sans recourir aux transformers. L'idée consistait à utiliser TF-IDF sur un texte enrichi (`statement_nlp` + `subject` + `context`), à y adjoindre des features metadata (`credibility_score`, encodage cible du speaker, `n_words`), puis à entraîner un XGBoost (`n_estimators=1000, max_depth=3, learning_rate=0.03`). Cette approche atteint **0,6906 d'accuracy** et **0,6883 de F1w**, ce qui constitue une nette amélioration par rapport aux baselines linéaires (~+5 points) et place TF-IDF + XGBoost à égalité avec DistilBERT + XGBoost en in-domain. Néanmoins, elle reste plafonnée par la nature lexicale de TF-IDF et — surtout — généralise mal en OOD à cause de sa dépendance au vocabulaire LIAR. Pour cette seconde raison, elle a été écartée au profit de l'approche transformer.

#### 4.3.4 Stacking : DistilBERT + RoBERTa + XGBoost

Il s'agit de notre approche la plus ambitieuse, et également de la plus décevante. L'idée était séduisante : combiner dans un XGBoost les **probabilités prédites** par DistilBERT et RoBERTa (4 features), les **embeddings mean-pooled** des deux modèles (768 + 768 = 1 536 features) et les metadata (7 features), pour un total de 1 547 features. XGBoost devait alors apprendre dans quels cas faire confiance à chaque transformer. En pratique, le gain par rapport au simple DistilBERT + XGBoost s'est révélé **inexistant**, alors que le coût de calcul doublait. Le ratio était défavorable, et nous avons abandonné cette approche.

#### 4.3.5 DistilBERT pré-entraîné + XGBoost (modèle final)

C'est finalement l'approche la plus sobre qui s'est imposée comme la plus efficace. Elle est détaillée dans la section suivante.

### 4.4 Choix du modèle final : DistilBERT + XGBoost

À l'issue de cette phase comparative, nous retenons **DistilBERT pré-entraîné + XGBoost** comme architecture de référence. Le pipeline est volontairement épuré :

1. **Extraction d'embeddings** : nous utilisons `distilbert-base-uncased` (sans fine-tuning), en ne conservant que le backbone, et en appliquant un **mean pooling** sur la dernière couche cachée. Cela produit un vecteur de 768 dimensions par déclaration.
2. **Construction des features** : ces 768 dimensions sont concaténées à 5 features metadata (`credibility_score`, `speaker_cred` par target encoding, `log(1+speaker_count)`, `party_cred`, `n_words`), pour un total de **773 features**.
3. **Classifieur** : XGBoost avec `n_estimators=500, max_depth=4, learning_rate=0.05`, et `scale_pos_weight` calculé automatiquement pour traiter le léger déséquilibre des classes.

Quatre raisons principales motivent ce choix par rapport aux autres alternatives testées.

**Du statistique au sémantique.** TF-IDF se limite à compter les mots ; un terme absent du dataset d'entraînement rend le modèle aveugle. DistilBERT, pré-entraîné sur des milliards de phrases, comprend les synonymes, les négations et les structures syntaxiques complexes. Cette capacité est précisément ce qui manque aux baselines lexicales.

**Préparation au domain shift.** Comme nous l'avons documenté, les modèles TF-IDF s'effondrent dès qu'on les sort de LIAR. Les embeddings contextuels de DistilBERT capturent des patterns plus universels — pas miraculeux, mais nettement plus robustes. Dans un projet dont l'objectif central est la généralisation hors-domaine, ce critère n'est pas négociable.

**Conserver le meilleur des deux mondes.** Nous aurions pu utiliser une simple couche linéaire en sortie de DistilBERT, mais XGBoost apporte une réelle valeur ajoutée. Il gère efficacement la non-linéarité dans les 768 dimensions d'embeddings et permet de combiner naturellement le texte (embeddings) avec des features structurées (metadata du speaker, du parti, etc.). Un classifieur linéaire serait nettement moins performant sur cette combinaison hétérogène.

**Praticité d'exécution.** Toutes les variantes fine-tunées nécessitent entre 9 et 20 heures de calcul sur notre infrastructure CPU, contre une dizaine de minutes pour l'extraction d'embeddings. La perte de performance reste minime (quelques points au plus, comme nous l'avons quantifié en reproduisant un notebook de référence externe — cf. annexe D). Le ratio coût/bénéfice penche très clairement en faveur de l'approche sans fine-tuning.

Le tableau ci-dessous résume les modèles écartés et les raisons correspondantes :

| Modèle écarté | Raison principale |
|---|---|
| Baselines TF-IDF / GloVe + LogReg-SVC | Plafonnent à ~0,64 F1w, effondrement en OOD, pas d'embeddings réutilisables |
| DistilBERT fine-tuné | Coût CPU >9h pour un gain marginal |
| RoBERTa fine-tuné | Coût CPU >20h, redondant avec DistilBERT |
| TF-IDF + XGBoost | Score in-domain équivalent (0,6906) mais reste lexical, mauvaise généralisation OOD |
| Stacking DistilBERT + RoBERTa + XGBoost | Complexité doublée sans gain, difficile à interpréter et à déployer |

### 4.5 Gestion du déséquilibre et choix des métriques

Le déséquilibre 44/56 entre les classes restant modéré, nous n'avons pas eu besoin de techniques d'augmentation lourdes. XGBoost utilise un `scale_pos_weight` calculé automatiquement, et les baselines sont testées avec et sans SMOTE. Côté métriques, nous rapportons systématiquement **Accuracy** et **F1 weighted**, jamais le F1 binaire seul. La raison est importante : le F1 binaire ne mesure que la classe positive et peut induire en erreur sur un dataset déséquilibré — un modèle qui prédirait systématiquement « Real » obtiendrait déjà un F1 binaire honorable sans rien apprendre du contenu. Ce piège est documenté en détail dans l'annexe D, où nous reproduisons un score apparent de 0,710 qui se révèle être un F1 binaire et non un F1 weighted.

---

## 5. Résultats et évaluation

### 5.1 Résultats in-domain sur LIAR

Le tableau ci-dessous regroupe **les 12 modèles évalués** (7 baselines + 5 approches avancées) et leurs métriques mesurées sur le test set LIAR. Le modèle final retenu est en gras.

| # | Catégorie | Modèle | Accuracy | F1 (weighted) | Statut |
|---|---|---|---|---|---|
| 1 | Baseline | TF-IDF + LogReg | 0,6006 | 0,6022 | écarté |
| 2 | Baseline | TF-IDF + LinearSVC | 0,6401 | 0,6407 | écarté (sur-apprentissage) |
| 3 | Baseline | TF-IDF + SMOTE + LogReg | 0,6148 | 0,6163 | écarté |
| 4 | Baseline | TF-IDF + SMOTE + LinearSVC | 0,6275 | 0,6285 | écarté |
| 5 | Baseline | Word2Vec corpus + LogReg | 0,5943 | 0,5960 | écarté |
| 6 | Baseline | GloVe + LogReg | 0,5872 | 0,5886 | écarté |
| 7 | Baseline | GloVe + Party + LogReg | 0,5919 | 0,5933 | écarté |
| 8 | Avancé | TF-IDF + XGBoost (texte enrichi) | 0,6906 | 0,6883 | écarté (lexical, mauvaise généralisation OOD) |
| 9 | Avancé | DistilBERT fine-tuné | n.d. | n.d. | abandonné (CPU >9h) |
| 10 | Avancé | RoBERTa fine-tuné | n.d. | n.d. | abandonné (CPU >20h) |
| 11 | Avancé | Stacking DistilBERT + RoBERTa + XGBoost | ~0,66 | ~0,66 | écarté (complexité sans gain) |
| 12 | **Final** | **DistilBERT + XGBoost** | **0,6882** | **0,6888** | **retenu** |

Plusieurs observations méritent d'être soulignées à la lecture de ce tableau.

D'abord, parmi les baselines linéaires, **TF-IDF + LinearSVC pose un plancher solide à 0,6407 F1w**, nettement au-dessus des autres représentations. L'écart avec GloVe (0,5886) est significatif et s'explique principalement par la longueur courte des déclarations LIAR : les bigrammes TF-IDF capturent des colocations politiques précises (« tax cut », « health care ») que le mean pooling de GloVe dilue dans une moyenne peu informative. LinearSVC présente toutefois un sur-apprentissage notable (gap train/test de 18,7 points), bien que sa généralisation reste meilleure que celle de LogReg.

Ensuite, **deux approches XGBoost se détachent nettement** des baselines linéaires et atteignent toutes deux la zone des 0,69 :

- **TF-IDF + XGBoost** sur texte enrichi atteint **0,6906 d'accuracy** et **0,6883 de F1w**, soit ~5 points au-dessus du meilleur modèle linéaire.
- **DistilBERT + XGBoost** atteint **0,6882 d'accuracy** et **0,6888 de F1w**, score quasi identique à la meilleure baseline lexicale.

Le résultat est intéressant : sur LIAR pris isolément, **TF-IDF + XGBoost et DistilBERT + XGBoost sont essentiellement à égalité**. Ce n'est donc pas la performance brute in-domain qui justifie notre choix final, mais **la capacité de généralisation hors-domaine** (cf. section 5.2) et la **richesse des embeddings sémantiques** réutilisables pour l'analyse cross-domain et l'interprétabilité (cf. section 6). Sur ces deux critères, DistilBERT prend nettement l'avantage.

Il faut enfin être lucide sur **le plafond intrinsèque de LIAR**. Une accuracy proche de 0,69 sur LIAR binaire est en réalité un très bon résultat : c'est dans la fourchette haute de l'état de l'art littéraire (~0,67-0,70). Le dataset est intrinsèquement difficile, les classes `half-true` et `barely-true` étant ambiguës par construction, et même les transformers fine-tunés les plus gros peinent à dépasser ce plafond. Un exercice de reproduction sur un notebook externe au projet, qui annonçait un F1 de 0,710 (chiffre qui nous semblait initialement hors d'atteinte), a révélé que ce score était en réalité un F1 **binaire** — calculé uniquement sur la classe `Real`, conformément au comportement par défaut de sklearn (`average='binary'`) — et non un F1 weighted. Sur la métrique équivalente, notre modèle s'avère **largement supérieur** (0,6888 F1w contre 0,6346). La leçon est claire : le choix de la métrique compte autant que celui du modèle, et nous y revenons en détail en annexe D.

### 5.2 Résultats out-of-domain sur ISOT et WELFake

C'est ici que nous mesurons réellement la robustesse de nos modèles. Nous évaluons ceux entraînés sur LIAR sur les deux datasets externes, avec un échantillon de 5 000 par dataset pour des raisons de temps de calcul. Une subtilité importante : les colonnes `speaker`, `party` et `credibility_score` n'existent pas dans ISOT/WELFake, et nous les remplaçons donc par les **moyennes globales** apprises sur LIAR — ce qui dégrade nécessairement le modèle hybride, mais constitue le seul moyen de l'évaluer hors de son domaine.

| Modèle | LIAR (in-domain) | ISOT (OOD) | WELFake (OOD) |
|---|---|---|---|
| TF-IDF + LogReg | 0,6006 | ~0,52 | ~0,49 |
| TF-IDF + XGBoost | 0,6906 | ~0,53 | ~0,50 |
| DistilBERT + XGBoost | 0,6882 | ~0,55 | ~0,52 |

Les chiffres exacts varient légèrement d'un run à l'autre (sampling aléatoire), mais l'ordre de grandeur reste constant : **la chute en OOD est de 10 à 15 points d'accuracy**, quel que soit le modèle. DistilBERT s'en tire systématiquement mieux que TF-IDF grâce à ses représentations pré-entraînées, mais cela ne suffit pas à considérer qu'un modèle « fonctionne » hors-domaine. Ce résultat, bien que décevant en valeur absolue, est cohérent avec les observations rapportées dans la littérature sur le *domain shift*.

### 5.3 Discussion des résultats

Trois facteurs expliquent cet écart in-domain vs out-of-domain, et il est utile de les examiner en détail.

Le premier est **la longueur des textes**. LIAR présente une moyenne d'environ 100 caractères, contre plus de 1 000 pour ISOT et WELFake. Un modèle entraîné à pondérer un signal sur quelques mots ne sait pas le faire correctement sur un article complet où l'information pertinente est dispersée. Ce n'est pas une question d'architecture mais une différence structurelle dans la distribution des entrées.

Le deuxième est **le vocabulaire LIAR-centré**. Notre modèle a vu des noms de politiciens américains, des sujets de campagne et des formulations propres aux déclarations courtes. Les datasets externes parlent en revanche d'autres médias, d'autres plateformes, d'événements internationaux, dans un registre journalistique. Une grande partie des mots-clés discriminants sur LIAR n'apparaissent tout simplement pas dans ISOT/WELFake — et réciproquement.

Le troisième facteur est **l'absence de métadonnées en OOD**. Notre modèle hybride s'appuie partiellement sur `credibility_score` et `speaker_cred` pour ses prédictions ; en OOD, ces features sont remplacées par des valeurs par défaut, ce qui prive le modèle de ses signaux les plus forts. Il est important de garder ce point en tête : une partie de notre performance in-domain vient de ces metadata, pas uniquement du texte.

**Implication pratique** : pour un déploiement en production, il serait nécessaire soit d'entraîner le modèle sur un **mélange multi-domaines** (LIAR + ISOT + WELFake), soit de recourir à des techniques d'**adaptation de domaine** plus sophistiquées. Notre travail ne résout pas le problème de la généralisation, mais il le **mesure proprement** et trace une voie claire pour la suite.

---

## 6. Interprétabilité, biais et IA responsable

### 6.1 Interprétabilité locale et globale

Comprendre **pourquoi** un modèle prend ses décisions est aussi important que mesurer sa performance brute. Nous avons combiné trois techniques d'interprétabilité complémentaires.

**LIME** d'abord, qui fournit des explications **locales** sur le pipeline TF-IDF + LogReg. Appliqué à des exemples corrects et incorrects du test set LIAR, il identifie les mots qui poussent le modèle vers FAKE ou REAL. Sur les vrais positifs FAKE, on retrouve fréquemment des termes comme `obama`, `tax`, `percent`, `say` — c'est-à-dire des mots-clés fortement chargés politiquement, qui n'ont aucun lien direct avec la véracité du propos. Sur les vrais positifs REAL, le vocabulaire est plus neutre : `state`, `program`, `report`. Cette observation confirme que le modèle apprend en partie une corrélation entre certains champs lexicaux et le label, ce qui correspond exactement au piège que nous voulions identifier.

**SHAP LinearExplainer** ensuite, pour l'importance globale des features TF-IDF. Nous extrayons les 30 mots les plus influents par valeur absolue moyenne de SHAP, ainsi que la direction signée pour distinguer les mots qui poussent vers FAKE de ceux qui poussent vers REAL. Les résultats confirment et complètent l'analyse locale obtenue avec LIME.

**SHAP TreeExplainer** enfin, appliqué à notre XGBoost final, pour comparer l'importance des **embeddings DistilBERT** (768 dimensions) à celle des **métadonnées** (5 features). C'est le résultat le plus marquant : les metadata `credibility_score` et `speaker_cred` présentent une importance **par feature** très élevée, ce qui signifie que notre modèle s'appuie en partie sur la **réputation historique du locuteur** plutôt que sur le seul contenu textuel. Ce comportement n'est pas nécessairement problématique — la réputation est un signal légitime — mais il pose une question éthique : un nouveau locuteur sans historique sera systématiquement évalué selon la moyenne globale, et non selon ce qu'il dit réellement.

### 6.2 Interprétabilité cross-domain

Nous avons étendu l'analyse SHAP aux datasets ISOT et WELFake, en conservant le même modèle TF-IDF + LogReg. Le résultat est frappant : **moins de 30 % des 100 mots les plus influents sur LIAR apparaissent significativement dans les datasets externes**. Autrement dit, le vocabulaire appris par notre modèle est presque inutile en OOD. Cette mesure constitue une quantification directe du domain shift et explique pourquoi nos performances chutent autant en section 5.2 — il ne s'agit pas d'une moindre « intelligence » du modèle, mais simplement de l'absence des signaux sur lesquels il s'était appuyé.

### 6.3 Biais, fairness et risques

**Biais par parti politique.** Le déséquilibre du dataset (49,8 % FAKE chez les Républicains contre 33,9 % chez les Démocrates) crée une corrélation que le modèle apprend mécaniquement. Concrètement, nous observons un **taux de faux positifs plus élevé** (déclarations vraies étiquetées FAKE) pour les Républicains. Faut-il interpréter ce résultat comme un biais du modèle ou comme le reflet d'une réalité factuelle dans les données PolitiFact ? La réponse la plus honnête est : les deux. D'un point de vue éthique cependant, le risque demeure majeur — un modèle de détection de fake news qui pénalise systématiquement un parti renforce une perception d'injustice algorithmique, même lorsqu'il n'est pas statistiquement « dans l'erreur ».

**Biais par locuteur.** Lorsque 15 personnes représentent une part disproportionnée du corpus (Obama, Trump, Clinton…), le risque de sur-apprentissage stylistique est réel. Notre analyse montre que l'accuracy varie fortement d'un top speaker à l'autre, ce qui suggère que le modèle a mémorisé des patterns personnels plutôt que des indicateurs généralisables. Il faut rappeler que la collecte LIAR date d'avant 2017, ce qui explique en grande partie cette sur-représentation, et qu'un volume élevé de déclarations n'implique pas que celles-ci soient majoritairement fausses.

**Biais par sujet.** Les sujets dominants (`health-care`, `taxes`, `immigration`) bénéficient d'un volume suffisant pour un apprentissage stable, mais les sujets rares présentent des variations de qualité importantes. Là encore, le contexte pré-électoral de la collecte amplifie le problème : certains sujets étaient sur-discutés à cette époque et le sont nettement moins aujourd'hui.

### 6.4 Limites du modèle

En synthèse, voici les principales limites identifiées :

- **Vocabulaire LIAR-centré** : faible robustesse hors-domaine, comme nous l'avons quantifié.
- **Dépendance aux métadonnées** : dégradation forte lorsque `speaker` et `party` sont inconnus, ce qui est précisément le cas dans tout déploiement réel sur du texte « sauvage ».
- **Plafond intrinsèque de LIAR** : ~0,67 d'accuracy au mieux, contraint par les classes intrinsèquement ambiguës (`half-true`, `barely-true`).
- **Absence de contexte multimodal** : pas d'images, pas de propagation, pas d'historique de partage. Or c'est souvent à ce niveau que se joue la viralité d'une fake news.

---

## 7. Discussion et perspectives

### 7.1 Principales conclusions

Avec le recul, quatre conclusions se dégagent de ce travail.

D'abord, les **modèles classiques TF-IDF restent étonnamment compétitifs** sur LIAR. Nous atteignons 0,640 F1w avec un LinearSVC, ce qui s'avère difficile à dépasser. La raison est structurelle : les déclarations LIAR sont courtes, et sur du texte court les bigrammes lexicaux capturent souvent mieux le signal que des embeddings moyennés. Ce résultat n'est pas une déception mais une leçon importante — des baselines bien réglées sont souvent plus robustes que ce que l'on imagine.

Ensuite, **DistilBERT + XGBoost apporte un gain net** par rapport aux baselines linéaires (~+5 points d'accuracy par rapport à TF-IDF + LinearSVC), tout en offrant une représentation sémantique exploitable pour l'analyse cross-domain et l'interprétabilité. Sur le score in-domain pur, il fait jeu égal avec TF-IDF + XGBoost (0,6882 contre 0,6906), mais c'est sur la robustesse OOD et la richesse de l'analyse que la différence se creuse.

Troisièmement, **la généralisation hors-domaine reste limitée**, et c'est probablement le résultat le plus honnête de notre projet. La chute est de 10 à 15 points en sortant de LIAR, et ni TF-IDF ni DistilBERT ne parviennent à la compenser. La cause ne réside pas dans le modèle, mais dans la nature même de LIAR : déclarations courtes, vocabulaire spécifique, métadonnées exclusives.

Quatrièmement, **les biais structurels révélés par l'analyse de fairness** (parti, locuteur, sujet) ne sont supprimés par aucun modèle purement statistique. Ils sont inscrits dans les données, et leur traitement passe nécessairement par une intervention au niveau des données ou par des contraintes explicites de fairness.

### 7.2 Pistes d'amélioration

Si nous devions poursuivre ce projet, plusieurs pistes seraient prioritaires :

- **Entraînement multi-domaines** sur un mélange LIAR + ISOT + WELFake, afin de forcer le modèle à apprendre des features plus universelles plutôt que LIAR-spécifiques.
- **Adaptation de domaine** plus sophistiquée (DANN, fine-tuning progressif sur la cible) pour réduire le drop OOD sans nécessiter d'annotation manuelle supplémentaire.
- **Modèles plus larges** : RoBERTa-large, DeBERTa, ou modèles spécialisés en fact-checking, fine-tunés cette fois sur GPU pour s'affranchir du coût CPU prohibitif.
- **Approche multimodale** intégrant les images et la propagation sur les réseaux sociaux. Des datasets de type FakeNewsNet, qui incluent les interactions Twitter, apporteraient un signal très complémentaire au texte seul.
- **Classification fine** (3 ou 6 classes au lieu du binaire), pour ne pas écraser l'ambiguïté de `half-true` et `barely-true`. Le binaire est pratique, mais il perd de l'information.
- **Audit fairness systématique** : contraintes de parité par parti, calibration par sous-groupe, mesures de disparate impact. Cela constituerait un travail à part entière.

---

## 8. Conclusion

Ce projet nous a permis de construire un pipeline complet de détection de fake news politiques sur LIAR, depuis l'analyse exploratoire jusqu'au déploiement applicatif. Notre architecture finale **DistilBERT + XGBoost** atteint **0,6882 d'accuracy** et **0,6888 de F1w** in-domain — soit dans la fourchette haute de l'état de l'art littéraire pour LIAR (~0,67-0,70) — et démontre une meilleure capacité de généralisation que les baselines TF-IDF sur les datasets externes ISOT et WELFake, sans pour autant rester pleinement opérationnelle hors-domaine.

Au-delà des chiffres, trois leçons méritent d'être retenues, et nous ne les avions pas anticipées au départ. Premièrement, **le choix de la métrique est critique** : un F1 binaire et un F1 weighted peuvent différer de 5 points et littéralement inverser le classement des modèles. Sans une analyse approfondie, nous aurions pu croire être très en retrait par rapport à une référence externe, alors que nous étions en réalité au-dessus. Deuxièmement, **la généralisation cross-domain est un problème structurel** qui dépasse le simple choix d'architecture — il ne suffit pas de changer de modèle, il faut changer de stratégie d'entraînement. Troisièmement, **les biais par parti, locuteur et sujet** exigent une vigilance éthique réelle et une supervision humaine pour tout déploiement en production : un modèle qui prédit bien mais qui discrimine n'est pas un modèle déployable.

Pour matérialiser concrètement notre travail, nous avons également développé une **application de démonstration** (Next.js + FastAPI déployée sur Vercel) qui permet de tester le modèle en direct sur de nouvelles déclarations. C'est une manière de boucler la boucle : du dataset brut au modèle utilisable en quelques clics, en assumant pleinement les limites discutées tout au long de ce rapport.

---

## Références

### Datasets

- **LIAR Dataset** — Wang, W. Y. (2017). *"Liar, Liar Pants on Fire": A New Benchmark Dataset for Fake News Detection*. ACL 2017.
  - Article : <https://aclanthology.org/P17-2067/>
  - arXiv : <https://arxiv.org/abs/1705.00648>
- **ISOT Fake News Dataset** — University of Victoria, ISOT Research Lab.
  - <https://onlineacademiccommunity.uvic.ca/isot/2022/11/27/fake-news-detection-datasets/>
- **WELFake Dataset** — Verma, P. K., Agrawal, P., Amorim, I., & Prodan, R. (2021). *WELFake: Word Embedding Over Linguistic Features for Fake News Detection*. IEEE Transactions on Computational Social Systems.
  - <https://ieeexplore.ieee.org/document/9395133>
  - Kaggle mirror : <https://www.kaggle.com/datasets/saurabhshahane/fake-news-classification>

### Modèles et représentations

- **TF-IDF** — Salton, G. & McGill, M. J. (1983). *Introduction to Modern Information Retrieval*. McGraw-Hill.
  - Implémentation scikit-learn : <https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html>
- **Word2Vec** — Mikolov, T., Chen, K., Corrado, G., & Dean, J. (2013). *Efficient Estimation of Word Representations in Vector Space*. ICLR Workshop.
  - <https://arxiv.org/abs/1301.3781>
- **GloVe** — Pennington, J., Socher, R., & Manning, C. D. (2014). *GloVe: Global Vectors for Word Representation*. EMNLP 2014.
  - Article : <https://aclanthology.org/D14-1162/>
  - Page projet : <https://nlp.stanford.edu/projects/glove/>
- **DistilBERT** — Sanh, V., Debut, L., Chaumond, J., & Wolf, T. (2019). *DistilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter*. NeurIPS 2019 Workshop on Energy Efficient Machine Learning.
  - <https://arxiv.org/abs/1910.01108>
  - Modèle HuggingFace : <https://huggingface.co/distilbert-base-uncased>
- **RoBERTa** — Liu, Y., Ott, M., Goyal, N., Du, J., Joshi, M., Chen, D., Levy, O., Lewis, M., Zettlemoyer, L., & Stoyanov, V. (2019). *RoBERTa: A Robustly Optimized BERT Pretraining Approach*.
  - <https://arxiv.org/abs/1907.11692>
  - Modèle HuggingFace : <https://huggingface.co/roberta-base>
- **BERT (référence d'origine)** — Devlin, J., Chang, M.-W., Lee, K., & Toutanova, K. (2019). *BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding*. NAACL 2019.
  - <https://arxiv.org/abs/1810.04805>
- **XGBoost** — Chen, T. & Guestrin, C. (2016). *XGBoost: A Scalable Tree Boosting System*. KDD 2016.
  - Article : <https://dl.acm.org/doi/10.1145/2939672.2939785>
  - arXiv : <https://arxiv.org/abs/1603.02754>
  - Documentation : <https://xgboost.readthedocs.io/>
- **SMOTE** — Chawla, N. V., Bowyer, K. W., Hall, L. O., & Kegelmeyer, W. P. (2002). *SMOTE: Synthetic Minority Over-sampling Technique*. Journal of Artificial Intelligence Research.
  - <https://www.jair.org/index.php/jair/article/view/10302>
  - Implémentation `imbalanced-learn` : <https://imbalanced-learn.org/stable/references/generated/imblearn.over_sampling.SMOTE.html>

### Interprétabilité et fairness

- **LIME** — Ribeiro, M. T., Singh, S., & Guestrin, C. (2016). *"Why Should I Trust You?": Explaining the Predictions of Any Classifier*. KDD 2016.
  - <https://arxiv.org/abs/1602.04938>
  - GitHub : <https://github.com/marcotcr/lime>
- **SHAP** — Lundberg, S. M. & Lee, S.-I. (2017). *A Unified Approach to Interpreting Model Predictions*. NeurIPS 2017.
  - <https://arxiv.org/abs/1705.07874>
  - Documentation : <https://shap.readthedocs.io/>
- **Fairness in ML** — Mehrabi, N., Morstatter, F., Saxena, N., Lerman, K., & Galstyan, A. (2021). *A Survey on Bias and Fairness in Machine Learning*. ACM Computing Surveys.
  - <https://arxiv.org/abs/1908.09635>

### Détection de fake news (état de l'art)

- Shu, K., Sliva, A., Wang, S., Tang, J., & Liu, H. (2017). *Fake News Detection on Social Media: A Data Mining Perspective*. ACM SIGKDD Explorations.
  - <https://arxiv.org/abs/1708.01967>
- Zhou, X. & Zafarani, R. (2020). *A Survey of Fake News: Fundamental Theories, Detection Methods, and Opportunities*. ACM Computing Surveys.
  - <https://arxiv.org/abs/1812.00315>
- Hasan, M. et al. (2025). *Binary framing for political fake news detection on LIAR* (référence interne au projet, voir Notion).

### Outils et frameworks

- **HuggingFace Transformers** — Wolf, T. et al. (2020). *Transformers: State-of-the-Art Natural Language Processing*. EMNLP 2020 (System Demonstrations).
  - <https://aclanthology.org/2020.emnlp-demos.6/>
  - Documentation : <https://huggingface.co/docs/transformers>
- **scikit-learn** — Pedregosa, F. et al. (2011). *Scikit-learn: Machine Learning in Python*. JMLR.
  - <https://jmlr.org/papers/v12/pedregosa11a.html>
- **PyTorch** — Paszke, A. et al. (2019). *PyTorch: An Imperative Style, High-Performance Deep Learning Library*. NeurIPS 2019.
  - <https://arxiv.org/abs/1912.01703>

---

## Annexes

### A. Structure du dépôt

```
grp3_projet3_data/
├── data/
│   ├── brutes/          (sources brutes : LIAR, FakeNewsNet…)
│   ├── externes/        (ISOT, WELFake — bruts, LFS)
│   ├── traitees/        (parquets pré-traités, LFS)
│   └── fusionnes/       (liar_unifie.csv)
├── notebooks/
│   ├── EDA_*.ipynb
│   ├── Modeles_de_Base.ipynb
│   ├── Modeles_Avances.ipynb
│   ├── Evaluation_Hors_Domaine.ipynb
│   └── Interpretabilite_Biais.ipynb
├── models/              (modèles sauvegardés + métriques JSON)
└── app/
    ├── api/             (FastAPI backend)
    └── frontend/        (Next.js frontend)
```

### B. Détail des hyperparamètres XGBoost final

```python
XGBClassifier(
    n_estimators=500,
    max_depth=4,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.5,
    scale_pos_weight=n_fake/n_real,
    objective="binary:logistic",
    random_state=42,
)
```

Features : embeddings DistilBERT mean-pooled (768) + `credibility_score`, `speaker_cred` (target encoding), `log(1+speaker_count)`, `party_cred`, `n_words`.

### C. Métriques détaillées de tous les modèles (LIAR test set)

| Modèle | Acc | F1w | Precision | Recall |
|---|---|---|---|---|
| TF-IDF + XGBoost (texte enrichi) | 0,6906 | 0,6883 | 0,6885 | 0,6906 |
| **DistilBERT + XGBoost (final)** | **0,6882** | **0,6888** | — | — |
| TF-IDF + LinearSVC | 0,6401 | 0,6407 | 0,6417 | 0,6401 |
| TF-IDF + SMOTE + LinearSVC | 0,6275 | 0,6285 | 0,6304 | 0,6275 |
| TF-IDF + SMOTE + LogReg | 0,6148 | 0,6163 | 0,6210 | 0,6148 |
| TF-IDF + LogReg | 0,6006 | 0,6022 | 0,6094 | 0,6006 |
| Word2Vec + LogReg | 0,5943 | 0,5960 | 0,6021 | 0,5943 |
| GloVe + Party + LogReg | 0,5919 | 0,5933 | 0,5959 | 0,5919 |
| GloVe + LogReg | 0,5872 | 0,5886 | 0,5918 | 0,5872 |

### D. Reproduction des résultats de Laura (DistilBERT + XGBoost)

En chargeant directement les embeddings `LABORATOIRE/Laura/X_train_bert.npy` et en réentraînant XGBoost avec ses hyperparamètres exacts (`n_estimators=100, learning_rate=0.1`), nous reproduisons :

- Accuracy : **0,6433**
- F1 binaire (classe Real, default sklearn) : **0,7095**
- F1 weighted (toutes classes) : **0,6346**

À comparer avec notre modèle final :

- Accuracy : **0,6882** (+4,5 points)
- F1 weighted : **0,6888** (+5,4 points)

Cette reproduction confirme deux choses importantes : (1) la différence apparente entre les notebooks venait d'une différence de **métrique** (binary vs weighted) et non d'une supériorité réelle du modèle de référence ; (2) sur la métrique équivalente, notre architecture finale est **nettement supérieure**.

### E. Application de démonstration

- Frontend Next.js : `https://sentinel-fakenews.vercel.app`
- Backend FastAPI : `https://api-vercel-seven-eta.vercel.app`
- Modèles servis : TF-IDF + LogReg / LinearSVC, et localement DistilBERT + XGBoost.
