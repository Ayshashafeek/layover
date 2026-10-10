"""Pydantic request/response models shared across routes."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------
class HealthResponse(BaseModel):
    status: Literal["ok"]
    app: str
    env: str
    mode: Literal["supabase", "offline"]
    time: datetime


# ---------------------------------------------------------------------------
# Layovers
# ---------------------------------------------------------------------------
class LayoverCreate(BaseModel):
    airport_code: str = Field(min_length=3, max_length=4)
    arrival_time: datetime
    departure_time: datetime
    baggage_count: int = Field(default=0, ge=0, le=10)
    budget_total: float = Field(default=0, ge=0)
    currency: str = Field(default="USD", min_length=3, max_length=3)
    interests: list[str] = Field(default_factory=list)


class Layover(BaseModel):
    id: str
    user_id: str
    airport_code: str
    arrival_time: datetime
    departure_time: datetime
    baggage_count: int
    budget_total: float
    currency: str
    interests: list[str]


class LayoverUsableTime(BaseModel):
    layover_id: str
    usable_minutes: int
    total_minutes: int
    buffer_minutes: int


# ---------------------------------------------------------------------------
# Matches
# ---------------------------------------------------------------------------
class MatchScoreBreakdown(BaseModel):
    total: float
    schedule: float
    baggage: float
    interest: float
    overlap_minutes: int


class Match(BaseModel):
    id: str | None = None
    layover_a: str
    layover_b: str
    user_a: str
    user_b: str
    score: float
    score_breakdown: MatchScoreBreakdown
    status: str = "proposed"
    simulated: bool = False


# ---------------------------------------------------------------------------
# Storage & pricing
# ---------------------------------------------------------------------------
class StorageFacility(BaseModel):
    id: str
    provider_name: str
    airport_code: str
    location: str
    lat: float | None = None
    lng: float | None = None
    price_per_bag_hour: float
    currency: str
    capacity_total: int
    share_min_users: int
    share_max_users: int
    opening_time: str
    closing_time: str
    sharing_allowed: bool
    simulated: bool = True  # providers are simulated in the MVP


class QuoteRequest(BaseModel):
    facility_id: str
    hours: int = Field(ge=1, le=24)
    bags: int = Field(ge=1, le=10)
    people: int = Field(ge=1, le=10)


class SharedQuoteResponse(BaseModel):
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


# ---------------------------------------------------------------------------
# Bookings
# ---------------------------------------------------------------------------
class BookingCreate(BaseModel):
    facility_id: str
    layover_id: str
    starts_at: datetime
    ends_at: datetime
    # people is used for the quote; server recomputes price & permissions.
    people: int = Field(default=1, ge=1, le=10)


class BookingMember(BaseModel):
    user_id: str
    cost_share: float
    currency: str
    payment_status: Literal["unpaid", "paid", "refunded"] = "unpaid"
    can_retrieve: bool = False


class Booking(BaseModel):
    id: str
    facility_id: str
    created_by: str
    layover_id: str
    starts_at: datetime
    ends_at: datetime
    total_price: float
    currency: str
    status: str
    members: list[BookingMember] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Payments (simulated)
# ---------------------------------------------------------------------------
class PaymentCreate(BaseModel):
    booking_id: str
    # amount intentionally NOT accepted from client — server computes from share


class PaymentResponse(BaseModel):
    id: str
    booking_id: str
    payer_id: str
    amount: float
    currency: str
    status: Literal["simulated_pending", "simulated_paid", "simulated_refunded", "failed"]
    transaction_ref: str
    simulated: bool


# ---------------------------------------------------------------------------
# Itineraries
# ---------------------------------------------------------------------------
class Activity(BaseModel):
    name: str
    start: datetime
    end: datetime
    travel_minutes: int
    kind: str
    avg_cost: float
    is_mock: bool


class ItineraryResponse(BaseModel):
    layover_id: str
    activities: list[Activity]
    return_time: datetime
    usable_minutes: int
    estimated_total_cost: float
    currency: str
    is_mock: bool
