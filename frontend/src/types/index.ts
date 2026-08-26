// Tipi condivisi tra i componenti, che rispecchiano il contratto delle API
// definite in backend/app/schemas/ e documentate in SPEC.md.

export interface ProductFamily {
  slug: string;
  name: string;
  description: string;
}

export interface ExtraOptionLine {
  id: number;
  name: string;
  cost: number;
}

// ---------------------------------------------------------------------------
// Finestre
// ---------------------------------------------------------------------------

export interface WindowOpeningType {
  id: number;
  name: string;
  description: string;
  base_price_per_sqm: number;
  min_width_mm: number;
  max_width_mm: number;
  min_height_mm: number;
  max_height_mm: number;
}

export interface WindowMaterial {
  id: number;
  name: string;
  price_multiplier: number;
}

export interface WindowSystem {
  id: number;
  name: string;
  material_id: number;
  description: string;
  price_multiplier: number;
}

export interface WindowProfile {
  id: number;
  name: string;
  system_id: number;
  description: string;
  air_permeability_class: string | null;
  water_tightness_class: string | null;
  wind_resistance_class: string | null;
  acoustic_performance_db: string | null;
  price_multiplier: number;
}

export interface WindowGlassType {
  id: number;
  name: string;
  extra_cost: number;
}

export interface WindowColor {
  id: number;
  name: string;
  extra_cost: number;
}

export interface WindowExtraOption {
  id: number;
  name: string;
  extra_cost: number;
}

export interface FinestreCatalog {
  opening_types: WindowOpeningType[];
  materials: WindowMaterial[];
  systems: WindowSystem[];
  profiles: WindowProfile[];
  glass_types: WindowGlassType[];
  colors: WindowColor[];
  extra_options: WindowExtraOption[];
}

export interface FinestreConfiguration {
  opening_type_id: number;
  width_mm: number;
  height_mm: number;
  material_id: number;
  system_id: number;
  profile_id: number;
  glass_type_id: number;
  color_id: number;
  extra_option_ids: number[];
}

export interface FinestrePriceBreakdown {
  area_m2: number;
  base_price_area: number;

  material_name: string;
  material_multiplier: number;
  price_after_material: number;

  system_name: string;
  system_multiplier: number;
  price_after_system: number;

  profile_name: string;
  profile_multiplier: number;
  price_after_profile: number;

  glass_name: string;
  glass_extra_cost: number;

  color_name: string;
  color_extra_cost: number;

  extra_options: ExtraOptionLine[];
  extra_options_total: number;

  subtotal_before_discount: number;
  volume_discount_applied: boolean;
  volume_discount_amount: number;

  final_price: number;
}

export interface FinestrePriceCalculationResponse {
  final_price: number;
  breakdown: FinestrePriceBreakdown;
}

// ---------------------------------------------------------------------------
// Portoncini
// ---------------------------------------------------------------------------

export interface DoorMaterial {
  id: number;
  name: string;
  price_multiplier: number;
}

export interface DoorBrand {
  id: number;
  name: string;
  description: string;
  price_multiplier: number;
}

export interface DoorSecurityClass {
  id: number;
  name: string;
  description: string;
  price_multiplier: number;
}

export interface DoorColor {
  id: number;
  name: string;
  extra_cost: number;
}

export interface DoorExtraOption {
  id: number;
  name: string;
  extra_cost: number;
}

export interface PortonciniCatalog {
  dimensions: {
    min_width_mm: number;
    max_width_mm: number;
    min_height_mm: number;
    max_height_mm: number;
  };
  materials: DoorMaterial[];
  brands: DoorBrand[];
  security_classes: DoorSecurityClass[];
  colors: DoorColor[];
  extra_options: DoorExtraOption[];
}

export interface PortonciniConfiguration {
  width_mm: number;
  height_mm: number;
  material_id: number;
  brand_id: number;
  security_class_id: number;
  color_id: number;
  extra_option_ids: number[];
}

export interface PortonciniPriceBreakdown {
  area_m2: number;
  base_price_area: number;

  material_name: string;
  material_multiplier: number;
  price_after_material: number;

  brand_name: string;
  brand_multiplier: number;
  price_after_brand: number;

  security_class_name: string;
  security_class_multiplier: number;
  price_after_security_class: number;

  color_name: string;
  color_extra_cost: number;

  extra_options: ExtraOptionLine[];
  extra_options_total: number;

  final_price: number;
}

export interface PortonciniPriceCalculationResponse {
  final_price: number;
  breakdown: PortonciniPriceBreakdown;
}

// ---------------------------------------------------------------------------
// Pergole
// ---------------------------------------------------------------------------

export interface PergolaMaterial {
  id: number;
  name: string;
  price_multiplier: number;
}

export interface PergolaSystem {
  id: number;
  name: string;
  description: string;
  price_multiplier: number;
}

export interface PergolaColor {
  id: number;
  name: string;
  extra_cost: number;
}

export interface PergolaExtraOption {
  id: number;
  name: string;
  extra_cost: number;
}

export interface PergoleCatalog {
  dimensions: {
    min_width_mm: number;
    max_width_mm: number;
    min_depth_mm: number;
    max_depth_mm: number;
  };
  materials: PergolaMaterial[];
  systems: PergolaSystem[];
  colors: PergolaColor[];
  extra_options: PergolaExtraOption[];
}

export interface PergoleConfiguration {
  width_mm: number;
  depth_mm: number;
  material_id: number;
  system_id: number;
  color_id: number;
  extra_option_ids: number[];
}

export interface PergolePriceBreakdown {
  area_m2: number;
  base_price_area: number;

  material_name: string;
  material_multiplier: number;
  price_after_material: number;

  system_name: string;
  system_multiplier: number;
  price_after_system: number;

  color_name: string;
  color_extra_cost: number;

  extra_options: ExtraOptionLine[];
  extra_options_total: number;

  subtotal_before_discount: number;
  volume_discount_applied: boolean;
  volume_discount_amount: number;

  final_price: number;
}

export interface PergolePriceCalculationResponse {
  final_price: number;
  breakdown: PergolePriceBreakdown;
}

// ---------------------------------------------------------------------------
// Richieste di preventivo
// ---------------------------------------------------------------------------

export type QuoteRequestStatus = "in_attesa" | "confermato" | "rifiutato";

// Dati di contatto raccolti nel form "Richiedi preventivo", in coda a
// ciascuna configurazione (nessuna password: identificazione per email).
export interface CustomerContact {
  customer_name: string;
  customer_email: string;
  customer_phone: string;
  customer_note: string;
}

export type FinestreQuoteRequestCreate = FinestreConfiguration & CustomerContact;
export type PortonciniQuoteRequestCreate = PortonciniConfiguration & CustomerContact;
export type PergoleQuoteRequestCreate = PergoleConfiguration & CustomerContact;

export interface QuoteRequestCreatedResponse {
  id: number;
  final_price: number;
  status: QuoteRequestStatus;
}

// Vista staff: una richiesta cosi' come salvata, indipendentemente dalla
// famiglia prodotto (configuration/breakdown restano oggetti generici,
// mostrati "cosi' come sono" nella tabella interna).
export interface QuoteRequestOut {
  id: number;
  product_family: string;
  configuration: Record<string, unknown>;
  final_price: number;
  breakdown: Record<string, unknown>;
  customer_name: string;
  customer_email: string;
  customer_phone: string;
  customer_note: string;
  status: QuoteRequestStatus;
  created_at: string;
}
