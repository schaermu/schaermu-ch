import 'dotenv/config'

import { Option, Command } from 'commander';

import { translate } from './translate.js';
import { generateImage, storeImage } from './image.js';

const program = new Command();

const globalOptions = [
    new Option('-d, --dry-run', 'Do not execute any actions, only log').default(false)
];

const translateCmd = program.command('translate <source> <target>');
translateCmd.addOption(...globalOptions);
translateCmd.addOption(new Option('-l, --language <language>', 'The target language to translate to').choices(['english', 'german']).default('english'));
translateCmd.description('Translate markdown post to a target language (english by default)')
translateCmd.action((source, targetFolder, options) => {
    translate(source, targetFolder, options)
});

const imageCmd = program.command('image');
const imgGenerate = imageCmd.command('generate <source>');
imgGenerate.addOption(...globalOptions);
imgGenerate.addOption(new Option('--force', 'Overwrite the image file if it already exists').default(false));
imgGenerate.description('Generate an image for the post in <source>')
imgGenerate.action((source, options) => {
    generateImage(source, options)
});

const imgStore = imageCmd.command('store <source>');
imgStore.addOption(...globalOptions);
imgStore.description('Store a previously generated image for <source> image in the cloud storage and link it to the post')
imgStore.action((imagePath, options) => {
    storeImage(imagePath, options)
});

program.parse(process.argv);