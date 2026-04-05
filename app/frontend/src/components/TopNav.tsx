"use client";

import { usePathname } from "next/navigation";
import { useTheme } from "@/context/ThemeContext";
import { Sun, Moon } from "lucide-react";

const PAGE_TITLES: Record<string, string> = {
  "/":             "Tableau de bord",
  "/historique":   "Historique",
  "/statistiques": "Statistiques",
  "/biais":        "Analyse des biais",
  "/parametres":   "Parametres",
};

export default function TopNav() {
  const pathname = usePathname();
  const { theme, toggleTheme } = useTheme();
  const title = PAGE_TITLES[pathname] ?? "The Sentinel";

  return (
    <header className="glass sticky top-0 z-50 flex justify-between items-center w-full px-8 py-4">
      <div>
        <h1 className="text-xl font-bold text-ios-label tracking-tight">{title}</h1>
        <p className="text-[12px] text-ios-label-tertiary">
          Detection de Fake News par IA
        </p>
      </div>

      <div className="flex items-center gap-2">
        <button
          type="button"
          onClick={toggleTheme}
          className="w-9 h-9 flex items-center justify-center rounded-xl text-ios-label-tertiary hover:bg-ios-card-hover transition-all"
          title={theme === "light" ? "Passer en mode sombre" : "Passer en mode clair"}
        >
          {theme === "light" ? <Moon className="w-[18px] h-[18px]" /> : <Sun className="w-[18px] h-[18px]" />}
        </button>
      </div>
    </header>
  );
}
