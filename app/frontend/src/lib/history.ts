import type { AnalyseResultat } from "./types";

const CLE_STOCKAGE = "sentinel_historique";
const MAX_ENTREES  = 50;

export function chargerHistorique(): AnalyseResultat[] {
  if (typeof window === "undefined") return [];
  try {
    const json = localStorage.getItem(CLE_STOCKAGE);
    return json ? (JSON.parse(json) as AnalyseResultat[]) : [];
  } catch {
    return [];
  }
}

export function sauvegarderResultat(resultat: AnalyseResultat): void {
  const historique = chargerHistorique();
  const mise_a_jour = [resultat, ...historique].slice(0, MAX_ENTREES);
  localStorage.setItem(CLE_STOCKAGE, JSON.stringify(mise_a_jour));
}

export function supprimerResultat(id: string): AnalyseResultat[] {
  const filtre = chargerHistorique().filter((r) => r.id !== id);
  localStorage.setItem(CLE_STOCKAGE, JSON.stringify(filtre));
  return filtre;
}

export function viderHistorique(): void {
  localStorage.removeItem(CLE_STOCKAGE);
}
