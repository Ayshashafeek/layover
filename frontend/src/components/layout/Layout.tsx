import { type ReactNode } from "react";
import { Link, NavLink } from "react-router-dom";
import { useAuth } from "../../features/auth/AuthContext";

const navItems = [
  { to: "/dashboard", label: "Dashboard" },
  { to: "/layover", label: "New layover" },
  { to: "/profile", label: "Profile" },
];

export default function Layout({ children }: { children: ReactNode }) {
  const { user, offlineMode, signOut } = useAuth();

  return (
    <div className="min-h-screen flex flex-col">
      <header className="sticky top-0 z-40 backdrop-blur bg-midnight-950/70 border-b border-midnight-800">
        <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
          <Link to="/" className="font-display text-xl font-extrabold tracking-tight">
            <span className="text-lavender-400">LAY</span>
            <span className="text-sunset-400">OVER</span>
          </Link>
          <nav className="hidden md:flex items-center gap-6">
            {navItems.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  `text-sm font-medium transition-colors hover:text-lavender-300 ${
                    isActive ? "text-lavender-300" : "text-midnight-200"
                  }`
                }
              >
                {item.label}
              </NavLink>
            ))}
          </nav>
          <div className="flex items-center gap-3">
            {offlineMode && (
              <span className="badge border-sunset-400/40 text-sunset-400">
                demo mode
              </span>
            )}
            {user ? (
              <button onClick={signOut} className="btn-secondary text-sm">
                Sign out
              </button>
            ) : (
              <Link to="/login" className="btn-primary text-sm">
                Sign in
              </Link>
            )}
          </div>
        </div>
      </header>
      <main className="flex-1">{children}</main>
      <footer className="border-t border-midnight-800 py-6 text-center text-sm text-midnight-300">
        LAYOVER — hackathon MVP. Matching &amp; pricing are real math; storage
        providers, payments, and flight times are <em>simulated</em>.
      </footer>
    </div>
  );
}
