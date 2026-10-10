"""Booking routes: create / list / get / cancel.

All authorization and price calculation happens server-side. The client never
sets total_price, user ids, member permissions or payment status.
"""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_current_user
from app.core.security import AuthenticatedUser
from app.repositories.memory_store import STORE
from app.schemas.core import Booking, BookingCreate, BookingMember
from app.services.booking_service import (
    BookingValidationError,
    can_cancel,
    member_shares,
    validate_booking,
)

router = APIRouter(prefix="/api/bookings", tags=["bookings"])


@router.post("", response_model=Booking, status_code=201)
def create_booking(
    body: BookingCreate,
    user: AuthenticatedUser = Depends(get_current_user),
) -> dict:
    facility = STORE.storage_facilities.get(body.facility_id)
    if facility is None:
        raise HTTPException(404, "Storage facility not found")
    layover = STORE.layovers.get(body.layover_id)
    if layover is None:
        raise HTTPException(404, "Layover not found")
    if layover["user_id"] != user.id:
        raise HTTPException(403, "You do not own this layover")

    try:
        validated = validate_booking(
            facility,
            layover,
            starts_at=body.starts_at,
            ends_at=body.ends_at,
            people=body.people,
        )
    except BookingValidationError as exc:
        raise HTTPException(422, str(exc)) from exc

    booking_id = str(uuid4())
    shares = member_shares(validated["total_price"], validated["people"])
    members: list[dict] = []
    for idx, share in enumerate(shares):
        members.append(
            {
                "user_id": user.id if idx == 0 else f"invited-{idx}",
                "cost_share": share,
                "currency": validated["currency"],
                "payment_status": "unpaid",
                "can_retrieve": idx == 0,  # creator can retrieve, others on check-in
            }
        )

    booking = {
        "id": booking_id,
        "facility_id": facility["id"],
        "created_by": user.id,
        "layover_id": layover["id"],
        "starts_at": validated["starts_at"],
        "ends_at": validated["ends_at"],
        "total_price": validated["total_price"],
        "currency": validated["currency"],
        "status": "pending",
        "members": members,
        "created_at": datetime.now().isoformat(),
    }
    STORE.bookings[booking_id] = booking
    STORE.access_logs.append(
        {
            "id": str(uuid4()),
            "booking_id": booking_id,
            "user_id": user.id,
            "action": "booking.created",
            "created_at": datetime.now().isoformat(),
        }
    )
    return booking


@router.get("/mine", response_model=list[Booking])
def my_bookings(user: AuthenticatedUser = Depends(get_current_user)) -> list[dict]:
    out = [b for b in STORE.bookings.values() if b["created_by"] == user.id]
    return out


@router.get("/{booking_id}", response_model=Booking)
def get_booking(
    booking_id: str,
    user: AuthenticatedUser = Depends(get_current_user),
) -> dict:
    booking = STORE.bookings.get(booking_id)
    if booking is None:
        raise HTTPException(404, "Booking not found")
    if user.id not in (booking["created_by"], *(m["user_id"] for m in booking["members"])):
        raise HTTPException(403, "Not a participant of this booking")
    return booking


@router.post("/{booking_id}/cancel", response_model=Booking)
def cancel_booking(
    booking_id: str,
    user: AuthenticatedUser = Depends(get_current_user),
) -> dict:
    booking = STORE.bookings.get(booking_id)
    if booking is None:
        raise HTTPException(404, "Booking not found")
    if not can_cancel(booking, user.id):
        raise HTTPException(
            409, "Booking cannot be cancelled (not creator, already cancelled, or started)"
        )
    booking["status"] = "cancelled"
    STORE.access_logs.append(
        {
            "id": str(uuid4()),
            "booking_id": booking_id,
            "user_id": user.id,
            "action": "booking.cancelled",
            "created_at": datetime.now().isoformat(),
        }
    )
    return booking
