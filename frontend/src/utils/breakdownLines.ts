import { formatCurrency, type BreakdownLine } from "../components/PriceBreakdown";
import type { FinestrePriceBreakdown, PergolePriceBreakdown, PortonciniPriceBreakdown } from "../types";

// Trasforma il breakdown restituito dalle API in righe leggibili, riusate sia
// nel configuratore (vista cliente) sia nel pannello di dettaglio dell'area
// staff (vista interna) — stessa formattazione in entrambi i posti, un solo
// punto da aggiornare se la formula cambia forma.

export function buildFinestreLines(breakdown: FinestrePriceBreakdown): BreakdownLine[] {
  return [
    { label: `Area (${breakdown.area_m2} m²) × prezzo base`, value: formatCurrency(breakdown.base_price_area) },
    {
      label: `Materiale ${breakdown.material_name} (×${breakdown.material_multiplier})`,
      value: formatCurrency(breakdown.price_after_material),
    },
    {
      label: `Sistema ${breakdown.system_name} (×${breakdown.system_multiplier})`,
      value: formatCurrency(breakdown.price_after_system),
    },
    {
      label: `Profilo ${breakdown.profile_name} (×${breakdown.profile_multiplier})`,
      value: formatCurrency(breakdown.price_after_profile),
    },
    { label: `Vetro ${breakdown.glass_name}`, value: formatCurrency(breakdown.glass_extra_cost) },
    { label: `Colore ${breakdown.color_name}`, value: formatCurrency(breakdown.color_extra_cost) },
    ...breakdown.extra_options.map((opt) => ({ label: opt.name, value: formatCurrency(opt.cost) })),
    ...(breakdown.volume_discount_applied
      ? [{ label: "Sconto volume (-10%)", value: `-${formatCurrency(breakdown.volume_discount_amount)}` }]
      : []),
    { label: "Totale", value: formatCurrency(breakdown.final_price), bold: true },
  ];
}

export function buildPortonciniLines(breakdown: PortonciniPriceBreakdown): BreakdownLine[] {
  return [
    { label: `Area (${breakdown.area_m2} m²) × prezzo base`, value: formatCurrency(breakdown.base_price_area) },
    {
      label: `Materiale ${breakdown.material_name} (×${breakdown.material_multiplier})`,
      value: formatCurrency(breakdown.price_after_material),
    },
    {
      label: `Marca ${breakdown.brand_name} (×${breakdown.brand_multiplier})`,
      value: formatCurrency(breakdown.price_after_brand),
    },
    {
      label: `Sicurezza ${breakdown.security_class_name} (×${breakdown.security_class_multiplier})`,
      value: formatCurrency(breakdown.price_after_security_class),
    },
    { label: `Colore ${breakdown.color_name}`, value: formatCurrency(breakdown.color_extra_cost) },
    ...breakdown.extra_options.map((opt) => ({ label: opt.name, value: formatCurrency(opt.cost) })),
    { label: "Totale", value: formatCurrency(breakdown.final_price), bold: true },
  ];
}

export function buildPergoleLines(breakdown: PergolePriceBreakdown): BreakdownLine[] {
  return [
    { label: `Area (${breakdown.area_m2} m²) × prezzo base`, value: formatCurrency(breakdown.base_price_area) },
    {
      label: `Materiale ${breakdown.material_name} (×${breakdown.material_multiplier})`,
      value: formatCurrency(breakdown.price_after_material),
    },
    {
      label: `Sistema ${breakdown.system_name} (×${breakdown.system_multiplier})`,
      value: formatCurrency(breakdown.price_after_system),
    },
    { label: `Colore ${breakdown.color_name}`, value: formatCurrency(breakdown.color_extra_cost) },
    ...breakdown.extra_options.map((opt) => ({ label: opt.name, value: formatCurrency(opt.cost) })),
    ...(breakdown.volume_discount_applied
      ? [{ label: "Sconto grande superficie (-8%)", value: `-${formatCurrency(breakdown.volume_discount_amount)}` }]
      : []),
    { label: "Totale", value: formatCurrency(breakdown.final_price), bold: true },
  ];
}

export function buildLinesForFamily(productFamily: string, breakdown: Record<string, unknown>): BreakdownLine[] {
  switch (productFamily) {
    case "finestre":
      return buildFinestreLines(breakdown as unknown as FinestrePriceBreakdown);
    case "portoncini":
      return buildPortonciniLines(breakdown as unknown as PortonciniPriceBreakdown);
    case "pergole":
      return buildPergoleLines(breakdown as unknown as PergolePriceBreakdown);
    default:
      return [];
  }
}
