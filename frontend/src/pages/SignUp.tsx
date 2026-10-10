import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { supabase, isOfflineMode } from "../lib/supabase";
import Card from "../components/common/Card";

export default function SignUp() {
  const nav = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [displayName, setDisplayName] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const offline = isOfflineMode();

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (offline) {
      setError("Demo mode: add Supabase credentials to .env to enable real sign-up.");
      return;
    }
    setBusy(true);
    setError(null);
    const { error } = await supabase!.auth.signUp({
      email,
      password,
      options: { data: { display_name: displayName } },
    });
    setBusy(false);
    if (error) setError(error.message);
    else nav("/dashboard");
  }

  return (
    <div className="max-w-md mx-auto px-4 py-20">
      <h1 className="font-display text-3xl font-bold mb-2">Join LAYOVER</h1>
      <p className="text-midnight-300 mb-6">
        Turn dead airport hours into something worth remembering.
      </p>
      <Card>
        <form onSubmit={submit} className="space-y-4">
          <input
            className="input"
            placeholder="Display name"
            value={displayName}
            onChange={(e) => setDisplayName(e.target.value)}
            required
          />
          <input
            className="input"
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            className="input"
            type="password"
            placeholder="Password (min 8 characters)"
            minLength={8}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          {error && <p className="text-sm text-sunset-500">{error}</p>}
          <button className="btn-primary w-full" disabled={busy}>
            {busy ? "Creating account…" : "Create account"}
          </button>
        </form>
        <p className="mt-4 text-sm text-midnight-300">
          Already onboard?{" "}
          <Link to="/login" className="text-lavender-300 hover:underline">
            Sign in
          </Link>
        </p>
      </Card>
    </div>
  );
}
