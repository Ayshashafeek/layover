# LAYOVER — 5-Minute Demo Script

## Before the demo (10 min prep)

```bash
# terminal 1
cd backend && source .venv/bin/activate   # Windows: .venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8001

# terminal 2
cd frontend && npm run dev
```

Open http://localhost:5173 and http://localhost:8001/docs in side-by-side tabs.
Confirm `GET /api/health` says `mode: offline` (no Supabase needed) and shows
the DB mode if credentials are configured.

## The story (5 minutes)

**0:00 — The pain.** "You land with 6 hours and two bags. You can't leave, you
can't rest, and locker rent is brutal for one person." Show the landing hero.

**0:45 — Enter the layover.** Fill the form: DXB, +1h to +7h, 1 bag, budget 80,
interests food. Hit **Find my people**.

**1:30 — Matching.** Show the scored traveller cards — point at the breakdown
(schedule/bags/interests). Explain: same airport, ≥60 shared minutes, score
out of 100 — real math, transparent. Accept Aisha.

**2:15 — Storage & the money moment.** Browse facilities. Pick SmartLocker Hub:
2 bags × 4 h = **$36 solo** → **$18 each** with 2 travellers (**50% saved**).
Emphasize: the price always comes from the facility row, never the client;
sharing respects each provider's min/max group rules.

**3:00 — Book & pay (simulated).** Reserve → booking page shows members,
shares, and status. Hit **Pay my share** → `SIM-XXXXXXXX` transaction, booking
goes to `confirmed` when everyone paid. Say plainly: "Payment is simulated —
Stripe integration is a natural next step."

**3:45 — Make the time yours.** Open the itinerary: street-food crawl, harbor
walk — each stamped `SIMULATED`, planned only inside the usable window (480 −
2×90 = 300 min). Show the **countdown to return**.

**4:30 — Close.** "Everything that can be real already is: matching, pricing,
booking rules, auth. Everything that needs partners is clearly labelled
simulated. Layover turns waiting into your time — safely, honestly, within
your window."

## Backup talking points

- `backend/tests/` — 19 automated tests covering matching, pricing, and the
  booking rules (run `pytest` to show green in 0.05 s).
- `GET /docs` — auto-generated Swagger for judges who want to poke the API.
- Access logs + RLS policies if asked about abuse/security.
- If Supabase is configured: do a live sign-up to show real auth.
