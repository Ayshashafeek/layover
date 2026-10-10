# LAYOVER — Frontend

React + Vite + TypeScript + Tailwind CSS.

## Setup

```bash
cd frontend
npm install
copy .env.example .env   # Windows
cp .env.example .env     # macOS/Linux
npm run dev
```

Open <http://localhost:5173>. The dev server proxies `/api/*` to the backend
(`VITE_API_BASE_URL`, default http://localhost:8001 — start the backend first).

## Build

```bash
npm run build     # typechecks + bundles to dist/
npm run preview   # serve the production build locally
```

## Structure

- `src/pages/` — one file per screen.
- `src/features/` — auth context & screen-scoped logic.
- `src/components/` — reusable UI (common/ + layout/).
- `src/services/` — the only module that calls the backend API.
- `src/lib/` — Supabase client and API wrapper.
- `src/data/` — future per-city mock catalogs (itinerary data lives server-side for now).
- `src/assets/`, `public/images/`, `public/icons/` — logo & artwork slots.

Note: without Supabase credentials the app runs in **demo mode** — pages render
and call the backend, and auth pages explain that sign-in needs credentials.
