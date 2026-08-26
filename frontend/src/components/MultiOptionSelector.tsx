interface Option {
  id: number;
  name: string;
  badge?: string;
}

interface MultiOptionSelectorProps {
  label: string;
  options: Option[];
  selectedIds: number[];
  onChange: (ids: number[]) => void;
}

// Selettore checkbox multi-selezione generico, riusato per le opzioni extra
// in tutte le famiglie prodotto.
export default function MultiOptionSelector({
  label,
  options,
  selectedIds,
  onChange,
}: MultiOptionSelectorProps) {
  const toggle = (id: number) => {
    if (selectedIds.includes(id)) {
      onChange(selectedIds.filter((selectedId) => selectedId !== id));
    } else {
      onChange([...selectedIds, id]);
    }
  };

  return (
    <div className="flex flex-col gap-2">
      <span className="text-xs font-medium uppercase tracking-wide text-ink-soft">{label}</span>
      <div className="grid grid-cols-1 gap-2 sm:grid-cols-2 lg:grid-cols-3">
        {options.map((option) => (
          <label
            key={option.id}
            className={`flex cursor-pointer items-center justify-between border px-3 py-2 text-sm transition-colors ${
              selectedIds.includes(option.id)
                ? "border-ink bg-ink text-paper"
                : "border-line hover:border-ink-soft"
            }`}
          >
            <span className="flex items-center gap-2">
              <input
                type="checkbox"
                checked={selectedIds.includes(option.id)}
                onChange={() => toggle(option.id)}
                className="accent-ink"
              />
              {option.name}
            </span>
            {option.badge && (
              <span className={`text-xs ${selectedIds.includes(option.id) ? "text-paper/70" : "text-ink-faint"}`}>
                {option.badge}
              </span>
            )}
          </label>
        ))}
      </div>
    </div>
  );
}
