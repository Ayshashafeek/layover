import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tsconfigPaths from "vite-tsconfig-paths";

// Backend port configurable via VITE_API_BASE_URL (build-time) and proxies for dev.
const backend =
  process.env.VITE_API_BASE_URL?.replace(/\/$/, "") || "http://localhost:8001";

export default defineConfig({
  plugins: [react(), tsconfigPaths()],
  server: {
    port: 5173,
    proxy: {
      "/api": {
        target: backend,
        changeOrigin: true,
      },
    },
  },
});
