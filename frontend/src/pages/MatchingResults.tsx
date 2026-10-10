import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { acceptMatch, getUsableTime, rejectMatch, runMatching } from "../services";
import { minutesLabel } from "../utils/format";
import Card from "../components/common/Card";
import Badge from "../components/common/Badge";
import type { Match, UsableTime } from "../types";

export default function MatchingResults() {
  const { layoverId } = useParams<{ layoverId: string }>();
  const nav = useNavigate();
  const [matches, setMatches] = useState<Match[]>([]);
  const [usable, setUsable] = useState<UsableTime | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(true);

  useEffect(() => {
    if (!layoverId) return;
    Promise.all([runMatching(layoverId), getUsableTime(layoverId)])
      .then(([m, u]) => {
        setMatches(m);
        setUsable(u);
      })
      .catch((err) => setError((err as Error).message))
      .finally(() => setBusy(false));
  }, [layoverId]);

  async function vote(matchId: string | null, accept: boolean) {
    if (!matchId) return;
    try {
      await (accept ? acceptMatch(matchId) : rejectMatch(matchId));
      setMatches((prev) =>
        prev.map((m) =>
          m.id === matchId ? { ...m, status: accept ? "accepted" : "rejected" } : m
        )
      );
    } catch (err) {
      setError((err as Error).message);
    }
  }

  if (busy) return <div className="py-24 text-center text-lavender-300 animate-pulse">Scoring travellers…</div>;

  return (
    <div className="max-w-4xl mx-auto px-4 py-16">
      <div className="flex flex-wrap items-center justify-between gap-3 mb-6">
        <div>
          <h1 className="font-display text-3xl font-bold">Traveller matches</h1>
          {usable && (
            <p className="text-midnight-300 mt-1">
              {minutesLabel(usable.usable_minutes)} usable · returns buffer {usable.buffer_minutes}m
            </p>
          )}
        </div>
        <Link to={`/storage/${layoverId}`} className="btn-secondary">
          Skip to storage →
        </Link>
      </div>
      {error && <p className="text-sunset-500 mb-4">{error}</p>}
      {matches.length === 0 && (
        <Card>
          <p className="text-midnight-200">
            No overlapping travellers right now — in the demo, seed another user's
            layover or change airports. Storage is still available!
          </p>
        </Card>
      )}
      <div className="grid gap-4">
        {matches.map((m) => (
          <Card key={m.id ?? m.layover_b} className="flex flex-wrap items-center gap-4">
            <div className="flex-none w-16 h-16 rounded-2xl bg-midnight-800 grid place-items-center text-2xl">
              🧑‍✈️
            </div>
            <div className="flex-1 min-w-[200px]">
              <div className="flex items-center gap-2">
                <h3 className="font-semibold">Traveller at {m.other_layover?.airport_code ?? ""}</h3>
                <Badge tone={m.status === "accepted" ? "lavender" : "neutral"}>{m.status}</Badge>
              </div>
              <p className="text-sm text-midnight-300">
                {m.other_layover?.interests?.join(" · ") || "no listed interests"} ·
                overlap {minutesLabel(m.score_breakdown.overlap_minutes)}
              </p>
              <div className="mt-2 flex gap-2 text-xs text-midnight-300">
                <span>schedule {m.score_breakdown.schedule}</span>
                <span>bags {m.score_breakdown.baggage}</span>
                <span>interests {m.score_breakdown.interest}</span>
              </div>
            </div>
            <div className="text-right">
              <div className="font-display text-3xl font-bold text-lavender-300">
                {m.score.toFixed(0)}
              </div>
              <div className="flex gap-2 mt-2">
                <button
                  className="btn-primary text-sm"
                  disabled={m.status !== "proposed"}
                  onClick={() => vote(m.id, true)}
                >
                  Accept
                </button>
                <button
                  className="btn-secondary text-sm"
                  disabled={m.status !== "proposed"}
                  onClick={() => vote(m.id, false)}
                >
                  Pass
                </button>
              </div>
            </div>
          </Card>
        ))}
      </div>
      {matches.some((m) => m.status === "accepted") && (
        <p className="mt-6 text-sm text-midnight-300">
          Matched! Next: lock a shared locker —{" "}
          <button className="text-lavender-300 underline" onClick={() => nav(`/storage/${layoverId}`)}>
            browse storage at your airport
          </button>
          .
        </p>
      )}
    </div>
  );
}
