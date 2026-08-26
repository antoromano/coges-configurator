import pytest

from app.services.pricing_portoncini import BASE_PRICE_PER_SQM, ExtraOptionInput, calculate_price


def price(**overrides):
    defaults = dict(
        width_mm=1000,
        height_mm=2000,
        material_name="Acciaio blindato",
        material_multiplier=1.0,
        brand_name="Dierre",
        brand_multiplier=1.0,
        security_class_name="RC2",
        security_class_multiplier=1.0,
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
    result = price(width_mm=1000, height_mm=2000)

    assert result.area_m2 == pytest.approx(2.0)
    assert result.base_price_area == pytest.approx(2.0 * BASE_PRICE_PER_SQM)
    assert result.final_price == pytest.approx(840.0)


# ---------------------------------------------------------------------------
# Dimensioni al limite minimo e massimo del range (700-1300 x 2000-2400)
# ---------------------------------------------------------------------------


def test_dimensioni_limite_minimo():
    result = price(width_mm=700, height_mm=2000)

    assert result.area_m2 == pytest.approx(1.4)
    assert result.final_price == pytest.approx(1.4 * BASE_PRICE_PER_SQM)


def test_dimensioni_limite_massimo():
    result = price(width_mm=1300, height_mm=2400)

    assert result.area_m2 == pytest.approx(3.12)
    assert result.final_price == pytest.approx(3.12 * BASE_PRICE_PER_SQM)


# ---------------------------------------------------------------------------
# Ogni combinazione di materiale
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "material_name,multiplier,expected_price",
    [
        ("Acciaio blindato", 1.00, 840.0),
        ("Alluminio design", 1.25, 1050.0),
        ("Legno-Alluminio", 1.35, 1134.0),
    ],
)
def test_moltiplicatore_materiale(material_name, multiplier, expected_price):
    result = price(material_name=material_name, material_multiplier=multiplier)

    assert result.final_price == pytest.approx(expected_price)


# ---------------------------------------------------------------------------
# Moltiplicatori a cascata: materiale -> brand -> classe di sicurezza
# ---------------------------------------------------------------------------


def test_moltiplicatori_a_cascata():
    result = price(
        material_name="Alluminio design",
        material_multiplier=1.25,
        brand_name="Oikos",
        brand_multiplier=1.35,
        security_class_name="RC4",
        security_class_multiplier=1.45,
    )

    assert result.price_after_material == pytest.approx(1050.0)
    assert result.price_after_brand == pytest.approx(1417.5)
    assert result.price_after_security_class == pytest.approx(2055.375, rel=1e-3)
    assert result.final_price == pytest.approx(2055.375, rel=1e-3)


# ---------------------------------------------------------------------------
# Tutte le opzioni extra selezionate contemporaneamente
# ---------------------------------------------------------------------------


def test_tutte_le_opzioni_extra():
    extra_options = [
        ExtraOptionInput(id=1, name="Spioncino digitale", cost=150.0),
        ExtraOptionInput(id=2, name="Maniglione antipanico", cost=180.0),
        ExtraOptionInput(id=3, name="Serratura maggiorata a 5 punti", cost=220.0),
    ]

    result = price(
        color_name="Grigio antracite (RAL 7016)",
        color_extra_cost=60.0,
        extra_options=extra_options,
    )

    assert result.extra_options_total == pytest.approx(550.0)
    assert len(result.extra_options) == 3
    # 840 (base, materiale/brand/sicurezza a moltiplicatore 1.0) + 60 (colore) + 550 (extra)
    assert result.final_price == pytest.approx(1450.0)
