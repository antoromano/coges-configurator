from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.db import get_session
from app.models import PergolaColor, PergolaExtraOption, PergolaMaterial, PergolaSystem
from app.schemas.common import ExtraOptionLine
from app.schemas.pergole import (
    MAX_DEPTH_MM,
    MAX_WIDTH_MM,
    MIN_DEPTH_MM,
    MIN_WIDTH_MM,
    PergoleCatalogResponse,
    PergoleConfigurationRequest,
    PergolePriceBreakdown,
    PergolePriceCalculationResponse,
)
from app.services.pricing_pergole import ExtraOptionInput, PriceResult, calculate_price

router = APIRouter(prefix="/api", tags=["pergole"])


def validate_and_price(config: PergoleConfigurationRequest, session: Session) -> PriceResult:
    """Condivisa tra calculate-price/pergole e quote-requests/pergole."""
    material = session.get(PergolaMaterial, config.material_id)
    if material is None:
        raise HTTPException(422, detail=f"material_id {config.material_id} non esiste")

    system = session.get(PergolaSystem, config.system_id)
    if system is None:
        raise HTTPException(422, detail=f"system_id {config.system_id} non esiste")

    color = session.get(PergolaColor, config.color_id)
    if color is None:
        raise HTTPException(422, detail=f"color_id {config.color_id} non esiste")

    extra_options: list[ExtraOptionInput] = []
    for option_id in config.extra_option_ids:
        option = session.get(PergolaExtraOption, option_id)
        if option is None:
            raise HTTPException(422, detail=f"extra_option_ids contiene un id inesistente: {option_id}")
        extra_options.append(ExtraOptionInput(id=option.id, name=option.name, cost=option.extra_cost))

    return calculate_price(
        width_mm=config.width_mm,
        depth_mm=config.depth_mm,
        material_name=material.name,
        material_multiplier=material.price_multiplier,
        system_name=system.name,
        system_multiplier=system.price_multiplier,
        color_name=color.name,
        color_extra_cost=color.extra_cost,
        extra_options=extra_options,
    )


def build_breakdown(result: PriceResult) -> PergolePriceBreakdown:
    return PergolePriceBreakdown(
        area_m2=result.area_m2,
        base_price_area=result.base_price_area,
        material_name=result.material_name,
        material_multiplier=result.material_multiplier,
        price_after_material=result.price_after_material,
        system_name=result.system_name,
        system_multiplier=result.system_multiplier,
        price_after_system=result.price_after_system,
        color_name=result.color_name,
        color_extra_cost=result.color_extra_cost,
        extra_options=[
            ExtraOptionLine(id=opt.id, name=opt.name, cost=opt.cost) for opt in result.extra_options
        ],
        extra_options_total=result.extra_options_total,
        subtotal_before_discount=result.subtotal_before_discount,
        volume_discount_applied=result.volume_discount_applied,
        volume_discount_amount=result.volume_discount_amount,
        final_price=result.final_price,
    )


@router.get("/catalog/pergole", response_model=PergoleCatalogResponse)
def get_catalog(session: Session = Depends(get_session)) -> PergoleCatalogResponse:
    return PergoleCatalogResponse(
        dimensions={
            "min_width_mm": MIN_WIDTH_MM,
            "max_width_mm": MAX_WIDTH_MM,
            "min_depth_mm": MIN_DEPTH_MM,
            "max_depth_mm": MAX_DEPTH_MM,
        },
        materials=session.exec(select(PergolaMaterial)).all(),
        systems=session.exec(select(PergolaSystem)).all(),
        colors=session.exec(select(PergolaColor)).all(),
        extra_options=session.exec(select(PergolaExtraOption)).all(),
    )


@router.post("/calculate-price/pergole", response_model=PergolePriceCalculationResponse)
def calculate_price_endpoint(
    config: PergoleConfigurationRequest, session: Session = Depends(get_session)
) -> PergolePriceCalculationResponse:
    result = validate_and_price(config, session)
    return PergolePriceCalculationResponse(final_price=result.final_price, breakdown=build_breakdown(result))
