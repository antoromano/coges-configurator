interface Option {
  id: number;
  name: string;
  description?: string;
  badge?: string;
}

interface OptionSelectorProps {
  label: string;
  options: Option[];
  selectedId: number | null;
  onChange: (id: number) => void;
}

// Selettore radio generico, riusato per Materiale/Sistema/Profilo/Vetro/
// Colore/Brand/Classe di sicurezza in tutte le famiglie prodotto: stessa
// interazione (scelta singola tra opzioni con eventuale badge di prezzo),
// cambia solo la lista di opzioni passata dal chiamante.
export default function OptionSelector({ label, options, selectedId, onChange }: OptionSelectorProps) {
  return (
    <div className="flex flex-col gap-2">
      <span className="text-xs font-medium uppercase tracking-wide text-ink-soft">{label}</span>
      <div className="grid grid-cols-1 gap-2 sm:grid-cols-2 lg:grid-cols-3">
        {options.map((option) => (
          <label
            key={option.id}
            className={`flex cursor-pointer flex-col gap-0.5 border px-3 py-2 text-sm transition-colors ${
              selectedId === option.id
                ? "border-ink bg-ink text-paper"
                : "border-line hover:border-ink-soft"
            }`}
          >
            <span className="flex items-center justify-between gap-2">
              <span className="flex items-center gap-2">
                <input
                  type="radio"
                  name={label}
                  checked={selectedId === option.id}
                  onChange={() => onChange(option.id)}
                  className="accent-ink"
                />
                {option.name}
              </span>
              {option.badge && (
                <span className={`text-xs ${selectedId === option.id ? "text-paper/70" : "text-ink-faint"}`}>
                  {option.badge}
                </span>
              )}
            </span>
            {option.description && (
              <span className={`pl-6 text-xs ${selectedId === option.id ? "text-paper/70" : "text-ink-faint"}`}>
                {option.description}
              </span>
            )}
          </label>
        ))}
      </div>
    </div>
  );
}
