/** Named service wrappers — the ONLY place pages/services touch the raw API. */
import { api } from "../lib/api";
import type {
  Booking,
  Itinerary,
  Layover,
  Match,
  Payment,
  SharedQuote,
  StorageFacility,
  UsableTime,
} from "../types";

// --- health ---------------------------------------------------------------
export function getHealth() {
  return api<{ status: string; mode: string }>("/api/health");
}

// --- layovers -------------------------------------------------------------
export function createLayover(body: {
  airport_code: string;
  arrival_time: string;
  departure_time: string;
  baggage_count: number;
  budget_total: number;
  interests: string[];
}) {
  return api<Layover>("/api/layovers", { method: "POST", body });
}
export function myLayovers() {
  return api<Layover[]>("/api/layovers/mine");
}
export function getUsableTime(layoverId: string) {
  return api<UsableTime>(`/api/layovers/${layoverId}/usable-time`);
}

// --- matching -------------------------------------------------------------
export function runMatching(layoverId: string) {
  return api<Match[]>(`/api/matches/${layoverId}/run`, { method: "POST" });
}
export function acceptMatch(matchId: string) {
  return api<Match>(`/api/matches/${matchId}/accept`, { method: "POST" });
}
export function rejectMatch(matchId: string) {
  return api<Match>(`/api/matches/${matchId}/reject`, { method: "POST" });
}

// --- storage --------------------------------------------------------------
export function listFacilities(airport: string) {
  return api<StorageFacility[]>(`/api/storage?airport=${encodeURIComponent(airport)}`);
}
export function quoteShared(body: {
  facility_id: string;
  hours: number;
  bags: number;
  people: number;
}) {
  return api<SharedQuote>("/api/storage/quote", { method: "POST", body });
}

// --- bookings -------------------------------------------------------------
export function createBooking(body: {
  facility_id: string;
  layover_id: string;
  starts_at: string;
  ends_at: string;
  people: number;
}) {
  return api<Booking>("/api/bookings", { method: "POST", body });
}
export function myBookings() {
  return api<Booking[]>("/api/bookings/mine");
}
export function cancelBooking(bookingId: string) {
  return api<Booking>(`/api/bookings/${bookingId}/cancel`, { method: "POST" });
}

// --- payments (simulated) ---------------------------------------------------
export function payShare(bookingId: string) {
  return api<Payment>("/api/payments/pay", { method: "POST", body: { booking_id: bookingId } });
}
export function refundShare(bookingId: string) {
  return api<Payment>("/api/payments/refund", { method: "POST", body: { booking_id: bookingId } });
}

// --- itineraries ------------------------------------------------------------
export function generateItinerary(layoverId: string) {
  return api<Itinerary>(`/api/itineraries/generate/${layoverId}`, { method: "POST" });
}
export function myItineraries() {
  return api<Itinerary[]>("/api/itineraries/mine");
}
