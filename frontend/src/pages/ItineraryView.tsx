import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { generateItinerary, getUsableTime } from "../services";
import { money, minutesLabel, timeStr } from "../utils/format";
import { useCountdown } from "../hooks";
import Card from "../components/common/Card";
import Badge from "../components/common/Badge";
import type { Itinerary, UsableTime } from "../types";

export default function ItineraryView() {
  const { layoverId } = useParams<{ layoverId: string }>();
  const [itinerary, setItinerary] = useState<Itinerary | null>(null);
  const [usable, setUsable] = useState<UsableTime | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(true);
  const { label } = useCountdown(itinerary?.return_time);

  useEffect(() => {
    if (!layoverId) return;
    getUsableTime(layoverId)
      .then(setUsable)
      .then(() => generateItinerary(layoverId))
      .then(setItinerary)
      .catch((err) => setError((err as Error).message))
      .finally(() => setBusy(false));
  }, [layoverId]);

  if (busy) return <div className="py-24 text-center text-lavender-300 animate-pulse">Planning your window…</div>;

  return (
    <div className="max-w-4xl mx-auto px-4 py-16">
      <div className="flex flex-wrap items-center justify-between gap-3 mb-6">
        <div>
          <h1 className="font-display text-3xl font-bold">Your city window</h1>
          {usable && (
            <p className="text-midnight-300 mt-1">{minutesLabel(usable.usable_minutes)} usable</p>
          )}
        </div>
        {itinerary && (
          <Badge tone="sunset">gate return: {timeStr(itinerary.return_time)} · in {label}</Badge>
        )}
      </div>
      {error && <p className="text-sunset-500 mb-4">{error}</p>}

      <div className="grid md:grid-cols-2 gap-6">
        <Card className="space-y-4">
          <h2 className="font-semibold text-lg">Plan (SIMULATED activities)</h2>
          {itinerary?.activities.length === 0 && (
            <p className="text-midnight-300">Not enough time to leave the airport — enjoy the lounge!</p>
          )}
          {itinerary?.activities.map((a, i) => (
            <div key={i} className="relative pl-6 border-l-2 border-lavender-400/30">
              <div className="absolute -left-[7px] top-1 w-3 h-3 rounded-full bg-lavender-400" />
              <div className="flex justify-between text-sm">
                <span className="font-medium">{a.name}</span>
                <span className="text-midnight-300">
                  {timeStr(a.start)}–{timeStr(a.end)}
                </span>
              </div>
              <p className="text-xs text-midnight-400 mt-0.5">
                {a.kind} · {money(a.avg_cost)} · travel {a.travel_minutes}m each way
              </p>
            </div>
          ))}
          {itinerary && itinerary.activities.length > 0 && (
            <p className="text-sm text-midnight-300">
              Estimated spend:{" "}
              <span className="text-sunset-400 font-semibold">
                {money(itinerary.estimated_total_cost, itinerary.currency)}
              </span>
            </p>
          )}
          <Link to={`/storage/${layoverId}`} className="btn-secondary text-sm">
            Store my bags first →
          </Link>
        </Card>

        {/* Map (MOCK is fine here) */}
        <Card className="flex flex-col">
          <h2 className="font-semibold text-lg mb-3">Map</h2>
          <div className="flex-1 min-h-[320px] rounded-xl overflow-hidden border border-midnight-700">
            <MockMap />
          </div>
          <p className="mt-3 text-xs text-midnight-400">
            Map integration is a stub with mock pins — swaps to Leaflet tiles with
            real place data in a later milestone.
          </p>
        </Card>
      </div>
    </div>
  );
}

// --- Simple mock map (no tile server dependency) -----------------------------
function MockMap() {
  // Places from the itinerary mock catalog at fixed demo coordinates.
  const pins = [
    { x: 30, y: 28, label: "Airport" },
    { x: 55, y: 40, label: "Souk" },
    { x: 72, y: 62, label: "Bridge deck" },
    { x: 44, y: 70, label: "Harbor" },
  ];
  return (
    <div className="relative w-full h-full bg-midnight-900">
      {/* faint "streets" */}
      <div className="absolute inset-0 opacity-20 bg-[repeating-linear-gradient(0deg,transparent_0_24px,rgb(167_143_221/0.5)_24px_25px),repeating-linear-gradient(90deg,transparent_0_32px,rgb(167_143_221/0.3)_32px_33px)]" />
      {pins.map((p) => (
        <div
          key={p.label}
          className="absolute -translate-x-1/2 -translate-y-1/2 group"
          style={{ left: `${p.x}%`, top: `${p.y}%` }}
        >
          <span className="block w-3.5 h-3.5 rounded-full bg-sunset-400 shadow-glow" />
          <span className="absolute left-5 top-0 whitespace-nowrap text-xs text-midnight-100">
            {p.label}
          </span>
        </div>
      ))}
    </div>
  );
}
