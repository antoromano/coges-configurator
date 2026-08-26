"""Schemi Pydantic per la famiglia prodotto "Pergole" (pergole bioclimatiche
outdoor). Range dimensionale fisso, in mm: larghezza e sporgenza (profondita')."""

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import ExtraOptionLine

MIN_WIDTH_MM = 2000
MAX_WIDTH_MM = 6000
MIN_DEPTH_MM = 2000
MAX_DEPTH_MM = 4000

# ---------------------------------------------------------------------------
# GET /api/catalog/pergole
# ---------------------------------------------------------------------------


class PergolaMaterialOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    price_multiplier: float


class PergolaSystemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    price_multiplier: float


class PergolaColorOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    extra_cost: float


class PergolaExtraOptionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    extra_cost: float


class PergoleCatalogResponse(BaseModel):
    dimensions: dict[str, int]
    materials: list[PergolaMaterialOut]
    systems: list[PergolaSystemOut]
    colors: list[PergolaColorOut]
    extra_options: list[PergolaExtraOptionOut]


# ---------------------------------------------------------------------------
# POST /api/calculate-price/pergole
# ---------------------------------------------------------------------------


class PergoleConfigurationRequest(BaseModel):
    width_mm: int = Field(ge=MIN_WIDTH_MM, le=MAX_WIDTH_MM, description="Larghezza in millimetri")
    depth_mm: int = Field(ge=MIN_DEPTH_MM, le=MAX_DEPTH_MM, description="Sporgenza in millimetri")
    material_id: int
    system_id: int
    color_id: int
    extra_option_ids: list[int] = Field(default_factory=list)


class PergolePriceBreakdown(BaseModel):
    area_m2: float
    base_price_area: float

    material_name: str
    material_multiplier: float
    price_after_material: float

    system_name: str
    system_multiplier: float
    price_after_system: float

    color_name: str
    color_extra_cost: float

    extra_options: list[ExtraOptionLine]
    extra_options_total: float

    subtotal_before_discount: float
    volume_discount_applied: bool
    volume_discount_amount: float

    final_price: float


class PergolePriceCalculationResponse(BaseModel):
    final_price: float
    breakdown: PergolePriceBreakdown
