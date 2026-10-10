"""Itinerary routes — generates a SIMULATED activity plan for a layover."""

from __future__ import annotations

from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.dependencies import get_current_user
from app.core.security import AuthenticatedUser
from app.repositories.memory_store import STORE
from app.schemas.core import ItineraryResponse
from app.services.itinerary_service import build_itinerary

router = APIRouter(prefix="/api/itineraries", tags=["itineraries"])


@router.post("/generate/{layover_id}", response_model=ItineraryResponse)
def generate(
    layover_id: str,
    user: AuthenticatedUser = Depends(get_current_user),
) -> dict:
    layover = STORE.layovers.get(layover_id)
    if layover is None:
        raise HTTPException(404, "Layover not found")
    if layover["user_id"] != user.id:
        raise HTTPException(403, "You do not own this layover")

    plan = build_itinerary(
        arrival=layover["arrival_time"],
        departure=layover["departure_time"],
        interests=layover.get("interests") or [],
        budget=float(layover.get("budget_total") or 0),
    )

    row = {
        "id": str(uuid4()),
        "layover_id": layover_id,
        "user_id": user.id,
        **plan,
        "currency": layover.get("currency", "USD"),
    }
    STORE.itineraries[row["id"]] = row
    return row


@router.get("/mine", response_model=list[ItineraryResponse])
def my_itineraries(user: AuthenticatedUser = Depends(get_current_user)) -> list[dict]:
    return [i for i in STORE.itineraries.values() if i["user_id"] == user.id]
