import { useState } from "react";

import BackToHomeLink from "../components/BackToHomeLink";
import QuoteRequestDetailModal from "../components/QuoteRequestDetailModal";
import { ApiError, fetchQuoteRequests, updateQuoteRequestStatus } from "../services/api";
import type { QuoteRequestOut, QuoteRequestStatus } from "../types";

interface StaffQuoteRequestsProps {
  onBack: () => void;
}

const familyLabels: Record<string, string> = {
  finestre: "Finestre",
  portoncini: "Portoncini",
  pergole: "Pergole",
};

const statusLabels: Record<QuoteRequestStatus, string> = {
  in_attesa: "In attesa",
  confermato: "Confermato",
  rifiutato: "Rifiutato",
};

const statusStyles: Record<QuoteRequestStatus, string> = {
  in_attesa: "border-ink-faint text-ink-soft",
  confermato: "border-ink bg-ink text-paper",
  rifiutato: "border-red-300 text-red-700",
};

const currencyFormatter = new Intl.NumberFormat("it-IT", { style: "currency", currency: "EUR" });

export default function StaffQuoteRequests({ onBack }: StaffQuoteRequestsProps) {
  const [token, setToken] = useState<string | null>(null);
  const [passwordInput, setPasswordInput] = useState("");
  const [loginError, setLoginError] = useState<string | null>(null);
  const [loggingIn, setLoggingIn] = useState(false);

  const [requests, setRequests] = useState<QuoteRequestOut[] | null>(null);
  const [listError, setListError] = useState<string | null>(null);
  const [updatingId, setUpdatingId] = useState<number | null>(null);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [refreshing, setRefreshing] = useState(false);

  const loadRequests = (staffToken: string) => {
    fetchQuoteRequests(staffToken)
      .then(setRequests)
      .catch((err: unknown) => {
        setListError(err instanceof ApiError ? err.message : "Errore di connessione al backend");
      });
  };

  const handleRefresh = () => {
    if (!token) return;
    setRefreshing(true);
    setListError(null);
    fetchQuoteRequests(token)
      .then(setRequests)
      .catch((err: unknown) => {
        setListError(err instanceof ApiError ? err.message : "Errore di connessione al backend");
      })
      .finally(() => setRefreshing(false));
  };

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    setLoggingIn(true);
    setLoginError(null);
    fetchQuoteRequests(passwordInput)
      .then((data) => {
        setToken(passwordInput);
        setRequests(data);
      })
      .catch((err: unknown) => {
        setLoginError(err instanceof ApiError ? err.message : "Errore di connessione al backend");
      })
      .finally(() => setLoggingIn(false));
  };

  const handleStatusChange = (id: number, status: QuoteRequestStatus) => {
    if (!token) return;
    setUpdatingId(id);
    updateQuoteRequestStatus(id, status, token)
      .then(() => loadRequests(token))
      .catch((err: unknown) => {
        setListError(err instanceof ApiError ? err.message : "Errore di connessione al backend");
      })
      .finally(() => setUpdatingId(null));
  };

  if (!token) {
    return (
      <div className="mx-auto max-w-sm p-6">
        <BackToHomeLink onClick={onBack} />
        <h1 className="mb-1 font-display text-2xl text-ink">Area riservata Coges</h1>
        <p className="mb-6 text-sm text-ink-soft">Inserisci la password per vedere le richieste di preventivo.</p>

        <form onSubmit={handleLogin} className="flex flex-col gap-3">
          <input
            type="password"
            required
            placeholder="Password"
            value={passwordInput}
            onChange={(e) => setPasswordInput(e.target.value)}
            className="border border-line px-3 py-2 text-sm focus:border-ink focus:outline-none"
          />
          {loginError && <p className="text-xs text-red-700">{loginError}</p>}
          <button
            type="submit"
            disabled={loggingIn}
            className="border border-ink bg-ink py-2 text-xs uppercase tracking-wide text-paper hover:opacity-90 disabled:opacity-40"
          >
            {loggingIn ? "Verifica..." : "Accedi"}
          </button>
        </form>
      </div>
    );
  }

  const selectedRequest = requests?.find((r) => r.id === selectedId) ?? null;

  return (
    <div className="mx-auto max-w-5xl p-6">
      <BackToHomeLink onClick={onBack} />
      <div className="mb-6 flex items-end justify-between gap-4">
        <div>
          <h1 className="mb-1 font-display text-2xl text-ink">Richieste di preventivo</h1>
          <p className="text-sm text-ink-soft">Stime inviate dai clienti dal configuratore, in attesa di conferma.</p>
        </div>
        <button
          type="button"
          onClick={handleRefresh}
          disabled={refreshing}
          className="shrink-0 border border-line px-3 py-2 text-xs uppercase tracking-wide text-ink-soft hover:border-ink disabled:opacity-40"
        >
          {refreshing ? "Aggiorno..." : "Aggiorna"}
        </button>
      </div>

      {listError && <p className="mb-4 text-sm text-red-700">{listError}</p>}
      {!requests && !listError && <p className="text-ink-soft">Caricamento...</p>}
      {requests && requests.length === 0 && <p className="text-ink-soft">Nessuna richiesta ricevuta finora.</p>}

      {requests && requests.length > 0 && (
        <div className="overflow-x-auto border border-line">
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b border-line bg-paper text-xs uppercase tracking-wide text-ink-soft">
                <th className="px-3 py-2">Data</th>
                <th className="px-3 py-2">Categoria</th>
                <th className="px-3 py-2">Cliente</th>
                <th className="px-3 py-2">Contatti</th>
                <th className="px-3 py-2 text-right">Prezzo</th>
                <th className="px-3 py-2">Stato</th>
                <th className="px-3 py-2">Azioni</th>
              </tr>
            </thead>
            <tbody>
              {requests.map((r) => (
                <tr key={r.id} className="border-b border-line last:border-b-0">
                  <td className="px-3 py-2 text-ink-soft">{new Date(r.created_at).toLocaleDateString("it-IT")}</td>
                  <td className="px-3 py-2">{familyLabels[r.product_family] ?? r.product_family}</td>
                  <td className="px-3 py-2">
                    {r.customer_name}
                    {r.customer_note && <div className="text-xs text-ink-faint">{r.customer_note}</div>}
                  </td>
                  <td className="px-3 py-2 text-xs text-ink-soft">
                    <div>{r.customer_email}</div>
                    <div>{r.customer_phone}</div>
                  </td>
                  <td className="px-3 py-2 text-right">{currencyFormatter.format(r.final_price)}</td>
                  <td className="px-3 py-2">
                    <span className={`border px-2 py-0.5 text-xs ${statusStyles[r.status]}`}>
                      {statusLabels[r.status]}
                    </span>
                  </td>
                  <td className="px-3 py-2">
                    <div className="flex gap-1">
                      <button
                        type="button"
                        onClick={() => setSelectedId(r.id)}
                        className="border border-ink px-2 py-1 text-xs uppercase tracking-wide text-ink hover:bg-ink hover:text-paper"
                      >
                        Dettagli
                      </button>
                      <button
                        type="button"
                        disabled={updatingId === r.id || r.status === "confermato"}
                        onClick={() => handleStatusChange(r.id, "confermato")}
                        className="border border-line px-2 py-1 text-xs uppercase tracking-wide text-ink-soft hover:border-ink disabled:cursor-not-allowed disabled:opacity-40"
                      >
                        Conferma
                      </button>
                      <button
                        type="button"
                        disabled={updatingId === r.id || r.status === "rifiutato"}
                        onClick={() => handleStatusChange(r.id, "rifiutato")}
                        className="border border-line px-2 py-1 text-xs uppercase tracking-wide text-ink-soft hover:border-ink disabled:cursor-not-allowed disabled:opacity-40"
                      >
                        Rifiuta
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {selectedRequest && (
        <QuoteRequestDetailModal
          request={selectedRequest}
          onClose={() => setSelectedId(null)}
          onStatusChange={(id, status) => {
            handleStatusChange(id, status);
            setSelectedId(null);
          }}
          updating={updatingId === selectedRequest.id}
        />
      )}
    </div>
  );
}
