"""Protezione minima per gli endpoint staff (lista richieste di preventivo).

Password condivisa unica (STAFF_ACCESS_TOKEN in .env), non un vero sistema di
account: sufficiente per il prototipo, dove la lista viene consultata da un
piccolo team Coges. Se in futuro servira' distinguere chi ha confermato cosa,
questo va sostituito con account individuali.
"""

import hmac

from fastapi import Header, HTTPException

from app.config import STAFF_ACCESS_TOKEN


def require_staff(x_staff_token: str = Header(default="")) -> None:
    if not STAFF_ACCESS_TOKEN or not hmac.compare_digest(x_staff_token, STAFF_ACCESS_TOKEN):
        raise HTTPException(401, detail="Accesso staff non autorizzato")
