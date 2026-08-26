"""Logica di calcolo del prezzo per la famiglia prodotto "Finestre".

v1 con dati fittizi per il prototipo: vedi SPEC.md per la formula completa
in italiano e per quali dati di catalogo sono reali vs fittizi. Isolata da
modelli DB e route cosi' da poter essere sostituita con la logica di
pricing reale senza toccare il resto dell'applicazione.
"""

from dataclasses import dataclass

# Soglia di area (m2) oltre la quale si applica lo sconto volume, e relativa
# percentuale. Valori fittizi v1, non presenti a catalogo perche' non sono
# ancora modellati come regola configurabile.
AREA_DISCOUNT_THRESHOLD_M2 = 1.5
AREA_DISCOUNT_RATE = 0.10


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


def calculate_price(
    *,
    width_mm: int,
    height_mm: int,
    base_price_per_sqm: float,
    material_name: str,
    material_multiplier: float,
    system_name: str,
    system_multiplier: float,
    profile_name: str,
    profile_multiplier: float,
    glass_name: str,
    glass_extra_cost: float,
    color_name: str,
    color_extra_cost: float,
    extra_options: list[ExtraOptionInput],
) -> PriceResult:
    # 1. Area in m2
    area_m2 = (width_mm * height_mm) / 1_000_000

    # 2. Prezzo base per area (dipende dal tipo di apertura selezionato)
    base_price_area = area_m2 * base_price_per_sqm

    # 3. Moltiplicatori a cascata: materiale -> sistema -> profilo
    price_after_material = base_price_area * material_multiplier
    price_after_system = price_after_material * system_multiplier
    price_after_profile = price_after_system * profile_multiplier

    extra_option_lines = [
        ExtraOptionLine(id=opt.id, name=opt.name, cost=opt.cost) for opt in extra_options
    ]
    extra_options_total = sum(opt.cost for opt in extra_option_lines)

    subtotal_before_discount = (
        price_after_profile + glass_extra_cost + color_extra_cost + extra_options_total
    )

    # Sconto volume oltre la soglia (economia di scala)
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
        profile_name=profile_name,
        profile_multiplier=profile_multiplier,
        price_after_profile=round(price_after_profile, 2),
        glass_name=glass_name,
        glass_extra_cost=glass_extra_cost,
        color_name=color_name,
        color_extra_cost=color_extra_cost,
        extra_options=extra_option_lines,
        extra_options_total=round(extra_options_total, 2),
        subtotal_before_discount=round(subtotal_before_discount, 2),
        volume_discount_applied=volume_discount_applied,
        volume_discount_amount=round(volume_discount_amount, 2),
        final_price=round(final_price, 2),
    )
