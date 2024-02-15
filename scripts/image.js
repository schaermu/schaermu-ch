import * as fs from 'node:fs'
import { resolve, parse } from 'node:path'
import { Readable } from 'node:stream'
import { finished } from 'node:stream/promises';

import OpenAI from 'openai'
import { getUnixTime } from 'date-fns/getUnixTime';
import fm from 'front-matter'
import { PutObjectCommand, S3Client } from "@aws-sdk/client-s3";
import { logger as log } from './openai.js'


const imageTempFolder = "src/content/temp"

const getPost = (source) => {
    const postContent = fs.readFileSync(source, 'utf8')
    const { attributes } = fm(postContent)
    if (!attributes) {
        throw new Error('The post does not contain front matter')
    }
    return { content: postContent, attributes }
}

const getNewImagePath = (sourcePost) => {
    const folderName = parse(sourcePost).name
    const imageFolderPath = resolve(imageTempFolder, folderName)
    if (!fs.existsSync(imageFolderPath)) {
        fs.mkdirSync(imageFolderPath);
    }
    return resolve(imageFolderPath, getUnixTime(new Date()) + '.png')
}

const getLatestImage = (sourcePost) => {
    const folderName = parse(sourcePost).name
    const imageFolderPath = resolve(imageTempFolder, folderName)
    const files = fs.readdirSync(imageFolderPath)
        .map(function (v) {
            return {
                name: v,
                time: fs.statSync(resolve(imageFolderPath, v)).mtime.getTime()
            };
        })
        .sort(function (a, b) { return b.time - a.time; })
        .map(function (v) { return v.name; });
    return files.length > 0 ? resolve(imageFolderPath, files[0]) : ''
}

export async function storeImage(source, { dryRun }) {
    const targetImage = getLatestImage(source)
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

        log.info(`Uploading latest image for ${source} to Cloudflare storage`)
        await S3.send(new PutObjectCommand({
            Bucket: process.env.CF_BUCKET,
            Key: `blog/${parse(source).name}/header.png`,
            Body: fs.readFileSync(targetImage),
            ContentType: 'image/png',
        }))
    }

    // replace cover in front matter with new image url
    const cdnUrl = `${process.env.CF_BUCKET_BASE_URL}/blog/${parse(source).name}/header.png`
    const newPostContent = content
        .replace(/    src: .+/, `    src: ${cdnUrl}`)
    fs.writeFileSync(source, newPostContent, 'utf8')
    log.info(`Updated post ${source} with new image ${cdnUrl}`)
}

export async function generateImage(source, { dryRun }) {
    // generate new target path
    const targetFilePath = getNewImagePath(source)

    // load post and parse it's front matter to get some clues for image generation
    const { content, attributes } = getPost(source)
    const { cover, tags } = attributes

    // generate prompt and send it to DALL-E-3
    const prompt = `Create a stylistic, yet simple header image for a blog post. The broad topic is ${cover.promptInput} with the following tags: ${tags.join(', ')}`
    log.info(`Generating image for prompt: ${prompt}`)
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

        // store image file locally for review
        const imageRes = await fetch(response.data[0].url)
        const targetFs = fs.createWriteStream(targetFilePath, { flags: 'wx' })
        await finished(Readable.fromWeb(imageRes.body).pipe(targetFs))
        log.info(`Stored generated image at ${targetFilePath}`)

        // set alt text to revised prompt in the post front matter
        const newPostContent = content
            .replace(/    alt: .+/, `    alt: "${response.data[0].revised_prompt}"`)
        fs.writeFileSync(source, newPostContent, 'utf8')
    } else {
        log.info(`Dry run, not generating and storing anything.`)
    }
}