"""Traveller-matching routes."""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_current_user
from app.core.security import AuthenticatedUser
from app.repositories.memory_store import STORE
from app.schemas.core import Match, MatchScoreBreakdown
from app.services.matching_service import compute_score, is_compatible

router = APIRouter(prefix="/api/matches", tags=["matches"])


def _iso(dt: datetime) -> str:
    return dt.isoformat()


def _layover_public(row: dict) -> dict:
    return {
        "id": row["id"],
        "user_id": row["user_id"],
        "airport_code": row["airport_code"],
        "arrival_time": _iso(row["arrival_time"]),
        "departure_time": _iso(row["departure_time"]),
        "baggage_count": row["baggage_count"],
        "interests": row["interests"],
    }


@router.post("/{layover_id}/run", response_model=list[Match])
def run_matching(
    layover_id: str,
    user: AuthenticatedUser = Depends(get_current_user),
) -> list[dict]:
    """Score the caller's layover against all other layovers at the airport."""
    source = STORE.layovers.get(layover_id)
    if source is None:
        raise HTTPException(404, "Layover not found")
    if source["user_id"] != user.id:
        raise HTTPException(403, "You do not own this layover")

    results: list[dict] = []
    other: dict
    for other in STORE.layovers.values():
        if other["id"] == layover_id:
            continue
        if not is_compatible(source, other):
            continue
        breakdown = compute_score(source, other)
        match_id = str(uuid4())
        row = {
            "id": match_id,
            "layover_a": source["id"],
            "layover_b": other["id"],
            "user_a": source["user_id"],
            "user_b": other["user_id"],
            "score": breakdown["total"],
            "score_breakdown": breakdown,
            "status": "proposed",
            "simulated": True,
            "other_layover": _layover_public(other),
        }
        STORE.matches[match_id] = row
        results.append(row)

    results.sort(key=lambda r: r["score"], reverse=True)
    return results


@router.get("", response_model=list[Match])
def my_matches(user: AuthenticatedUser = Depends(get_current_user)) -> list[dict]:
    """List stored matches involving the current user."""
    out = []
    for row in STORE.matches.values():
        if user.id in (row["user_a"], row["user_b"]):
            out.append(row)
    out.sort(key=lambda r: r["score"], reverse=True)
    return out


@router.post("/{match_id}/accept")
def accept_match(
    match_id: str,
    user: AuthenticatedUser = Depends(get_current_user),
) -> dict:
    row = STORE.matches.get(match_id)
    if row is None:
        raise HTTPException(404, "Match not found")
    if user.id not in (row["user_a"], row["user_b"]):
        raise HTTPException(403, "Not a participant of this match")
    if row["status"] not in ("proposed", "accepted"):
        raise HTTPException(409, f"Match is {row['status']}; cannot accept")
    row["status"] = "accepted"
    return row


@router.post("/{match_id}/reject")
def reject_match(
    match_id: str,
    user: AuthenticatedUser = Depends(get_current_user),
) -> dict:
    row = STORE.matches.get(match_id)
    if row is None:
        raise HTTPException(404, "Match not found")
    if user.id not in (row["user_a"], row["user_b"]):
        raise HTTPException(403, "Not a participant of this match")
    row["status"] = "rejected"
    return row
