export type Verdict = "Réel" | "Faux";

export interface FacteurCle {
  mot: string;
  poids: number;
}

export interface AnalyseResultat {
  id: string;
  declaration: string;
  orateur: string;
  parti: string;
  sujet: string;
  date: string;
  verdict: Verdict;
  confiance: number;
  probaFaux: number;   // 0–100
  probaReel: number;   // 0–100
  modele: string;
  facteursCles: FacteurCle[];
}

export interface FormulaireSaisie {
  declaration: string;
  orateur?: string;
  parti?: string;
  sujet?: string;
}
