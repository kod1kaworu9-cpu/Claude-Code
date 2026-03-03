'use strict';

const { program } = require('commander');
const { version } = require('../package.json');

program
  .name('claude-code')
  .description('CLI tool for Claude Code')
  .version(version);

program
  .command('run <file>')
  .description('Run a code file')
  .option('-o, --output <path>', 'Output file path')
  .action((file, options) => {
    const fs = require('fs');
    const path = require('path');

    const filePath = path.resolve(file);

    if (!fs.existsSync(filePath)) {
      console.error(`Error: File not found: ${filePath}`);
      process.exit(1);
    }

    const ext = path.extname(filePath);
    const content = fs.readFileSync(filePath, 'utf8');

    console.log(`Running: ${filePath}`);
    console.log(`Language: ${detectLanguage(ext)}`);

    if (options.output) {
      fs.writeFileSync(options.output, content);
      console.log(`Output written to: ${options.output}`);
    }
  });

program
  .command('info')
  .description('Show system information')
  .action(() => {
    console.log('claude-code CLI');
    console.log(`Version: ${version}`);
    console.log(`Node.js: ${process.version}`);
    console.log(`Platform: ${process.platform}`);
    console.log(`Working directory: ${process.cwd()}`);
  });

program
  .command('list [dir]')
  .description('List files in a directory')
  .option('-e, --ext <extension>', 'Filter by extension')
  .action((dir = '.', options) => {
    const fs = require('fs');
    const path = require('path');

    const targetDir = path.resolve(dir);

    if (!fs.existsSync(targetDir)) {
      console.error(`Error: Directory not found: ${targetDir}`);
      process.exit(1);
    }

    const entries = fs.readdirSync(targetDir, { withFileTypes: true });

    entries.forEach((entry) => {
      if (entry.isFile()) {
        const name = entry.name;
        if (!options.ext || name.endsWith(options.ext)) {
          console.log(path.join(targetDir, name));
        }
      }
    });
  });

function detectLanguage(ext) {
  const map = {
    '.js': 'JavaScript',
    '.ts': 'TypeScript',
    '.py': 'Python',
    '.rb': 'Ruby',
    '.go': 'Go',
    '.rs': 'Rust',
    '.java': 'Java',
    '.c': 'C',
    '.cpp': 'C++',
    '.sh': 'Shell',
  };
  return map[ext] || 'Unknown';
}

program.parse(process.argv);
