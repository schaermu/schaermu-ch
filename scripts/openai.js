import 'dotenv/config'

import { program, Option } from 'commander';

import { translate } from './translate.js';

program
    .command('translate <source> <target>')
    .addOption(new Option('-l, --language <language>', 'The target language to translate to').choices(['english', 'german']).default('english'))
    .description('Translate markdown post to a target language (english by default)')
    .action((source, targetFolder, options) => {
        translate(source, targetFolder, options.language)
    });

program.parse();