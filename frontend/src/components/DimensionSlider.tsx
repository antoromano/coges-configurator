interface DimensionSliderProps {
  label: string;
  value: number;
  min: number;
  max: number;
  onChange: (value: number) => void;
}

export default function DimensionSlider({ label, value, min, max, onChange }: DimensionSliderProps) {
  const clamp = (v: number) => Math.min(max, Math.max(min, v));

  return (
    <div className="flex flex-col gap-2">
      <div className="flex items-center justify-between">
        <label className="text-xs font-medium uppercase tracking-wide text-ink-soft">{label}</label>
        <div className="flex items-center gap-1">
          <input
            type="number"
            min={min}
            max={max}
            value={value}
            onChange={(e) => {
              const raw = Number(e.target.value);
              if (!Number.isNaN(raw)) onChange(clamp(raw));
            }}
            className="w-20 border border-line px-2 py-1 text-right text-sm focus:border-ink focus:outline-none"
          />
          <span className="text-sm text-ink-soft">mm</span>
        </div>
      </div>
      <input
        type="range"
        min={min}
        max={max}
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
        className="w-full accent-ink"
      />
      <div className="flex justify-between text-xs text-ink-faint">
        <span>{min} mm</span>
        <span>{max} mm</span>
      </div>
    </div>
  );
}
