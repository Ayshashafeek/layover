import { createClient, type SupabaseClient } from "@supabase/supabase-js";

const url = import.meta.env.VITE_SUPABASE_URL as string | undefined;
const anonKey = import.meta.env.VITE_SUPABASE_ANON_KEY as string | undefined;

/**
 * Shared Supabase client. Only the ANON key is ever used here — the
 * service-role key must never reach the frontend. When credentials are
 * missing (offline demo) the app degrades gracefully to mock data.
 */
export const supabase: SupabaseClient | null =
  url && anonKey ? createClient(url, anonKey) : null;

/** True when the app runs without Supabase creds (browser-only demo mode). */
export function isOfflineMode(): boolean {
  return supabase === null;
}
