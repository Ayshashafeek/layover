import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { supabase, isOfflineMode } from "../lib/supabase";
import Card from "../components/common/Card";

export default function Login() {
  const nav = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const offline = isOfflineMode();

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (offline) {
      // SIMULATED: no Supabase creds configured — demo-only sign-in stub.
      setError("Demo mode: add Supabase credentials to .env to enable real sign-in.");
      return;
    }
    setBusy(true);
    setError(null);
    const { error } = await supabase!.auth.signInWithPassword({ email, password });
    setBusy(false);
    if (error) setError(error.message);
    else nav("/dashboard");
  }

  return (
    <div className="max-w-md mx-auto px-4 py-20">
      <h1 className="font-display text-3xl font-bold mb-2">Welcome back</h1>
      <p className="text-midnight-300 mb-6">Your layover receipts are waiting.</p>
      <Card>
        <form onSubmit={submit} className="space-y-4">
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
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          {error && <p className="text-sm text-sunset-500">{error}</p>}
          <button className="btn-primary w-full" disabled={busy}>
            {busy ? "Signing in…" : "Sign in"}
          </button>
        </form>
        <p className="mt-4 text-sm text-midnight-300">
          New here?{" "}
          <Link to="/signup" className="text-lavender-300 hover:underline">
            Create an account
          </Link>
        </p>
      </Card>
    </div>
  );
}
