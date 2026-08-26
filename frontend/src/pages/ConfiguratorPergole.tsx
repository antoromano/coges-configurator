import { useEffect, useMemo, useRef, useState } from "react";

import BackToHomeLink from "../components/BackToHomeLink";
import DimensionSlider from "../components/DimensionSlider";
import MultiOptionSelector from "../components/MultiOptionSelector";
import OptionSelector from "../components/OptionSelector";
import PriceBreakdown from "../components/PriceBreakdown";
import QuoteRequestForm from "../components/QuoteRequestForm";
import { ApiError, calculatePergolePrice, fetchPergoleCatalog, submitPergoleQuoteRequest } from "../services/api";
import type {
  CustomerContact,
  PergoleCatalog,
  PergoleConfiguration,
  PergolePriceCalculationResponse,
} from "../types";
import { buildPergoleLines } from "../utils/breakdownLines";

const DEBOUNCE_MS = 400;

interface ConfiguratorPergoleProps {
  onBack: () => void;
}

export default function ConfiguratorPergole({ onBack }: ConfiguratorPergoleProps) {
  const [catalog, setCatalog] = useState<PergoleCatalog | null>(null);
  const [catalogError, setCatalogError] = useState<string | null>(null);

  const [width, setWidth] = useState(3000);
  const [depth, setDepth] = useState(3000);
  const [materialId, setMaterialId] = useState<number | null>(null);
  const [systemId, setSystemId] = useState<number | null>(null);
  const [colorId, setColorId] = useState<number | null>(null);
  const [extraOptionIds, setExtraOptionIds] = useState<number[]>([]);

  const [priceResponse, setPriceResponse] = useState<PergolePriceCalculationResponse | null>(null);
  const [priceLoading, setPriceLoading] = useState(false);
  const [priceError, setPriceError] = useState<string | null>(null);

  const debounceTimer = useRef<number | undefined>(undefined);

  useEffect(() => {
    fetchPergoleCatalog()
      .then((data) => {
        setCatalog(data);
        setWidth(Math.round((data.dimensions.min_width_mm + data.dimensions.max_width_mm) / 2));
        setDepth(Math.round((data.dimensions.min_depth_mm + data.dimensions.max_depth_mm) / 2));
        setMaterialId(data.materials[0]?.id ?? null);
        setSystemId(data.systems[0]?.id ?? null);
        setColorId(data.colors[0]?.id ?? null);
      })
      .catch((err: unknown) => {
        setCatalogError(err instanceof ApiError ? err.message : "Errore di connessione al backend");
      });
  }, []);

  const configuration: PergoleConfiguration | null = useMemo(() => {
    if (materialId === null || systemId === null || colorId === null) {
      return null;
    }
    return {
      width_mm: width,
      depth_mm: depth,
      material_id: materialId,
      system_id: systemId,
      color_id: colorId,
      extra_option_ids: extraOptionIds,
    };
  }, [width, depth, materialId, systemId, colorId, extraOptionIds]);

  useEffect(() => {
    if (!configuration) return;

    window.clearTimeout(debounceTimer.current);
    setPriceLoading(true);

    debounceTimer.current = window.setTimeout(() => {
      calculatePergolePrice(configuration)
        .then((result) => {
          setPriceResponse(result);
          setPriceError(null);
        })
        .catch((err: unknown) => {
          setPriceError(err instanceof ApiError ? err.message : "Errore di connessione al backend");
        })
        .finally(() => {
          setPriceLoading(false);
        });
    }, DEBOUNCE_MS);

    return () => window.clearTimeout(debounceTimer.current);
  }, [configuration]);

  if (catalogError) {
    return (
      <div className="mx-auto max-w-2xl p-6">
        <BackToHomeLink onClick={onBack} />
        <div className="border border-red-300 bg-red-50 p-4 text-red-700">
          Impossibile caricare il catalogo dal backend: {catalogError}. Verifica che il backend sia
          avviato su {import.meta.env.VITE_API_URL}.
        </div>
      </div>
    );
  }

  if (!catalog) {
    return (
      <div className="mx-auto max-w-2xl p-6">
        <BackToHomeLink onClick={onBack} />
        <div className="text-ink-soft">Caricamento catalogo...</div>
      </div>
    );
  }

  const breakdown = priceResponse?.breakdown;
  const lines = breakdown ? buildPergoleLines(breakdown) : [];

  return (
    <div className="mx-auto max-w-4xl p-6">
      <BackToHomeLink onClick={onBack} />
      <h1 className="mb-1 font-display text-3xl text-ink">Configuratore pergole</h1>
      <p className="mb-6 text-sm text-ink-soft">Prototipo con dati fittizi, prezzi indicativi.</p>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <div className="flex flex-col gap-6 lg:col-span-2">
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
            <DimensionSlider
              label="Larghezza"
              value={width}
              min={catalog.dimensions.min_width_mm}
              max={catalog.dimensions.max_width_mm}
              onChange={setWidth}
            />
            <DimensionSlider
              label="Sporgenza"
              value={depth}
              min={catalog.dimensions.min_depth_mm}
              max={catalog.dimensions.max_depth_mm}
              onChange={setDepth}
            />
          </div>

          <OptionSelector
            label="Materiale"
            options={catalog.materials.map((m) => ({ id: m.id, name: m.name, badge: `×${m.price_multiplier}` }))}
            selectedId={materialId}
            onChange={setMaterialId}
          />

          <OptionSelector
            label="Tipo di copertura"
            options={catalog.systems.map((s) => ({
              id: s.id,
              name: s.name,
              description: s.description,
              badge: `×${s.price_multiplier}`,
            }))}
            selectedId={systemId}
            onChange={setSystemId}
          />

          <OptionSelector
            label="Colore"
            options={catalog.colors.map((c) => ({
              id: c.id,
              name: c.name,
              badge: c.extra_cost === 0 ? "incluso" : `+${c.extra_cost}€`,
            }))}
            selectedId={colorId}
            onChange={setColorId}
          />

          <MultiOptionSelector
            label="Opzioni extra"
            options={catalog.extra_options.map((o) => ({ id: o.id, name: o.name, badge: `+${o.extra_cost}€` }))}
            selectedIds={extraOptionIds}
            onChange={setExtraOptionIds}
          />
        </div>

        <div className="lg:col-span-1">
          <div className="lg:sticky lg:top-6">
            <PriceBreakdown
              finalPrice={priceResponse?.final_price ?? null}
              lines={lines}
              loading={priceLoading}
              error={priceError}
            />
            <QuoteRequestForm
              disabled={!configuration || !priceResponse}
              onSubmit={(contact: CustomerContact) =>
                submitPergoleQuoteRequest({ ...(configuration as PergoleConfiguration), ...contact })
              }
            />
          </div>
        </div>
      </div>
    </div>
  );
}
