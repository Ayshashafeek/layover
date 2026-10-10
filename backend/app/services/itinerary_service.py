"""Itinerary generation (SIMULATED activity catalog).

Generates an activity plan fitting the usable layover window. Every activity
is mock data — a real integration would pull from a places API.
"""

from __future__ import annotations

from datetime import datetime, timedelta

from app.utils.time_utils import DEFAULT_BUFFER_MINUTES, usable_minutes

# Mock activity catalog; durations are minutes at the venue (excl. travel).
ACTIVITY_CATALOG: list[dict] = [
    {"name": "Skyline photos at the Rail Bridge deck", "minutes": 45, "kind": "sightseeing", "avg_cost": 0},
    {"name": "Street-food crawl in the old souk",      "minutes": 60, "kind": "food",       "avg_cost": 12},
    {"name": "Compressed museum highlights tour",      "minutes": 90, "kind": "culture",    "avg_cost": 15},
    {"name": "Harbor walk + coffee stop",              "minutes": 50, "kind": "relax",      "avg_cost": 5},
    {"name": "Quick rooftop brunch",                   "minutes": 75, "kind": "food",       "avg_cost": 22},
]

# Round-trip travel minutes between airport and city center (SIMULATED).
TRAVEL_MINUTES = 30


def build_itinerary(
    arrival: datetime,
    departure: datetime,
    *,
    interests: list[str] | None = None,
    budget: float = 0,
) -> dict:
    """Greedy plan inside [arrival, departure], leaving return buffer."""
    interests = [i.lower() for i in (interests or [])]
    usable = usable_minutes(arrival, departure, DEFAULT_BUFFER_MINUTES)
    return_at = departure - timedelta(minutes=DEFAULT_BUFFER_MINUTES)
    cursor = arrival + timedelta(minutes=DEFAULT_BUFFER_MINUTES)

    activities: list[dict] = []
    spent = 0.0

    def sort_key(a: dict) -> tuple[int, str]:
        # Matching-interest activities first, then stable name order.
        return (0 if a["kind"] in interests else 1, a["name"])

    pool = sorted(ACTIVITY_CATALOG, key=sort_key)

    for activity in pool:
        travel_pad = timedelta(minutes=TRAVEL_MINUTES)
        slot = activity["minutes"]
        end = cursor + timedelta(minutes=slot)
        if end + travel_pad > return_at:
            continue  # can't fit; try next (shorter) activity
        if budget and spent + activity["avg_cost"] > budget:
            continue
        activities.append(
            {
                "name": activity["name"],
                "start": cursor.isoformat(),
                "end": end.isoformat(),
                "travel_minutes": TRAVEL_MINUTES,
                "kind": activity["kind"],
                "avg_cost": activity["avg_cost"],
                "is_mock": True,  # SIMULATED activity
            }
        )
        spent += activity["avg_cost"]
        cursor = end + travel_pad

    return {
        "activities": activities,
        "return_time": return_at.isoformat(),
        "usable_minutes": usable,
        "estimated_total_cost": round(spent, 2),
        "is_mock": True,  # whole itinerary is SIMULATED
    }
