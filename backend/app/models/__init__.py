from app.models.configuration import QuoteRequest
from app.models.finestre import (
    WindowColor,
    WindowExtraOption,
    WindowGlassType,
    WindowMaterial,
    WindowOpeningType,
    WindowProfile,
    WindowSystem,
)
from app.models.pergole import (
    PergolaColor,
    PergolaExtraOption,
    PergolaMaterial,
    PergolaSystem,
)
from app.models.portoncini import (
    DoorBrand,
    DoorColor,
    DoorExtraOption,
    DoorMaterial,
    DoorSecurityClass,
)

__all__ = [
    "QuoteRequest",
    # Finestre
    "WindowMaterial",
    "WindowSystem",
    "WindowProfile",
    "WindowOpeningType",
    "WindowGlassType",
    "WindowColor",
    "WindowExtraOption",
    # Portoncini
    "DoorMaterial",
    "DoorBrand",
    "DoorSecurityClass",
    "DoorColor",
    "DoorExtraOption",
    # Pergole
    "PergolaMaterial",
    "PergolaSystem",
    "PergolaColor",
    "PergolaExtraOption",
]
