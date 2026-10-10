"""LAYOVER FastAPI application entry point.

Run:  uvicorn app.main:app --reload --port 8000
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.logging import setup_logging
from app.api.routes import (
    auth,
    bookings,
    health,
    itineraries,
    layovers,
    matches,
    payments,
    storage,
    users,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    s = get_settings()
    mode = "supabase" if s.supabase_configured else "offline (seed demo data)"
    print(f"LAYOVER API starting — mode: {mode}")
    yield


app = FastAPI(
    title="LAYOVER API",
    description=(
        "Don't Just Wait. Make the Time Yours. — hackathon MVP backend. "
        "Simulated integrations are labelled and must not be presented as real."
    ),
    version="0.1.0",
    lifespan=lifespan,
)

# CORS: restrict to origins we know about via env (no wildcard in prod).
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(layovers.router)
app.include_router(matches.router)
app.include_router(storage.router)
app.include_router(bookings.router)
app.include_router(payments.router)
app.include_router(itineraries.router)
