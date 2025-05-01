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
    target: "http://localhost:8000",
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
  allowedHosts: ['sar2.andreasmaita.com', 'localhost', '0.0.0.0']
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