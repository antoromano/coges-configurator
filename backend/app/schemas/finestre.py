"""Schemi Pydantic per la famiglia prodotto "Finestre".

Distinti dai modelli SQLModel in app/models/finestre.py: questi rappresentano
il contratto HTTP, non le tabelle del database.
"""

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import ExtraOptionLine

# ---------------------------------------------------------------------------
# GET /api/catalog/finestre
# ---------------------------------------------------------------------------


class WindowMaterialOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    price_multiplier: float


class WindowSystemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    material_id: int
    description: str
    price_multiplier: float


class WindowProfileOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    system_id: int
    description: str
    air_permeability_class: str | None
    water_tightness_class: str | None
    wind_resistance_class: str | None
    acoustic_performance_db: str | None
    price_multiplier: float


class WindowOpeningTypeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    base_price_per_sqm: float
    min_width_mm: int
    max_width_mm: int
    min_height_mm: int
    max_height_mm: int


class WindowGlassTypeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    extra_cost: float


class WindowColorOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    extra_cost: float


class WindowExtraOptionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    extra_cost: float


class FinestreCatalogResponse(BaseModel):
    opening_types: list[WindowOpeningTypeOut]
    materials: list[WindowMaterialOut]
    systems: list[WindowSystemOut]
    profiles: list[WindowProfileOut]
    glass_types: list[WindowGlassTypeOut]
    colors: list[WindowColorOut]
    extra_options: list[WindowExtraOptionOut]


# ---------------------------------------------------------------------------
# POST /api/calculate-price/finestre
# ---------------------------------------------------------------------------


class FinestreConfigurationRequest(BaseModel):
    opening_type_id: int
    width_mm: int = Field(ge=100, le=6000, description="Larghezza in millimetri")
    height_mm: int = Field(ge=100, le=6000, description="Altezza in millimetri")
    material_id: int
    system_id: int
    profile_id: int
    glass_type_id: int
    color_id: int
    extra_option_ids: list[int] = Field(default_factory=list)


class FinestrePriceBreakdown(BaseModel):
    area_m2: float
    base_price_area: float

    material_name: str
    material_multiplier: float
    price_after_material: float

    system_name: str
    system_multiplier: float
    price_after_system: float

    profile_name: str
    profile_multiplier: float
    price_after_profile: float

    glass_name: str
    glass_extra_cost: float

    color_name: str
    color_extra_cost: float

    extra_options: list[ExtraOptionLine]
    extra_options_total: float

    subtotal_before_discount: float
    volume_discount_applied: bool
    volume_discount_amount: float

    final_price: float


class FinestrePriceCalculationResponse(BaseModel):
    final_price: float
    breakdown: FinestrePriceBreakdown
