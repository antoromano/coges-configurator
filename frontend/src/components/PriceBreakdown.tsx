export interface BreakdownLine {
  label: string;
  value: string;
  bold?: boolean;
}

interface PriceBreakdownProps {
  finalPrice: number | null;
  lines: BreakdownLine[];
  loading: boolean;
  error: string | null;
}

const currencyFormatter = new Intl.NumberFormat("it-IT", {
  style: "currency",
  currency: "EUR",
});

export function formatCurrency(value: number): string {
  return currencyFormatter.format(value);
}

// Componente generico: ogni pagina configuratore costruisce le righe del
// breakdown dalla forma specifica della propria risposta API (che varia per
// famiglia prodotto), questo componente si occupa solo della presentazione.
export default function PriceBreakdown({ finalPrice, lines, loading, error }: PriceBreakdownProps) {
  return (
    <div className="border border-line bg-white p-4">
      <h2 className="mb-2 text-xs font-medium uppercase tracking-wide text-ink-soft">Prezzo stimato</h2>

      {error && (
        <div className="border border-red-300 bg-red-50 p-3 text-sm text-red-700">
          Impossibile calcolare il prezzo: {error}
        </div>
      )}

      {!error && (
        <>
          <div className={`font-display text-4xl text-ink ${loading ? "opacity-40" : ""}`}>
            {finalPrice !== null ? formatCurrency(finalPrice) : "—"}
          </div>
          {loading && <p className="mt-1 text-xs text-ink-faint">Calcolo in corso...</p>}
          <p className="mt-1 text-xs text-ink-faint">
            Stima indicativa, non vincolante. Il prezzo definitivo sarà confermato da Coges.
          </p>

          {lines.length > 0 && (
            <dl className="mt-4 flex flex-col gap-1 border-t border-line pt-3 text-sm">
              {lines.map((line, index) => (
                <div
                  key={index}
                  className={`flex justify-between ${line.bold ? "font-semibold text-ink" : "text-ink-soft"}`}
                >
                  <dt>{line.label}</dt>
                  <dd>{line.value}</dd>
                </div>
              ))}
            </dl>
          )}
        </>
      )}
    </div>
  );
}
