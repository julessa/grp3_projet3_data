"use client";

import { useAnalyse } from "@/context/AnalysisContext";
import ResultCard from "./ResultCard";
import SidePanels from "./SidePanels";
import { User, AlertTriangle, Brain } from "lucide-react";

function detecterIndicateursBiais(text: string): { label: string; type: "warning" | "info"; detail: string }[] {
  const lower = text.toLowerCase();
  const indicators: { label: string; type: "warning" | "info"; detail: string }[] = [];

  const superlatifs = ["meilleur", "pire", "plus", "moins", "jamais", "toujours", "tous", "aucun", "chaque", "personne", "tout le monde", "record", "historique", "best", "worst", "greatest", "lowest", "highest", "most", "never", "always", "all", "none", "every", "no one"];
  const trouves = superlatifs.filter(s => lower.includes(s));
  if (trouves.length > 0) {
    indicators.push({ label: "Langage absolu", type: "warning", detail: `Utilise des termes absolus : ${trouves.slice(0, 3).join(", ")}` });
  }

  const emotionnel = ["incroyable", "choquant", "devastateur", "extraordinaire", "terrible", "horrible", "fantastique", "invraisemblable", "scandaleux", "catastrophique", "miracle", "desastre", "urgent", "exclusif", "incredible", "shocking", "amazing", "unbelievable", "outrageous", "breaking"];
  const trouvesEmo = emotionnel.filter(s => lower.includes(s));
  if (trouvesEmo.length > 0) {
    indicators.push({ label: "Ton emotionnel", type: "warning", detail: `Formulation sensationnelle : ${trouvesEmo.slice(0, 3).join(", ")}` });
  }

  if (/\b(millions?|milliards?|milliers?|millions?|billions?|thousands?)\b/.test(lower) && !/\b\d+\s*(million|milliard|millier)/.test(lower)) {
    indicators.push({ label: "Quantites vagues", type: "info", detail: "Utilise des chiffres arrondis sans precision" });
  }

  if (/\b(des sources|on dit que|beaucoup pensent|les experts|des etudes montrent|les scientifiques confirment|selon des recherches|sources say|experts say|studies show)\b/i.test(text)) {
    indicators.push({ label: "Sources non attribuees", type: "warning", detail: "Reference des sources ou etudes non identifiees" });
  }

  if (/\b\d+(\.\d+)?%/.test(text) || /\b(augmente|baisse|progresse|recule|chute|hausse|grew|dropped|increased|decreased)\b/i.test(text)) {
    indicators.push({ label: "Affirmation statistique", type: "info", detail: "Contient des chiffres a verifier aupres de sources officielles" });
  }

  if (/\b(a cause de|grace a|en raison de|provoque par|du a|a conduit a|responsable de|because of|caused by|thanks to|due to)\b/i.test(text)) {
    indicators.push({ label: "Attribution causale", type: "info", detail: "Etablit un lien de cause a effet — verifier si le lien est fonde" });
  }

  if (indicators.length === 0) {
    indicators.push({ label: "Ton neutre", type: "info", detail: "Aucun indicateur de biais fort detecte dans le langage" });
  }

  return indicators;
}

