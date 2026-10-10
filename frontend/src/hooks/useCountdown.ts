import { useEffect, useState } from "react";

/** Ticks every second toward `targetIso`; returns ms left (<= 0 when passed). */
export function useCountdown(targetIso: string | undefined): {
  msLeft: number;
  label: string;
} {
  const [msLeft, setMsLeft] = useState(() =>
    targetIso ? new Date(targetIso).getTime() - Date.now() : 0
  );

  useEffect(() => {
    if (!targetIso) return;
    const t = setInterval(() => {
      setMsLeft(new Date(targetIso).getTime() - Date.now());
    }, 1000);
    return () => clearInterval(t);
  }, [targetIso]);

  const abs = Math.max(0, msLeft);
  const hh = Math.floor(abs / 3_600_000);
  const mm = Math.floor((abs % 3_600_000) / 60_000);
  const ss = Math.floor((abs % 60_000) / 1000);
  const label =
    msLeft <= 0
      ? "Time's up"
      : `${hh}h ${String(mm).padStart(2, "0")}m ${String(ss).padStart(2, "0")}s`;

  return { msLeft, label };
}
