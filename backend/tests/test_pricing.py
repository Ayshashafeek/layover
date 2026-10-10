import pytest

from app.services.pricing_service import quote

FACILITY = {
    "id": "fac-1",
    "price_per_bag_hour": 4.50,
    "currency": "USD",
    "sharing_allowed": True,
    "share_min_users": 2,
    "share_max_users": 4,
}


def test_solo_pricing_is_full_rate():
    q = quote(FACILITY, hours=3, bags=2, people=1)
    assert q.solo_total == 27.0
    assert q.shared_per_person == 27.0
    assert q.savings_per_person == 0.0


def test_sharing_splits_cost():
    q = quote(FACILITY, hours=3, bags=2, people=2)
    assert q.shared_total == 27.0
    assert q.shared_per_person == 13.5
    assert q.savings_per_person == 13.5
    assert q.savings_percent == 50.0


def test_below_min_users_no_discount():
    q = quote(FACILITY, hours=3, bags=2, people=1)
    assert q.violates_min_users
    assert q.shared_per_person == q.solo_total


def test_above_max_users_no_discount():
    q = quote(FACILITY, hours=3, bags=1, people=5)
    assert q.violates_max_users
    assert q.shared_per_person == q.solo_total


def test_sharing_disallowed_no_discount():
    facility = {**FACILITY, "sharing_allowed": False}
    q = quote(facility, hours=2, bags=1, people=2)
    assert q.shared_per_person == q.solo_total
    assert q.savings_per_person == 0.0


def test_invalid_hours_rejected():
    with pytest.raises(ValueError):
        quote(FACILITY, hours=0, bags=1, people=1)
