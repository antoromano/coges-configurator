"""Schemi Pydantic per l'invio e la gestione delle richieste di preventivo.

Il body di invio accetta la stessa configurazione di
POST /api/calculate-price/{family} (vedi schemas/finestre.py, portoncini.py,
pergole.py) piu' i dati di contatto del cliente. Il prezzo NON viene accettato
dal client: viene sempre ricalcolato lato server con lo stesso servizio di
pricing usato da /api/calculate-price, per evitare che un client malevolo
possa inviare un prezzo manomesso.
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.schemas.finestre import FinestreConfigurationRequest
from app.schemas.pergole import PergoleConfigurationRequest
from app.schemas.portoncini import PortonciniConfigurationRequest


class CustomerContact(BaseModel):
    customer_name: str = Field(min_length=1, max_length=200)
    customer_email: EmailStr
    customer_phone: str = Field(min_length=1, max_length=50)
    customer_note: str = Field(default="", max_length=2000)


class FinestreQuoteRequestCreate(FinestreConfigurationRequest, CustomerContact):
    pass


class PortonciniQuoteRequestCreate(PortonciniConfigurationRequest, CustomerContact):
    pass


class PergoleQuoteRequestCreate(PergoleConfigurationRequest, CustomerContact):
    pass


class QuoteRequestCreatedResponse(BaseModel):
    id: int
    final_price: float
    status: str


class QuoteRequestOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_family: str
    configuration: dict[str, Any]
    final_price: float
    breakdown: dict[str, Any]
    customer_name: str
    customer_email: str
    customer_phone: str
    customer_note: str
    status: str
    created_at: datetime


class QuoteRequestStatusUpdate(BaseModel):
    status: str = Field(pattern="^(in_attesa|confermato|rifiutato)$")
