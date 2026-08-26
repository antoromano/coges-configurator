from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.db import get_session
from app.models import DoorBrand, DoorColor, DoorExtraOption, DoorMaterial, DoorSecurityClass
from app.schemas.common import ExtraOptionLine
from app.schemas.portoncini import (
    MAX_HEIGHT_MM,
    MAX_WIDTH_MM,
    MIN_HEIGHT_MM,
    MIN_WIDTH_MM,
    PortonciniCatalogResponse,
    PortonciniConfigurationRequest,
    PortonciniPriceBreakdown,
    PortonciniPriceCalculationResponse,
)
from app.services.pricing_portoncini import ExtraOptionInput, PriceResult, calculate_price

router = APIRouter(prefix="/api", tags=["portoncini"])


def validate_and_price(config: PortonciniConfigurationRequest, session: Session) -> PriceResult:
    """Condivisa tra calculate-price/portoncini e quote-requests/portoncini."""
    material = session.get(DoorMaterial, config.material_id)
    if material is None:
        raise HTTPException(422, detail=f"material_id {config.material_id} non esiste")

    brand = session.get(DoorBrand, config.brand_id)
    if brand is None:
        raise HTTPException(422, detail=f"brand_id {config.brand_id} non esiste")

    security_class = session.get(DoorSecurityClass, config.security_class_id)
    if security_class is None:
        raise HTTPException(422, detail=f"security_class_id {config.security_class_id} non esiste")

    color = session.get(DoorColor, config.color_id)
    if color is None:
        raise HTTPException(422, detail=f"color_id {config.color_id} non esiste")

    extra_options: list[ExtraOptionInput] = []
    for option_id in config.extra_option_ids:
        option = session.get(DoorExtraOption, option_id)
        if option is None:
            raise HTTPException(422, detail=f"extra_option_ids contiene un id inesistente: {option_id}")
        extra_options.append(ExtraOptionInput(id=option.id, name=option.name, cost=option.extra_cost))

    return calculate_price(
        width_mm=config.width_mm,
        height_mm=config.height_mm,
        material_name=material.name,
        material_multiplier=material.price_multiplier,
        brand_name=brand.name,
        brand_multiplier=brand.price_multiplier,
        security_class_name=security_class.name,
        security_class_multiplier=security_class.price_multiplier,
        color_name=color.name,
        color_extra_cost=color.extra_cost,
        extra_options=extra_options,
    )


def build_breakdown(result: PriceResult) -> PortonciniPriceBreakdown:
    return PortonciniPriceBreakdown(
        area_m2=result.area_m2,
        base_price_area=result.base_price_area,
        material_name=result.material_name,
        material_multiplier=result.material_multiplier,
        price_after_material=result.price_after_material,
        brand_name=result.brand_name,
        brand_multiplier=result.brand_multiplier,
        price_after_brand=result.price_after_brand,
        security_class_name=result.security_class_name,
        security_class_multiplier=result.security_class_multiplier,
        price_after_security_class=result.price_after_security_class,
        color_name=result.color_name,
        color_extra_cost=result.color_extra_cost,
        extra_options=[
            ExtraOptionLine(id=opt.id, name=opt.name, cost=opt.cost) for opt in result.extra_options
        ],
        extra_options_total=result.extra_options_total,
        final_price=result.final_price,
    )


@router.get("/catalog/portoncini", response_model=PortonciniCatalogResponse)
def get_catalog(session: Session = Depends(get_session)) -> PortonciniCatalogResponse:
    return PortonciniCatalogResponse(
        dimensions={
            "min_width_mm": MIN_WIDTH_MM,
            "max_width_mm": MAX_WIDTH_MM,
            "min_height_mm": MIN_HEIGHT_MM,
            "max_height_mm": MAX_HEIGHT_MM,
        },
        materials=session.exec(select(DoorMaterial)).all(),
        brands=session.exec(select(DoorBrand)).all(),
        security_classes=session.exec(select(DoorSecurityClass)).all(),
        colors=session.exec(select(DoorColor)).all(),
        extra_options=session.exec(select(DoorExtraOption)).all(),
    )


@router.post("/calculate-price/portoncini", response_model=PortonciniPriceCalculationResponse)
def calculate_price_endpoint(
    config: PortonciniConfigurationRequest, session: Session = Depends(get_session)
) -> PortonciniPriceCalculationResponse:
    result = validate_and_price(config, session)
    return PortonciniPriceCalculationResponse(final_price=result.final_price, breakdown=build_breakdown(result))
