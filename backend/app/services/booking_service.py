"""Booking business rules and validation.

Route handlers call these helpers before persisting bookings. All critical
decisions (price, permissions, status) are made here, never trusted from the
client.
"""

from __future__ import annotations

from datetime import datetime

from app.services.pricing_service import quote as shared_quote
from app.services.pricing_service import round2


class BookingValidationError(Exception):
    """Raised when a booking request violates business rules."""


def validate_booking(
    facility: dict,
    layover: dict,
    starts_at: datetime,
    ends_at: datetime,
    people: int,
) -> dict:
    """Validate a prospective booking; returns the canonical booking payload.

    Raises BookingValidationError on any rule violation.
    """
    if ends_at <= starts_at:
        raise BookingValidationError("Booking must end after it starts")

    if starts_at < datetime.now(starts_at.tzinfo):
        raise BookingValidationError("Booking cannot start in the past")

    layover_start = layover["arrival_time"]
    layover_end = layover["departure_time"]
    if starts_at < layover_start or ends_at > layover_end:
        raise BookingValidationError("Booking window must fall inside the layover")

    facility_open = facility["opening_time"]
    facility_close = facility["closing_time"]
    start_time = starts_at.time().isoformat("minutes")
    end_time = ends_at.time().isoformat("minutes")
    if start_time < facility_open or end_time > facility_close:
        raise BookingValidationError(
            f"Facility is open {facility_open}-{facility_close}; "
            f"requested {start_time}-{end_time}"
        )

    people = max(1, people)
    if people > facility.get("share_max_users", people):
        raise BookingValidationError(
            f"Facility supports at most {facility['share_max_users']} sharing users"
        )

    hours = max(1, round((ends_at - starts_at).total_seconds() / 3600))
    bags = max(1, layover.get("baggage_count") or 1)
    q = shared_quote(facility, hours=hours, bags=bags, people=people)

    return {
        "facility_id": facility["id"],
        "starts_at": starts_at,
        "ends_at": ends_at,
        "hours": hours,
        "bags": bags,
        "people": people,
        "total_price": q.solo_total,  # price never accepted from the client
        "currency": facility["currency"],
        "per_person": q.shared_per_person,
        "savings_per_person": q.savings_per_person,
    }


def member_shares(total: float, people: int) -> list[float]:
    """Split a total into `people` shares (last share absorbs rounding)."""
    if people < 1:
        raise ValueError("people must be >= 1")
    each = round2(total / people)
    shares = [each] * (people - 1)
    shares.append(round2(total - sum(shares)))
    return shares


def can_cancel(booking: dict, user_id: str, now: datetime | None = None) -> bool:
    """Only the creator may cancel, and only before the booking starts."""
    if booking["created_by"] != user_id:
        return False
    if booking.get("status") not in ("pending", "confirmed"):
        return False
    now = now or datetime.now(booking["starts_at"].tzinfo)
    return now < booking["starts_at"]
