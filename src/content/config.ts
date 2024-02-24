import { defineCollection, reference, z } from 'astro:content';

const blogCollection = defineCollection({
    type: 'content',
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
    type: 'data',
    schema: z.object({
        title: z.string(),
        posts: z.array(z.object({
            label: z.string(),
            post: reference('blog')
        }))
    })
})

export const collections = {
    'blog': blogCollection,
    'blog-series': blogSeriesCollection
};