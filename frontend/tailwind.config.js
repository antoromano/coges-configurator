/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        // Font reali del sito cogesinfissi.it: Belleza per i titoli
        // (carattere editoriale), Roboto per testo/etichette.
        display: ["Belleza", "ui-sans-serif", "sans-serif"],
        sans: ["Roboto", "ui-sans-serif", "system-ui", "sans-serif"],
      },
      colors: {
        // Palette neutra ripresa dal sito Coges: nessun colore acceso,
        // solo bianco/nero e grigi. "ink" fa da accento (stato selezionato)
        // al posto del blu, per restare fedeli all'identità monocroma.
        ink: {
          DEFAULT: "#1A1A1A",
          soft: "#7A7A7A",
          faint: "#B0B0AC",
        },
        paper: "#FAFAF8",
        line: "#E2E0D8",
      },
      borderRadius: {
        none: "0px",
      },
    },
  },
  plugins: [],
};
