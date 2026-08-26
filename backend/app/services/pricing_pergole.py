"""Logica di calcolo del prezzo per la famiglia prodotto "Pergole".

v1 con dati fittizi per il prototipo: vedi SPEC.md per la formula completa
in italiano. Soglia e percentuale di sconto volume diverse dalle Finestre,
perche' le superfici tipiche di una pergola sono molto piu' grandi (alcuni
m2 contro alcune decine di m2).
"""

from dataclasses import dataclass

BASE_PRICE_PER_SQM = 260.0
AREA_DISCOUNT_THRESHOLD_M2 = 15.0
AREA_DISCOUNT_RATE = 0.08


@dataclass
class ExtraOptionInput:
    id: int
    name: str
    cost: float


@dataclass
class ExtraOptionLine:
    id: int
    name: str
    cost: float


@dataclass
class PriceResult:
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


def calculate_price(
    *,
    width_mm: int,
    depth_mm: int,
    material_name: str,
    material_multiplier: float,
    system_name: str,
    system_multiplier: float,
    color_name: str,
    color_extra_cost: float,
    extra_options: list[ExtraOptionInput],
) -> PriceResult:
    area_m2 = (width_mm * depth_mm) / 1_000_000

    base_price_area = area_m2 * BASE_PRICE_PER_SQM

    price_after_material = base_price_area * material_multiplier
    price_after_system = price_after_material * system_multiplier

    extra_option_lines = [
        ExtraOptionLine(id=opt.id, name=opt.name, cost=opt.cost) for opt in extra_options
    ]
    extra_options_total = sum(opt.cost for opt in extra_option_lines)

    subtotal_before_discount = price_after_system + color_extra_cost + extra_options_total

    volume_discount_applied = area_m2 > AREA_DISCOUNT_THRESHOLD_M2
    volume_discount_amount = (
        subtotal_before_discount * AREA_DISCOUNT_RATE if volume_discount_applied else 0.0
    )

    final_price = subtotal_before_discount - volume_discount_amount

    return PriceResult(
        area_m2=round(area_m2, 4),
        base_price_area=round(base_price_area, 2),
        material_name=material_name,
        material_multiplier=material_multiplier,
        price_after_material=round(price_after_material, 2),
        system_name=system_name,
        system_multiplier=system_multiplier,
        price_after_system=round(price_after_system, 2),
        color_name=color_name,
        color_extra_cost=color_extra_cost,
        extra_options=extra_option_lines,
        extra_options_total=round(extra_options_total, 2),
        subtotal_before_discount=round(subtotal_before_discount, 2),
        volume_discount_applied=volume_discount_applied,
        volume_discount_amount=round(volume_discount_amount, 2),
        final_price=round(final_price, 2),
    )
