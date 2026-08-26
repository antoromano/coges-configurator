import pytest

from app.services.pricing_finestre import ExtraOptionInput, calculate_price

BASE_PRICE_PER_SQM = 180.0


def price(**overrides):
    """Helper: calcola il prezzo con valori di default sovrascrivibili."""
    defaults = dict(
        width_mm=1000,
        height_mm=1000,
        base_price_per_sqm=BASE_PRICE_PER_SQM,
        material_name="Alluminio",
        material_multiplier=1.0,
        system_name="AURA - Profilo Coges",
        system_multiplier=1.0,
        profile_name="COGES 72 TS",
        profile_multiplier=1.0,
        glass_name="Normale",
        glass_extra_cost=0.0,
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
    result = price(width_mm=1000, height_mm=1000)

    assert result.area_m2 == pytest.approx(1.0)
    assert result.base_price_area == pytest.approx(180.0)
    assert result.price_after_material == pytest.approx(180.0)
    assert result.price_after_system == pytest.approx(180.0)
    assert result.price_after_profile == pytest.approx(180.0)
    assert result.volume_discount_applied is False
    assert result.final_price == pytest.approx(180.0)


# ---------------------------------------------------------------------------
# Dimensioni al limite minimo e massimo del range
# ---------------------------------------------------------------------------


def test_dimensioni_limite_minimo():
    # 400x400mm = 0.16 m2
    result = price(width_mm=400, height_mm=400)

    assert result.area_m2 == pytest.approx(0.16)
    assert result.final_price == pytest.approx(28.8)
    assert result.volume_discount_applied is False


def test_dimensioni_limite_massimo():
    # 2000x1500mm = 3.0 m2, sopra soglia sconto volume
    result = price(width_mm=2000, height_mm=1500)

    assert result.area_m2 == pytest.approx(3.0)
    assert result.subtotal_before_discount == pytest.approx(540.0)
    assert result.volume_discount_applied is True
    assert result.final_price == pytest.approx(486.0)  # 540 - 10%


# ---------------------------------------------------------------------------
# Ogni combinazione di materiale: verifica applicazione del moltiplicatore
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "material_name,multiplier,expected_price",
    [
        ("Alluminio", 1.0, 180.0),
        ("PVC", 0.85, 153.0),
        ("PVC-Alluminio", 1.05, 189.0),
        ("Legno", 1.4, 252.0),
        ("Legno-Alluminio", 1.55, 279.0),
    ],
)
def test_moltiplicatore_materiale(material_name, multiplier, expected_price):
    result = price(
        width_mm=1000,
        height_mm=1000,
        material_name=material_name,
        material_multiplier=multiplier,
    )

    assert result.price_after_material == pytest.approx(expected_price)
    assert result.final_price == pytest.approx(expected_price)


# ---------------------------------------------------------------------------
# Moltiplicatori a cascata sistema e profilo
# ---------------------------------------------------------------------------


def test_moltiplicatori_sistema_e_profilo_a_cascata():
    # 180 (base) x1.15 (sistema Schuco AWS) x1.10 (profilo AWS 90) = 227.7
    result = price(
        width_mm=1000,
        height_mm=1000,
        system_name="Schuco AWS - Anta a Vista",
        system_multiplier=1.15,
        profile_name="AWS 90",
        profile_multiplier=1.10,
    )

    assert result.price_after_system == pytest.approx(207.0)
    assert result.price_after_profile == pytest.approx(227.7)
    assert result.final_price == pytest.approx(227.7)


# ---------------------------------------------------------------------------
# Sconto volume: area sopra e sotto la soglia di 1.5 m2
# ---------------------------------------------------------------------------


def test_sconto_volume_area_sotto_soglia():
    # 1500x1000mm = 1.5 m2 esatti: la soglia e' > 1.5, quindi NON scatta
    result = price(width_mm=1500, height_mm=1000)

    assert result.area_m2 == pytest.approx(1.5)
    assert result.volume_discount_applied is False
    assert result.volume_discount_amount == pytest.approx(0.0)


def test_sconto_volume_area_sopra_soglia():
    # 1600x1000mm = 1.6 m2: sopra soglia, sconto 10% applicato
    result = price(width_mm=1600, height_mm=1000)

    assert result.area_m2 == pytest.approx(1.6)
    assert result.volume_discount_applied is True
    expected_subtotal = 1.6 * BASE_PRICE_PER_SQM
    assert result.subtotal_before_discount == pytest.approx(expected_subtotal)
    assert result.final_price == pytest.approx(expected_subtotal * 0.9)


# ---------------------------------------------------------------------------
# Tutte le opzioni extra selezionate contemporaneamente
# ---------------------------------------------------------------------------


def test_tutte_le_opzioni_extra():
    extra_options = [
        ExtraOptionInput(id=1, name="Zanzariera", cost=45.0),
        ExtraOptionInput(id=2, name="Grata di sicurezza", cost=120.0),
        ExtraOptionInput(id=3, name="Apertura motorizzata (Schuco Tip Tronic)", cost=280.0),
    ]

    result = price(
        width_mm=1000,
        height_mm=1000,
        glass_name="Triplo vetro",
        glass_extra_cost=150.0,
        color_name="Nero (RAL 9005)",
        color_extra_cost=50.0,
        extra_options=extra_options,
    )

    assert result.extra_options_total == pytest.approx(445.0)
    assert len(result.extra_options) == 3

    # 180 (base) + 150 (vetro) + 50 (colore) + 445 (extra) = 825, area 1.0 m2 no sconto
    assert result.subtotal_before_discount == pytest.approx(825.0)
    assert result.volume_discount_applied is False
    assert result.final_price == pytest.approx(825.0)
