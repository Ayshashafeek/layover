# LAYOVER ✈️

![status](https://img.shields.io/badge/status-hackathon_MVP-blue)
![stack](https://img.shields.io/badge/stack-React_%2B_FastAPI_%2B_Supabase-orange)
![license](https://img.shields.io/badge/license-MIT-yellow)

> **Don't Just Wait. Make the Time Yours.**

LAYOVER turns a boring airport layover into something useful, social and fun:
it matches compatible travellers with overlapping schedules, lets them split
shared luggage storage transparently, and suggests short city experiences that
still get you back to your gate in time.

Everything here is a **hackathon MVP**. Airport APIs, flight feeds, verified
identities, live locker availability and payments are **simulated** and clearly
labeled. See [Features: implemented vs simulated](#features-implemented-vs-simulated).

---

## Tech stack

| Layer      | Technology                                              |
| ---------- | ------------------------------------------------------- |
| Frontend   | React + Vite + TypeScript + Tailwind CSS                |
| Backend    | Python 3.11+ / FastAPI                                   |
| Database   | PostgreSQL via [Supabase](https://supabase.com)          |
| Auth       | Supabase Auth (email magic link/password)                |
| API        | REST + JSON                                              |
| Maps       | Map placeholder with mock geo data (swap in Leaflet later) |

## Repository layout

```
LAYOVER/
├── frontend/     React+Vite app (pages, features, components, services)
├── backend/      FastAPI app (api/, core/, schemas/, services/, repositories/)
├── database/     schema.sql + seed.sql to run in the Supabase SQL editor
├── docs/         overview, architecture, database design, API docs, demo script
├── .env.example  shared env template (frontend + backend read their own copies)
└── README.md     ← you are here
```

Purpose of each major directory:

- **frontend/src/pages** — one file per screen (landing, login, dashboard…).
- **frontend/src/features** — screen-scoped logic kept beside its domain (auth,
  layovers, matches, bookings, profile).
- **frontend/src/services** — the only place that talks to the backend API.
- **frontend/src/components** — reusable UI split by domain and by role.
- **backend/app/api/routes** — one router file per resource; handlers stay thin.
- **backend/app/services** — matching / pricing / booking / itinerary business
  logic lives here, NOT inside route handlers.
- **backend/app/repositories** — all SQL / Supabase access goes through here.
- **backend/app/schemas** — pydantic request/response models.
- **backend/tests** — pytest suite for matching, pricing and booking rules.
- **database/** — the single source of truth for the Postgres schema + seed data.
- **docs/** — team documentation; `demo-script.md` is the one to open on demo day.

## Quickstart

Prerequisites: **Node 18+** and **Python 3.11+**.

### 1. Clone & environment files

```bash
git clone <your-repo-url> LAYOVER
cd LAYOVER

# Copy templates (Windows: use `copy` instead of `cp`; see per-app READMEs)
cp backend/.env.example  backend/.env
cp frontend/.env.example frontend/.env
```

Fill in your Supabase credentials in both `.env` files (see
[database/README.md](database/README.md) for where to find them).
`SUPABASE_SERVICE_ROLE_KEY` is **backend-only**; the frontend never sees it.

### 2. Database

Open your Supabase project → **SQL editor** → paste and run
`database/schema.sql`, then `database/seed.sql`. Full walkthrough in
[database/README.md](database/README.md).

### 3. Backend

```bash
cd backend
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux/Git Bash:
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

Health check: open <http://localhost:8001/api/health> and the interactive API
docs at <http://localhost:8001/docs>.

### 4. Frontend (new terminal)

```bash
cd frontend
npm install
npm run dev
```

Open <http://localhost:5173>.

Windows notes: `copy backend\.env.example backend\.env` and
`copy frontend\.env.example frontend\.env`; install Python from
python.org with "Add to PATH" ticked; for Node, an LTS installer or
`nvm-windows` both work fine.

## Smoke test (2 minutes)

1. `GET http://localhost:8001/api/health` → `{"status": "ok", ...}`
2. `POST /api/layovers` with the sample payload from
   [docs/api-documentation.md](docs/api-documentation.md) after logging in.
3. `GET /api/matches` → returns compatibly-scored travellers from seed data.
4. `GET /api/storage` → lists storage facilities with operator-published prices.
5. `POST /api/storage/quote` → returns the shared cost split and savings.
6. Frontend landing page loads, sign-up creates a Supabase Auth user, and the
   profile row appears in `public.profiles`.

## Features: implemented vs simulated

| Feature                                   | Status      | Notes |
| ----------------------------------------- | ----------- | ----- |
| Email/password auth via Supabase          | ✅ real     | RLS-protected profiles |
| Layover CRUD + usable-time calculation    | ✅ real     | Pure math, no flight feed |
| Traveller matching + compatibility score  | ✅ real     | Seed/demo data; no live flights |
| Storage facility discovery                | ✅ real     | From seeded `storage_facilities` |
| Shared-cost calculation & savings         | ✅ real     | Respects provider min/max sharing rules |
| Booking simulation (create/view/cancel)   | ✅ real     | No provider integration |
| Simulated payments & refunds              | 🔶 simulated| Records rows, never touches real money |
| Itinerary generation + return countdown   | ✅ real     | Static per-city activity catalog |
| Maps                                      | 🔶 simulated| Mock geo data; map widget looms in docs |
| Flight tracking (delays, gate changes)    | ❌ not built| Self-reported times only |
| Verified identity / KYC                   | ❌ not built| Profiles carry `verification_status` only |
| Live locker availability                  | ❌ not built| `storage_facilities.capacity` is static seed data |
| Airport partnerships / real providers     | ❌ not built| Facility "providers" are invented |
| Insurance / custody of luggage            | ❌ not built| Out of MVP scope |
| Real payment processing (Stripe, etc.)    | ❌ not built| `payments` are simulation rows |

Every simulated area is commented `SIMULATED` in code and
marked above so nobody accidentally demos it as real.

## Suggested build order for the team

1. Wire auth end-to-end (sign-up → profile row → protected routes).
2. Layover CRUD + `services/usable_time` — the stem of every other feature.
3. Matching service + matching results page (works on seed data, no external API).
4. Storage discovery + pricing/quote endpoint.
5. Booking flow with `booking_members` cost shares and cancellation rules.
6. Simulated payment flow + `booking_members.payment_status` updates.
7. Itinerary generation + countdown + map view.
8. Passes, README/docs polish, demo-script rehearsal.

Details in [docs/project-overview.md](docs/project-overview.md) and
[docs/demo-script.md](docs/demo-script.md).

## License

MIT — see [LICENSE](LICENSE).
