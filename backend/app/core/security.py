"""Authentication & authorization primitives.

Token verification decodes Supabase JWTs (HS256/RS256 depending on project
settings). When no Supabase key is configured (offline demo mode) unauthentated
requests are treated as the pre-registered demo profile so the API stays
explorable without real credentials.
"""

import logging
from typing import Any

import jwt  # PyJWT
from fastapi import HTTPException, status

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger("security")

UNAUTHORIZED = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Missing or invalid bearer token",
    headers={"WWW-Authenticate": "Bearer"},
)

# Demo profile used when the backend runs in offline mode without Supabase.
DEMO_OFFLINE_PROFILE_ID = "11111111-1111-1111-1111-111111111111"


class AuthenticatedUser:
    """Minimal identity carried through request lifetime."""

    def __init__(self, profile_id: str, email: str | None, claims: dict[str, Any]):
        self.id = profile_id  # equals profiles.id == auth.users.id
        self.email = email
        self.claims = claims


def verify_supabase_jwt(token: str) -> dict[str, Any]:
    """Decode a Supabase Auth JWT without network calls."""
    try:
        # Supabase signs with HS256 using the anon key by default.
        return jwt.decode(
            token,
            settings.supabase_anon_key,
            algorithms=["HS256"],
            audience="authenticated",
            options={"require": ["exp", "sub"]},
        )
    except jwt.PyJWTError as exc:  # covers expired / bad signature / malformed
        logger.info("JWT verification failed: %s", exc)
        raise UNAUTHORIZED from exc


def build_offline_user() -> AuthenticatedUser:
    """Demo user used in offline mode (no Supabase configured)."""
    return AuthenticatedUser(
        profile_id=DEMO_OFFLINE_PROFILE_ID,
        email="demo@layover.local",
        claims={"sub": DEMO_OFFLINE_PROFILE_ID, "email": "demo@layover.local"},
    )
