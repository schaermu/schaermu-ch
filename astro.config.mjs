import { defineConfig } from 'astro/config';

import svelte from "@astrojs/svelte";
import tailwind from "@astrojs/tailwind";
import icon from "astro-icon";

// https://astro.build/config
export default defineConfig({
  integrations: [
    svelte(),
    tailwind({
      config: { applyBaseStyles: false },
    }),
    icon({
      include: {
        'fa-brands': ["github", "stack-overflow", "linkedin"],
        'fa-solid':["*"],
      }
    }),
  ]
});