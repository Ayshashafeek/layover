/** Types mirroring the FastAPI schemas in backend/app/schemas/core.py. */

export interface Profile {
  id: string;
  display_name: string;
  avatar_url: string | null;
  verification_status: "unverified" | "pending" | "verified";
  interests: string[];
}

export interface Layover {
  id: string;
  user_id: string;
  airport_code: string;
  arrival_time: string;
  departure_time: string;
  baggage_count: number;
  budget_total: number;
  currency: string;
  interests: string[];
}

export interface UsableTime {
  layover_id: string;
  usable_minutes: number;
  total_minutes: number;
  buffer_minutes: number;
  hint?: string;
}

export interface Match {
  id: string | null;
  layover_a: string;
  layover_b: string;
  user_a: string;
  user_b: string;
  score: number;
  score_breakdown: {
    total: number;
    schedule: number;
    baggage: number;
    interest: number;
    overlap_minutes: number;
  };
  status: "proposed" | "accepted" | "rejected" | "expired";
  other_layover?: Layover;
}

export interface StorageFacility {
  id: string;
  provider_name: string;
  airport_code: string;
  location: string;
  lat: number | null;
  lng: number | null;
  price_per_bag_hour: number;
  currency: string;
  capacity_total: number;
  share_min_users: number;
  share_max_users: number;
  opening_time: string;
  closing_time: string;
  sharing_allowed: boolean;
  simulated: boolean;
}

export interface SharedQuote {
  facility_id: string;
  hours: number;
  bags: number;
  people: number;
  solo_total: number;
  shared_total: number;
  shared_per_person: number;
  savings_per_person: number;
  savings_percent: number;
  currency: string;
  sharing_allowed: boolean;
  violates_min_users: boolean;
  violates_max_users: boolean;
}

export interface BookingMember {
  user_id: string;
  cost_share: number;
  currency: string;
  payment_status: "unpaid" | "paid" | "refunded";
  can_retrieve: boolean;
}

export interface Booking {
  id: string;
  facility_id: string;
  created_by: string;
  layover_id: string;
  starts_at: string;
  ends_at: string;
  total_price: number;
  currency: string;
  status: "pending" | "confirmed" | "cancelled" | "expired";
  members: BookingMember[];
}

export interface Payment {
  id: string;
  booking_id: string;
  payer_id: string;
  amount: number;
  currency: string;
  status: "simulated_pending" | "simulated_paid" | "simulated_refunded" | "failed";
  transaction_ref: string;
  simulated: boolean;
}

export interface Activity {
  name: string;
  start: string;
  end: string;
  travel_minutes: number;
  kind: string;
  avg_cost: number;
  is_mock: boolean;
}

export interface Itinerary {
  layover_id: string;
  activities: Activity[];
  return_time: string;
  usable_minutes: number;
  estimated_total_cost: number;
  currency: string;
  is_mock: boolean;
}
