import { useState } from "react";

import { ApiError } from "../services/api";
import type { CustomerContact, QuoteRequestCreatedResponse } from "../types";

interface QuoteRequestFormProps {
  disabled: boolean;
  onSubmit: (contact: CustomerContact) => Promise<QuoteRequestCreatedResponse>;
}

const emptyContact: CustomerContact = {
  customer_name: "",
  customer_email: "",
  customer_phone: "",
  customer_note: "",
};

// Il configuratore resta libero per chiunque: questo form compare solo nel
// momento in cui il cliente vuole davvero inviare la richiesta a Coges, e
// raccoglie solo dati di contatto (nessun account/password).
export default function QuoteRequestForm({ disabled, onSubmit }: QuoteRequestFormProps) {
  const [expanded, setExpanded] = useState(false);
  const [contact, setContact] = useState<CustomerContact>(emptyContact);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<QuoteRequestCreatedResponse | null>(null);

  const updateField = (field: keyof CustomerContact) => (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setContact((prev) => ({ ...prev, [field]: e.target.value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    onSubmit(contact)
      .then((response) => {
        setResult(response);
      })
      .catch((err: unknown) => {
        setError(err instanceof ApiError ? err.message : "Errore di connessione al backend");
      })
      .finally(() => setSubmitting(false));
  };

  if (result) {
    return (
      <div className="mt-4 border border-ink bg-ink p-4 text-sm text-paper">
        Richiesta inviata (n. {result.id}). Un referente Coges la contatterà per confermare il
        preventivo definitivo.
      </div>
    );
  }

  if (!expanded) {
    return (
      <button
        type="button"
        disabled={disabled}
        onClick={() => setExpanded(true)}
        className="mt-4 w-full border border-ink bg-ink py-2.5 text-xs uppercase tracking-wide text-paper transition-opacity hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-40"
      >
        Richiedi preventivo
      </button>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="mt-4 flex flex-col gap-3 border border-line bg-white p-4">
      <span className="text-xs font-medium uppercase tracking-wide text-ink-soft">I tuoi dati</span>

      <input
        type="text"
        required
        placeholder="Nome e cognome"
        value={contact.customer_name}
        onChange={updateField("customer_name")}
        className="border border-line px-3 py-2 text-sm focus:border-ink focus:outline-none"
      />
      <input
        type="email"
        required
        placeholder="Email"
        value={contact.customer_email}
        onChange={updateField("customer_email")}
        className="border border-line px-3 py-2 text-sm focus:border-ink focus:outline-none"
      />
      <input
        type="tel"
        required
        placeholder="Telefono"
        value={contact.customer_phone}
        onChange={updateField("customer_phone")}
        className="border border-line px-3 py-2 text-sm focus:border-ink focus:outline-none"
      />
      <textarea
        placeholder="Note (opzionale)"
        value={contact.customer_note}
        onChange={updateField("customer_note")}
        rows={2}
        className="border border-line px-3 py-2 text-sm focus:border-ink focus:outline-none"
      />

      {error && <p className="text-xs text-red-700">Impossibile inviare la richiesta: {error}</p>}

      <div className="flex gap-2">
        <button
          type="submit"
          disabled={submitting}
          className="flex-1 border border-ink bg-ink py-2 text-xs uppercase tracking-wide text-paper transition-opacity hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-40"
        >
          {submitting ? "Invio in corso..." : "Invia richiesta"}
        </button>
        <button
          type="button"
          onClick={() => setExpanded(false)}
          className="border border-line px-3 text-xs uppercase tracking-wide text-ink-soft hover:border-ink-soft"
        >
          Annulla
        </button>
      </div>
    </form>
  );
}
