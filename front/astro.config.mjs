import { defineConfig } from 'astro/config';
import react from "@astrojs/react";
import dotenv from "dotenv";

import tailwind from "@astrojs/tailwind";

dotenv.config();

// https://astro.build/config
export default defineConfig({
  integrations: [react(), tailwind()],
  buildOptions: {
    env: {
      API_URL: process.env.API_URL
    }
  }
});