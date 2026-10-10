-- ============================================================================
-- LAYOVER — seed data for demo
-- Run AFTER schema.sql in the Supabase SQL editor.
-- NOTE: profile rows reference auth.users via the "demo user" invited below —
--       see database/README.md for how to attach these to a real Supabase user.
-- ============================================================================
-- Because auth.users rows can only be created through Supabase Auth, we seed
-- profile rows with fixed UUIDs; if you invite users with these same emails
-- Supabase will produce matching ids you can update to. For the hackathon demo
-- we insert demo profiles straddling auth and hope you onboard quickly.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Demo profiles (attach real auth users later, see README)
-- ----------------------------------------------------------------------------
insert into public.profiles (id, display_name, avatar_url, verification_status, interests) values
  ('11111111-1111-1111-1111-111111111111', 'Demo Admin',    null, 'verified',   {'food','architecture'}),
  ('22222222-2222-2222-2222-222222222222', 'Aisha Sharma',  null, 'verified',   {'food','art'}),
  ('33333333-3333-3333-3333-333333333333', 'Marco Rossi',   null, 'unverified', {'history','walking tours'})
on conflict (id) do nothing;

-- ----------------------------------------------------------------------------
-- Storage facilities (SIMULATED providers — not real airport partners)
-- ----------------------------------------------------------------------------
insert into public.storage_facilities
  (provider_name, airport_code, location, lat, lng, price_per_bag_hour, currency,
   capacity_total, share_max_users, share_min_users, opening_time, closing_time, sharing_allowed) values
  ('SmartLocker Hub',  'DXB', 'Terminal 1, Level 1 near Exit 4',   25.253200,  55.365400, 4.50, 'USD', 120, 4, 1, '00:00', '23:59', true),
  ('BagsAway DXB',     'DXB', 'Terminal 3, Arrivals Hall',          25.258000,  55.361000, 5.00, 'USD',  60, 3, 2, '05:00', '23:00', true),
  ('Fly&Store Lounge', 'DXB', 'Terminal 2, near Gate C12',          25.249000,  55.370000, 3.75, 'USD',  40, 2, 2, '06:00', '22:00', true),
  ('CityLocker Small', 'DXB', 'Airport Metro station, Exit 2',      25.247000,  55.355000, 2.50, 'USD',  20, 2, 1, '07:00', '21:00', false),
  ('SmartLocker Hub',  'JFK', 'Terminal 4, Level 2, near Gate B30', 40.644600, -73.779700, 6.00, 'USD',  80, 4, 2, '00:00', '23:59', true),
  ('BagsAway Lounge',  'JFK', 'Terminal 1, Arrivals Hall level 1',  40.649800, -73.780900, 5.50, 'USD',  35, 2, 2, '05:00', '23:00', true);

-- ----------------------------------------------------------------------------
-- Demo layovers attached to demo profiles (times chosen so a demo "now" sorts
-- in the near future; adjust timestamps as needed for your demo timezone)
-- ----------------------------------------------------------------------------
insert into public.layovers (user_id, airport_code, arrival_time, departure_time, baggage_count, budget_total, currency, interests) values
  ('11111111-1111-1111-1111-111111111111', 'DXB', now() + interval '1 hour',  now() + interval '7 hours',  1, 80.00, 'USD', array['food','city tour']),
  ('22222222-2222-2222-2222-222222222222', 'DXB', now() + interval '2 hours', now() + interval '8 hours',  2, 120.00,'USD', array['food','art']),
  ('33333333-3333-3333-3333-333333333333', 'DXB', now() + interval '3 hours', now() + interval '9 hours',  1, 50.00, 'USD', array['history','walking tours']);

-- Matching has not run yet on first boot; the match endpoint will insert rows
-- lazily once a user calls POST /api/matches with their layover id.
