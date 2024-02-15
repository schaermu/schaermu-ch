import { defineCollection, z } from 'astro:content';

const blogCollection = defineCollection({
    type: 'content',
    schema: ({ image }) => z.object({
        title: z.string(),
        pubDate: z.date(),
        lead: z.string().optional(),
        cover: z.object({
            src: z.string(),
            alt: z.string(),
            promptInput: z.string().optional(),
        }),
        tags: z.array(z.string()),
    })
});

export const collections = {
    'blog': blogCollection
};