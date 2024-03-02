import { defineConfig } from 'astro/config';
import svelte from "@astrojs/svelte";
import tailwind from "@astrojs/tailwind";
import markdoc from '@astrojs/markdoc';
import icon from "astro-icon";

// https://astro.build/config
export default defineConfig({
  redirects: {
    '/': '/blog/',
  },
  server: { port: 3000 },
  image: {
    domains: ['storage.schaermu.ch'],
  },
  integrations: [markdoc(), svelte(), tailwind({
    applyBaseStyles: false,
    nesting: true,
  }), icon({
    include: {
      'fa-brands': ["github", "stack-overflow", "linkedin"],
      'fa-solid': ["bars", "times", "heart", "rocket"]
    }
  })]
});