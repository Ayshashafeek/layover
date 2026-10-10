import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { createBooking, getUsableTime, quoteShared } from "../services";
import { money } from "../utils/format";
import Card from "../components/common/Card";
import Badge from "../components/common/Badge";
import type { SharedQuote, UsableTime } from "../types";

export default function CostBreakdown() {
  const { layoverId, facilityId } = useParams<{ layoverId: string; facilityId: string }>();
  const nav = useNavigate();
  const [quote, setQuote] = useState<SharedQuote | null>(null);
  const [usable, setUsable] = useState<UsableTime | null>(null);
  const [people, setPeople] = useState(2);
  const [hours, setHours] = useState(4);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    if (!layoverId || !facilityId) return;
    getUsableTime(layoverId)
      .then((u) => {
        setUsable(u);
        // Suggest max sensible hours within the usable window.
        setHours(Math.max(1, Math.min(4, Math.floor(u.usable_minutes / 120))));
      })
      .catch((err) => setError((err as Error).message));
  }, [layoverId, facilityId]);

  async function refreshQuote(p: number, h: number) {
    if (!facilityId) return;
    setBusy(true);
    setError(null);
    try {
      setQuote(
        await quoteShared({ facility_id: facilityId, hours: h, bags: 1, people: p })
      );
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusy(false);
    }
  }

  // Initial quote fetch once hours are known.
  useEffect(() => {
    if (usable && !quote) refreshQuote(people, hours);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [usable]);

  async function book() {
    if (!layoverId || !usable) return;
    const start = new Date(Date.now() + 60 * 60 * 1000); // 1 h from now — demo
    const end = new Date(start.getTime() + hours * 3_600_000);
    setBusy(true);
    setError(null);
    try {
      const booking = await createBooking({
        facility_id: facilityId!,
        layover_id: layoverId,
        starts_at: start.toISOString(),
        ends_at: end.toISOString(),
        people,
      });
      nav(`/booking/${booking.id}`);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="max-w-2xl mx-auto px-4 py-16">
      <h1 className="font-display text-3xl font-bold mb-2">Shared cost breakdown</h1>
      <p className="text-midnight-300 mb-6">
        Prices come from the facility — we only do the math.
      </p>
      <Card className="space-y-5">
        <div className="grid sm:grid-cols-2 gap-4">
          <label className="block">
            <span className="text-sm text-midnight-200">People sharing</span>
            <input
              className="input mt-1"
              type="number"
              min={1}
              max={8}
              value={people}
              onChange={(e) => {
                const p = Number(e.target.value);
                setPeople(p);
                refreshQuote(p, hours);
              }}
            />
          </label>
          <label className="block">
            <span className="text-sm text-midnight-200">Hours needed</span>
            <input
              className="input mt-1"
              type="number"
              min={1}
              max={24}
              value={hours}
              onChange={(e) => {
                const h = Number(e.target.value);
                setHours(h);
                refreshQuote(people, h);
              }}
            />
          </label>
        </div>

        {quote && (
          <div className="rounded-xl bg-midnight-800/60 border border-midnight-700 p-4 space-y-2">
            <div className="flex justify-between text-sm">
              <span>Solo price</span>
              <span>{money(quote.solo_total, quote.currency)}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span>Shared per person</span>
              <span className="font-semibold text-lavender-300">
                {money(quote.shared_per_person, quote.currency)}
              </span>
            </div>
            <div className="flex justify-between text-sm">
              <span>You save</span>
              <span className="text-sunset-400">
                {money(quote.savings_per_person, quote.currency)} ({quote.savings_percent}%)
              </span>
            </div>
            {(quote.violates_max_users || !quote.sharing_allowed) && (
              <Badge tone="sunset">
                {quote.sharing_allowed
                  ? "Group exceeds this facility's max sharing size — solo price applies"
                  : "This facility doesn't allow sharing — solo price applies"}
              </Badge>
            )}
          </div>
        )}
        {error && <p className="text-sm text-sunset-500">{error}</p>}
        <button className="btn-primary w-full" disabled={busy || !quote} onClick={book}>
          {busy ? "Working…" : "Reserve locker (demo)"}
        </button>
        <Link to={`/storage/${layoverId}`} className="block text-center text-sm text-midnight-300 hover:underline">
          ← pick a different facility
        </Link>
      </Card>
      <p className="mt-3 text-xs text-midnight-400">
        Booking start defaults to 1 h from now; adjust in a later milestone.
        Reservation is SIMULATED — no real locker is held.
      </p>
    </div>
  );
}
