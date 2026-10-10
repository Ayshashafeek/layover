# LAYOVER — Project Overview

> **Don't Just Wait. Make the Time Yours.**

## One-liner

LAYOVER turns a dead airport layover into a live plan: match with travellers
whose layovers overlap yours, share a luggage locker to cut the cost, and get a
city micro-itinerary with a hard countdown back to the gate.

## The five pillars

1. **Smart matching** — compatibility score (schedule 0-60 · baggage 0-20 · interests 0-20) for travellers at the same airport with ≥60 min of shared time.
2. **Transparent shared storage** — a quote that respects each provider's min/max sharing rules; savings per person shown in plain numbers.
3. **Booking simulation** — reserve, split shares between members, pay/refund in a friction-free simulation.
4. **Time-aware itineraries** — a greedy planner that only proposes what fits the usable window (±90 min airport buffer on each end).
5. **Return countdown** — a second-by-second reminder so nobody misses boarding.

## What is REAL vs SIMULATED (read before demoing)

| Real math / logic | Simulated (labelled in code & UI) |
| --- | --- |
| Matching score | Storage providers ("SmartLocker Hub", …) |
| Pricing & savings engine | Locker availability/capacity |
| Usable-time calculation | Flight times (self-entered) |
| Booking rules & validation | Payment/refund transactions |
| Auth via Supabase (when configured) | Identity verification |
| Itinerary feasibility (does it fit?) | Activity catalog, travel durations, map pins |

Simulated pieces always carry a `SIMULATED` flag in code and a "simulated" chip
in the UI. Never present them as live/verified data.

## MVP scope boundary (do NOT build in 48 h)

- No live flight feeds or gate data.
- No real provider integration or real bookings.
- No real payments (Stripe etc.).
- No identity verification/KYC.
- No insurance, custody or liability features.

## Tech stack

React + Vite + TS + Tailwind (frontend) · FastAPI + Pydantic (backend) ·
PostgreSQL via Supabase (data, auth, RLS).

See [architecture.md](architecture.md) for how it fits together.
