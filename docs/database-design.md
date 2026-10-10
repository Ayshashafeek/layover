# LAYOVER — Database Design

Source of truth: [`database/schema.sql`](../database/schema.sql). Seed:
[`database/seed.sql`](../database/seed.sql).

## Entity relationships

```
auth.users (Supabase)
   │ 1:1
   ▼
profiles ──< layovers ──< matches >── layovers (other traveller)
                │                        │
                │                        └──── user_a / user_b → profiles
                ├──< itineraries
                │
                ├──< bookings >── storage_facilities
                │         │
                │         ├──< booking_members >── profiles
                │         ├──< payments
                │         └──< access_logs
```

## Tables

| Table | Key columns & constraints |
| --- | --- |
| `profiles` | `id` = auth.users.id (FK cascade); `verification_status` CHECK; interests `text[]` |
| `layovers` | FKs to profiles; CHECK `departure > arrival`; index on `(airport_code, arrival_time, departure_time)` for matching scans |
| `storage_facilities` | `share_min_users ≤ share_max_users` CHECK; `sharing_allowed` gates split pricing |
| `matches` | `score 0–100` CHECK, status CHECK; unique index on the unordered pair to prevent duplicates |
| `bookings` | FK facility/layover; CHECK `ends_at > starts_at`; price always server-computed |
| `booking_members` | `payment_status` CHECK; unique `(booking_id, user_id)`; `can_retrieve` permission flag |
| `payments` | `simulated` boolean always true in MVP; `transaction_ref` prefixed `SIM-` |
| `itineraries` | activities as JSONB; `return_time` NOT NULL; `is_mock` flag |
| `access_logs` | Audit trail: who did what to which booking, when |

## Integrity & security rules

- **No passwords, no card data, no identity documents.** Credentials live in
  Supabase Auth; payments are simulation rows only.
- **RLS everywhere**: profiles are read by all authenticated users (needed for
  matching) but writable only by their owner; layovers, bookings, itineraries
  are owner-scoped; facilities are read-only from the app.
- All tables carry `created_at`; mutable ones add `updated_at` (trigger).
- Demo profiles in `seed.sql` use fixed UUIDs — rebind them to real
  `auth.users` ids as described in [`database/README.md`](../database/README.md).

## Known MVP simplification

The FastAPI backend currently serves from an in-memory store with the same
shapes. The swap-in point is `app/repositories/` only — schemas and services
stay untouched.
