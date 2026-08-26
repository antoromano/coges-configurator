from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.db import get_session
from app.models import QuoteRequest
from app.routes import finestre as finestre_routes
from app.routes import pergole as pergole_routes
from app.routes import portoncini as portoncini_routes
from app.schemas.quote_requests import (
    FinestreQuoteRequestCreate,
    PergoleQuoteRequestCreate,
    PortonciniQuoteRequestCreate,
    QuoteRequestCreatedResponse,
    QuoteRequestOut,
    QuoteRequestStatusUpdate,
)
from app.staff_auth import require_staff

router = APIRouter(prefix="/api", tags=["quote-requests"])

_CONTACT_FIELDS = {"customer_name", "customer_email", "customer_phone", "customer_note"}


def _save_quote_request(
    session: Session, product_family: str, payload, final_price: float, breakdown: dict
) -> QuoteRequest:
    configuration = payload.model_dump(exclude=_CONTACT_FIELDS)
    quote_request = QuoteRequest(
        product_family=product_family,
        configuration=configuration,
        final_price=final_price,
        breakdown=breakdown,
        customer_name=payload.customer_name,
        customer_email=payload.customer_email,
        customer_phone=payload.customer_phone,
        customer_note=payload.customer_note,
    )
    session.add(quote_request)
    session.commit()
    session.refresh(quote_request)
    return quote_request


@router.post("/quote-requests/finestre", response_model=QuoteRequestCreatedResponse)
def create_finestre_quote_request(
    payload: FinestreQuoteRequestCreate, session: Session = Depends(get_session)
) -> QuoteRequestCreatedResponse:
    result = finestre_routes.validate_and_price(payload, session)
    breakdown = finestre_routes.build_breakdown(result).model_dump()
    saved = _save_quote_request(session, "finestre", payload, result.final_price, breakdown)
    return QuoteRequestCreatedResponse(id=saved.id, final_price=saved.final_price, status=saved.status)


@router.post("/quote-requests/portoncini", response_model=QuoteRequestCreatedResponse)
def create_portoncini_quote_request(
    payload: PortonciniQuoteRequestCreate, session: Session = Depends(get_session)
) -> QuoteRequestCreatedResponse:
    result = portoncini_routes.validate_and_price(payload, session)
    breakdown = portoncini_routes.build_breakdown(result).model_dump()
    saved = _save_quote_request(session, "portoncini", payload, result.final_price, breakdown)
    return QuoteRequestCreatedResponse(id=saved.id, final_price=saved.final_price, status=saved.status)


@router.post("/quote-requests/pergole", response_model=QuoteRequestCreatedResponse)
def create_pergole_quote_request(
    payload: PergoleQuoteRequestCreate, session: Session = Depends(get_session)
) -> QuoteRequestCreatedResponse:
    result = pergole_routes.validate_and_price(payload, session)
    breakdown = pergole_routes.build_breakdown(result).model_dump()
    saved = _save_quote_request(session, "pergole", payload, result.final_price, breakdown)
    return QuoteRequestCreatedResponse(id=saved.id, final_price=saved.final_price, status=saved.status)


@router.get(
    "/quote-requests",
    response_model=list[QuoteRequestOut],
    dependencies=[Depends(require_staff)],
)
def list_quote_requests(session: Session = Depends(get_session)) -> list[QuoteRequest]:
    statement = select(QuoteRequest).order_by(QuoteRequest.created_at.desc())
    return session.exec(statement).all()


@router.patch(
    "/quote-requests/{quote_request_id}/status",
    response_model=QuoteRequestOut,
    dependencies=[Depends(require_staff)],
)
def update_quote_request_status(
    quote_request_id: int, payload: QuoteRequestStatusUpdate, session: Session = Depends(get_session)
) -> QuoteRequest:
    quote_request = session.get(QuoteRequest, quote_request_id)
    if quote_request is None:
        raise HTTPException(404, detail=f"Richiesta {quote_request_id} non trovata")

    quote_request.status = payload.status
    session.add(quote_request)
    session.commit()
    session.refresh(quote_request)
    return quote_request
