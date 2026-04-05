"use client";

import { useAnalyse } from "@/context/AnalysisContext";
import { MODELES_DISPONIBLES } from "@/lib/predict";
import { BarChart3, Cpu, TrendingUp, Zap } from "lucide-react";

export default function SidePanels() {
  const { resultatCourant, chargement, modeleSelectionne } = useAnalyse();
  const modele = MODELES_DISPONIBLES[modeleSelectionne];

  const BARRES = [
    { label: "Reel",  color: "#34C759", getVal: (r: typeof resultatCourant) => r?.probaReel ?? 0 },
    { label: "Faux",  color: "#FF3B30", getVal: (r: typeof resultatCourant) => r?.probaFaux ?? 0 },
  ];

  return (
    <div className="col-span-12 lg:col-span-4 flex flex-col gap-4">
      {/* Probabilites */}
      <div className="glass rounded-3xl p-5 flex-1 shadow-glass">
        <h4 className="text-[12px] font-semibold text-ios-label-tertiary mb-5 flex items-center gap-2">
          <BarChart3 className="w-4 h-4" />
          Probabilites
        </h4>

        {chargement ? (
          <div className="space-y-4">
            {BARRES.map((b) => (
              <div key={b.label}>
                <div className="flex justify-between text-[12px] font-semibold mb-1.5">
                  <span className="text-ios-label-tertiary">{b.label}</span>
                  <span className="text-ios-label-tertiary">--</span>
                </div>
                <div className="h-2 w-full bg-ios-bg rounded-full overflow-hidden">
                  <div className="h-full rounded-full bg-ios-bg animate-pulse" style={{ width: "30%" }} />
                </div>
              </div>
            ))}
          </div>
        ) : resultatCourant ? (
          <div className="space-y-4">
            {BARRES.map(({ label, color, getVal }) => {
              const pct = getVal(resultatCourant);
              const active = resultatCourant.verdict === (label === "Reel" ? "Réel" : "Faux");
              return (
                <div key={label}>
                  <div className="flex justify-between text-[12px] font-semibold mb-1.5">
                    <span className={active ? "text-ios-label" : "text-ios-label-tertiary"}>
                      {active && "● "}{label}
                    </span>
                    <span style={{ color: active ? color : undefined }}>{pct}%</span>
                  </div>
                  <div className="h-2 w-full bg-ios-bg rounded-full overflow-hidden">
                    <div className="h-full rounded-full transition-all duration-700"
                      style={{ width: `${pct}%`, backgroundColor: color, opacity: active ? 1 : 0.35 }} />
                  </div>
                </div>
              );
            })}
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center h-28 gap-2">
            <BarChart3 className="w-8 h-8 text-ios-label-tertiary/30" />
            <p className="text-[12px] text-ios-label-tertiary/60 text-center">Apres l&apos;analyse</p>
          </div>
        )}
      </div>

      {/* Modele utilise */}
      <div className="glass rounded-3xl p-5 shadow-glass">
        <h4 className="text-[12px] font-semibold text-ios-label-tertiary mb-4 flex items-center gap-2">
          <Cpu className="w-4 h-4" />
          Modele utilise
        </h4>
        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-10 rounded-xl flex items-center justify-center"
            style={{ backgroundColor: `${modele.couleur}15` }}>
            <Zap className="w-5 h-5" style={{ color: modele.couleur }} />
          </div>
          <div>
            <p className="text-[14px] font-semibold text-ios-label">{modele.court}</p>
            <p className="text-[11px] text-ios-label-tertiary">{modele.type}</p>
          </div>
        </div>
        <div className="grid grid-cols-2 gap-2">
          {[
            { label: "Precision", value: `${modele.precision.toFixed(1)}%`, icon: TrendingUp },
            { label: "Macro F1", value: `${modele.f1.toFixed(1)}%`, icon: BarChart3 },
          ].map(({ label, value, icon: Icon }) => (
            <div key={label} className="bg-ios-bg rounded-xl p-3">
              <div className="flex items-center gap-1.5 mb-1">
                <Icon className="w-3 h-3 text-ios-label-tertiary" />
                <p className="text-[10px] font-semibold text-ios-label-tertiary">{label}</p>
              </div>
              <p className="text-[16px] font-bold text-ios-label">{value}</p>
            </div>
          ))}
        </div>
        {modele.badge && (
          <p className="text-[11px] font-semibold mt-3 text-center" style={{ color: modele.couleur }}>
            {modele.badge}
          </p>
        )}
      </div>
    </div>
  );
}
