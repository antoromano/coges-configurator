import { useEffect, useMemo, useRef, useState } from "react";

import BackToHomeLink from "../components/BackToHomeLink";
import DimensionSlider from "../components/DimensionSlider";
import MultiOptionSelector from "../components/MultiOptionSelector";
import OptionSelector from "../components/OptionSelector";
import PriceBreakdown from "../components/PriceBreakdown";
import QuoteRequestForm from "../components/QuoteRequestForm";
import { ApiError, calculateFinestrePrice, fetchFinestreCatalog, submitFinestreQuoteRequest } from "../services/api";
import type {
  CustomerContact,
  FinestreCatalog,
  FinestreConfiguration,
  FinestrePriceCalculationResponse,
} from "../types";
import { buildFinestreLines } from "../utils/breakdownLines";

const DEBOUNCE_MS = 400;

function clampToRange(value: number, min: number, max: number): number {
  return Math.min(max, Math.max(min, value));
}

function profileDescription(profile: FinestreCatalog["profiles"][number]): string {
  const specs = [
    profile.air_permeability_class && `Permeabilita' aria: ${profile.air_permeability_class}`,
    profile.water_tightness_class && `Tenuta acqua: ${profile.water_tightness_class}`,
    profile.wind_resistance_class && `Resistenza vento: ${profile.wind_resistance_class}`,
    profile.acoustic_performance_db && `Acustica: ${profile.acoustic_performance_db}`,
  ].filter(Boolean);
  return specs.length > 0 ? `${profile.description} ${specs.join(" · ")}` : profile.description;
}

interface ConfiguratorFinestreProps {
  onBack: () => void;
}

