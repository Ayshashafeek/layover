import { useEffect, useState } from "react";
import { api } from "../lib/api";
import Card from "../components/common/Card";
import Badge from "../components/common/Badge";
import type { Profile as ProfileType } from "../types";

export default function Profile() {
  const [profile, setProfile] = useState<ProfileType | null>(null);
  const [displayName, setDisplayName] = useState("");
  const [interests, setInterests] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    api<ProfileType>("/api/users/me")
      .then((p) => {
        setProfile(p);
        setDisplayName(p.display_name);
        setInterests(p.interests.join(", "));
      })
      .catch((err) => setError((err as Error).message));
  }, []);

  async function save(e: React.FormEvent) {
    e.preventDefault();
    try {
      const updated = await api<ProfileType>("/api/users/me", {
        method: "PATCH",
        body: {
          display_name: displayName,
          interests: interests
            .split(",")
            .map((i) => i.trim())
            .filter(Boolean),
        },
      });
      setProfile(updated);
      setSaved(true);
      setTimeout(() => setSaved(false), 2500);
    } catch (err) {
      setError((err as Error).message);
    }
  }

  return (
    <div className="max-w-xl mx-auto px-4 py-16">
      <h1 className="font-display text-3xl font-bold mb-6">Profile</h1>
      <Card className="space-y-4">
        {profile && (
          <div className="flex items-center gap-3">
            <div className="w-14 h-14 rounded-2xl bg-midnight-800 grid place-items-center text-2xl">
              🧑‍✈️
            </div>
            <div>
              <div className="font-semibold">{profile.display_name}</div>
              <Badge
                tone={
                  profile.verification_status === "verified"
                    ? "lavender"
                    : "sunset"
                }
              >
                verification: {profile.verification_status} (SIMULATED)
              </Badge>
            </div>
          </div>
        )}
        <form onSubmit={save} className="space-y-4">
          <label className="block">
            <span className="text-sm text-midnight-200">Display name</span>
            <input
              className="input mt-1"
              value={displayName}
              onChange={(e) => setDisplayName(e.target.value)}
              required
            />
          </label>
          <label className="block">
            <span className="text-sm text-midnight-200">Interests (comma-separated)</span>
            <input
              className="input mt-1"
              value={interests}
              onChange={(e) => setInterests(e.target.value)}
              placeholder="food, art, history"
            />
          </label>
          {error && <p className="text-sm text-sunset-500">{error}</p>}
          <button className="btn-primary">{saved ? "Saved ✓" : "Save changes"}</button>
        </form>
        <p className="text-xs text-midnight-400">
          Verification status is SIMULATED — LAYOVER does not verify identity documents.
        </p>
      </Card>
    </div>
  );
}
