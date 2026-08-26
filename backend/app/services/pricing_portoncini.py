"""Logica di calcolo del prezzo per la famiglia prodotto "Portoncini".

v1 con dati fittizi per il prototipo: vedi SPEC.md per la formula completa
in italiano. A differenza delle Finestre, non e' applicato uno sconto
volume: un portoncino e' un'unita' singola con range dimensionale ristretto
(porta a battente singola), non ha la stessa logica di economia di scala di
una grande vetrata.
"""

from dataclasses import dataclass

# Prezzo base al m2, fittizio: piu' alto delle finestre per riflettere la
# maggiore robustezza/sicurezza costruttiva di una porta blindata.
BASE_PRICE_PER_SQM = 420.0


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


def calculate_price(
    *,
    width_mm: int,
    height_mm: int,
    material_name: str,
    material_multiplier: float,
    brand_name: str,
    brand_multiplier: float,
    security_class_name: str,
    security_class_multiplier: float,
    color_name: str,
    color_extra_cost: float,
    extra_options: list[ExtraOptionInput],
) -> PriceResult:
    area_m2 = (width_mm * height_mm) / 1_000_000

    base_price_area = area_m2 * BASE_PRICE_PER_SQM

    price_after_material = base_price_area * material_multiplier
    price_after_brand = price_after_material * brand_multiplier
    price_after_security_class = price_after_brand * security_class_multiplier

    extra_option_lines = [
        ExtraOptionLine(id=opt.id, name=opt.name, cost=opt.cost) for opt in extra_options
    ]
    extra_options_total = sum(opt.cost for opt in extra_option_lines)

    final_price = price_after_security_class + color_extra_cost + extra_options_total

    return PriceResult(
        area_m2=round(area_m2, 4),
        base_price_area=round(base_price_area, 2),
        material_name=material_name,
        material_multiplier=material_multiplier,
        price_after_material=round(price_after_material, 2),
        brand_name=brand_name,
        brand_multiplier=brand_multiplier,
        price_after_brand=round(price_after_brand, 2),
        security_class_name=security_class_name,
        security_class_multiplier=security_class_multiplier,
        price_after_security_class=round(price_after_security_class, 2),
        color_name=color_name,
        color_extra_cost=color_extra_cost,
        extra_options=extra_option_lines,
        extra_options_total=round(extra_options_total, 2),
        final_price=round(final_price, 2),
    )
