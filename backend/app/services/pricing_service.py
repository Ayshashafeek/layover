"""Shared-cost pricing logic.

The facility sets `price_per_bag_hour`, `share_min_users`, `share_max_users`
and `sharing_allowed`. We compute what each member would pay if they share,
respecting those rules and never exceeding the max group size.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SharedQuote:
    facility_id: str
    hours: int
    bags: int
    people: int
    solo_total: float
    shared_total: float
    shared_per_person: float
    savings_per_person: float
    savings_percent: float
    currency: str
    sharing_allowed: bool
    violates_min_users: bool
    violates_max_users: bool


def round2(value: float) -> float:
    return round(value + 1e-9, 2)


def quote(
    facility: dict,
    hours: int,
    bags: int,
    people: int,
) -> SharedQuote:
    """Compute a shared-locker quote.

    facility fields required: price_per_bag_hour, currency, sharing_allowed,
    share_min_users, share_max_users, id.
    """
    if hours < 1:
        raise ValueError("hours must be >= 1")
    if bags < 1:
        raise ValueError("bags must be >= 1")
    if people < 1:
        raise ValueError("people must be >= 1")

    sharing_allowed = bool(facility.get("sharing_allowed", True))
    solo_total = round2(facility["price_per_bag_hour"] * bags * hours)

    violates_min = people < facility.get("share_min_users", 1)
    violates_max = people > facility.get("share_max_users", people)

    if sharing_allowed and not violates_min and not violates_max:
        shared_total = solo_total          # the locker is priced by bag-hour
        per_person = round2(shared_total / people)
        saving = round2(solo_total - per_person)
        percent = round2(saving / solo_total * 100) if solo_total else 0.0
    else:
        shared_total = solo_total
        per_person = solo_total
        saving = 0.0
        percent = 0.0

    return SharedQuote(
        facility_id=facility["id"],
        hours=hours,
        bags=bags,
        people=people,
        solo_total=solo_total,
        shared_total=shared_total,
        shared_per_person=per_person,
        savings_per_person=saving,
        savings_percent=percent,
        currency=facility["currency"],
        sharing_allowed=sharing_allowed,
        violates_min_users=violates_min,
        violates_max_users=violates_max,
    )


__all__ = ["SharedQuote", "quote", "round2"]
