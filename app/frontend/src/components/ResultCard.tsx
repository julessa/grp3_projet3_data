"use client";

import { useAnalyse } from "@/context/AnalysisContext";
import { VERDICT_CONFIG } from "@/lib/predict";
import { ShieldCheck, ShieldAlert, AlertCircle, User, Building2, Tag, Calendar, Loader2 } from "lucide-react";

export default function ResultCard() {
  const { resultatCourant, chargement, erreur } = useAnalyse();

  if (erreur) {
    return (
      <div className="col-span-12 lg:col-span-8 glass rounded-3xl p-8 flex flex-col items-center justify-center gap-4 min-h-[280px] shadow-glass border-ios-red/20">
        <div className="w-14 h-14 rounded-2xl bg-ios-red/10 flex items-center justify-center">
          <AlertCircle className="w-7 h-7 text-ios-red" />
        </div>
        <div className="text-center">
          <p className="font-semibold text-ios-red mb-1">Erreur d&apos;analyse</p>
          <p className="text-[13px] text-ios-label-tertiary max-w-sm">{erreur}</p>
        </div>
      </div>
    );
  }

  if (chargement) {
    return (
      <div className="col-span-12 lg:col-span-8 glass rounded-3xl p-8 flex flex-col items-center justify-center gap-5 min-h-[280px] shadow-glass">
        <div className="w-14 h-14 rounded-2xl bg-ios-blue/10 flex items-center justify-center">
          <Loader2 className="w-7 h-7 text-ios-blue animate-spin" />
        </div>
        <div className="text-center">
          <p className="font-semibold text-ios-label mb-1">Analyse en cours...</p>
          <p className="text-[13px] text-ios-label-tertiary">Le modele classifie la declaration</p>
        </div>
        <div className="w-48 h-1.5 bg-ios-bg rounded-full overflow-hidden">
          <div className="h-full rounded-full bg-ios-blue animate-pulse" style={{ width: "65%" }} />
        </div>
      </div>
    );
  }

  if (!resultatCourant) {
    return (
      <div className="col-span-12 lg:col-span-8 glass rounded-3xl p-8 flex flex-col items-center justify-center gap-4 min-h-[280px] shadow-glass border-dashed border-2 border-ios-border">
        <div className="w-14 h-14 rounded-2xl bg-ios-bg flex items-center justify-center">
          <ShieldCheck className="w-7 h-7 text-ios-label-tertiary" />
        </div>
        <div className="text-center">
          <p className="font-semibold text-ios-label-secondary mb-1">Aucune analyse en cours</p>
          <p className="text-[13px] text-ios-label-tertiary max-w-xs">
            Saisissez une declaration ci-dessus et cliquez sur Analyser
          </p>
        </div>
      </div>
    );
  }

  const r = resultatCourant;
  const cfg = VERDICT_CONFIG[r.verdict];
  const isReal = r.verdict === "Réel";
  const VerdictIcon = isReal ? ShieldCheck : ShieldAlert;

  return (
    <div className="col-span-12 lg:col-span-8 glass rounded-3xl p-7 shadow-glass-lg animate-slide-up">
      {/* En-tete */}
      <div className="flex justify-between items-start mb-6">
        <div className="flex-1 min-w-0 pr-6">
          <span className="inline-flex items-center gap-1.5 text-[11px] font-semibold px-3 py-1 rounded-full mb-4"
            style={{ color: cfg.couleur, background: cfg.fond }}>
            <VerdictIcon className="w-3 h-3" />
            Analyse terminee
          </span>
          <blockquote className="text-xl font-semibold text-ios-label leading-relaxed mb-3">
            &ldquo;{r.declaration}&rdquo;
          </blockquote>
          <div className="flex items-center gap-4 text-[12px] text-ios-label-tertiary flex-wrap">
            <span className="flex items-center gap-1"><User className="w-3 h-3" />{r.orateur}</span>
            <span className="flex items-center gap-1"><Building2 className="w-3 h-3" />{r.parti}</span>
            <span className="flex items-center gap-1"><Tag className="w-3 h-3" />{r.sujet}</span>
            <span className="flex items-center gap-1"><Calendar className="w-3 h-3" />{r.date}</span>
          </div>
        </div>

        {/* Badge verdict */}
        <div className="flex flex-col items-end shrink-0">
          <div className="text-4xl font-bold tracking-tight" style={{ color: cfg.couleur }}>
            {r.confiance}<span className="text-lg text-ios-label-tertiary">%</span>
          </div>
          <span className="text-[12px] font-bold mt-1 px-3 py-1 rounded-full"
            style={{ color: cfg.couleur, background: cfg.fond }}>
            {r.verdict}
          </span>
          <p className="text-[11px] text-ios-label-tertiary mt-1.5">{r.modele}</p>
        </div>
      </div>

      {/* Barre de probabilite */}
      <div className="mb-6">
        <div className="flex justify-between text-[12px] font-semibold mb-2">
          <span className="text-ios-red">Faux — {r.probaFaux}%</span>
          <span className="text-ios-green">Reel — {r.probaReel}%</span>
        </div>
        <div className="h-2.5 w-full bg-ios-bg rounded-full overflow-hidden">
          <div className="h-full flex rounded-full overflow-hidden">
            <div className="h-full transition-all duration-700 bg-ios-red" style={{ width: `${r.probaFaux}%` }} />
            <div className="h-full transition-all duration-700 bg-ios-green" style={{ width: `${r.probaReel}%` }} />
          </div>
        </div>
      </div>

      {/* Grille stats */}
      <div className="grid grid-cols-3 gap-3">
        {[
          { label: "Verdict", value: r.verdict, color: cfg.couleur, sub: "Classification binaire" },
          { label: "Confiance", value: `${r.confiance}%`, color: "#007AFF", sub: r.modele },
          { label: "Sujet", value: r.sujet, color: "#5856D6", sub: "Categorie" },
        ].map(({ label, value, color, sub }) => (
          <div key={label} className="bg-ios-bg rounded-2xl p-4" style={{ borderLeft: `3px solid ${color}` }}>
            <p className="text-[11px] font-semibold text-ios-label-tertiary mb-1">{label}</p>
            <p className="text-[16px] font-bold truncate" style={{ color }}>{value}</p>
            <p className="text-[11px] text-ios-label-tertiary mt-0.5">{sub}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
