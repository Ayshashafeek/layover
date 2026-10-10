import { Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./features/auth/AuthContext";
import Layout from "./components/layout/Layout";
import Landing from "./pages/Landing";
import Login from "./pages/Login";
import SignUp from "./pages/SignUp";
import LayoverForm from "./pages/LayoverForm";
import MatchingResults from "./pages/MatchingResults";
import StorageResults from "./pages/StorageResults";
import CostBreakdown from "./pages/CostBreakdown";
import BookingConfirmation from "./pages/BookingConfirmation";
import Dashboard from "./pages/Dashboard";
import ItineraryView from "./pages/ItineraryView";
import Profile from "./pages/Profile";

function Protected({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth();
  if (loading) return <Loading />;
  if (!user) return <Navigate to="/login" replace />;
  return <>{children}</>;
}

function Loading() {
  return (
    <div className="min-h-[60vh] grid place-items-center text-lavender-300 animate-pulse">
      Checking your session…
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <Layout>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<SignUp />} />

          <Route
            path="/layover"
            element={
              <Protected>
                <LayoverForm />
              </Protected>
            }
          />
          <Route
            path="/matches/:layoverId"
            element={
              <Protected>
                <MatchingResults />
              </Protected>
            }
          />
          <Route
            path="/storage/:layoverId"
            element={
              <Protected>
                <StorageResults />
              </Protected>
            }
          />
          <Route
            path="/cost/:layoverId/:facilityId"
            element={
              <Protected>
                <CostBreakdown />
              </Protected>
            }
          />
          <Route
            path="/booking/:bookingId"
            element={
              <Protected>
                <BookingConfirmation />
              </Protected>
            }
          />
          <Route
            path="/dashboard"
            element={
              <Protected>
                <Dashboard />
              </Protected>
            }
          />
          <Route
            path="/itinerary/:layoverId"
            element={
              <Protected>
                <ItineraryView />
              </Protected>
            }
          />
          <Route
            path="/profile"
            element={
              <Protected>
                <Profile />
              </Protected>
            }
          />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Layout>
    </AuthProvider>
  );
}
