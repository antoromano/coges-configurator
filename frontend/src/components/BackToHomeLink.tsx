interface BackToHomeLinkProps {
  onClick: () => void;
}

export default function BackToHomeLink({ onClick }: BackToHomeLinkProps) {
  return (
    <button
      type="button"
      onClick={onClick}
      className="mb-4 text-xs uppercase tracking-wide text-ink-soft hover:text-ink"
    >
      &larr; Cambia categoria prodotto
    </button>
  );
}
