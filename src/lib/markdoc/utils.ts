import Markdoc from "@markdoc/markdoc";
import { config } from "./markdoc.config";
import { getEntry } from "astro:content";

async function parseAndTransform({ content }: { content: string }) {
    const ast = Markdoc.parse(content);

    const errors = Markdoc.validate(ast, config);
    if (errors.length) {
        console.error(errors);
        throw new Error("Markdoc validation error");
    }
    const transformedContent = Markdoc.transform(ast, config);

    return transformedContent;
}

export async function read({
    slug,
}: {
    slug: string;
}) {
    const entry = await getEntry('blog', slug);
    if (!entry) {
        throw new Error(`No unique entry found for slug: ${slug}`);
    }
    const transformedContent = await parseAndTransform({ content: entry.body });

    return {
        slug: entry.slug,
        content: transformedContent,
    };
}