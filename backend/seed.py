"""Popola il database con i dati fittizi del catalogo v2 (multi-categoria).

Uso:
    python seed.py

Idempotente: se una tabella contiene gia' righe, viene saltata (non duplica
i dati se lo script viene rilanciato).

Provenienza dei dati: nomi di categoria, marche/sistemi (Schuco, AURA,
Dierre, Oikos, KE) e i dati tecnici del profilo AURA sono presi da
cogesinfissi.it (vedi SPEC.md per il dettaglio di cosa e' reale). Tutti i
moltiplicatori e importi di prezzo sono fittizi, per il prototipo.
"""

from sqlmodel import Session, select

from app.db import create_tables, engine
from app.models import (
    DoorBrand,
    DoorColor,
    DoorExtraOption,
    DoorMaterial,
    DoorSecurityClass,
    PergolaColor,
    PergolaExtraOption,
    PergolaMaterial,
    PergolaSystem,
    WindowColor,
    WindowExtraOption,
    WindowGlassType,
    WindowMaterial,
    WindowOpeningType,
    WindowProfile,
    WindowSystem,
)

# ---------------------------------------------------------------------------
# FINESTRE
# ---------------------------------------------------------------------------

WINDOW_OPENING_TYPES = [
    WindowOpeningType(
        name="1 Anta",
        description="Finestra a battente singola anta.",
        base_price_per_sqm=180.0,
        min_width_mm=400,
        max_width_mm=1200,
        min_height_mm=400,
        max_height_mm=1500,
    ),
    WindowOpeningType(
        name="2 Ante",
        description="Finestra a battente a due ante.",
        base_price_per_sqm=195.0,
        min_width_mm=800,
        max_width_mm=2000,
        min_height_mm=400,
        max_height_mm=1500,
    ),
    WindowOpeningType(
        name="Portafinestra",
        description="Finestra a battente che arriva a terra, con accesso pedonale.",
        base_price_per_sqm=210.0,
        min_width_mm=600,
        max_width_mm=1800,
        min_height_mm=1800,
        max_height_mm=2400,
    ),
    WindowOpeningType(
        name="Scorrevole",
        description="Grande apertura scorrevole, tipicamente per ampie vetrate.",
        base_price_per_sqm=260.0,
        min_width_mm=1500,
        max_width_mm=4000,
        min_height_mm=1000,
        max_height_mm=2400,
    ),
]

WINDOW_MATERIALS = [
    WindowMaterial(name="PVC", price_multiplier=0.85),
    WindowMaterial(name="PVC-Alluminio", price_multiplier=1.05),
    WindowMaterial(name="Legno", price_multiplier=1.40),
    WindowMaterial(name="Legno-Alluminio", price_multiplier=1.55),
    WindowMaterial(name="Alluminio", price_multiplier=1.00),
]


def _window_systems(materials_by_name: dict[str, WindowMaterial]) -> list[WindowSystem]:
    return [
        WindowSystem(
            name="PVC 5 Camere Standard",
            material_id=materials_by_name["PVC"].id,
            description="Sistema PVC a 5 camere, buon isolamento termico, soluzione entry-level.",
            price_multiplier=1.00,
        ),
        WindowSystem(
            name="PVC 6 Camere Premium",
            material_id=materials_by_name["PVC"].id,
            description="Sistema PVC a 6 camere, isolamento termico superiore.",
            price_multiplier=1.12,
        ),
        WindowSystem(
            name="PVC-Alluminio Rivestito",
            material_id=materials_by_name["PVC-Alluminio"].id,
            description="Profilo PVC con rivestimento esterno in alluminio.",
            price_multiplier=1.00,
        ),
        WindowSystem(
            name="Legno Lamellare Classico",
            material_id=materials_by_name["Legno"].id,
            description="Legno lamellare a tre strati, estetica tradizionale.",
            price_multiplier=1.00,
        ),
        WindowSystem(
            name="Legno-Alluminio Protetto",
            material_id=materials_by_name["Legno-Alluminio"].id,
            description="Legno internamente, alluminio a protezione esterna.",
            price_multiplier=1.00,
        ),
        WindowSystem(
            name="Schuco AWS - Anta a Vista",
            material_id=materials_by_name["Alluminio"].id,
            description=(
                "Sistema Schuco AWS a taglio termico, isolamento fino a standard Casa "
                "Passiva, design con anta in vista."
            ),
            price_multiplier=1.15,
        ),
        WindowSystem(
            name="Schuco Block System - Anta a Scomparsa",
            material_id=materials_by_name["Alluminio"].id,
            description=(
                "Tecnologia Schuco Block System ad anta a scomparsa: fino al 10% di luce "
                "naturale in piu', ideale per ristrutturazioni."
            ),
            price_multiplier=1.30,
        ),
        WindowSystem(
            name="AURA - Profilo Coges",
            material_id=materials_by_name["Alluminio"].id,
            description="Profilo di design originale Coges Infissi, in lega di alluminio EN AW-6060.",
            price_multiplier=1.20,
        ),
    ]


