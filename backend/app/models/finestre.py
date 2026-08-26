"""Tabelle di catalogo per la famiglia prodotto "Finestre" (infissi in
apertura: finestre, portefinestre, scorrevoli).

Gerarchia di selezione, sul modello di configuratori reali del settore:
Materiale -> Sistema (marca/linea produttore) -> Profilo (variante tecnica
specifica del sistema). Vedi SPEC.md per quali dati tecnici sono reali
(profilo AURA, pubblicato su cogesinfissi.it) e quali sono fittizi/plausibili
per il prototipo (tutti i moltiplicatori di prezzo).
"""

from typing import Optional

from sqlmodel import Field

from app.models.base import TimestampMixin


class WindowMaterial(TimestampMixin, table=True):
    """Materiale del telaio (es. PVC, Alluminio, Legno)."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    price_multiplier: float


class WindowSystem(TimestampMixin, table=True):
    """Sistema/linea del produttore, disponibile per un dato materiale
    (es. "Schuco AWS - Anta a Vista" per il materiale Alluminio)."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    material_id: int = Field(foreign_key="windowmaterial.id")
    description: str
    price_multiplier: float


class WindowProfile(TimestampMixin, table=True):
    """Variante tecnica specifica all'interno di un Sistema, con eventuali
    dati tecnici certificati (solo per il profilo AURA sono dati reali
    pubblicati da Coges; per gli altri sistemi restano vuoti perche' non
    verificati, per non attribuire certificazioni non confermate a marchi
    reali come Schuco)."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    system_id: int = Field(foreign_key="windowsystem.id")
    description: str

    air_permeability_class: Optional[str] = Field(default=None)
    water_tightness_class: Optional[str] = Field(default=None)
    wind_resistance_class: Optional[str] = Field(default=None)
    acoustic_performance_db: Optional[str] = Field(default=None)

    price_multiplier: float


class WindowOpeningType(TimestampMixin, table=True):
    """Tipo di apertura/prodotto (1 anta, 2 ante, portafinestra, scorrevole),
    ciascuno con proprio range dimensionale e prezzo base al m2."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    description: str
    base_price_per_sqm: float
    min_width_mm: int
    max_width_mm: int
    min_height_mm: int
    max_height_mm: int


class WindowGlassType(TimestampMixin, table=True):
    """Tipo di vetro (es. Normale, Basso emissivo, Triplo vetro, Acustico)."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    extra_cost: float


class WindowColor(TimestampMixin, table=True):
    """Colore/rivestimento del telaio."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    extra_cost: float


class WindowExtraOption(TimestampMixin, table=True):
    """Opzione extra selezionabile (es. Zanzariera, Grata di sicurezza)."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    extra_cost: float