export default function AnalysisResults() {
  const { resultatCourant, chargement } = useAnalyse();
  const r = resultatCourant;

  const indicateurs = r ? detecterIndicateursBiais(r.declaration) : [];

  return (
    <div id="resultats" className="grid grid-cols-12 gap-4">
      <ResultCard />
      <SidePanels />

      {(r || chargement) && (
        <div className="col-span-12 grid grid-cols-1 md:grid-cols-3 gap-4 animate-slide-up">
          {/* Infos orateur */}
          <div className="glass rounded-3xl p-5 shadow-glass">
            <div className="w-9 h-9 rounded-xl bg-ios-blue/10 flex items-center justify-center mb-3">
              <User className="w-4 h-4 text-ios-blue" />
            </div>
            <h5 className="text-[14px] font-semibold text-ios-label mb-2">Infos orateur</h5>
            {chargement ? (
              <div className="space-y-2">
                {[80, 60, 40].map(w => (
                  <div key={w} className="h-2.5 rounded-full bg-ios-bg animate-pulse" style={{ width: `${w}%` }} />
                ))}
              </div>
            ) : r && (
              <>
                <p className="text-[13px] text-ios-label-secondary mb-2">
                  <span className="font-semibold text-ios-label">{r.orateur}</span>
                  {r.parti !== "Non renseigne" && r.parti !== "Non renseigné" && (
                    <> · <span className="text-ios-blue">{r.parti}</span></>
                  )}
                </p>
                {r.sujet !== "Politique generale" && r.sujet !== "Politique générale" && (
                  <p className="text-[12px] text-ios-label-tertiary">Sujet : {r.sujet}</p>
                )}
                <p className="text-[10px] text-ios-label-tertiary mt-3">Analyse du {r.date}</p>
              </>
            )}
          </div>

          {/* Indicateurs de biais — adaptatif au texte */}
          <div className="glass rounded-3xl p-5 shadow-glass">
            <div className="w-9 h-9 rounded-xl bg-ios-orange/10 flex items-center justify-center mb-3">
              <AlertTriangle className="w-4 h-4 text-ios-orange" />
            </div>
            <h5 className="text-[14px] font-semibold text-ios-label mb-2">Indicateurs de biais</h5>
            {chargement ? (
              <div className="space-y-2">
                {[90, 70, 50].map(w => (
                  <div key={w} className="h-2.5 rounded-full bg-ios-bg animate-pulse" style={{ width: `${w}%` }} />
                ))}
              </div>
            ) : r && (
              <div className="space-y-2.5">
                {indicateurs.map(({ label, type, detail }) => (
                  <div key={label} className="flex items-start gap-2">
                    <span className={`w-1.5 h-1.5 rounded-full mt-1.5 shrink-0 ${
                      type === "warning" ? "bg-ios-orange" : "bg-ios-blue"
                    }`} />
                    <div>
                      <p className={`text-[12px] font-semibold ${
                        type === "warning" ? "text-ios-orange" : "text-ios-blue"
                      }`}>{label}</p>
                      <p className="text-[11px] text-ios-label-tertiary leading-snug">{detail}</p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Facteurs cles */}
          <div className="glass rounded-3xl p-5 shadow-glass">
            <div className="w-9 h-9 rounded-xl bg-ios-green/10 flex items-center justify-center mb-3">
              <Brain className="w-4 h-4 text-ios-green" />
            </div>
            <h5 className="text-[14px] font-semibold text-ios-label mb-2">Facteurs cles</h5>
            <p className="text-[12px] text-ios-label-tertiary mb-3">
              Tokens TF-IDF x coefficient du modele (+ = Reel, - = Faux).
            </p>
            {chargement ? (
              <div className="space-y-2">
                {[90, 70, 55, 40].map(w => (
                  <div key={w} className="h-2.5 rounded-full bg-ios-bg animate-pulse" style={{ width: `${w}%` }} />
                ))}
              </div>
            ) : r && r.facteursCles.map(({ mot, poids }) => {
              const positif = poids >= 0;
              const color = positif ? "#007AFF" : "#FF3B30";
              return (
                <div key={mot} className="flex items-center gap-2 mb-2">
                  <span className="text-[11px] font-mono font-semibold text-ios-label w-20 truncate">{mot}</span>
                  <div className="flex-1 h-1.5 bg-ios-bg rounded-full overflow-hidden">
                    <div className="h-full rounded-full"
                      style={{ width: `${Math.min(Math.abs(poids) * 200, 100)}%`, backgroundColor: color }} />
                  </div>
                  <span className="text-[10px] font-bold w-12 text-right" style={{ color }}>
                    {poids > 0 ? "+" : ""}{poids.toFixed(3)}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
