import 'dotenv/config'
import pino from "pino"

import { Option, Command } from 'commander';

import { translate } from './translate.js';
import { generateImage, storeImage } from './image.js';

export const logger = pino({
    transport: {
        target: 'pino-pretty',
        options: {
            colorize: true,
            ignore: 'pid,hostname'
        }
    }
});

const program = new Command();

const globalOptions = [
    new Option('-d, --dry-run', 'Do not execute any actions, only log').default(false)
];

const translateCmd = program.command('translate <source> <target>');
translateCmd.addOption(...globalOptions);
translateCmd.addOption(new Option('-l, --language <language>', 'The target language to translate to').choices(['english', 'german']).default('english'));
translateCmd.description('Translate markdown post to a target language (english by default)')
translateCmd.action(translate);

const imageCmd = program.command('image');
const imgGenerate = imageCmd.command('generate <source>');
imgGenerate.addOption(...globalOptions);
imgGenerate.description('Generate a new image for the post in <source> for local review')
imgGenerate.action(generateImage);

const imgStore = imageCmd.command('store <source>');
imgStore.addOption(...globalOptions);
imgStore.description('Store a previously generated image for <source> image in the cloud storage and link it to the post')
imgStore.action(storeImage);

await program.parseAsync(process.argv);
