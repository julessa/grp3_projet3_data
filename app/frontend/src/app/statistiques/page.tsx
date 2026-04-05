"use client";

import SideNav from "@/components/SideNav";
import TopNav from "@/components/TopNav";
import { MODELES_DISPONIBLES } from "@/lib/predict";
import { useAnalyse } from "@/context/AnalysisContext";
import { Trophy, BarChart3, Activity, TrendingUp } from "lucide-react";

export default function PageStatistiques() {
  const { historique } = useAnalyse();

  const total = historique.length;
  const fakeCount = historique.filter(r => r.verdict === "Faux").length;
  const realCount = total - fakeCount;
  const avgConfidence = total > 0 ? Math.round(historique.reduce((s, r) => s + r.confiance, 0) / total) : 0;

  const parModele: Record<string, number> = {};
  historique.forEach(r => {
    parModele[r.modele] = (parModele[r.modele] || 0) + 1;
  });

  return (
    <div className="bg-ios-bg min-h-screen">
      <SideNav />
      <main className="ml-[260px] min-h-screen">
        <TopNav />
        <div className="p-8 max-w-6xl mx-auto">
          <div className="mb-8">
            <h2 className="text-3xl font-bold text-ios-label tracking-tight">Statistiques</h2>
            <p className="text-[13px] text-ios-label-tertiary mt-1">
              Performances des modeles et apercu de votre utilisation
            </p>
          </div>

          {/* KPIs d'utilisation */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-8">
            {[
              { label: "Analyses effectuees", value: total.toString(), icon: Activity,    color: "#007AFF" },
              { label: "Classes Reel",        value: realCount.toString(), icon: TrendingUp, color: "#34C759" },
              { label: "Classes Faux",        value: fakeCount.toString(), icon: BarChart3,  color: "#FF3B30" },
              { label: "Confiance moyenne",   value: total > 0 ? `${avgConfidence}%` : "--", icon: Trophy, color: "#5856D6" },
            ].map(({ label, value, icon: Icon, color }) => (
              <div key={label} className="glass rounded-2xl p-5 shadow-glass">
                <div className="w-9 h-9 rounded-xl flex items-center justify-center mb-3"
                  style={{ backgroundColor: `${color}12` }}>
                  <Icon className="w-4 h-4" style={{ color }} />
                </div>
                <p className="text-2xl font-bold text-ios-label">{value}</p>
                <p className="text-[11px] text-ios-label-tertiary font-medium mt-0.5">{label}</p>
              </div>
            ))}
          </div>

          {/* Modeles disponibles */}
          <div className="glass rounded-3xl p-6 mb-6 shadow-glass">
            <h3 className="text-[13px] font-semibold text-ios-label-tertiary mb-5 flex items-center gap-2">
              <Trophy className="w-4 h-4" />
              Modeles disponibles
            </h3>
            <div className="overflow-x-auto">
              <table className="w-full text-[13px]">
                <thead>
                  <tr className="border-b border-ios-border">
                    <th className="text-left text-[11px] text-ios-label-tertiary font-semibold pb-3">Modele</th>
                    <th className="text-right text-[11px] text-ios-label-tertiary font-semibold pb-3">Precision</th>
                    <th className="text-right text-[11px] text-ios-label-tertiary font-semibold pb-3">F1 pondere</th>
                    <th className="text-right text-[11px] text-ios-label-tertiary font-semibold pb-3">Rappel</th>
                    <th className="text-right text-[11px] text-ios-label-tertiary font-semibold pb-3">Latence</th>
                    <th className="w-32 text-left text-[11px] text-ios-label-tertiary font-semibold pb-3 pl-4">F1</th>
                  </tr>
                </thead>
                <tbody>
                  {Object.values(MODELES_DISPONIBLES).map((m) => (
                    <tr key={m.nom} className="border-b border-ios-border/50 hover:bg-ios-card-hover transition-colors">
                      <td className="py-3.5 pr-4">
                        <div className="flex items-center gap-2">
                          <div className="w-2 h-2 rounded-full shrink-0" style={{ backgroundColor: m.couleur }} />
                          <span className="font-medium text-ios-label">{m.nom}</span>
                          {m.badge && (
                            <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full"
                              style={{ backgroundColor: `${m.couleur}12`, color: m.couleur }}>{m.badge}</span>
                          )}
                        </div>
                      </td>
                      <td className="text-right font-semibold py-3.5" style={{ color: m.couleur }}>{m.precision}%</td>
                      <td className="text-right font-semibold py-3.5" style={{ color: m.couleur }}>{m.f1}%</td>
                      <td className="text-right font-semibold py-3.5 text-ios-label-secondary">{m.rappel}%</td>
                      <td className="text-right text-ios-label-tertiary py-3.5">~{(m.delaiMs / 1000).toFixed(1)}s</td>
                      <td className="py-3.5 pl-4">
                        <div className="h-2 bg-ios-bg rounded-full overflow-hidden">
                          <div className="h-full rounded-full" style={{ width: `${m.f1}%`, backgroundColor: m.couleur }} />
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <p className="text-[11px] text-ios-label-tertiary mt-4">
              Metriques issues de l&apos;evaluation sur le jeu de test. Pipeline TF-IDF + SMOTE.
            </p>
          </div>

          {/* Utilisation par modele */}
          {total > 0 && Object.keys(parModele).length > 0 && (
            <div className="glass rounded-3xl p-6 shadow-glass">
              <h3 className="text-[13px] font-semibold text-ios-label-tertiary mb-5">
                Votre utilisation par modele
              </h3>
              <div className="space-y-3">
                {Object.entries(parModele).sort((a, b) => b[1] - a[1]).map(([model, count]) => {
                  const pct = Math.round((count / total) * 100);
                  return (
                    <div key={model}>
                      <div className="flex justify-between text-[12px] font-semibold mb-1">
                        <span className="text-ios-label">{model}</span>
                        <span className="text-ios-label-tertiary">{count} utilisation{count > 1 ? "s" : ""} ({pct}%)</span>
                      </div>
                      <div className="h-2 bg-ios-bg rounded-full overflow-hidden">
                        <div className="h-full rounded-full bg-ios-blue" style={{ width: `${pct}%` }} />
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
