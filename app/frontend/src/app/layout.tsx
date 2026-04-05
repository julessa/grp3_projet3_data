import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { AnalyseProvider } from "@/context/AnalysisContext";
import { ThemeProvider } from "@/context/ThemeContext";

const inter = Inter({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
  variable: "--font-inter",
  display: "swap",
});

export const metadata: Metadata = {
  title: "The Sentinel | Fake News Detection",
  description: "Plateforme de detection automatique de fake news politiques par IA",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="fr" translate="no" className={inter.variable} suppressHydrationWarning>
      <head>
        <script
          dangerouslySetInnerHTML={{
            __html: `try{var t=localStorage.getItem('sentinel_theme');if(t==='dark'){document.documentElement.classList.add('dark')}}catch(e){}`,
          }}
        />
      </head>
      <body className="font-sans antialiased">
        <ThemeProvider>
          <AnalyseProvider>
            {children}
          </AnalyseProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
