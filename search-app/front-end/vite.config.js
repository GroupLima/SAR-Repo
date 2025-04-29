import { fileURLToPath, URL } from "node:url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import vueDevTools from "vite-plugin-vue-devtools";

// https://vite.dev/config/
export default defineConfig({
 plugins: [vue(), vueDevTools()],
 server: {
  port: 5173,
  host: "0.0.0.0",
  proxy: {
   "/api": {
    target: "http://backend:8000", // Use Docker container name for better networking
    changeOrigin: true,
    // REMOVE this rewrite line:
    // rewrite: (path) => path.replace(/^\/api/, ""),
   },
  },
  // Add this to allow your domain
  hmr: {
    clientPort: 443,
    protocol: 'wss'
  },
  // Add the allowedHosts configuration
  allowedHosts: ['sar2.andreasmaita.com', 'localhost']
 },
 resolve: {
  alias: {
   "@": fileURLToPath(new URL("./src", import.meta.url)),
  },
 },
 test: {
    environment: "jsdom",
 }
});