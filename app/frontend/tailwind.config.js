/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: "class",
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        ios: {
          bg:          "var(--ios-bg)",
          card:        "var(--ios-card)",
          "card-hover":"var(--ios-card-hover)",
          sidebar:     "var(--ios-sidebar)",
          border:      "var(--ios-border)",
          "border-strong": "var(--ios-border-strong)",
          label:       "var(--ios-label)",
          "label-secondary": "var(--ios-label-secondary)",
          "label-tertiary":  "var(--ios-label-tertiary)",
          blue:        "#007AFF",
          green:       "#34C759",
          red:         "#FF3B30",
          orange:      "#FF9500",
          yellow:      "#FFCC00",
          purple:      "#AF52DE",
          pink:        "#FF2D55",
          teal:        "#5AC8FA",
          indigo:      "#5856D6",
        },
      },
      fontFamily: {
        sans: ["var(--font-inter)", "SF Pro Display", "-apple-system", "BlinkMacSystemFont", "sans-serif"],
      },
      borderRadius: {
        "2xl": "1rem",
        "3xl": "1.25rem",
        "4xl": "1.5rem",
      },
      boxShadow: {
        "glass":  "0 2px 20px rgba(0, 0, 0, 0.04), 0 0 0 1px var(--ios-border)",
        "glass-lg": "0 8px 40px rgba(0, 0, 0, 0.06), 0 0 0 1px var(--ios-border)",
        "glass-xl": "0 16px 60px rgba(0, 0, 0, 0.08), 0 0 0 1px var(--ios-border)",
        "ios-sm": "0 1px 3px rgba(0, 0, 0, 0.04)",
        "ios-md": "0 4px 16px rgba(0, 0, 0, 0.06)",
        "ios-lg": "0 8px 32px rgba(0, 0, 0, 0.08)",
      },
      backdropBlur: {
        glass: "20px",
        "glass-heavy": "40px",
      },
    },
  },
  plugins: [],
};
