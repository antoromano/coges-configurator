import pytest

from app.services.pricing_pergole import BASE_PRICE_PER_SQM, ExtraOptionInput, calculate_price


def price(**overrides):
    defaults = dict(
        width_mm=3000,
        depth_mm=3000,
        material_name="Alluminio anodizzato",
        material_multiplier=1.0,
        system_name="KE Copertura Fissa",
        system_multiplier=1.0,
        color_name="Bianco",
        color_extra_cost=0.0,
        extra_options=[],
    )
    defaults.update(overrides)
    return calculate_price(**defaults)


# ---------------------------------------------------------------------------
# Caso base con valori medi
# ---------------------------------------------------------------------------


def test_caso_base_valori_medi():
    result = price(width_mm=3000, depth_mm=3000)

    assert result.area_m2 == pytest.approx(9.0)
    assert result.base_price_area == pytest.approx(9.0 * BASE_PRICE_PER_SQM)
    assert result.volume_discount_applied is False
    assert result.final_price == pytest.approx(2340.0)


# ---------------------------------------------------------------------------
# Dimensioni al limite minimo e massimo del range (2000-6000 x 2000-4000)
# ---------------------------------------------------------------------------


def test_dimensioni_limite_minimo():
    result = price(width_mm=2000, depth_mm=2000)

    assert result.area_m2 == pytest.approx(4.0)
    assert result.final_price == pytest.approx(1040.0)


def test_dimensioni_limite_massimo():
    # 24 m2, sopra soglia sconto volume (15 m2)
    result = price(width_mm=6000, depth_mm=4000)

    assert result.area_m2 == pytest.approx(24.0)
    assert result.volume_discount_applied is True
    assert result.subtotal_before_discount == pytest.approx(6240.0)
    assert result.final_price == pytest.approx(5740.8)  # 6240 - 8%


# ---------------------------------------------------------------------------
# Ogni combinazione di materiale e sistema: verifica applicazione moltiplicatore
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "material_name,multiplier,expected_price",
    [
        ("Alluminio anodizzato", 1.00, 2340.0),
        ("Alluminio verniciato RAL", 1.15, 2691.0),
    ],
)
def test_moltiplicatore_materiale(material_name, multiplier, expected_price):
    result = price(material_name=material_name, material_multiplier=multiplier)

    assert result.final_price == pytest.approx(expected_price)


@pytest.mark.parametrize(
    "system_name,multiplier,expected_price",
    [
        ("KE Copertura Fissa", 1.00, 2340.0),
        ("KE Lamelle Orientabili Bioclimatica", 1.45, 3393.0),
    ],
)
def test_moltiplicatore_sistema(system_name, multiplier, expected_price):
    result = price(system_name=system_name, system_multiplier=multiplier)

    assert result.final_price == pytest.approx(expected_price)


# ---------------------------------------------------------------------------
# Sconto volume: area sopra e sotto la soglia di 15 m2
# ---------------------------------------------------------------------------


def test_sconto_volume_area_sotto_soglia():
    # 5000x3000mm = 15 m2 esatti: la soglia e' > 15, quindi NON scatta
    result = price(width_mm=5000, depth_mm=3000)

    assert result.area_m2 == pytest.approx(15.0)
    assert result.volume_discount_applied is False
    assert result.final_price == pytest.approx(3900.0)


def test_sconto_volume_area_sopra_soglia():
    # 5000x3100mm = 15.5 m2: sopra soglia, sconto 8% applicato
    result = price(width_mm=5000, depth_mm=3100)

    assert result.area_m2 == pytest.approx(15.5)
    assert result.volume_discount_applied is True
    expected_subtotal = 15.5 * BASE_PRICE_PER_SQM
    assert result.subtotal_before_discount == pytest.approx(expected_subtotal)
    assert result.final_price == pytest.approx(expected_subtotal * 0.92)


# ---------------------------------------------------------------------------
# Tutte le opzioni extra selezionate contemporaneamente
# ---------------------------------------------------------------------------


def test_tutte_le_opzioni_extra():
    extra_options = [
        ExtraOptionInput(id=1, name="Chiusure laterali in vetro scorrevoli", cost=850.0),
        ExtraOptionInput(id=2, name="Illuminazione LED integrata", cost=320.0),
        ExtraOptionInput(id=3, name="Sensori pioggia/vento (chiusura automatica lamelle)", cost=380.0),
    ]

    result = price(
        color_name="Grigio antracite (RAL 7016)",
        color_extra_cost=80.0,
        extra_options=extra_options,
    )

    assert result.extra_options_total == pytest.approx(1550.0)
    assert len(result.extra_options) == 3
    # 2340 (base) + 80 (colore) + 1550 (extra) = 3970, area 9 m2 no sconto
    assert result.subtotal_before_discount == pytest.approx(3970.0)
    assert result.volume_discount_applied is False
    assert result.final_price == pytest.approx(3970.0)
