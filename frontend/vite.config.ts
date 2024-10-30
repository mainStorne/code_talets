import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import sass from "sass";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  css: {
    preprocessorOptions: {
      scss: {
        implementation: sass,
        api: "modern-compiler",
      },
    },
  },
});
