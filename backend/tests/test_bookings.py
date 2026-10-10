from datetime import UTC, datetime, timedelta

import pytest

from app.services.booking_service import (
    BookingValidationError,
    can_cancel,
    member_shares,
    validate_booking,
)
from app.services.pricing_service import round2  # noqa: F401

NOW = datetime.now(UTC).replace(second=0, microsecond=0)

FACILITY = {
    "id": "fac-1",
    "share_max_users": 4,
    "price_per_bag_hour": 5.0,
    "currency": "USD",
    "opening_time": "05:00",
    "closing_time": "23:00",
}

LAYOVER = {
    "arrival_time": NOW + timedelta(hours=1),
    "departure_time": NOW + timedelta(hours=7),
    "baggage_count": 2,
}


def test_valid_booking_returns_canonical_price():
    result = validate_booking(
        FACILITY,
        LAYOVER,
        starts_at=NOW + timedelta(hours=2),
        ends_at=NOW + timedelta(hours=5),
        people=2,
    )
    # 2 bags x 3 h x 5.0 = 30, price computed server-side
    assert result["total_price"] == 30.0
    assert result["per_person"] == 15.0


def test_booking_window_must_be_inside_layover():
    with pytest.raises(BookingValidationError):
        validate_booking(
            FACILITY,
            LAYOVER,
            starts_at=NOW,
            ends_at=NOW + timedelta(hours=8),  # extends past departure
            people=1,
        )


def test_booking_cannot_start_in_past():
    with pytest.raises(BookingValidationError):
        validate_booking(
            FACILITY,
            LAYOVER,
            starts_at=NOW - timedelta(minutes=10),
            ends_at=NOW + timedelta(hours=1),
            people=1,
        )


def test_booking_outside_facility_hours_rejected():
    facility = {**FACILITY, "opening_time": "23:00", "closing_time": "23:59"}
    with pytest.raises(BookingValidationError):
        validate_booking(
            facility,
            LAYOVER,  # layover runs during the afternoon -- before opening
            starts_at=NOW + timedelta(hours=2),
            ends_at=NOW + timedelta(hours=3),
            people=1,
        )


def test_too_many_sharing_users_rejected():
    with pytest.raises(BookingValidationError):
        validate_booking(
            FACILITY,
            LAYOVER,
            starts_at=NOW + timedelta(hours=2),
            ends_at=NOW + timedelta(hours=4),
            people=9,
        )


def test_member_shares_sum_to_total():
    shares = member_shares(100.0, 3)
    assert round2(sum(shares)) == 100.0
    assert len(shares) == 3


def test_cancel_rules():
    booking = {
        "created_by": "user-1",
        "status": "confirmed",
        "starts_at": NOW + timedelta(hours=2),
    }
    assert can_cancel(booking, "user-1", now=NOW)
    assert not can_cancel(booking, "user-2", now=NOW)
    assert not can_cancel(booking, "user-1", now=NOW + timedelta(hours=3))
    cancelled = {**booking, "status": "cancelled"}
    assert not can_cancel(cancelled, "user-1", now=NOW)
