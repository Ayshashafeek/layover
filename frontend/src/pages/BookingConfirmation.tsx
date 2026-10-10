import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { cancelBooking, myBookings, payShare, refundShare } from "../services";
import { money, timeStr } from "../utils/format";
import { useCountdown } from "../hooks";
import Card from "../components/common/Card";
import Badge from "../components/common/Badge";
import type { Booking, Payment } from "../types";

export default function BookingConfirmation() {
  const { bookingId } = useParams<{ bookingId: string }>();
  const [booking, setBooking] = useState<Booking | null>(null);
  const [payment, setPayment] = useState<Payment | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(true);
  const { label } = useCountdown(booking?.starts_at);

  async function load() {
    try {
      const res = await fetchBooking();
      setBooking(res);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusy(false);
    }
  }

  function fetchBooking(): Promise<Booking> {
    // my-bookings is the lightest safe endpoint for demo; in a full app we
    // would add GET /api/bookings/{id}.
    return myBookings().then((all) => {
      const found = all.find((b) => b.id === bookingId);
      if (!found) throw new Error("Booking not found in your list");
      return found;
    });
  }

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [bookingId]);

  async function doPay() {
    if (!bookingId) return;
    try {
      setPayment(await payShare(bookingId));
      await load();
    } catch (err) {
      setError((err as Error).message);
    }
  }

  async function doRefund() {
    if (!bookingId) return;
    try {
      setPayment(await refundShare(bookingId));
      await load();
    } catch (err) {
      setError((err as Error).message);
    }
  }

  async function doCancel() {
    if (!booking) return;
    try {
      const updated = await cancelBooking(booking.id);
      setBooking(updated);
    } catch (err) {
      setError((err as Error).message);
    }
  }

  if (busy) return <div className="py-24 text-center text-lavender-300 animate-pulse">Loading booking…</div>;
  if (!booking) return <div className="py-24 text-center text-midnight-200">{error ?? "Booking not found"}</div>;

  return (
    <div className="max-w-2xl mx-auto px-4 py-16">
      <h1 className="font-display text-3xl font-bold mb-2">Your locker booking</h1>
      <p className="text-midnight-300 mb-6">
        Starts {timeStr(booking.starts_at)} — in {label}
      </p>
      <Card className="space-y-4">
        <div className="flex items-center justify-between">
          <span className="text-midnight-200">Status</span>
          <Badge tone={booking.status === "confirmed" ? "lavender" : "neutral"}>
            {booking.status}
          </Badge>
        </div>
        <div className="flex items-center justify-between">
          <span className="text-midnight-200">Total</span>
          <span className="font-semibold">{money(booking.total_price, booking.currency)}</span>
        </div>
        <div>
          <span className="text-midnight-200 text-sm">Members &amp; shares</span>
          <ul className="mt-2 space-y-1">
            {booking.members.map((m, i) => (
              <li key={i} className="flex justify-between text-sm">
                <span className="text-midnight-300">
                  {m.user_id.slice(0, 8)}… {m.can_retrieve && "🔑 retriever"}
                </span>
                <span>
                  {money(m.cost_share, m.currency)} · {m.payment_status}
                </span>
              </li>
            ))}
          </ul>
        </div>
        {payment && (
          <p className="text-xs text-midnight-400">
            Last transaction: {payment.transaction_ref} ({payment.status}) — SIMULATED,
            no real money moved.
          </p>
        )}
        {error && <p className="text-sm text-sunset-500">{error}</p>}
        <div className="flex flex-wrap gap-3">
          <button className="btn-primary" onClick={doPay} disabled={booking.status === "cancelled"}>
            Pay my share
          </button>
          <button className="btn-secondary" onClick={doRefund} disabled={booking.status === "cancelled"}>
            Refund (simulated)
          </button>
          <button className="btn-secondary" onClick={doCancel} disabled={booking.status === "cancelled"}>
            Cancel booking
          </button>
        </div>
        <Link to="/dashboard" className="block text-center text-sm text-midnight-300 hover:underline">
          ← dashboard
        </Link>
      </Card>
      <p className="mt-3 text-xs text-midnight-400">
        Payments and confirmation are SIMULATED for the MVP; no locker is actually reserved.
      </p>
    </div>
  );
}
