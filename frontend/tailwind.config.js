/** LAYOVER design system — deep navy base, lavender accents, warm highlights. */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        // Base
        midnight: {
          50: "#f4f4fb",
          100: "#e6e6f5",
          200: "#c9c9ea",
          300: "#a3a3d8",
          400: "#7b7cc0",
          500: "#585aa6",
          600: "#454785",
          700: "#37396b",
          800: "#282a50",
          900: "#1b1c3a",
          950: "#12132b",
        },
        // Accents
        lavender: {
          100: "#f0edfc",
          200: "#ddd6f3",
          300: "#c4b8e8",
          400: "#a78fdd",
          500: "#8a6dd1",
          600: "#6f53b5",
        },
        // Warm highlights
        sunset: {
          300: "#ffd6a0",
          400: "#ffb86b",
          500: "#ff9b3f",
          600: "#f2851f",
        },
      },
      fontFamily: {
        display: ["Sora", "system-ui", "sans-serif"],
        body: ["Inter", "system-ui", "sans-serif"],
      },
      borderRadius: {
        xl: "1rem",
        "2xl": "1.5rem",
      },
      boxShadow: {
        card: "0 4px 24px -4px rgb(18 19 43 / 0.25)",
        glow: "0 0 32px -8px rgb(167 143 221 / 0.55)",
      },
      keyframes: {
        "fade-up": {
          "0%": { opacity: "0", transform: "translateY(12px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        shimmer: {
          "0%": { backgroundPosition: "-200% 0" },
          "100%": { backgroundPosition: "200% 0" },
        },
      },
      animation: {
        "fade-up": "fade-up 0.5s ease-out both",
        shimmer: "shimmer 2.2s linear infinite",
      },
    },
  },
  plugins: [],
};
