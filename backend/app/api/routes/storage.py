"""Storage routes: facility discovery & shared-cost quotes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_current_user
from app.core.security import AuthenticatedUser
from app.repositories.memory_store import STORE
from app.schemas.core import QuoteRequest, SharedQuoteResponse, StorageFacility
from app.services.pricing_service import SharedQuote, quote as compute_quote

router = APIRouter(prefix="/api/storage", tags=["storage"])


@router.get("", response_model=list[StorageFacility])
def list_facilities(
    airport: str | None = None,
    user: AuthenticatedUser = Depends(get_current_user),
) -> list[dict]:
    """List storage facilities. Data comes from seed / SIMULATED providers."""
    rows = list(STORE.storage_facilities.values())
    if airport:
        rows = [r for r in rows if r["airport_code"].upper() == airport.upper()]
    return rows


@router.post("/quote", response_model=SharedQuoteResponse)
def shared_quote(
    body: QuoteRequest,
    user: AuthenticatedUser = Depends(get_current_user),
) -> dict:
    """Compute a shared-locker quote. Prices come ONLY from the facility row."""
    facility = STORE.storage_facilities.get(body.facility_id)
    if facility is None:
        raise HTTPException(404, "Storage facility not found")
    try:
        q: SharedQuote = compute_quote(
            facility, hours=body.hours, bags=body.bags, people=body.people
        )
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc
    return q.__dict__
