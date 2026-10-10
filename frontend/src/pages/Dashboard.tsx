import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getHealth, myBookings, myLayovers } from "../services";
import { minutesLabel, money, timeStr } from "../utils/format";
import Card from "../components/common/Card";
import Badge from "../components/common/Badge";
import type { Booking, Layover } from "../types";

export default function Dashboard() {
  const [layovers, setLayovers] = useState<Layover[]>([]);
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [mode, setMode] = useState<string>("");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([myLayovers(), myBookings(), getHealth()])
      .then(([l, b, h]) => {
        setLayovers(l);
        setBookings(b);
        setMode(h.mode);
      })
      .catch((err) => setError((err as Error).message));
  }, []);

  return (
    <div className="max-w-4xl mx-auto px-4 py-16">
      <div className="flex flex-wrap items-center justify-between gap-3 mb-6">
        <h1 className="font-display text-3xl font-bold">Your layover dashboard</h1>
        {mode && <Badge tone={mode === "offline" ? "sunset" : "lavender"}>backend: {mode}</Badge>}
      </div>
      {error && <p className="text-sunset-500 mb-4">{error}</p>}

      <Card className="mb-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="font-semibold text-lg">New layover</h2>
            <p className="text-sm text-midnight-300">Enter your times to unlock matching, storage and plans.</p>
          </div>
          <Link to="/layover" className="btn-primary">+ add</Link>
        </div>
      </Card>

      <h2 className="font-semibold mb-3">My layovers</h2>
      <div className="grid gap-3 mb-8">
        {layovers.length === 0 && <p className="text-midnight-300">None yet — add your first.</p>}
        {layovers.map((l) => (
          <Card key={l.id} className="flex flex-wrap items-center gap-4">
            <div className="font-display text-xl font-bold text-lavender-300 w-16">{l.airport_code}</div>
            <div className="flex-1 min-w-[180px] text-sm text-midnight-300">
              {timeStr(l.arrival_time)} → {timeStr(l.departure_time)} · {l.baggage_count} bag(s) ·{" "}
              {money(l.budget_total, l.currency)}
            </div>
            <div className="flex gap-2">
              <Link to={`/matches/${l.id}`} className="btn-secondary text-sm">matches</Link>
              <Link to={`/itinerary/${l.id}`} className="btn-secondary text-sm">itinerary</Link>
            </div>
          </Card>
        ))}
      </div>

      <h2 className="font-semibold mb-3">My bookings</h2>
      <div className="grid gap-3">
        {bookings.length === 0 && <p className="text-midnight-300">No locker bookings yet.</p>}
        {bookings.map((b) => (
          <Card key={b.id} className="flex flex-wrap items-center gap-4">
            <Badge tone={b.status === "confirmed" ? "lavender" : "neutral"}>{b.status}</Badge>
            <div className="text-sm text-midnight-300">
              {timeStr(b.starts_at)}–{timeStr(b.ends_at)}
            </div>
            <div className="ml-auto font-semibold">
              {money(b.total_price, b.currency)}
            </div>
            <Link to={`/booking/${b.id}`} className="btn-secondary text-sm">details</Link>
          </Card>
        ))}
      </div>
      <p className="mt-8 text-xs text-midnight-400">
        Layover usable time is real math (buffers {minutesLabel(90)} on each end);
        bookings and payments remain SIMULATED.
      </p>
    </div>
  );
}
