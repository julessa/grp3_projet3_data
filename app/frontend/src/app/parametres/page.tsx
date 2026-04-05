"use client";

import { useAnalyse } from "@/context/AnalysisContext";
import { MODELES_DISPONIBLES, type ModeleId } from "@/lib/predict";
import SideNav from "@/components/SideNav";
import TopNav from "@/components/TopNav";
import { CheckCircle2, Timer, Zap } from "lucide-react";

export default function PageParametres() {
  const { modeleSelectionne, changerModele } = useAnalyse();

  return (
    <div className="bg-ios-bg min-h-screen">
      <SideNav />
      <main className="ml-[260px] min-h-screen">
        <TopNav />
        <div className="p-8 max-w-5xl mx-auto">
          <div className="mb-8">
            <h2 className="text-3xl font-bold text-ios-label tracking-tight">Parametres</h2>
            <p className="text-[13px] text-ios-label-tertiary mt-1">
              Choisissez le modele de classification pour les analyses.
            </p>
          </div>

          {/* Selection du modele */}
          <div className="mb-6">
            <h3 className="text-[13px] font-semibold text-ios-label-tertiary mb-4 flex items-center gap-2">
              <Zap className="w-4 h-4" />
              Modele de classification
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {(Object.entries(MODELES_DISPONIBLES) as [ModeleId, typeof MODELES_DISPONIBLES[ModeleId]][]).map(([id, modele]) => {
                const actif = modeleSelectionne === id;
                return (
                  <button
                    key={id}
                    type="button"
                    onClick={() => changerModele(id)}
                    className={`text-left glass rounded-2xl p-5 transition-all duration-200 relative shadow-glass ${
                      actif ? "ring-2" : "hover:bg-ios-card-hover"
                    }`}
                    style={actif ? { boxShadow: `0 0 0 2px ${modele.couleur}` } : undefined}
                  >
                    {modele.badge && (
                      <span className="absolute top-4 right-4 text-[10px] font-semibold px-2.5 py-0.5 rounded-full"
                        style={{ backgroundColor: `${modele.couleur}12`, color: modele.couleur }}>
                        {modele.badge}
                      </span>
                    )}

                    <div className="flex items-center gap-3 mb-3">
                      <div className="w-10 h-10 rounded-xl flex items-center justify-center"
                        style={{ backgroundColor: `${modele.couleur}12` }}>
                        <Zap className="w-5 h-5" style={{ color: modele.couleur }} />
                      </div>
                      <div>
                        <p className="text-[11px] font-semibold text-ios-label-tertiary">{modele.type}</p>
                        <p className="text-[15px] font-bold text-ios-label">{modele.court}</p>
                      </div>
                    </div>

                    <p className="text-[12px] text-ios-label-tertiary mb-4 leading-relaxed">{modele.description}</p>

                    <div className="grid grid-cols-3 gap-2 mb-3">
                      {[
                        { label: "Precision", value: modele.precision },
                        { label: "Macro F1",  value: modele.f1 },
                        { label: "Rappel",    value: modele.rappel },
                      ].map(({ label, value }) => (
                        <div key={label} className="bg-ios-bg rounded-xl p-2.5 text-center">
                          <p className="text-[9px] font-semibold text-ios-label-tertiary mb-0.5">{label}</p>
                          <p className="text-[14px] font-bold" style={{ color: actif ? modele.couleur : "var(--ios-label)" }}>
                            {value.toFixed(1)}%
                          </p>
                        </div>
                      ))}
                    </div>

                    <div className="flex items-center justify-between">
                      <span className="text-[11px] text-ios-label-tertiary flex items-center gap-1">
                        <Timer className="w-3 h-3" />
                        ~{(modele.delaiMs / 1000).toFixed(1)}s
                      </span>
                      {actif && (
                        <span className="text-[11px] font-semibold flex items-center gap-1" style={{ color: modele.couleur }}>
                          <CheckCircle2 className="w-3.5 h-3.5" />
                          Actif
                        </span>
                      )}
                    </div>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Resume modele actif */}
          <div className="glass rounded-2xl p-5 shadow-glass">
            <h3 className="text-[12px] font-semibold text-ios-label-tertiary mb-3">Modele actif</h3>
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl flex items-center justify-center"
                style={{ backgroundColor: `${MODELES_DISPONIBLES[modeleSelectionne].couleur}12` }}>
                <Zap className="w-5 h-5" style={{ color: MODELES_DISPONIBLES[modeleSelectionne].couleur }} />
              </div>
              <div>
                <p className="text-[14px] font-semibold text-ios-label">{MODELES_DISPONIBLES[modeleSelectionne].nom}</p>
                <p className="text-[12px] text-ios-label-tertiary">
                  F1 {MODELES_DISPONIBLES[modeleSelectionne].f1.toFixed(1)}% · Precision {MODELES_DISPONIBLES[modeleSelectionne].precision.toFixed(1)}%
                </p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