export default function ConfiguratorFinestre({ onBack }: ConfiguratorFinestreProps) {
  const [catalog, setCatalog] = useState<FinestreCatalog | null>(null);
  const [catalogError, setCatalogError] = useState<string | null>(null);

  const [openingTypeId, setOpeningTypeId] = useState<number | null>(null);
  const [width, setWidth] = useState(1000);
  const [height, setHeight] = useState(1000);
  const [materialId, setMaterialId] = useState<number | null>(null);
  const [systemId, setSystemId] = useState<number | null>(null);
  const [profileId, setProfileId] = useState<number | null>(null);
  const [glassTypeId, setGlassTypeId] = useState<number | null>(null);
  const [colorId, setColorId] = useState<number | null>(null);
  const [extraOptionIds, setExtraOptionIds] = useState<number[]>([]);

  const [priceResponse, setPriceResponse] = useState<FinestrePriceCalculationResponse | null>(null);
  const [priceLoading, setPriceLoading] = useState(false);
  const [priceError, setPriceError] = useState<string | null>(null);

  const debounceTimer = useRef<number | undefined>(undefined);

  useEffect(() => {
    fetchFinestreCatalog()
      .then((data) => {
        setCatalog(data);
        const openingType = data.opening_types[0];
        const material = data.materials[0];
        const system = data.systems.find((s) => s.material_id === material?.id) ?? null;
        const profile = data.profiles.find((p) => p.system_id === system?.id) ?? null;

        if (openingType) {
          setOpeningTypeId(openingType.id);
          setWidth(clampToRange(1000, openingType.min_width_mm, openingType.max_width_mm));
          setHeight(clampToRange(1000, openingType.min_height_mm, openingType.max_height_mm));
        }
        setMaterialId(material?.id ?? null);
        setSystemId(system?.id ?? null);
        setProfileId(profile?.id ?? null);
        setGlassTypeId(data.glass_types[0]?.id ?? null);
        setColorId(data.colors[0]?.id ?? null);
      })
      .catch((err: unknown) => {
        setCatalogError(err instanceof ApiError ? err.message : "Errore di connessione al backend");
      });
  }, []);

  const openingType = catalog?.opening_types.find((o) => o.id === openingTypeId) ?? null;
  const availableSystems = useMemo(
    () => catalog?.systems.filter((s) => s.material_id === materialId) ?? [],
    [catalog, materialId],
  );
  const availableProfiles = useMemo(
    () => catalog?.profiles.filter((p) => p.system_id === systemId) ?? [],
    [catalog, systemId],
  );

  const handleOpeningTypeChange = (id: number) => {
    setOpeningTypeId(id);
    const newType = catalog?.opening_types.find((o) => o.id === id);
    if (newType) {
      setWidth((w) => clampToRange(w, newType.min_width_mm, newType.max_width_mm));
      setHeight((h) => clampToRange(h, newType.min_height_mm, newType.max_height_mm));
    }
  };

  const handleMaterialChange = (id: number) => {
    setMaterialId(id);
    const newSystem = catalog?.systems.find((s) => s.material_id === id) ?? null;
    setSystemId(newSystem?.id ?? null);
    const newProfile = catalog?.profiles.find((p) => p.system_id === newSystem?.id) ?? null;
    setProfileId(newProfile?.id ?? null);
  };

  const handleSystemChange = (id: number) => {
    setSystemId(id);
    const newProfile = catalog?.profiles.find((p) => p.system_id === id) ?? null;
    setProfileId(newProfile?.id ?? null);
  };

  const configuration: FinestreConfiguration | null = useMemo(() => {
    if (
      !openingTypeId ||
      materialId === null ||
      systemId === null ||
      profileId === null ||
      glassTypeId === null ||
      colorId === null
    ) {
      return null;
    }
    return {
      opening_type_id: openingTypeId,
      width_mm: width,
      height_mm: height,
      material_id: materialId,
      system_id: systemId,
      profile_id: profileId,
      glass_type_id: glassTypeId,
      color_id: colorId,
      extra_option_ids: extraOptionIds,
    };
  }, [openingTypeId, width, height, materialId, systemId, profileId, glassTypeId, colorId, extraOptionIds]);

  useEffect(() => {
    if (!configuration) return;

    window.clearTimeout(debounceTimer.current);
    setPriceLoading(true);

    debounceTimer.current = window.setTimeout(() => {
      calculateFinestrePrice(configuration)
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

  if (!catalog || !openingType) {
    return (
      <div className="mx-auto max-w-2xl p-6">
        <BackToHomeLink onClick={onBack} />
        <div className="text-ink-soft">Caricamento catalogo...</div>
      </div>
    );
  }

  const breakdown = priceResponse?.breakdown;
  const lines = breakdown ? buildFinestreLines(breakdown) : [];

  return (
    <div className="mx-auto max-w-4xl p-6">
      <BackToHomeLink onClick={onBack} />
      <h1 className="mb-1 font-display text-3xl text-ink">Configuratore finestre</h1>
      <p className="mb-6 text-sm text-ink-soft">Prototipo con dati fittizi, prezzi indicativi.</p>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <div className="flex flex-col gap-6 lg:col-span-2">
          <OptionSelector
            label="Tipo di apertura"
            options={catalog.opening_types.map((o) => ({
              id: o.id,
              name: o.name,
              description: o.description,
              badge: `da ${o.base_price_per_sqm}€/m²`,
            }))}
            selectedId={openingTypeId}
            onChange={handleOpeningTypeChange}
          />

          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
            <DimensionSlider
              label="Larghezza"
              value={width}
              min={openingType.min_width_mm}
              max={openingType.max_width_mm}
              onChange={setWidth}
            />
            <DimensionSlider
              label="Altezza"
              value={height}
              min={openingType.min_height_mm}
              max={openingType.max_height_mm}
              onChange={setHeight}
            />
          </div>

          <OptionSelector
            label="Materiale"
            options={catalog.materials.map((m) => ({ id: m.id, name: m.name, badge: `×${m.price_multiplier}` }))}
            selectedId={materialId}
            onChange={handleMaterialChange}
          />

          <OptionSelector
            label="Sistema"
            options={availableSystems.map((s) => ({
              id: s.id,
              name: s.name,
              description: s.description,
              badge: `×${s.price_multiplier}`,
            }))}
            selectedId={systemId}
            onChange={handleSystemChange}
          />

          <OptionSelector
            label="Profilo"
            options={availableProfiles.map((p) => ({
              id: p.id,
              name: p.name,
              description: profileDescription(p),
              badge: `×${p.price_multiplier}`,
            }))}
            selectedId={profileId}
            onChange={setProfileId}
          />

          <OptionSelector
            label="Tipo di vetro"
            options={catalog.glass_types.map((g) => ({
              id: g.id,
              name: g.name,
              badge: g.extra_cost === 0 ? "incluso" : `+${g.extra_cost}€`,
            }))}
            selectedId={glassTypeId}
            onChange={setGlassTypeId}
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
                submitFinestreQuoteRequest({ ...(configuration as FinestreConfiguration), ...contact })
              }
            />
          </div>
        </div>
      </div>
    </div>
  );
}
