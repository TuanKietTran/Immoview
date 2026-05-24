import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { resolve } from "path";

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: { "@shared": resolve(__dirname, "src/shared") },
  },
  build: {
    outDir: "../django-core/static/islands",
    emptyOutDir: true,
    sourcemap: true,
    rollupOptions: {
      input: {
        "price-calculator": resolve(__dirname, "src/islands/price-calculator/index.tsx"),
        "lead-funnel-chart": resolve(__dirname, "src/islands/lead-funnel-chart/index.tsx"),
        "listing-bulk-editor": resolve(__dirname, "src/islands/listing-bulk-editor/index.tsx"),
      },
      output: {
        // Stable file names so Django templates don't need content-hash aware references
        entryFileNames: "[name].js",
        chunkFileNames: "chunks/[name]-[hash].js",
        assetFileNames: "assets/[name]-[hash][extname]",
      },
    },
  },
});
