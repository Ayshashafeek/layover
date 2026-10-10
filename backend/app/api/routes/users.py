"""User profile routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.api.dependencies import get_current_user
from app.core.security import AuthenticatedUser
from app.repositories.memory_store import STORE

router = APIRouter(prefix="/api/users", tags=["users"])


class ProfileUpdate(BaseModel):
    display_name: str | None = Field(default=None, min_length=1, max_length=80)
    avatar_url: str | None = None
    interests: list[str] | None = None
    # NOTE: verification_status is intentionally NOT updatable here —
    #       it is set by the (simulated) verification service only.


@router.get("/me")
def get_my_profile(user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    profile = STORE.profiles.get(user.id)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.patch("/me")
def update_my_profile(
    body: ProfileUpdate,
    user: AuthenticatedUser = Depends(get_current_user),
) -> dict:
    profile = STORE.profiles.get(user.id)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    if body.display_name is not None:
        profile["display_name"] = body.display_name
    if body.avatar_url is not None:
        profile["avatar_url"] = body.avatar_url
    if body.interests is not None:
        profile["interests"] = body.interests
    return profile
