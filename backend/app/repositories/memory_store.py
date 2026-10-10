"""Simple in-memory data store used for offline/demo mode (no Supabase).

Real mode swaps this out for database/repositories in a later milestone; for
the hackathon MVP we start with a minimal, well-labelled simulation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from typing import Any


def _utc_iso(dt: datetime) -> str:
    return dt.isoformat()


@dataclass
class InMemoryStore:
    """Holds dicts keyed by id, mirroring the SQL tables."""

    profiles: dict[str, dict[str, Any]] = field(default_factory=dict)
    layovers: dict[str, dict[str, Any]] = field(default_factory=dict)
    storage_facilities: dict[str, dict[str, Any]] = field(default_factory=dict)
    matches: dict[str, dict[str, Any]] = field(default_factory=dict)
    bookings: dict[str, dict[str, Any]] = field(default_factory=dict)
    booking_members: dict[str, dict[str, Any]] = field(default_factory=dict)
    payments: dict[str, dict[str, Any]] = field(default_factory=dict)
    itineraries: dict[str, dict[str, Any]] = field(default_factory=dict)
    access_logs: list[dict[str, Any]] = field(default_factory=list)


def seed_offline_data(store: InMemoryStore) -> InMemoryStore:
    """Populate demo data mirroring database/seed.sql."""
    now = datetime.now(UTC)

    profiles = {
        "11111111-1111-1111-1111-111111111111": {
            "id": "11111111-1111-1111-1111-111111111111",
            "display_name": "Demo Admin",
            "avatar_url": None,
            "verification_status": "verified",
            "interests": ["food", "architecture"],
        },
        "22222222-2222-2222-2222-222222222222": {
            "id": "22222222-2222-2222-2222-222222222222",
            "display_name": "Aisha Sharma",
            "avatar_url": None,
            "verification_status": "verified",
            "interests": ["food", "art"],
        },
        "33333333-3333-3333-3333-333333333333": {
            "id": "33333333-3333-3333-3333-333333333333",
            "display_name": "Marco Rossi",
            "avatar_url": None,
            "verification_status": "unverified",
            "interests": ["history", "walking tours"],
        },
    }

    layovers = {
        "a1000000-0000-0000-0000-000000000001": {
            "id": "a1000000-0000-0000-0000-000000000001",
            "user_id": "11111111-1111-1111-1111-111111111111",
            "airport_code": "DXB",
            "arrival_time": now + timedelta(hours=1),
            "departure_time": now + timedelta(hours=7),
            "baggage_count": 1,
            "budget_total": 80.0,
            "currency": "USD",
            "interests": ["food", "city tour"],
        },
        "a1000000-0000-0000-0000-000000000002": {
            "id": "a1000000-0000-0000-0000-000000000002",
            "user_id": "22222222-2222-2222-2222-222222222222",
            "airport_code": "DXB",
            "arrival_time": now + timedelta(hours=2),
            "departure_time": now + timedelta(hours=8),
            "baggage_count": 2,
            "budget_total": 120.0,
            "currency": "USD",
            "interests": ["food", "art"],
        },
    }

    facilities = {
        "f1000000-0000-0000-0000-000000000001": {
            "id": "f1000000-0000-0000-0000-000000000001",
            "provider_name": "SmartLocker Hub",  # SIMULATED provider
            "airport_code": "DXB",
            "location": "Terminal 1, Level 1 near Exit 4",
            "lat": 25.2532,
            "lng": 55.3654,
            "price_per_bag_hour": 4.50,
            "currency": "USD",
            "capacity_total": 120,
            "share_max_users": 4,
            "share_min_users": 1,
            "opening_time": "00:00",
            "closing_time": "23:59",
            "sharing_allowed": True,
        },
        "f1000000-0000-0000-0000-000000000002": {
            "id": "f1000000-0000-0000-0000-000000000002",
            "provider_name": "BagsAway DXB",  # SIMULATED provider
            "airport_code": "DXB",
            "location": "Terminal 3, Arrivals Hall",
            "lat": 25.258,
            "lng": 55.361,
            "price_per_bag_hour": 5.00,
            "currency": "USD",
            "capacity_total": 60,
            "share_max_users": 3,
            "share_min_users": 2,
            "opening_time": "05:00",
            "closing_time": "23:00",
            "sharing_allowed": True,
        },
        "f1000000-0000-0000-0000-000000000003": {
            "id": "f1000000-0000-0000-0000-000000000003",
            "provider_name": "Fly&Store Lounge",  # SIMULATED provider
            "airport_code": "DXB",
            "location": "Terminal 2, near Gate C12",
            "lat": 25.249,
            "lng": 55.370,
            "price_per_bag_hour": 3.75,
            "currency": "USD",
            "capacity_total": 40,
            "share_max_users": 2,
            "share_min_users": 2,
            "opening_time": "06:00",
            "closing_time": "22:00",
            "sharing_allowed": True,
        },
        "f1000000-0000-0000-0000-000000000004": {
            "id": "f1000000-0000-0000-0000-000000000004",
            "provider_name": "CityLocker Small",  # SIMULATED provider
            "airport_code": "DXB",
            "location": "Airport Metro station, Exit 2",
            "lat": 25.247,
            "lng": 55.355,
            "price_per_bag_hour": 2.50,
            "currency": "USD",
            "capacity_total": 20,
            "share_max_users": 2,
            "share_min_users": 1,
            "opening_time": "07:00",
            "closing_time": "21:00",
            "sharing_allowed": False,
        },
    }

    store.profiles = profiles
    store.layovers = layovers
    store.storage_facilities = facilities
    return store


# One shared store instance for the life of the process (fine for a demo).
STORE = seed_offline_data(InMemoryStore())
