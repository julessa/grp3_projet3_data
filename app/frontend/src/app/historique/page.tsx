"use client";

import SideNav from "@/components/SideNav";
import TopNav from "@/components/TopNav";
import { useAnalyse } from "@/context/AnalysisContext";
import { VERDICT_CONFIG } from "@/lib/predict";
import type { AnalyseResultat } from "@/lib/types";
import { Trash2, History, ShieldCheck, ShieldAlert, HelpCircle } from "lucide-react";

export default function PageHistorique() {
  const { historique, supprimerEntree, viderTout } = useAnalyse();

  return (
    <div className="bg-ios-bg min-h-screen">
      <SideNav />
      <main className="ml-[260px] min-h-screen">
        <TopNav />
        <div className="p-8 max-w-5xl mx-auto">
          <div className="flex justify-between items-end mb-8">
            <div>
              <h2 className="text-3xl font-bold text-ios-label tracking-tight">Historique</h2>
              <p className="text-[13px] text-ios-label-tertiary mt-1">
                {historique.length} analyse{historique.length !== 1 ? "s" : ""} enregistree{historique.length !== 1 ? "s" : ""}
              </p>
            </div>
            {historique.length > 0 && (
              <button type="button" onClick={viderTout}
                className="flex items-center gap-2 px-4 py-2 rounded-xl text-[13px] font-semibold text-ios-red bg-ios-red/10 hover:bg-ios-red/15 transition-all">
                <Trash2 className="w-4 h-4" />
                Tout effacer
              </button>
            )}
          </div>

          {historique.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-24 gap-4">
              <div className="w-16 h-16 rounded-2xl bg-ios-bg flex items-center justify-center">
                <History className="w-8 h-8 text-ios-label-tertiary/30" />
              </div>
              <p className="font-semibold text-ios-label-secondary">Aucune analyse pour le moment</p>
              <p className="text-[13px] text-ios-label-tertiary text-center max-w-xs">
                Rendez-vous sur le tableau de bord pour analyser votre premiere declaration.
              </p>
            </div>
          ) : (
            <div className="flex flex-col gap-3">
              {historique.map((r: AnalyseResultat) => {
                const cfg = VERDICT_CONFIG[r.verdict as keyof typeof VERDICT_CONFIG]
                  ?? { couleur: "#8E8E93", fond: "rgba(142,142,147,0.1)", icone: "help" };
                const Icon = r.verdict === "Réel" ? ShieldCheck : r.verdict === "Faux" ? ShieldAlert : HelpCircle;

                return (
                  <div key={r.id}
                    className="glass rounded-2xl p-4 flex items-center gap-4 hover:bg-ios-card-hover transition-all group shadow-glass">
                    <div className="w-10 h-10 rounded-xl flex items-center justify-center shrink-0"
                      style={{ background: cfg.fond }}>
                      <Icon className="w-5 h-5" style={{ color: cfg.couleur }} />
                    </div>

                    <div className="flex-1 min-w-0">
                      <p className="font-medium text-ios-label truncate text-[14px]">
                        &ldquo;{r.declaration}&rdquo;
                      </p>
                      <div className="flex items-center gap-3 mt-1 flex-wrap">
                        <span className="text-[11px] font-semibold px-2 py-0.5 rounded-full"
                          style={{ color: cfg.couleur, background: cfg.fond }}>{r.verdict}</span>
                        <span className="text-[11px] text-ios-label-tertiary">{r.confiance}% confiance</span>
                        {r.orateur !== "Orateur inconnu" && (
                          <span className="text-[11px] text-ios-label-tertiary">{r.orateur}</span>
                        )}
                        <span className="text-[11px] text-ios-label-tertiary">{r.date}</span>
                      </div>
                    </div>

                    <div className="text-right shrink-0">
                      <p className="text-2xl font-bold" style={{ color: cfg.couleur }}>
                        {r.confiance}%
                      </p>
                    </div>

                    <button type="button" onClick={() => supprimerEntree(r.id)}
                      title="Supprimer"
                      className="opacity-0 group-hover:opacity-100 text-ios-label-tertiary hover:text-ios-red transition-all p-2 rounded-xl hover:bg-ios-red/10 shrink-0">
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
