import pytest
from fastapi import HTTPException

from app import staff_auth


def test_token_corretto_passa(monkeypatch):
    monkeypatch.setattr(staff_auth, "STAFF_ACCESS_TOKEN", "segreto-corretto")
    # non deve sollevare eccezioni
    staff_auth.require_staff(x_staff_token="segreto-corretto")


def test_token_errato_viene_rifiutato(monkeypatch):
    monkeypatch.setattr(staff_auth, "STAFF_ACCESS_TOKEN", "segreto-corretto")
    with pytest.raises(HTTPException) as exc_info:
        staff_auth.require_staff(x_staff_token="tentativo-sbagliato")
    assert exc_info.value.status_code == 401


def test_token_mancante_viene_rifiutato(monkeypatch):
    monkeypatch.setattr(staff_auth, "STAFF_ACCESS_TOKEN", "segreto-corretto")
    with pytest.raises(HTTPException) as exc_info:
        staff_auth.require_staff(x_staff_token="")
    assert exc_info.value.status_code == 401


def test_password_non_configurata_rifiuta_sempre(monkeypatch):
    # Se STAFF_ACCESS_TOKEN non e' impostata (stringa vuota), l'accesso deve
    # essere negato di default (fail-closed), anche con un token vuoto.
    monkeypatch.setattr(staff_auth, "STAFF_ACCESS_TOKEN", "")
    with pytest.raises(HTTPException) as exc_info:
        staff_auth.require_staff(x_staff_token="")
    assert exc_info.value.status_code == 401
