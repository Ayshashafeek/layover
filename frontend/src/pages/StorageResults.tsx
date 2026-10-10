import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { listFacilities } from "../services";
import { money } from "../utils/format";
import Card from "../components/common/Card";
import Badge from "../components/common/Badge";
import type { StorageFacility } from "../types";

export default function StorageResults() {
  const { layoverId, airport: airportParam } = useParams<{ layoverId: string; airport: string }>();
  const airport = airportParam ?? "DXB";
  const [facilities, setFacilities] = useState<StorageFacility[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(true);

  useEffect(() => {
    if (!layoverId) return;
    listFacilities(airport ?? "DXB")
      .then(setFacilities)
      .catch((err) => setError((err as Error).message))
      .finally(() => setBusy(false));
  }, [layoverId, airport]);

  if (busy) return <div className="py-24 text-center text-lavender-300 animate-pulse">Finding lockers…</div>;

  return (
    <div className="max-w-4xl mx-auto px-4 py-16">
      <div className="flex items-center justify-between mb-6">
        <h1 className="font-display text-3xl font-bold">Storage at {airport ?? "airport"}</h1>
        <Link to={`/matches/${layoverId}`} className="btn-secondary">
          ← Back to matches
        </Link>
      </div>
      {error && <p className="text-sunset-500 mb-4">{error}</p>}
      <div className="grid gap-4">
        {facilities.map((f) => (
          <Card key={f.id} className="flex flex-wrap items-center gap-4">
            <div className="flex-1 min-w-[220px]">
              <div className="flex items-center gap-2 flex-wrap">
                <h3 className="font-semibold">{f.provider_name}</h3>
                {f.simulated && <Badge tone="sunset">simulated</Badge>}
                {f.sharing_allowed ? (
                  <Badge>shareable</Badge>
                ) : (
                  <Badge tone="neutral">solo only</Badge>
                )}
              </div>
              <p className="text-sm text-midnight-300 mt-1">{f.location}</p>
              <p className="text-xs text-midnight-400 mt-1">
                Open {f.opening_time}–{f.closing_time} · capacity {f.capacity_total} ·
                groups {f.share_min_users}–{f.share_max_users}
              </p>
            </div>
            <div className="text-right">
              <div className="font-display text-2xl font-bold text-sunset-400">
                {money(f.price_per_bag_hour, f.currency)}
              </div>
              <div className="text-xs text-midnight-400">per bag · hour</div>
              <Link
                to={`/cost/${layoverId}/${f.id}`}
                className="btn-primary text-sm mt-2"
              >
                Split cost →
              </Link>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
