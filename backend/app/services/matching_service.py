"""Traveller matching logic.

Score components (0-100):
  * 60 pts  schedule overlap  — shared minutes at the same airport
  * 20 pts  baggage typology — comparable bags means comparable storage needs
  * 20 pts  interest overlap  — shared ideas about what to do in the city
Only pairs at the same airport whose windows overlap by at least
MIN_OVERLAP_MINUTES are considered compatible candidates.
"""

from __future__ import annotations

from datetime import datetime

from app.utils.time_utils import overlap_minutes

MIN_OVERLAP_MINUTES = 60
MAX_BAGGAGE_DIFF = 2

Pts = dict[str, float]


def compute_score(
    loc_a: dict,
    loc_b: dict,
    now: datetime | None = None,
) -> Pts:
    """Numeric detail of the match between two layovers.

    Each input dict must contain:
      airport_code, arrival_time, departure_time, baggage_count, interests
    """
    schedule_pts = 0.0
    baggage_pts = 0.0
    interest_pts = 0.0

    if loc_a["airport_code"].upper() != loc_b["airport_code"].upper():
        return {"total": 0.0, "schedule": 0, "baggage": 0, "interest": 0}

    shared = overlap_minutes(
        [(loc_a["arrival_time"], loc_a["departure_time"])],
        (loc_b["arrival_time"], loc_b["departure_time"]),
    )
    if shared >= MIN_OVERLAP_MINUTES:
        schedule_pts = 60 * min(1.0, shared / 240)

    baggage_pts = 20 * max(0.0, 1.0 - abs(loc_a["baggage_count"] - loc_b["baggage_count"]) / (MAX_BAGGAGE_DIFF + 1))

    a_set = set(i.lower() for i in loc_a["interests"])
    b_set = set(i.lower() for i in loc_b["interests"])
    shared_interests = len(a_set & b_set)
    if a_set or b_set:
        interest_pts = 20 * shared_interests / max(len(a_set), len(b_set))

    total = round(schedule_pts + baggage_pts + interest_pts, 2)
    return {
        "total": total,
        "schedule": round(schedule_pts, 2),
        "baggage": round(baggage_pts, 2),
        "interest": round(interest_pts, 2),
        "overlap_minutes": shared,
    }


def is_compatible(loc_a: dict, loc_b: dict) -> bool:
    """Boolean check used before running full score logic."""
    if loc_a["airport_code"].upper() != loc_b["airport_code"].upper():
        return False
    return compute_score(loc_a, loc_b)["overlap_minutes"] >= MIN_OVERLAP_MINUTES
