import type { Verdict } from "./types";

export const MODELES_DISPONIBLES = {
  "logreg-tfidf": {
    nom:         "TF-IDF + Regression Logistique",
    court:       "LogReg TF-IDF",
    description: "Pipeline TF-IDF bi-grammes + SMOTE + LogReg. Meilleure performance en classification binaire.",
    precision:   63.7,
    f1:          63.2,
    rappel:      63.2,
    delaiMs:     600,
    couleur:     "#007AFF",
    icone:       "functions",
    badge:       "Recommande",
    type:        "Classique",
  },
  "linearsvc-tfidf": {
    nom:         "TF-IDF + LinearSVC",
    court:       "SVC TF-IDF",
    description: "Pipeline TF-IDF bi-grammes + SMOTE + SVM lineaire. Performance quasi-identique, legerement plus rapide.",
    precision:   63.8,
    f1:          63.2,
    rappel:      63.1,
    delaiMs:     400,
    couleur:     "#5856D6",
    icone:       "scatter_plot",
    badge:       null,
    type:        "Classique",
  },
} as const;

export type ModeleId = keyof typeof MODELES_DISPONIBLES;
export const MODELE_DEFAUT: ModeleId = "logreg-tfidf";

export const VERDICT_CONFIG: Record<Verdict, { couleur: string; fond: string; icone: string }> = {
  "Réel": { couleur: "#34C759", fond: "rgba(52, 199, 89, 0.1)",  icone: "verified"  },
  "Faux": { couleur: "#FF3B30", fond: "rgba(255, 59, 48, 0.1)",  icone: "dangerous" },
};
