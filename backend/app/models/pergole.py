"""Tabelle di catalogo per la famiglia prodotto "Pergole" (pergole
bioclimatiche outdoor). Marca di riferimento (KE Outdoor Design) presa da
cogesinfissi.it/pergole/; moltiplicatori di prezzo fittizi."""

from typing import Optional

from sqlmodel import Field

from app.models.base import TimestampMixin


class PergolaMaterial(TimestampMixin, table=True):
    """Finitura della struttura in alluminio (es. Anodizzato, Verniciato RAL)."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    price_multiplier: float


class PergolaSystem(TimestampMixin, table=True):
    """Tipo di copertura (es. Fissa, Lamelle orientabili bioclimatiche)."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    description: str
    price_multiplier: float


class PergolaColor(TimestampMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    extra_cost: float


class PergolaExtraOption(TimestampMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    extra_cost: float
