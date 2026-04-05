"use client";

import { createContext, useContext, useState, useCallback, useEffect, type ReactNode } from "react";
import type { AnalyseResultat, FormulaireSaisie } from "@/lib/types";
import { MODELE_DEFAUT, MODELES_DISPONIBLES, type ModeleId } from "@/lib/predict";
import { chargerHistorique, sauvegarderResultat, supprimerResultat, viderHistorique } from "@/lib/history";

interface ContexteAnalyse {
  resultatCourant: AnalyseResultat | null;
  historique: AnalyseResultat[];
  chargement: boolean;
  erreur: string | null;
  modeleSelectionne: ModeleId;
  analyser: (saisie: FormulaireSaisie) => Promise<void>;
  changerModele: (id: ModeleId) => void;
  supprimerEntree: (id: string) => void;
  viderTout: () => void;
  effacerResultatCourant: () => void;
}

const ContexteAnalyse = createContext<ContexteAnalyse | null>(null);

export function AnalyseProvider({ children }: { children: ReactNode }) {
  const [resultatCourant, setResultatCourant]     = useState<AnalyseResultat | null>(null);
  const [historique, setHistorique]               = useState<AnalyseResultat[]>([]);
  const [chargement, setChargement]               = useState(false);
  const [erreur, setErreur]                       = useState<string | null>(null);
  const [modeleSelectionne, setModeleSelectionne] = useState<ModeleId>(MODELE_DEFAUT);

  useEffect(() => {
    setHistorique(chargerHistorique());
    const saved = localStorage.getItem("sentinel_modele") as ModeleId | null;
    if (saved && saved in MODELES_DISPONIBLES) setModeleSelectionne(saved);
  }, []);

  const changerModele = useCallback((id: ModeleId) => {
    setModeleSelectionne(id);
    localStorage.setItem("sentinel_modele", id);
  }, []);

  const analyser = useCallback(async (saisie: FormulaireSaisie) => {
    if (!saisie.declaration.trim()) return;
    setChargement(true);
    setErreur(null);

    try {
      const res = await fetch("/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ texte: saisie.declaration, modele: modeleSelectionne }),
      });

      const data = await res.json();

      if (!res.ok) {
        setErreur(data.error ?? "Erreur lors de l'analyse.");
        return;
      }

      const modele = MODELES_DISPONIBLES[modeleSelectionne];
      const resultat: AnalyseResultat = {
        id:           `${Date.now()}`,
        declaration:  saisie.declaration,
        orateur:      saisie.orateur  || "Orateur inconnu",
        parti:        saisie.parti    || "Non renseigné",
        sujet:        saisie.sujet    || "Politique générale",
        date:         new Date().toLocaleDateString("fr-FR", { day: "numeric", month: "long", year: "numeric" }),
        verdict:      data.label,           // "Réel" | "Faux"
        confiance:    data.confiance,
        probaFaux:    Math.round(data.proba_faux * 100),
        probaReel:    Math.round(data.proba_reel * 100),
        modele:       modele.nom,
        facteursCles: (data.facteurs_cles ?? []).map((f: { mot: string; poids: number }) => ({
          mot: f.mot, poids: f.poids,
        })),
      };

      setResultatCourant(resultat);
      sauvegarderResultat(resultat);
      setHistorique(chargerHistorique());
    } catch (err) {
      setErreur("Impossible de contacter l'API. Assurez-vous que le serveur Python tourne.");
      console.error(err);
    } finally {
      setChargement(false);
    }
  }, [modeleSelectionne]);

  const supprimerEntree = useCallback((id: string) => {
    setHistorique(supprimerResultat(id));
  }, []);

  const viderTout = useCallback(() => {
    viderHistorique();
    setHistorique([]);
  }, []);

  const effacerResultatCourant = useCallback(() => {
    setResultatCourant(null);
    setErreur(null);
  }, []);

  return (
    <ContexteAnalyse.Provider
      value={{ resultatCourant, historique, chargement, erreur, modeleSelectionne, analyser, changerModele, supprimerEntree, viderTout, effacerResultatCourant }}
    >
      {children}
    </ContexteAnalyse.Provider>
  );
}

export function useAnalyse(): ContexteAnalyse {
  const ctx = useContext(ContexteAnalyse);
  if (!ctx) throw new Error("useAnalyse doit être utilisé dans un AnalyseProvider");
  return ctx;
}
