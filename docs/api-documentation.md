# LAYOVER — API Reference

Base URL (dev): `http://localhost:8001` (start the backend with `uvicorn app.main:app --reload --port 8001`).
Interactive docs: `GET /docs` (Swagger UI) · `GET /openapi.json`.

All endpoints (except `/api/health`) resolve the caller from the `Authorization:
Bearer <supabase-jwt>` header. **Offline demo mode** (no Supabase creds) accepts
requests without a token as the demo profile.

## Health

```
GET /api/health
→ 200 {"status":"ok","app":"LAYOVER API","env":"development","mode":"offline","time":"..."}
```

## Auth

```
GET  /api/auth/me      → current identity + profile (null profile before register)
POST /api/auth/register → ensure a profile row exists for the validated caller
POST /api/auth/login    → token sanity check: 200 if the JWT is valid
```

## Users

```
GET  /api/users/me                → profile
PATCH /api/users/me  {display_name?, avatar_url?, interests?} → updated profile
```
`verification_status` is intentionally not client-editable.

## Layovers

```
POST /api/layovers
  {"airport_code":"DXB","arrival_time":"2026-10-11T10:00:00Z",
   "departure_time":"2026-10-11T18:00:00Z","baggage_count":2,
   "budget_total":90,"interests":["food"]}
→ 201 Layover    (422 if departure ≤ arrival; user_id comes from the JWT)

GET  /api/layovers?airport=DXB   → list (any user, for matching)
GET  /api/layovers/mine          → my layovers
GET  /api/layovers/{id}          → one layover
GET  /api/layovers/{id}/usable-time
→ 200 {"layover_id":"...","usable_minutes":300,"total_minutes":480,"buffer_minutes":90}
```

## Matches

```
POST /api/matches/{layover_id}/run   → scored candidates (desc), stores rows
GET  /api/matches                    → my stored matches
POST /api/matches/{id}/accept        → participant-only
POST /api/matches/{id}/reject        → participant-only
```
Score breakdown: `schedule (0-60) · baggage (0-20) · interest (0-20)`; only
pairs with ≥60 shared minutes at the same airport are candidates.

## Storage & pricing

```
GET  /api/storage?airport=DXB        → facilities (SIMULATED providers)
POST /api/storage/quote
  {"facility_id":"...","hours":4,"bags":2,"people":2}
→ 200 {"solo_total":36.0,"shared_per_person":18.0,"savings_per_person":18.0,
       "savings_percent":50.0,"violates_min_users":false,"violates_max_users":false,...}
```

## Bookings

```
POST /api/bookings    {facility_id, layover_id, starts_at, ends_at, people}
→ 201 Booking with members[] (server-computed shares & price)
422 on: window outside layover, outside facility hours, past start, group > max
GET  /api/bookings/mine                 → my bookings
GET  /api/bookings/{id}                 → participant-only
POST /api/bookings/{id}/cancel          → creator-only, before start
```

## Payments (SIMULATED)

```
POST /api/payments/pay    {booking_id} → payment row (amount from cost_share!)
POST /api/payments/refund {booking_id} → flips payment + member status
GET  /api/payments/mine                → my payment records
```

## Itineraries

```
POST /api/itineraries/generate/{layover_id} → plan (is_mock: true everywhere)
GET  /api/itineraries/mine
```

## Error format

Non-2xx responses use FastAPI's `{"detail": "<message>"}`; validation errors
return 422 with FastAPI's standard error body.
