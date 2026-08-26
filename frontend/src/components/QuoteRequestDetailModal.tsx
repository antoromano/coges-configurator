import { formatCurrency } from "./PriceBreakdown";
import type { QuoteRequestOut, QuoteRequestStatus } from "../types";
import { buildLinesForFamily } from "../utils/breakdownLines";

interface QuoteRequestDetailModalProps {
  request: QuoteRequestOut;
  onClose: () => void;
  onStatusChange: (id: number, status: QuoteRequestStatus) => void;
  updating: boolean;
}

const familyLabels: Record<string, string> = {
  finestre: "Finestre",
  portoncini: "Portoncini",
  pergole: "Pergole",
};

function dimensionsLabel(productFamily: string, configuration: Record<string, unknown>): string {
  const width = configuration.width_mm as number | undefined;
  if (productFamily === "pergole") {
    return `${width} × ${configuration.depth_mm as number} mm (larghezza × sporgenza)`;
  }
  return `${width} × ${configuration.height_mm as number} mm (larghezza × altezza)`;
}

export default function QuoteRequestDetailModal({
  request,
  onClose,
  onStatusChange,
  updating,
}: QuoteRequestDetailModalProps) {
  const lines = buildLinesForFamily(request.product_family, request.breakdown);

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center overflow-y-auto bg-ink/50 p-6" onClick={onClose}>
      <div
        className="mt-6 w-full max-w-lg border border-line bg-white p-6"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="mb-4 flex items-start justify-between gap-4">
          <div>
            <span className="text-xs uppercase tracking-wide text-ink-faint">
              Richiesta n. {request.id} · {familyLabels[request.product_family] ?? request.product_family}
            </span>
            <h2 className="font-display text-2xl text-ink">{formatCurrency(request.final_price)}</h2>
          </div>
          <button type="button" onClick={onClose} className="text-xs uppercase tracking-wide text-ink-soft hover:text-ink">
            Chiudi ✕
          </button>
        </div>

        <div className="mb-5 grid grid-cols-2 gap-x-4 gap-y-1 border border-line bg-paper p-3 text-sm">
          <div className="col-span-2 text-xs font-medium uppercase tracking-wide text-ink-soft">Cliente</div>
          <div className="text-ink">{request.customer_name}</div>
          <div className="text-ink-soft">{new Date(request.created_at).toLocaleString("it-IT")}</div>
          <div className="text-ink-soft">{request.customer_email}</div>
          <div className="text-ink-soft">{request.customer_phone}</div>
          {request.customer_note && (
            <div className="col-span-2 mt-1 text-ink-soft">Nota: {request.customer_note}</div>
          )}
        </div>

        <div className="mb-5 text-sm">
          <div className="mb-1 text-xs font-medium uppercase tracking-wide text-ink-soft">Dimensioni</div>
          <div className="text-ink">{dimensionsLabel(request.product_family, request.configuration)}</div>
        </div>

        <div className="mb-5">
          <div className="mb-1 text-xs font-medium uppercase tracking-wide text-ink-soft">
            Dettaglio calcolo (verifica correttezza)
          </div>
          <dl className="flex flex-col gap-1 border-t border-line pt-2 text-sm">
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
        </div>

        <div className="flex gap-2">
          <button
            type="button"
            disabled={updating || request.status === "confermato"}
            onClick={() => onStatusChange(request.id, "confermato")}
            className="flex-1 border border-ink bg-ink py-2 text-xs uppercase tracking-wide text-paper hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-40"
          >
            Conferma preventivo
          </button>
          <button
            type="button"
            disabled={updating || request.status === "rifiutato"}
            onClick={() => onStatusChange(request.id, "rifiutato")}
            className="flex-1 border border-line py-2 text-xs uppercase tracking-wide text-ink-soft hover:border-ink disabled:cursor-not-allowed disabled:opacity-40"
          >
            Rifiuta
          </button>
        </div>
      </div>
    </div>
  );
}
