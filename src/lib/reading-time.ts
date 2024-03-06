import type { CollectionEntry } from "astro:content";

export const readingTimeInMin = (entry: CollectionEntry<"blog">) => {
    const WORDS_PER_MIN = 150;
    if (entry === null) return;
    let wordCount = entry.body.match(/\w+/g)?.length || 0;
    wordCount += entry.data.lead?.match(/\w+/g)?.length || 0;
    const time = Math.ceil(wordCount / WORDS_PER_MIN);
    return time;
}