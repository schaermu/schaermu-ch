import { defineConfig } from 'astro/config';
import svelte from "@astrojs/svelte";
import tailwind from "@astrojs/tailwind";
import icon from "astro-icon";

// https://astro.build/config
export default defineConfig({
  integrations: [svelte(), tailwind({
    applyBaseStyles: false
  }), icon({
    include: {
      'fa-brands': ["github", "stack-overflow", "linkedin"],
      'fa-solid': ["bars", "times"]
    }
  })],
  experimental: {
    assets: true,
  }
});