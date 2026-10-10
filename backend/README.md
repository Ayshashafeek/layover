# LAYOVER — Backend

FastAPI service. Thin route handlers, business logic in `app/services/`,
database access in `app/repositories/`.

## Setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1      # Windows PowerShell
source .venv/bin/activate       # macOS / Linux / Git Bash
pip install -r requirements.txt
copy .env.example .env          # Windows   ((fill in Supabase values)
cp .env.example .env            # macOS/Linux
```

## Run

```bash
uvicorn app.main:app --reload --port 8000
```

- Health check: `GET http://localhost:8000/api/health`
- Swagger UI:     http://localhost:8000/docs
- OpenAPI JSON:   http://localhost:8000/openapi.json

In offline/demo mode (no Supabase credentials in `.env`) the backend runs with
an in-memory repository and seeded sample data — labelled `mode: "offline"`
on `/api/health`. With real credentials supplied it uses Supabase.

## Tests

```bash
pytest
```

Covers matching scoring, shared pricing math and booking validation.
