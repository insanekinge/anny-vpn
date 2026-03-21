import { defineConfig } from "vite";
import legacy from "@vitejs/plugin-legacy";
import react from "@vitejs/plugin-react-swc";

export default defineConfig({
  plugins: [
    react(),
    legacy({
      targets: ["Chrome >= 58", "Android >= 8", "Safari >= 12", "iOS >= 12"],
      renderLegacyChunks: true,
      renderModernChunks: false,
    }),
  ],
  build: {
    target: "es2018",
  },
  server: {
    host: "0.0.0.0",
    port: 3001,
  },
});
