"""Schemi Pydantic per la famiglia prodotto "Portoncini" (porte blindate).

Range dimensionale fisso (a differenza delle Finestre, qui non varia in
base a un tipo di apertura: e' sempre una porta a battente singola).
"""

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import ExtraOptionLine

MIN_WIDTH_MM = 700
MAX_WIDTH_MM = 1300
MIN_HEIGHT_MM = 2000
MAX_HEIGHT_MM = 2400

# ---------------------------------------------------------------------------
# GET /api/catalog/portoncini
# ---------------------------------------------------------------------------


class DoorMaterialOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    price_multiplier: float


class DoorBrandOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    price_multiplier: float


class DoorSecurityClassOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    price_multiplier: float


class DoorColorOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    extra_cost: float


class DoorExtraOptionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    extra_cost: float


class PortonciniCatalogResponse(BaseModel):
    dimensions: dict[str, int]
    materials: list[DoorMaterialOut]
    brands: list[DoorBrandOut]
    security_classes: list[DoorSecurityClassOut]
    colors: list[DoorColorOut]
    extra_options: list[DoorExtraOptionOut]


# ---------------------------------------------------------------------------
# POST /api/calculate-price/portoncini
# ---------------------------------------------------------------------------


class PortonciniConfigurationRequest(BaseModel):
    width_mm: int = Field(ge=MIN_WIDTH_MM, le=MAX_WIDTH_MM, description="Larghezza in millimetri")
    height_mm: int = Field(ge=MIN_HEIGHT_MM, le=MAX_HEIGHT_MM, description="Altezza in millimetri")
    material_id: int
    brand_id: int
    security_class_id: int
    color_id: int
    extra_option_ids: list[int] = Field(default_factory=list)


class PortonciniPriceBreakdown(BaseModel):
    area_m2: float
    base_price_area: float

    material_name: str
    material_multiplier: float
    price_after_material: float

    brand_name: str
    brand_multiplier: float
    price_after_brand: float

    security_class_name: str
    security_class_multiplier: float
    price_after_security_class: float

    color_name: str
    color_extra_cost: float

    extra_options: list[ExtraOptionLine]
    extra_options_total: float

    final_price: float


class PortonciniPriceCalculationResponse(BaseModel):
    final_price: float
    breakdown: PortonciniPriceBreakdown
