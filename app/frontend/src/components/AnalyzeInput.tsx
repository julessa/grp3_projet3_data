"use client";

import { useState } from "react";
import { useAnalyse } from "@/context/AnalysisContext";
import { Search, FileText, Layers, ChevronRight } from "lucide-react";

type Tab = "declaration" | "contexte";

const EXEMPLES = [
  "Le president a annonce une baisse d'impots de 50% pour tous les citoyens.",
  "Des scientifiques confirment que le changement climatique a ete totalement inverse.",
  "Le taux de chomage a atteint son plus bas niveau depuis 50 ans.",
  "Une nouvelle etude montre que les vaccins causent plus de mal que de bien.",
  "Le gouvernement prevoit d'investir 2 milliards dans les energies renouvelables.",
];

export default function AnalyzeInput() {
  const { analyser, chargement } = useAnalyse();
  const [tab, setTab] = useState<Tab>("declaration");
  const [declaration, setDeclaration] = useState("");
  const [orateur, setOrateur] = useState("");
  const [parti, setParti] = useState("");
  const [sujet, setSujet] = useState("");

  async function handleSubmit() {
    if (!declaration.trim() || chargement) return;
    await analyser({ declaration, orateur, parti, sujet });
    setTimeout(() => {
      document.getElementById("resultats")?.scrollIntoView({ behavior: "smooth" });
    }, 200);
  }

  return (
    <section className="mb-10 animate-slide-up">
      <div className="mb-6">
        <h2 className="text-3xl font-bold text-ios-label tracking-tight mb-1">
          Verifier une declaration
        </h2>
        <p className="text-[14px] text-ios-label-tertiary">
          Saisissez une declaration politique pour analyser sa veracite par IA.
        </p>
      </div>

      <div className="glass rounded-3xl p-6 shadow-glass-lg">
        {/* Onglets */}
        <div className="flex gap-1 p-1 bg-ios-bg rounded-xl w-fit mb-5">
          {([
            { id: "declaration" as Tab, label: "Declaration",   icon: FileText },
            { id: "contexte" as Tab,    label: "Avec contexte", icon: Layers },
          ]).map(({ id, label, icon: Icon }) => (
            <button key={id} type="button" onClick={() => setTab(id)}
              className={`flex items-center gap-1.5 px-4 py-2 rounded-lg text-[13px] font-medium transition-all ${
                tab === id
                  ? "bg-white dark:bg-white/10 text-ios-blue shadow-ios-sm"
                  : "text-ios-label-tertiary hover:text-ios-label-secondary"
              }`}
            >
              <Icon className="w-3.5 h-3.5" />
              {label}
            </button>
          ))}
        </div>

        {/* Saisie */}
        <div className="flex gap-3 mb-4">
          <div className="flex-1">
            <textarea
              value={declaration}
              onChange={(e) => setDeclaration(e.target.value)}
              onKeyDown={(e) => { if (e.key === "Enter" && e.ctrlKey) handleSubmit(); }}
              placeholder='Ex : "L&#39;economie a progresse de 10% ce trimestre, un record historique."'
              rows={3}
              className="w-full bg-ios-bg rounded-2xl py-4 px-5 text-[15px] text-ios-label placeholder:text-ios-label-tertiary/40 border border-ios-border focus:border-ios-blue/40 focus:ring-2 focus:ring-ios-blue/10 transition-all outline-none resize-none"
            />
            <p className="text-[11px] text-ios-label-tertiary mt-1.5 px-1">Ctrl + Entree pour analyser</p>
          </div>

          <button
            type="button"
            onClick={handleSubmit}
            disabled={!declaration.trim() || chargement}
            className="flex flex-col items-center justify-center gap-2 px-8 rounded-2xl bg-ios-blue text-white text-[13px] font-semibold transition-all hover:brightness-110 active:scale-[0.97] shrink-0 disabled:opacity-40 disabled:cursor-not-allowed shadow-ios-md"
            style={{ minHeight: "96px", minWidth: "100px" }}
          >
            {chargement ? (
              <>
                <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                Analyse...
              </>
            ) : (
              <>
                <Search className="w-5 h-5" strokeWidth={2.5} />
                Analyser
              </>
            )}
          </button>
        </div>

        {/* Champs contexte */}
        {tab === "contexte" && (
          <div className="grid grid-cols-3 gap-3 mb-4 animate-fade-in">
            <div>
              <label className="text-[11px] font-semibold text-ios-label-tertiary mb-1.5 block">Orateur</label>
              <input type="text" value={orateur} onChange={(e) => setOrateur(e.target.value)}
                placeholder="Ex : Joe Biden"
                className="w-full bg-ios-bg rounded-xl py-2.5 px-4 text-[13px] text-ios-label placeholder:text-ios-label-tertiary/40 outline-none border border-ios-border focus:border-ios-blue/40 focus:ring-2 focus:ring-ios-blue/10 transition-all"
              />
            </div>
            <div>
              <label className="text-[11px] font-semibold text-ios-label-tertiary mb-1.5 block">Parti / Source</label>
              <input type="text" value={parti} onChange={(e) => setParti(e.target.value)}
                placeholder="Ex : Democrate, Reuters..."
                className="w-full bg-ios-bg rounded-xl py-2.5 px-4 text-[13px] text-ios-label placeholder:text-ios-label-tertiary/40 outline-none border border-ios-border focus:border-ios-blue/40 focus:ring-2 focus:ring-ios-blue/10 transition-all"
              />
            </div>
            <div>
              <label className="text-[11px] font-semibold text-ios-label-tertiary mb-1.5 block">Sujet</label>
              <input type="text" value={sujet} onChange={(e) => setSujet(e.target.value)}
                placeholder="Ex : Economie, Sante..."
                className="w-full bg-ios-bg rounded-xl py-2.5 px-4 text-[13px] text-ios-label placeholder:text-ios-label-tertiary/40 outline-none border border-ios-border focus:border-ios-blue/40 focus:ring-2 focus:ring-ios-blue/10 transition-all"
              />
            </div>
          </div>
        )}

        {/* Exemples rapides */}
        <div className="flex flex-wrap gap-2 items-center">
          <span className="text-[11px] text-ios-label-tertiary font-medium">Essayer :</span>
          {EXEMPLES.map((ex) => (
            <button key={ex} type="button"
              onClick={() => { setDeclaration(ex); setTab("declaration"); }}
              className="flex items-center gap-1 text-[11px] text-ios-blue/80 px-3 py-1.5 rounded-full bg-ios-blue/5 hover:bg-ios-blue/10 transition-all truncate max-w-[300px]"
            >
              <ChevronRight className="w-3 h-3 shrink-0" />
              {ex}
            </button>
          ))}
        </div>
      </div>
    </section>
  );
}
