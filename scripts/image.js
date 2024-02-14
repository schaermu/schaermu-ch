import * as fs from 'node:fs'
import { basename, resolve } from 'node:path'
import { finished } from 'node:stream/promises'
import { Readable } from 'node:stream'

import fm from 'front-matter'
import { PutObjectCommand, S3Client } from "@aws-sdk/client-s3";
import sharp from 'sharp'

import OpenAI from 'openai'


const imageTempFolder = "src/content/temp"

const getPost = (source) => {
    const postContent = fs.readFileSync(source, 'utf8')
    const { attributes } = fm(postContent)
    if (!attributes) {
        throw new Error('The post does not contain front matter')
    }
    return { content: postContent, attributes }
}

const getTargetImagePath = (source, format = 'png') => {
    const targetFileName = basename(source).replace('.md', `.${format}`)
    return resolve(imageTempFolder, targetFileName)
}

export async function storeImage(source, { dryRun }) {
    const targetImage = getTargetImagePath(source, 'webp')
    if (!fs.existsSync(targetImage)) {
        throw new Error(`The image file does not exist: ${targetImage}`)
    }

    const { content } = getPost(source)

    // create s3 client and upload image to cloudflare storage
    if (!dryRun) {
        const S3 = new S3Client({
            region: "auto",
            endpoint: `https://${process.env.CF_ACCOUNT_ID}.r2.cloudflarestorage.com`,
            credentials: {
                accessKeyId: process.env.CF_ACCESS_KEY_ID,
                secretAccessKey: process.env.CF_SECRET_ACCESS_KEY,
            },
        });

        await S3.send(new PutObjectCommand({
            Bucket: process.env.CF_BUCKET,
            Key: `blog/headers/${basename(targetImage)}`,
            Body: fs.readFileSync(targetImage),
            ContentType: 'image/webp',
        }))
    }

    // replace cover in front matter with new image url
    const cdnUrl = `${process.env.CF_BUCKET_BASE_URL}/blog/headers/${basename(targetImage)}`
    const newPostContent = content
        .replace(/    src: .+/, `cover: ${cdnUrl}`)
    fs.writeFileSync(source, newPostContent, 'utf8')
}

export async function generateImage(source, { dryRun, force }) {
    // generate proper target path, check image existence and remove if necessary
    const targetFilePath = getTargetImagePath(source, 'webp')
    if (!force && fs.existsSync(targetFilePath)) {
        throw new Error(`The image file already exists: ${targetFilePath}, use --force to overwrite it`)
    } else if (force) {
        fs.rmSync(targetFilePath, { force: true })
    }

    // load post and parse it's front matter to get some clues for image generation
    const { content, attributes } = getPost(source)
    const { cover, tags } = attributes

    // generate prompt and send it to DALL-E-3
    const prompt = `Create a stylistic, yet simple header image for a blog post titled "${cover.promptInput}" with the following tags: ${tags.join(', ')}`
    if (!dryRun) {
        const openai = new OpenAI()
        const response = await openai.images.generate({
            prompt,
            model: 'dall-e-3',
            n: 1,
            quality: 'hd',
            size: '1792x1024',
            style: 'vivid'
        })

        // store & convert image file locally for review
        const imageRes = await fetch(response.data[0].url)
        await sharp(await imageRes.arrayBuffer())
            .webp({ lossless: true })
            .toFile(targetFilePath);

        // set coverAlt to revised prompt in the post front matter
        const newPostContent = content
            .replace(/    alt: .+/, `    alt: "${response.data[0].revised_prompt}"`)
        fs.writeFileSync(source, newPostContent, 'utf8')
    } else {
        console.log(`Generated prompt: ${prompt}`)
    }
}