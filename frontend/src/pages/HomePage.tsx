import { useEffect, useState } from "react";

import { ApiError, fetchProductFamilies } from "../services/api";
import type { ProductFamily } from "../types";

interface HomePageProps {
  onSelect: (slug: string) => void;
}

export default function HomePage({ onSelect }: HomePageProps) {
  const [families, setFamilies] = useState<ProductFamily[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchProductFamilies()
      .then(setFamilies)
      .catch((err: unknown) => {
        setError(err instanceof ApiError ? err.message : "Errore di connessione al backend");
      });
  }, []);

  return (
    <div className="mx-auto max-w-4xl p-6">
      <h1 className="mb-1 font-display text-4xl text-ink">Configuratore Coges Infissi</h1>
      <p className="mb-8 text-sm text-ink-soft">
        Prototipo con dati fittizi, prezzi indicativi. Scegli una categoria per iniziare.
      </p>

      {error && (
        <div className="border border-red-300 bg-red-50 p-4 text-red-700">
          Impossibile caricare le categorie prodotto dal backend: {error}. Verifica che il backend
          sia avviato su {import.meta.env.VITE_API_URL}.
        </div>
      )}

      {!error && !families && <p className="text-ink-soft">Caricamento categorie...</p>}

      {families && (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
          {families.map((family) => (
            <button
              key={family.slug}
              type="button"
              onClick={() => onSelect(family.slug)}
              className="flex flex-col items-start gap-2 border border-line bg-white p-5 text-left transition-colors hover:border-ink"
            >
              <span className="font-display text-xl text-ink">{family.name}</span>
              <span className="text-sm text-ink-soft">{family.description}</span>
              <span className="mt-2 text-xs uppercase tracking-wide text-ink">Configura &rarr;</span>
            </button>
          ))}
        </div>
      )}

      <button
        type="button"
        onClick={() => onSelect("staff")}
        className="mt-16 text-xs uppercase tracking-wide text-ink-faint hover:text-ink-soft"
      >
        Area riservata Coges
      </button>
    </div>
  );
}
