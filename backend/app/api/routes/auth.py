"""Auth routes.

Supabase Auth itself happens client-side (frontend uses the anon key);
this router exists for (a) validating that a Bearer token works,
(b) demo-mode register/login helpers, (c) current-user lookup.

Client-supplied user IDs are NEVER trusted — we always derive identity from
the validated JWT (or offline demo identity).
"""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user
from app.core.config import get_settings
from app.core.security import AuthenticatedUser
from app.repositories.memory_store import STORE

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.get("/me")
def me(user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    profile = STORE.profiles.get(user.id)
    return {
        "id": user.id,
        "email": user.email,
        "profile": profile,
        "mode": "supabase" if get_settings().supabase_configured else "offline",
    }


@router.post("/register")
def register(user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    """Demo-mode hiccup helper — real sign-up happens in Supabase Auth.

    Ensures a profile row exists for the (validated) caller.
    """
    if user.id in STORE.profiles:
        return {"status": "exists", "profile": STORE.profiles[user.id]}
    profile = {
        "id": user.id,
        "display_name": user.email or user.id,
        "avatar_url": None,
        "verification_status": "unverified",
        "interests": [],
    }
    STORE.profiles[user.id] = profile
    return {"status": "created", "profile": profile}


@router.post("/login")
def login(user: AuthenticatedUser = Depends(get_current_user)) -> dict:
    """Demo token verification: if this route answers 200 your JWT is valid."""
    return {"status": "ok", "id": user.id}
