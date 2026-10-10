# LAYOVER — Database

This directory is the single source of truth for the LAYOVER Postgres schema.

## Connecting your Supabase project (one-time, ~5 min)

1. Go to <https://supabase.com> → **Sign in** → **New project**.
   - Choose a name (e.g. `layover-hackathon`), a region near your team, and a
     database password. **Store this password somewhere safe** (a shared
     password manager works fine).
2. When the project finishes provisioning, open
   **Project Settings → API** and copy:
   - **Project URL** → set this to `SUPABASE_URL` in `backend/.env` and
     `VITE_SUPABASE_URL` in `frontend/.env`
   - **anon public key** → `SUPABASE_ANON_KEY` / `VITE_SUPABASE_ANON_KEY`
   - **service_role key** → `SUPABASE_SERVICE_ROLE_KEY` **backend only**
3. Open **SQL editor** in the left sidebar.
4. Paste the full contents of [`schema.sql`](schema.sql) and click **Run**.
5. Paste the full contents of [`seed.sql`](seed.sql) and click **Run**.
6. Go to **Authentication → Providers → Email** and enable it (password or
   magic-link, either works — the backend validates bearer tokens either way).

## Tables created

| Table | Purpose |
| --- | --- |
| `profiles` | User-facing profile + `verification_status` + interests |
| `layovers` | One traveller's airport time window and preferences |
| `storage_facilities` | SIMULATED luggage storage providers (no real partner) |
| `matches` | Candidate traveller pairs + compatibility `score` 0-100 |
| `bookings` | Reservation against a facility, interval + total_price |
| `booking_members` | Participants, `cost_share`, `payment_status`, `can_retrieve` |
| `payments` | SIMULATED payment/refund records (no real gateway) |
| `itineraries` | Generated activities + return_time, all activities have `is_mock` |
| `access_logs` | Audit trail of booking actions |

## Attaching the seed profiles to real Supabase users

`seed.sql` inserts three demo `profiles` rows with hard-coded UUIDs and no
backing `auth.users` rows. To demo properly:

1. In the Supabase dashboard go to **Authentication → Users → Add user** and
   create accounts with any emails/passwords, e.g `aisha@demo.layover` /
   `marco@demo.layover`.
2. In the SQL editor, `update public.profiles set id = '<auth-users-uuid>'
   where id = '<seed-uuid>';` — the cascade-mapped FKs follow automatically.
   (Or simply delete the seeded rows and let matching insert fresh ones.)

## Local psql alternative

If you prefer a local Postgres instead of Supabase for offline work:

```bash
psql -U postgres -c "create database layover;"
psql -U postgres -d layover -f database/schema.sql
psql -U postgres -d layover -f database/seed.sql
```

Note: the RLS policies use `auth.uid()` / `auth.role()`, which are Supabase
functions. For local-only hacking, replace them with `true` / stub functions,
or run Supabase local dev (`npx supabase init && npx supabase start`).

## Reset / clean-up

```sql
drop schema public cascade;
create schema public;
```
Then re-run `schema.sql` and `seed.sql`.
