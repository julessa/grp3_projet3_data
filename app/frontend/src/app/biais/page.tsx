"use client";

import SideNav from "@/components/SideNav";
import TopNav from "@/components/TopNav";
import { useAnalyse } from "@/context/AnalysisContext";
import { AlertTriangle, BarChart3, PieChart, Info } from "lucide-react";

function analyserBiaisHistorique(historique: ReturnType<typeof useAnalyse>["historique"]) {
  if (historique.length === 0) return null;

  const total = historique.length;
  const fakeCount = historique.filter(r => r.verdict === "Faux").length;
  const realCount = total - fakeCount;
  const fakePct = Math.round((fakeCount / total) * 100);
  const realPct = 100 - fakePct;
  const confMoyenne = Math.round(historique.reduce((s, r) => s + r.confiance, 0) / total);

  const parOrateur: Record<string, { total: number; faux: number }> = {};
  historique.forEach(r => {
    const key = r.orateur;
    if (key === "Orateur inconnu") return;
    if (!parOrateur[key]) parOrateur[key] = { total: 0, faux: 0 };
    parOrateur[key].total++;
    if (r.verdict === "Faux") parOrateur[key].faux++;
  });
  const topOrateurs = Object.entries(parOrateur)
    .map(([nom, { total: t, faux }]) => ({ nom, total: t, fauxPct: Math.round((faux / t) * 100) }))
    .sort((a, b) => b.total - a.total)
    .slice(0, 5);

  const parSujet: Record<string, { total: number; faux: number }> = {};
  historique.forEach(r => {
    const key = r.sujet;
    if (key === "Politique generale" || key === "Politique générale") return;
    if (!parSujet[key]) parSujet[key] = { total: 0, faux: 0 };
    parSujet[key].total++;
    if (r.verdict === "Faux") parSujet[key].faux++;
  });
  const topSujets = Object.entries(parSujet)
    .map(([sujet, { total: t, faux }]) => ({ sujet, total: t, fauxPct: Math.round((faux / t) * 100) }))
    .sort((a, b) => b.total - a.total)
    .slice(0, 6);

  return { total, fakeCount, realCount, fakePct, realPct, confMoyenne, topOrateurs, topSujets };
}

