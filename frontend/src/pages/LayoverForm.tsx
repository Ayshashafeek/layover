import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createLayover } from "../services";
import Card from "../components/common/Card";

const INTEREST_OPTIONS = ["food", "art", "history", "nature", "shopping", "nightlife"];

export default function LayoverForm() {
  const nav = useNavigate();
  const [airport, setAirport] = useState("DXB");
  const [arrivalTime, setArrivalTime] = useState("");
  const [departureTime, setDepartureTime] = useState("");
  const [bags, setBags] = useState(1);
  const [budget, setBudget] = useState(80);
  const [interests, setInterests] = useState<string[]>(["food"]);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  function toggleInterest(item: string) {
    setInterests((prev) =>
      prev.includes(item) ? prev.filter((i) => i !== item) : [...prev, item]
    );
  }

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setBusy(true);
    setError(null);
    try {
      const layover = await createLayover({
        airport_code: airport.trim().toUpperCase(),
        arrival_time: new Date(arrivalTime).toISOString(),
        departure_time: new Date(departureTime).toISOString(),
        baggage_count: bags,
        budget_total: budget,
        interests,
      });
      nav(`/matches/${layover.id}`);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="max-w-2xl mx-auto px-4 py-16">
      <h1 className="font-display text-3xl font-bold mb-2">Your layover</h1>
      <p className="text-midnight-300 mb-6">
        Tell us when and where — we'll find matches, storage, and things to do.
      </p>
      <Card>
        <form onSubmit={submit} className="space-y-5">
          <div className="grid sm:grid-cols-2 gap-4">
            <label className="block">
              <span className="text-sm text-midnight-200">Airport (IATA)</span>
              <input
                className="input mt-1"
                maxLength={4}
                placeholder="e.g. DXB"
                value={airport}
                onChange={(e) => setAirport(e.target.value)}
                required
              />
            </label>
            <label className="block">
              <span className="text-sm text-midnight-200">Checked bags</span>
              <input
                className="input mt-1"
                type="number"
                min={0}
                max={10}
                value={bags}
                onChange={(e) => setBags(Number(e.target.value))}
              />
            </label>
          </div>
          <div className="grid sm:grid-cols-2 gap-4">
            <label className="block">
              <span className="text-sm text-midnight-200">Arrival</span>
              <input
                className="input mt-1"
                type="datetime-local"
                value={arrivalTime}
                onChange={(e) => setArrivalTime(e.target.value)}
                required
              />
            </label>
            <label className="block">
              <span className="text-sm text-midnight-200">Departure</span>
              <input
                className="input mt-1"
                type="datetime-local"
                value={departureTime}
                onChange={(e) => setDepartureTime(e.target.value)}
                required
              />
            </label>
          </div>
          <label className="block">
            <span className="text-sm text-midnight-200">Budget (USD)</span>
            <input
              className="input mt-1"
              type="number"
              min={0}
              value={budget}
              onChange={(e) => setBudget(Number(e.target.value))}
            />
          </label>
          <div>
            <span className="text-sm text-midnight-200">Interests</span>
            <div className="mt-2 flex flex-wrap gap-2">
              {INTEREST_OPTIONS.map((item) => (
                <button
                  type="button"
                  key={item}
                  onClick={() => toggleInterest(item)}
                  className={`badge cursor-pointer ${
                    interests.includes(item)
                      ? "border-lavender-400 bg-lavender-500/20 text-lavender-200"
                      : "border-midnight-600 text-midnight-300"
                  }`}
                >
                  {item}
                </button>
              ))}
            </div>
          </div>
          {error && <p className="text-sm text-sunset-500">{error}</p>}
          <button className="btn-primary w-full" disabled={busy}>
            {busy ? "Finding matches…" : "Find my people →"}
          </button>
        </form>
      </Card>
      <p className="mt-3 text-xs text-midnight-400">
        Flight times are self-reported (SIMULATED — no live flight feed).
      </p>
    </div>
  );
}
