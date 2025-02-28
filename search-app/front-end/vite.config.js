import { fileURLToPath, URL } from "node:url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import vueDevTools from "vite-plugin-vue-devtools";

// https://vite.dev/config/
export default defineConfig({
 plugins: [vue(), vueDevTools()],
 build: {
  outDir: "../laravel-server/public/vue", //directly output to laravel's public folder when running npm run build
  emptyOutDir: true,
 },
 server: {
  port: 5173,
  host: process.env.VITE_HOST || 'localhost',
  allowedHosts: ["sar2.andreasmaita.com"],
  proxy: {
   "laravel-server": {
    target: "http://localhost:5173/",
    changeOrigin: true,
    rewrite: (path) => path.replace(/^\/laravel-server/, ""),
   },
   "sar-db": {
    target: "http://localhost:8000",
    changeOrigin: true,
    rewrite: (path) => path.replace(/^\/sar-db/, "api"),
   },
  },
  middlewareMode: 'html',
  setupMiddlewares: (middlewares, { app }) => {
   app.use((req, res, next) => {
    try {
     next();
    } catch (error) {
     console.error('Error in middleware:', error);
     res.status(500).send('Internal Server Error');
    }
   });
   return middlewares;
  },
 },
 resolve: {
  alias: {
   "@": fileURLToPath(new URL("./src", import.meta.url)),
  },
 },
});
