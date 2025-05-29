import { glob } from 'astro/loaders';
import { defineCollection, reference, z } from 'astro:content';

const blogCollection = defineCollection({
    loader: glob({ pattern: '**/*.mdoc', base: './src/content/blog' }),
    schema: z.object({
        title: z.string(),
        pubDate: z.date(),
        lead: z.string().optional(),
        partOfSeries: reference('blog-series').optional(),
        cover: z.object({
            src: z.string(),
            alt: z.string(),
            promptInput: z.string().optional(),
        }),
        tags: z.array(z.string()),
    })
});

const blogSeriesCollection = defineCollection({
    loader: glob({ pattern: '**/*.json', base: './src/content/blog-series' }),
    schema: z.object({
        title: z.string(),
        posts: z.array(z.object({
            label: z.string(),
            post: reference('blog')
        }))
    })
})

const cvEntryCollection = defineCollection({
    loader: glob({ pattern: '**/*.yml', base: './src/content/cv-entries' }),
    schema: z.object({
        from: z.date(),
        to: z.date().optional(),
        title: z.string(),
        role: z.string(),
        company: z.object({
            name: z.string(),
            icon: z.string().optional(),
            url: z.string().optional()
        }),
        description: z.string(),
        skills: z.array(z.string())
    })

})

export const collections = {
    'blog': blogCollection,
    'blog-series': blogSeriesCollection,
    'cv-entries': cvEntryCollection
};