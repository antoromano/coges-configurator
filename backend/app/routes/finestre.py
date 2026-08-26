from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.db import get_session
from app.models import (
    WindowColor,
    WindowExtraOption,
    WindowGlassType,
    WindowMaterial,
    WindowOpeningType,
    WindowProfile,
    WindowSystem,
)
from app.schemas.common import ExtraOptionLine
from app.schemas.finestre import (
    FinestreCatalogResponse,
    FinestreConfigurationRequest,
    FinestrePriceBreakdown,
    FinestrePriceCalculationResponse,
)
from app.services.pricing_finestre import ExtraOptionInput, PriceResult, calculate_price

router = APIRouter(prefix="/api", tags=["finestre"])


def validate_and_price(config: FinestreConfigurationRequest, session: Session) -> PriceResult:
    """Valida la configurazione contro il catalogo e calcola il prezzo.

    Condivisa tra POST /api/calculate-price/finestre e
    POST /api/quote-requests/finestre, cosi' entrambi gli endpoint applicano
    esattamente le stesse regole e non c'e' modo di forzare un prezzo diverso
    da quello che il sistema calcolerebbe da solo.
    """
    opening_type = session.get(WindowOpeningType, config.opening_type_id)
    if opening_type is None:
        raise HTTPException(422, detail=f"opening_type_id {config.opening_type_id} non esiste")

    if not (opening_type.min_width_mm <= config.width_mm <= opening_type.max_width_mm):
        raise HTTPException(
            422,
            detail=(
                f"width_mm deve essere tra {opening_type.min_width_mm} e "
                f"{opening_type.max_width_mm} per il tipo '{opening_type.name}'"
            ),
        )
    if not (opening_type.min_height_mm <= config.height_mm <= opening_type.max_height_mm):
        raise HTTPException(
            422,
            detail=(
                f"height_mm deve essere tra {opening_type.min_height_mm} e "
                f"{opening_type.max_height_mm} per il tipo '{opening_type.name}'"
            ),
        )

    material = session.get(WindowMaterial, config.material_id)
    if material is None:
        raise HTTPException(422, detail=f"material_id {config.material_id} non esiste")

    system = session.get(WindowSystem, config.system_id)
    if system is None:
        raise HTTPException(422, detail=f"system_id {config.system_id} non esiste")
    if system.material_id != material.id:
        raise HTTPException(
            422, detail=f"il sistema '{system.name}' non e' disponibile per il materiale '{material.name}'"
        )

    profile = session.get(WindowProfile, config.profile_id)
    if profile is None:
        raise HTTPException(422, detail=f"profile_id {config.profile_id} non esiste")
    if profile.system_id != system.id:
        raise HTTPException(
            422, detail=f"il profilo '{profile.name}' non appartiene al sistema '{system.name}'"
        )

    glass_type = session.get(WindowGlassType, config.glass_type_id)
    if glass_type is None:
        raise HTTPException(422, detail=f"glass_type_id {config.glass_type_id} non esiste")

    color = session.get(WindowColor, config.color_id)
    if color is None:
        raise HTTPException(422, detail=f"color_id {config.color_id} non esiste")

    extra_options: list[ExtraOptionInput] = []
    for option_id in config.extra_option_ids:
        option = session.get(WindowExtraOption, option_id)
        if option is None:
            raise HTTPException(422, detail=f"extra_option_ids contiene un id inesistente: {option_id}")
        extra_options.append(ExtraOptionInput(id=option.id, name=option.name, cost=option.extra_cost))

    return calculate_price(
        width_mm=config.width_mm,
        height_mm=config.height_mm,
        base_price_per_sqm=opening_type.base_price_per_sqm,
        material_name=material.name,
        material_multiplier=material.price_multiplier,
        system_name=system.name,
        system_multiplier=system.price_multiplier,
        profile_name=profile.name,
        profile_multiplier=profile.price_multiplier,
        glass_name=glass_type.name,
        glass_extra_cost=glass_type.extra_cost,
        color_name=color.name,
        color_extra_cost=color.extra_cost,
        extra_options=extra_options,
    )


def build_breakdown(result: PriceResult) -> FinestrePriceBreakdown:
    return FinestrePriceBreakdown(
        area_m2=result.area_m2,
        base_price_area=result.base_price_area,
        material_name=result.material_name,
        material_multiplier=result.material_multiplier,
        price_after_material=result.price_after_material,
        system_name=result.system_name,
        system_multiplier=result.system_multiplier,
        price_after_system=result.price_after_system,
        profile_name=result.profile_name,
        profile_multiplier=result.profile_multiplier,
        price_after_profile=result.price_after_profile,
        glass_name=result.glass_name,
        glass_extra_cost=result.glass_extra_cost,
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


@router.get("/catalog/finestre", response_model=FinestreCatalogResponse)
def get_catalog(session: Session = Depends(get_session)) -> FinestreCatalogResponse:
    """Ritorna tutti i dati di catalogo per la famiglia Finestre (tipi di
    apertura, materiali, sistemi, profili, vetri, colori, opzioni extra) con
    i relativi prezzi. Il frontend usa questa risposta per popolare i
    controlli, senza avere alcun prezzo hardcoded lato client."""

    return FinestreCatalogResponse(
        opening_types=session.exec(select(WindowOpeningType)).all(),
        materials=session.exec(select(WindowMaterial)).all(),
        systems=session.exec(select(WindowSystem)).all(),
        profiles=session.exec(select(WindowProfile)).all(),
        glass_types=session.exec(select(WindowGlassType)).all(),
        colors=session.exec(select(WindowColor)).all(),
        extra_options=session.exec(select(WindowExtraOption)).all(),
    )


@router.post("/calculate-price/finestre", response_model=FinestrePriceCalculationResponse)
def calculate_price_endpoint(
    config: FinestreConfigurationRequest, session: Session = Depends(get_session)
) -> FinestrePriceCalculationResponse:
    result = validate_and_price(config, session)
    return FinestrePriceCalculationResponse(final_price=result.final_price, breakdown=build_breakdown(result))
