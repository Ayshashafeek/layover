"""Layover routes: create, list, retrieve, usable-time calculation."""

from __future__ import annotations

from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_current_user
from app.core.config import settings
from app.core.security import AuthenticatedUser
from app.repositories.memory_store import STORE
from app.schemas.core import Layover, LayoverCreate, LayoverUsableTime
from app.utils.time_utils import (
    DEFAULT_BUFFER_MINUTES,
    usable_minutes,
    format_countdown,
)
from uuid import uuid4

router = APIRouter(prefix="/api/layovers", tags=["layovers"])


def _toIso(row: dict) -> dict:
    out = dict(row)
    for k in ("arrival_time", "departure_time"):
        v = out.get(k)
        if isinstance(v, datetime):
            out[k] = v.isoformat()
    return out


@router.post("", response_model=Layover, status_code=201)
def create_layover(
    body: LayoverCreate,
    user: AuthenticatedUser = Depends(get_current_user),
) -> dict:
    """Create a layover. user_id always derived from the JWT, never the body."""
    if body.departure_time <= body.arrival_time:
        raise HTTPException(422, "departure_time must be after arrival_time")
    row = {
        "id": str(uuid4()),
        "user_id": user.id,
        **body.model_dump(),
    }
    STORE.layovers[row["id"]] = row
    return _toIso(row)


@router.get("", response_model=list[Layover])
def list_layovers(
    airport: str | None = None,
    user: AuthenticatedUser = Depends(get_current_user),
) -> list[dict]:
    rows = list(STORE.layovers.values())
    if airport:
        rows = [r for r in rows if r["airport_code"].upper() == airport.upper()]
    return [_toIso(r) for r in rows]


@router.get("/mine", response_model=list[Layover])
def my_layovers(user: AuthenticatedUser = Depends(get_current_user)) -> list[dict]:
    rows = [r for r in STORE.layovers.values() if r["user_id"] == user.id]
    return [_toIso(r) for r in rows]


@router.get("/{layover_id}", response_model=Layover)
def get_layover(
    layover_id: str,
    user: AuthenticatedUser = Depends(get_current_user),
) -> dict:
    row = STORE.layovers.get(layover_id)
    if row is None:
        raise HTTPException(404, "Layover not found")
    return _toIso(row)


@router.get("/{layover_id}/usable-time", response_model=LayoverUsableTime)
def usable_time(
    layover_id: str,
    user: AuthenticatedUser = Depends(get_current_user),
) -> dict:
    row = STORE.layovers.get(layover_id)
    if row is None:
        raise HTTPException(404, "Layover not found")
    total = int((row["departure_time"] - row["arrival_time"]).total_seconds() // 60)
    usable = usable_minutes(row["arrival_time"], row["departure_time"])
    return {
        "layover_id": row["id"],
        "usable_minutes": usable,
        "total_minutes": total,
        "buffer_minutes": DEFAULT_BUFFER_MINUTES,
        "hint": format_countdown(usable),
    }
