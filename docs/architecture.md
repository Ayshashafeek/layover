# LAYOVER — Architecture

```
┌──────────────────────────────┐        HTTPS/JSON        ┌──────────────────────────┐
│  frontend (React + Vite)     │  ──────────────────────► │  backend (FastAPI)       │
│  pages → features → services │                          │  routes → services →     │
│  only services/ touches API  │                          │  repositories            │
└──────────┬───────────────────┘                          └────────────┬─────────────┘
           │ anon key only                                        │ service-role key
           ▼                                                      ▼
   ┌───────────────────────────── Supabase (Postgres + Auth) ─────────────────────┐
   │  auth.users  →  profiles → layovers → matches → bookings → booking_members   │
   │                                    storage_facilities · payments (SIM) ·     │
   │                                    itineraries · access_logs                 │
   └──────────────────────────────────────────────────────────────────────────────┘
```

## Layers & responsibilities

| Layer | Directory | Rule |
| --- | --- | --- |
| UI | `frontend/src/pages` | Render only; no business logic |
| Feature glue | `frontend/src/features/*` | React context/hooks per domain |
| API client | `frontend/src/services` | The ONLY module allowed to `fetch()` the backend |
| HTTP | `backend/app/api/routes` | Thin: parse → call service → serialize |
| Business rules | `backend/app/services` | matching · pricing · booking · itinerary |
| Data | `backend/app/repositories` | In-memory demo store for MVP; swap for Supabase client here later |
| Contracts | `backend/app/schemas` | Pydantic models shared with `frontend/src/types` |

## Request lifecycle (example: create a booking)

1. UI posts `BookingCreate` (facility, layover, times, people).
2. Route resolves the **current user from the JWT** — client-supplied user IDs
   are never trusted.
3. `booking_service.validate_booking` re-derives price from the facility row,
   checks window ⊂ layover, facility hours, sharing limits, and start time.
4. Repository stores the booking + `booking_members` shares; an `access_logs`
   row is appended.
5. Payment endpoints read the member's `cost_share` from the DB — the amount is
   never accepted from the request body.

## Offline mode

When Supabase creds aren't set, the backend runs with `repositories/
memory_store.py` (seeded demo data) and auth defaults to a demo identity.
The health endpoint reports `mode: "offline"`; with creds supplied it reports
`mode: "supabase"`. This keeps the demo shippable with zero external deps.

## Next integration point

Replace `repositories/memory_store.py` with a `supabase_repository.py`
implementing the same functions (it is the single seam), and switch the
verified frontend flows to run against `auth.users` + RLS. Nothing else in the
codebase should change.
