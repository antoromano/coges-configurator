"""Tabelle di catalogo per la famiglia prodotto "Portoncini" (porte
d'ingresso blindate). Marche di riferimento (Dierre, Oikos, Schuco) prese
da cogesinfissi.it/portoncini/; moltiplicatori di prezzo fittizi."""

from typing import Optional

from sqlmodel import Field

from app.models.base import TimestampMixin


class DoorMaterial(TimestampMixin, table=True):
    """Materiale strutturale della porta (es. Acciaio blindato, Alluminio)."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    price_multiplier: float


class DoorBrand(TimestampMixin, table=True):
    """Marca/linea produttore (es. Dierre, Oikos, Schuco)."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    description: str
    price_multiplier: float


class DoorSecurityClass(TimestampMixin, table=True):
    """Classe di resistenza all'effrazione (nomenclatura standard EN 1627
    RC2-RC4; descrizioni indicative, non certificazioni di uno specifico
    prodotto)."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    description: str
    price_multiplier: float


class DoorColor(TimestampMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    extra_cost: float


class DoorExtraOption(TimestampMixin, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    extra_cost: float
