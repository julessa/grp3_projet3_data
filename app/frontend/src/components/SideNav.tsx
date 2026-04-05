"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAnalyse } from "@/context/AnalysisContext";
import {
  Shield, Search, History, BarChart3, Scale, Settings, Plus,
} from "lucide-react";

const NAV_LINKS = [
  { href: "/",             icon: Search,    label: "Analyser"     },
  { href: "/historique",   icon: History,   label: "Historique"   },
  { href: "/statistiques", icon: BarChart3, label: "Statistiques" },
  { href: "/biais",        icon: Scale,     label: "Biais"       },
  { href: "/parametres",   icon: Settings,  label: "Parametres"  },
];

export default function SideNav() {
  const pathname = usePathname();
  const { historique, effacerResultatCourant } = useAnalyse();

  return (
    <aside className="glass-sidebar h-screen w-[260px] fixed left-0 top-0 z-[60] flex flex-col py-6 px-4">
      {/* Logo */}
      <div className="flex items-center gap-3 px-3 mb-8">
        <div className="w-9 h-9 rounded-xl bg-ios-blue flex items-center justify-center">
          <Shield className="w-5 h-5 text-white" strokeWidth={2.5} />
        </div>
        <div>
          <h1 className="text-[15px] font-bold text-ios-label tracking-tight leading-none">
            The Sentinel
          </h1>
          <p className="text-[10px] text-ios-label-tertiary mt-0.5">Detection de Fake News</p>
        </div>
      </div>

      {/* Bouton nouvelle analyse */}
      <Link
        href="/"
        onClick={effacerResultatCourant}
        className="flex items-center justify-center gap-2 mx-2 mb-6 py-3 rounded-2xl bg-ios-blue text-white text-[13px] font-semibold transition-all hover:brightness-110 active:scale-[0.98] shadow-ios-md"
      >
        <Plus className="w-4 h-4" strokeWidth={2.5} />
        Nouvelle analyse
      </Link>

      {/* Navigation */}
      <nav className="flex-1 flex flex-col gap-0.5 px-1">
        {NAV_LINKS.map(({ href, icon: Icon, label }) => {
          const active = pathname === href;
          return (
            <Link
              key={href}
              href={href}
              className={`flex items-center gap-3 px-3 py-2.5 rounded-xl text-[13px] font-medium transition-all duration-200 ${
                active
                  ? "bg-ios-blue/10 text-ios-blue"
                  : "text-ios-label-secondary hover:bg-ios-card-hover"
              }`}
            >
              <Icon className="w-[18px] h-[18px]" strokeWidth={active ? 2.5 : 2} />
              {label}
              {href === "/historique" && historique.length > 0 && (
                <span className="ml-auto text-[10px] bg-ios-blue text-white rounded-full min-w-[20px] h-5 flex items-center justify-center font-bold px-1.5">
                  {historique.length}
                </span>
              )}
            </Link>
          );
        })}
      </nav>

      {/* Version */}
      <div className="mt-auto px-3 pt-4 border-t border-ios-border">
        <p className="text-[10px] text-ios-label-tertiary">The Sentinel v2.0</p>
        <p className="text-[10px] text-ios-label-tertiary">Epitech Digital School</p>
      </div>
    </aside>
  );
}
