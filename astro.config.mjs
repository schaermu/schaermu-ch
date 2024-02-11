import { defineConfig, passthroughImageService } from 'astro/config';
import svelte from "@astrojs/svelte";
import tailwind from "@astrojs/tailwind";
import icon from "astro-icon";

// https://astro.build/config
export default defineConfig({
  redirects: {
    '/': '/blog/',
  },
  server: { port: 3000 },
  image: {
    service: passthroughImageService(),
  },
  integrations: [svelte(), tailwind({
    applyBaseStyles: false
  }), icon({
    include: {
      'fa-brands': ["github", "stack-overflow", "linkedin"],
      'fa-solid': ["bars", "times"]
    }
  })]
});