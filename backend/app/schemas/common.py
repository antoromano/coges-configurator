"""Schemi Pydantic condivisi tra le famiglie prodotto."""

from pydantic import BaseModel


class ExtraOptionLine(BaseModel):
    id: int
    name: str
    cost: float
