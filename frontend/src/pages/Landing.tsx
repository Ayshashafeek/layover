import { Link } from "react-router-dom";

const features = [
  {
    icon: "🤝",
    title: "Smart matching",
    text: "We pair you with travellers whose layovers overlap yours at the same airport.",
  },
  {
    icon: "🧳",
    title: "Shared storage",
    text: "Split a locker with your matches — see exactly what each person pays before booking.",
  },
  {
    icon: "🗺️",
    title: "City micro-trips",
    text: "A plan that fits your window, with a countdown to get you back to the gate.",
  },
];
// SIMULATED: hero imagery is decorative CSS; no live airport-data integration.

export default function Landing() {
  return (
    <div>
      {/* Hero */}
      <section className="relative overflow-hidden">
        <div className="max-w-6xl mx-auto px-4 pt-20 pb-24 text-center">
          <span className="badge border-lavender-400/40 text-lavender-300 animate-fade-up">
            ✈️ Travel-tech hackathon MVP
          </span>
          <h1
            className="mt-6 font-display text-5xl md:text-7xl font-extrabold leading-tight animate-fade-up"
            style={{ animationDelay: "80ms" }}
          >
            Don't Just Wait.
            <br />
            <span className="bg-gradient-to-r from-lavender-400 via-lavender-300 to-sunset-400 bg-clip-text text-transparent">
              Make the Time Yours.
            </span>
          </h1>
          <p
            className="mt-6 max-w-2xl mx-auto text-lg text-midnight-200 animate-fade-up"
            style={{ animationDelay: "160ms" }}
          >
            Match with compatible travellers, share luggage storage, and squeeze
            a real city experience into your layover — with a countdown that
            always gets you back on time.
          </p>
          <div
            className="mt-10 flex flex-col sm:flex-row gap-4 justify-center animate-fade-up"
            style={{ animationDelay: "240ms" }}
          >
            <Link to="/signup" className="btn-primary text-lg">
              Start your layover
            </Link>
            <Link to="/login" className="btn-secondary text-lg">
              I already have an account
            </Link>
          </div>
          <div className="flight-path mx-auto mt-16 w-2/3" />
        </div>
      </section>

      {/* Features */}
      <section className="max-w-6xl mx-auto px-4 pb-24 grid gap-6 md:grid-cols-3">
        {features.map((f, i) => (
          <div
            key={f.title}
            className="card p-6 animate-fade-up"
            style={{ animationDelay: `${i * 90}ms` }}
          >
            <div className="text-3xl">{f.icon}</div>
            <h3 className="mt-3 font-display text-xl font-bold">{f.title}</h3>
            <p className="mt-2 text-midnight-200">{f.text}</p>
          </div>
        ))}
      </section>
    </div>
  );
}