def _window_profiles(systems_by_name: dict[str, WindowSystem]) -> list[WindowProfile]:
    return [
        WindowProfile(
            name="Profilo Standard 70mm",
            system_id=systems_by_name["PVC 5 Camere Standard"].id,
            description="Profondita' 70mm.",
            price_multiplier=1.00,
        ),
        WindowProfile(
            name="Profilo Premium 76mm",
            system_id=systems_by_name["PVC 6 Camere Premium"].id,
            description="Profondita' 76mm.",
            price_multiplier=1.05,
        ),
        WindowProfile(
            name="Profilo Rivestito 70mm",
            system_id=systems_by_name["PVC-Alluminio Rivestito"].id,
            description="Profondita' 70mm.",
            price_multiplier=1.00,
        ),
        WindowProfile(
            name="Profilo Lamellare 68mm",
            system_id=systems_by_name["Legno Lamellare Classico"].id,
            description="Profondita' 68mm.",
            price_multiplier=1.00,
        ),
        WindowProfile(
            name="Profilo Protetto 78mm",
            system_id=systems_by_name["Legno-Alluminio Protetto"].id,
            description="Profondita' 78mm.",
            price_multiplier=1.00,
        ),
        WindowProfile(
            name="AWS 75",
            system_id=systems_by_name["Schuco AWS - Anta a Vista"].id,
            description="Profondita' 75mm.",
            price_multiplier=1.00,
        ),
        WindowProfile(
            name="AWS 90",
            system_id=systems_by_name["Schuco AWS - Anta a Vista"].id,
            description="Profondita' maggiorata 90mm, per prestazioni superiori.",
            price_multiplier=1.10,
        ),
        WindowProfile(
            name="Block System BS",
            system_id=systems_by_name["Schuco Block System - Anta a Scomparsa"].id,
            description="Profilo a scomparsa nel controtelaio.",
            price_multiplier=1.00,
        ),
        WindowProfile(
            # Dati tecnici REALI, pubblicati su cogesinfissi.it/aura-2/
            # (descrizione di capitolato d'appalto COGES 72 TS).
            name="COGES 72 TS",
            system_id=systems_by_name["AURA - Profilo Coges"].id,
            description=(
                "Profili metallici estrusi in lega primaria alluminio EN AW-6060. "
                "Finiture: verniciatura Qualicoat, ossidazione anodica Qualanod/EURAS-EWAA."
            ),
            air_permeability_class="Classe 4",
            water_tightness_class="Classe 9A",
            wind_resistance_class="Classe C3/B3",
            acoustic_performance_db="Rw 41 dB (C;Ctr)",
            price_multiplier=1.00,
        ),
    ]


WINDOW_GLASS_TYPES = [
    WindowGlassType(name="Normale", extra_cost=0.0),
    WindowGlassType(name="Basso emissivo", extra_cost=80.0),
    WindowGlassType(name="Triplo vetro", extra_cost=150.0),
    WindowGlassType(name="Acustico (fonoisolante)", extra_cost=130.0),
]

WINDOW_COLORS = [
    WindowColor(name="Bianco", extra_cost=0.0),
    WindowColor(name="Grigio (RAL 7016)", extra_cost=30.0),
    WindowColor(name="Nero (RAL 9005)", extra_cost=50.0),
]

WINDOW_EXTRA_OPTIONS = [
    WindowExtraOption(name="Zanzariera", extra_cost=45.0),
    WindowExtraOption(name="Grata di sicurezza", extra_cost=120.0),
    WindowExtraOption(name="Apertura motorizzata (Schuco Tip Tronic)", extra_cost=280.0),
]

# ---------------------------------------------------------------------------
# PORTONCINI
# ---------------------------------------------------------------------------

DOOR_MATERIALS = [
    DoorMaterial(name="Acciaio blindato", price_multiplier=1.00),
    DoorMaterial(name="Alluminio design", price_multiplier=1.25),
    DoorMaterial(name="Legno-Alluminio", price_multiplier=1.35),
]

DOOR_BRANDS = [
    DoorBrand(
        name="Dierre",
        description="Porte blindate dal design italiano, sicurezza dal 1975.",
        price_multiplier=1.00,
    ),
    DoorBrand(
        name="Oikos",
        description="Architetture d'ingresso: design e personalizzazione estrema.",
        price_multiplier=1.35,
    ),
    DoorBrand(
        name="Schuco",
        description="Porte da esterno in alluminio, elevata stabilita' strutturale e isolamento termico.",
        price_multiplier=1.20,
    ),
]

