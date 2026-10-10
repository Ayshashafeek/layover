"""Payment routes — SIMULATED only. No real money moves in the MVP."""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_current_user
from app.core.security import AuthenticatedUser
from app.repositories.memory_store import STORE
from app.schemas.core import PaymentCreate, PaymentResponse

router = APIRouter(prefix="/api/payments", tags=["payments"])


@router.post("/pay", response_model=PaymentResponse, status_code=201)
def pay_share(
    body: PaymentCreate,
    user: AuthenticatedUser = Depends(get_current_user),
) -> dict:
    """Simulate paying your share of a booking.

    The amount is read from the caller's `booking_members.cost_share` — never
    from the request body (server-side price enforcement).
    """
    booking = STORE.bookings.get(body.booking_id)
    if booking is None:
        raise HTTPException(404, "Booking not found")
    membership = next(
        (m for m in booking["members"] if m["user_id"] == user.id), None
    )
    if membership is None:
        raise HTTPException(403, "You are not a member of this booking")
    if membership["payment_status"] != "unpaid":
        raise HTTPException(409, f"Share is already {membership['payment_status']}")

    payment_id = str(uuid4())
    payment = {
        "id": payment_id,
        "booking_id": booking["id"],
        "payer_id": user.id,
        "amount": membership["cost_share"],
        "currency": membership["currency"],
        "status": "simulated_paid",
        "transaction_ref": f"SIM-{uuid4().hex[:12].upper()}",
        "simulated": True,
        "created_at": datetime.now().isoformat(),
    }
    STORE.payments[payment_id] = payment
    membership["payment_status"] = "paid"

    # All members paid -> booking is confirmed (SIMULATED confirmation).
    if all(m["payment_status"] == "paid" for m in booking["members"]):
        booking["status"] = "confirmed"

    return payment


@router.post("/refund", response_model=PaymentResponse)
def refund(
    body: PaymentCreate,
    user: AuthenticatedUser = Depends(get_current_user),
) -> dict:
    """Refund the caller's (simulated) payment for a booking."""
    booking = STORE.bookings.get(body.booking_id)
    if booking is None:
        raise HTTPException(404, "Booking not found")
    membership = next((m for m in booking["members"] if m["user_id"] == user.id), None)
    if membership is None:
        raise HTTPException(403, "You are not a member of this booking")
    if membership["payment_status"] != "paid":
        raise HTTPException(409, "Nothing to refund for this member")

    payment = next(
        (
            p
            for p in STORE.payments.values()
            if p["booking_id"] == booking["id"] and p["payer_id"] == user.id
            and p["status"] == "simulated_paid"
        ),
        None,
    )
    if payment is None:
        raise HTTPException(409, "No paid payment record found")

    payment["status"] = "simulated_refunded"
    membership["payment_status"] = "refunded"
    if booking["status"] == "confirmed":
        booking["status"] = "pending"
    return payment


@router.get("/mine", response_model=list[PaymentResponse])
def my_payments(user: AuthenticatedUser = Depends(get_current_user)) -> list[dict]:
    out = [p for p in STORE.payments.values() if p["payer_id"] == user.id]
    return out
