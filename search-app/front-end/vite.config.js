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
 build: {
  rollupOptions: {
    output: {
      manualChunks(id) {
        if (id.includes('node_modules')) {
          return id.toString().split('node_modules/')[1].split('/')[0].toString();
        }
      },
    },
  },
  chunkSizeWarningLimit: 1000,
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