DOOR_SECURITY_CLASSES = [
    DoorSecurityClass(
        name="RC2",
        description="Protezione base contro tentativi di effrazione occasionali.",
        price_multiplier=1.00,
    ),
    DoorSecurityClass(
        name="RC3",
        description="Protezione elevata, standard consigliato per abitazioni.",
        price_multiplier=1.20,
    ),
    DoorSecurityClass(
        name="RC4",
        description="Protezione massima contro effrazione professionale.",
        price_multiplier=1.45,
    ),
]

DOOR_COLORS = [
    DoorColor(name="Bianco", extra_cost=0.0),
    DoorColor(name="Grigio antracite (RAL 7016)", extra_cost=60.0),
    DoorColor(name="Rovere naturale (effetto legno)", extra_cost=90.0),
]

DOOR_EXTRA_OPTIONS = [
    DoorExtraOption(name="Spioncino digitale", extra_cost=150.0),
    DoorExtraOption(name="Maniglione antipanico", extra_cost=180.0),
    DoorExtraOption(name="Serratura maggiorata a 5 punti", extra_cost=220.0),
]

# ---------------------------------------------------------------------------
# PERGOLE
# ---------------------------------------------------------------------------

PERGOLA_MATERIALS = [
    PergolaMaterial(name="Alluminio anodizzato", price_multiplier=1.00),
    PergolaMaterial(name="Alluminio verniciato RAL", price_multiplier=1.15),
]

PERGOLA_SYSTEMS = [
    PergolaSystem(
        name="KE Copertura Fissa",
        description="Struttura fissa, soluzione essenziale per copertura outdoor.",
        price_multiplier=1.00,
    ),
    PergolaSystem(
        name="KE Lamelle Orientabili Bioclimatica",
        description="Lamelle orientabili motorizzate: regolano luce e ventilazione.",
        price_multiplier=1.45,
    ),
]

PERGOLA_COLORS = [
    PergolaColor(name="Bianco", extra_cost=0.0),
    PergolaColor(name="Grigio antracite (RAL 7016)", extra_cost=80.0),
    PergolaColor(name="Testa di moro (RAL 8019)", extra_cost=100.0),
]

PERGOLA_EXTRA_OPTIONS = [
    PergolaExtraOption(name="Chiusure laterali in vetro scorrevoli", extra_cost=850.0),
    PergolaExtraOption(name="Illuminazione LED integrata", extra_cost=320.0),
    PergolaExtraOption(name="Sensori pioggia/vento (chiusura automatica lamelle)", extra_cost=380.0),
]


def seed_table(session: Session, model, rows: list) -> bool:
    """Ritorna True se ha inserito righe, False se la tabella era gia' popolata."""
    existing = session.exec(select(model)).first()
    if existing is not None:
        print(f"  {model.__name__}: gia' popolata, salto.")
        return False
    session.add_all(rows)
    session.flush()
    print(f"  {model.__name__}: inserite {len(rows)} righe.")
    return True


def main() -> None:
    print("Creazione tabelle (se non esistono)...")
    create_tables()

    with Session(engine) as session:
        print("Seed FINESTRE:")
        seed_table(session, WindowOpeningType, WINDOW_OPENING_TYPES)
        seed_table(session, WindowMaterial, WINDOW_MATERIALS)

        materials_by_name = {m.name: m for m in session.exec(select(WindowMaterial)).all()}
        seed_table(session, WindowSystem, _window_systems(materials_by_name))

        systems_by_name = {s.name: s for s in session.exec(select(WindowSystem)).all()}
        seed_table(session, WindowProfile, _window_profiles(systems_by_name))

        seed_table(session, WindowGlassType, WINDOW_GLASS_TYPES)
        seed_table(session, WindowColor, WINDOW_COLORS)
        seed_table(session, WindowExtraOption, WINDOW_EXTRA_OPTIONS)

        print("Seed PORTONCINI:")
        seed_table(session, DoorMaterial, DOOR_MATERIALS)
        seed_table(session, DoorBrand, DOOR_BRANDS)
        seed_table(session, DoorSecurityClass, DOOR_SECURITY_CLASSES)
        seed_table(session, DoorColor, DOOR_COLORS)
        seed_table(session, DoorExtraOption, DOOR_EXTRA_OPTIONS)

        print("Seed PERGOLE:")
        seed_table(session, PergolaMaterial, PERGOLA_MATERIALS)
        seed_table(session, PergolaSystem, PERGOLA_SYSTEMS)
        seed_table(session, PergolaColor, PERGOLA_COLORS)
        seed_table(session, PergolaExtraOption, PERGOLA_EXTRA_OPTIONS)

        session.commit()

    print("Seed completato.")


if __name__ == "__main__":
    main()
