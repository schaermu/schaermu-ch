import { defineMarkdocConfig, component, nodes } from '@astrojs/markdoc/config';
import shiki from '@astrojs/markdoc/shiki';

export default defineMarkdocConfig({
    extends: [
        shiki({
            theme: 'github-dark',
            experimentalThemes: {
                light: 'github-light',
                dark: 'github-dark',
            },
            wrap: true,
        }),
    ],
    tags: {
        sup: {
            render: "sup",
            children: nodes.strong.children,
        },
        sub: {
            render: "sub",
            children: nodes.strong.children,
        },
        abbr: {
            render: "abbr",
            attributes: {
                title: { type: String },
            },
            children: nodes.strong.children,
        },
        kbd: {
            render: "kbd",
            children: nodes.strong.children,
        },
        mark: {
            render: "mark",
            children: nodes.strong.children,
        },
        image: {
            render: component('src/components/Renderer/Figure.astro'),
            attributes: {
                src: { type: String, required: true },
                alt: { type: String, required: true },
                height: { type: Number, required: false },
                width: { type: Number, required: false },
                caption: { type: String, required: false },
            },
            selfClosing: true,
        },
        youtube: {
            render: component('src/components/Renderer/YouTubeEmbed.astro'),
            attributes: {
                url: { type: String, required: true },
                label: { type: String, required: true },
            },
            selfClosing: true,
        },
        tweet: {
            render: component('src/components/Renderer/TweetEmbed.astro'),
            attributes: {
                url: { type: String, required: true },
            },
            selfClosing: true,
        },
    },
    nodes: {
        document: {
            ...nodes.document,
            render: component('src/components/Renderer/Article.astro'),
        },
        heading: {
            ...nodes.heading,
            render: component('src/components/Renderer/Heading.astro')
        }
    },
})