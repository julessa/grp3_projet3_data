"use client";

import { createContext, useContext, useState, useEffect, useCallback, type ReactNode } from "react";

type Theme = "light" | "dark";

interface ContexteTheme {
  theme: Theme;
  toggleTheme: () => void;
}

const ContexteTheme = createContext<ContexteTheme>({ theme: "light", toggleTheme: () => {} });

function appliquerTheme(t: Theme) {
  const html = document.documentElement;
  if (t === "dark") {
    html.classList.add("dark");
  } else {
    html.classList.remove("dark");
  }
  localStorage.setItem("sentinel_theme", t);
}

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<Theme>("light");

  useEffect(() => {
    const saved = localStorage.getItem("sentinel_theme") as Theme | null;
    const initial = saved === "dark" ? "dark" : "light";
    setTheme(initial);
    appliquerTheme(initial);
  }, []);

  const toggleTheme = useCallback(() => {
    setTheme((prev) => {
      const next = prev === "light" ? "dark" : "light";
      appliquerTheme(next);
      return next;
    });
  }, []);

  return (
    <ContexteTheme.Provider value={{ theme, toggleTheme }}>
      {children}
    </ContexteTheme.Provider>
  );
}

export function useTheme(): ContexteTheme {
  return useContext(ContexteTheme);
}
