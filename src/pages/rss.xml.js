import rss, { pagesGlobToRssItems } from '@astrojs/rss';

export async function get() {
    return rss({
        title: 'Astro Learner | Blog',
        description: 'My journey learning Astro',
        site: 'https://www.schaermu.ch',
        items: await pagesGlobToRssItems(import.meta.glob('./**/*.mdoc')),
        customData: `<language>en-us</language>`,
    })
}