export default function PageBiais() {
  const { historique } = useAnalyse();
  const stats = analyserBiaisHistorique(historique);

  return (
    <div className="bg-ios-bg min-h-screen">
      <SideNav />
      <main className="ml-[260px] min-h-screen">
        <TopNav />
        <div className="p-8 max-w-6xl mx-auto">
          <div className="mb-8">
            <h2 className="text-3xl font-bold text-ios-label tracking-tight">Analyse des biais</h2>
            <p className="text-[13px] text-ios-label-tertiary mt-1">
              Tendances et patterns issus de votre historique d&apos;analyses
            </p>
          </div>

          {/* Info */}
          <div className="glass rounded-2xl p-4 mb-8 flex items-start gap-3 shadow-glass">
            <div className="w-8 h-8 rounded-lg bg-ios-blue/10 flex items-center justify-center shrink-0 mt-0.5">
              <Info className="w-4 h-4 text-ios-blue" />
            </div>
            <p className="text-[13px] text-ios-label-secondary">
              Cette page analyse les tendances de <strong>votre historique d&apos;analyses</strong>.
              Plus vous analysez de declarations, plus ces informations seront riches.
              Les resultats refletent les predictions du modele, pas une verite absolue.
            </p>
          </div>

          {!stats ? (
            <div className="flex flex-col items-center justify-center py-24 gap-4">
              <div className="w-16 h-16 rounded-2xl bg-ios-bg flex items-center justify-center">
                <BarChart3 className="w-8 h-8 text-ios-label-tertiary/30" />
              </div>
              <p className="font-semibold text-ios-label-secondary">Pas encore de donnees</p>
              <p className="text-[13px] text-ios-label-tertiary text-center max-w-xs">
                Analysez des declarations d&apos;abord. Les tendances apparaitront ici a partir de votre historique.
              </p>
            </div>
          ) : (
            <>
              {/* KPIs */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
                {[
                  { label: "Analysees",         value: stats.total.toString(),      color: "#007AFF" },
                  { label: "Classees Faux",      value: stats.fakeCount.toString(),  color: "#FF3B30" },
                  { label: "Classees Reel",      value: stats.realCount.toString(),  color: "#34C759" },
                  { label: "Confiance moy.",     value: `${stats.confMoyenne}%`,     color: "#5856D6" },
                ].map(({ label, value, color }) => (
                  <div key={label} className="glass rounded-2xl p-5 shadow-glass">
                    <p className="text-2xl font-bold" style={{ color }}>{value}</p>
                    <p className="text-[11px] text-ios-label-tertiary font-medium mt-0.5">{label}</p>
                  </div>
                ))}
              </div>

              {/* Repartition des verdicts */}
              <div className="glass rounded-3xl p-6 mb-6 shadow-glass">
                <h3 className="text-[13px] font-semibold text-ios-label-tertiary mb-5 flex items-center gap-2">
                  <PieChart className="w-4 h-4" />
                  Repartition des verdicts
                </h3>
                <div className="flex h-8 rounded-xl overflow-hidden gap-[1px] mb-3">
                  <div className="h-full flex items-center justify-center bg-ios-green transition-all"
                    style={{ width: `${stats.realPct}%` }}>
                    <span className="text-[11px] font-bold text-white">Reel {stats.realPct}%</span>
                  </div>
                  <div className="h-full flex items-center justify-center bg-ios-red transition-all"
                    style={{ width: `${stats.fakePct}%` }}>
                    <span className="text-[11px] font-bold text-white">Faux {stats.fakePct}%</span>
                  </div>
                </div>
                <p className="text-[11px] text-ios-label-tertiary">
                  Base sur {stats.total} declaration{stats.total !== 1 ? "s" : ""} analysee{stats.total !== 1 ? "s" : ""}
                </p>

                {stats.fakePct > 60 && (
                  <div className="flex items-start gap-2 mt-4 p-3 rounded-xl bg-ios-orange/10 border border-ios-orange/15">
                    <AlertTriangle className="w-4 h-4 text-ios-orange shrink-0 mt-0.5" />
                    <p className="text-[12px] text-ios-label-secondary">
                      <strong className="text-ios-orange">Taux eleve de faux :</strong> Plus de 60% des declarations analysees ont ete classees comme fausses.
                      Cela peut indiquer un biais de selection dans les textes testes, ou une prudence excessive du modele.
                    </p>
                  </div>
                )}
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Par sujet */}
                {stats.topSujets.length > 0 && (
                  <div className="glass rounded-3xl p-6 shadow-glass">
                    <h3 className="text-[13px] font-semibold text-ios-label-tertiary mb-5">
                      Par sujet
                    </h3>
                    <div className="space-y-3">
                      {stats.topSujets.map(({ sujet, total, fauxPct }) => (
                        <div key={sujet}>
                          <div className="flex justify-between text-[12px] font-semibold mb-1">
                            <span className="text-ios-label">{sujet}</span>
                            <span className="text-ios-label-tertiary">
                              {total} analysee{total > 1 ? "s" : ""} · <span className={fauxPct > 50 ? "text-ios-red" : "text-ios-green"}>{fauxPct}% faux</span>
                            </span>
                          </div>
                          <div className="h-1.5 bg-ios-bg rounded-full overflow-hidden">
                            <div className="h-full rounded-full bg-ios-red" style={{ width: `${fauxPct}%` }} />
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Par orateur */}
                {stats.topOrateurs.length > 0 && (
                  <div className="glass rounded-3xl p-6 shadow-glass">
                    <h3 className="text-[13px] font-semibold text-ios-label-tertiary mb-5">
                      Par orateur
                    </h3>
                    <div className="space-y-3">
                      {stats.topOrateurs.map(({ nom, total, fauxPct }) => (
                        <div key={nom} className="flex items-center gap-3">
                          <div className="w-9 h-9 rounded-xl bg-ios-blue/10 flex items-center justify-center shrink-0 text-[13px] font-bold text-ios-blue">
                            {nom.charAt(0).toUpperCase()}
                          </div>
                          <div className="flex-1 min-w-0">
                            <p className="text-[13px] font-semibold text-ios-label truncate">{nom}</p>
                            <p className="text-[11px] text-ios-label-tertiary">{total} analysee{total > 1 ? "s" : ""}</p>
                          </div>
                          <p className={`text-[15px] font-bold shrink-0 ${fauxPct > 50 ? "text-ios-red" : "text-ios-green"}`}>
                            {fauxPct}% faux
                          </p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {stats.topSujets.length === 0 && stats.topOrateurs.length === 0 && (
                  <div className="glass rounded-3xl p-6 shadow-glass col-span-2 text-center py-12">
                    <p className="text-[13px] text-ios-label-tertiary">
                      Utilisez l&apos;onglet &laquo; Avec contexte &raquo; lors de l&apos;analyse pour ajouter orateurs et sujets.
                      Cela debloquera des details ici.
                    </p>
                  </div>
                )}
              </div>
            </>
          )}
        </div>
      </main>
    </div>
  );
}
