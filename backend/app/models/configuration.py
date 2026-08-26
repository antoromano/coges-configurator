from typing import Any, Optional

from sqlalchemy import JSON, Column
from sqlmodel import Field

from app.models.base import TimestampMixin

STATUS_IN_ATTESA = "in_attesa"
STATUS_CONFERMATO = "confermato"
STATUS_RIFIUTATO = "rifiutato"


class QuoteRequest(TimestampMixin, table=True):
    """Richiesta di preventivo inviata da un cliente dal configuratore.

    Il prezzo mostrato in configurazione e' una stima indicativa non
    vincolante (vedi PriceBreakdown nel frontend): diventa un'offerta reale
    solo dopo la conferma di un membro dello staff Coges tramite la pagina
    interna protetta da password (vedi app/staff_auth.py).

    La forma della configurazione varia per famiglia prodotto (finestre,
    portoncini, pergole hanno parametri diversi), quindi e' salvata come
    JSON invece di colonne fisse - stessa forma del corpo della request
    POST /api/calculate-price/{family}.
    """

    id: Optional[int] = Field(default=None, primary_key=True)

    product_family: str = Field(index=True)  # "finestre" | "portoncini" | "pergole"

    configuration: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    final_price: float
    breakdown: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))

    customer_name: str
    customer_email: str
    customer_phone: str
    customer_note: str = Field(default="")

    status: str = Field(default=STATUS_IN_ATTESA, index=True)
