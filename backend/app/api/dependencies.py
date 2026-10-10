"""FastAPI dependencies: current-user resolution shared by all routes."""

from __future__ import annotations

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import settings, get_settings
from app.core.security import (
    DEMO_OFFLINE_PROFILE_ID,
    AuthenticatedUser,
    UNAUTHORIZED,
    build_offline_user,
    verify_supabase_jwt,
)

bearer_scheme = HTTPBearer(auto_error=False)


def _settings() -> settings.__class__:  # helper for tests to override
    return get_settings()


def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> AuthenticatedUser:
    """Resolve the caller.

    * Supabase configured  -> require a valid bearer JWT.
    * Offline demo mode    -> allow anonymous access as the demo profile.
    """
    get_settings.cache_clear()
    s = get_settings()

    if s.supabase_configured:
        if credentials is None:
            raise UNAUTHORIZED
        claims = verify_supabase_jwt(credentials.credentials)
        return AuthenticatedUser(
            profile_id=claims["sub"], email=claims.get("email"), claims=claims
        )

    # Offline mode: no Supabase -> unauthenticated requests demo the app.
    if credentials is not None:
        try:
            claims = verify_supabase_jwt(credentials.credentials)
            return AuthenticatedUser(
                profile_id=claims["sub"], email=claims.get("email"), claims=claims
            )
        except HTTPException:
            pass  # fall through to demo user
    return build_offline_user()
