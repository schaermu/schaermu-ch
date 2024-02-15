import * as fs from 'node:fs'

import OpenAI from 'openai'

export async function translate(source, target, { language, dryRun }) {
    // load the post content from the file, extract original tags
    const fileContent = fs.readFileSync(source, 'utf8')
    const originalTags = fileContent.match(/tags: (.+)/g)

    // use OpenAI to translate the content
    const openai = new OpenAI()
    const response = await openai.chat.completions.create({
        model: 'gpt-3.5-turbo-16k',
        messages: [
            { role: 'system', content: 'You are a text translator' },
            {
                role: 'user', content: `Translate the text delimited by triple quotes to ${language}. """${fileContent}"""`
            },
        ]
    })

    // restore the original tags and save the translated content to the target file
    const translatedContent = response.choices[0].message.content.replace(/tags: (.+)/g, originalTags)
    fs.writeFileSync(target, translatedContent.replaceAll('"""', ''), 'utf8')
}