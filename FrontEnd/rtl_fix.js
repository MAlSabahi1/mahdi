const fs = require('fs');
const path = require('path');

function walkDir(dir, callback) {
    fs.readdirSync(dir).forEach(f => {
        let dirPath = path.join(dir, f);
        let isDirectory = fs.statSync(dirPath).isDirectory();
        isDirectory ? walkDir(dirPath, callback) : callback(path.join(dir, f));
    });
}

const replaceRules = [
    // Margins
    { regex: /\bml-([\d]+(?:px)?)\b/g, replacement: 'ms-$1' },
    { regex: /\bmr-([\d]+(?:px)?)\b/g, replacement: 'me-$1' },
    { regex: /\b-ml-([\d]+(?:px)?)\b/g, replacement: '-ms-$1' },
    { regex: /\b-mr-([\d]+(?:px)?)\b/g, replacement: '-me-$1' },
    // Paddings
    { regex: /\bpl-([\d]+(?:px)?)\b/g, replacement: 'ps-$1' },
    { regex: /\bpr-([\d]+(?:px)?)\b/g, replacement: 'pe-$1' },
    // Absolute/Fixed Positioning
    { regex: /\bleft-([\d]+(?:px)?)\b/g, replacement: 'start-$1' },
    { regex: /\bright-([\d]+(?:px)?)\b/g, replacement: 'end-$1' },
    { regex: /\b-left-([\d]+(?:px)?)\b/g, replacement: '-start-$1' },
    { regex: /\b-right-([\d]+(?:px)?)\b/g, replacement: '-end-$1' },
    { regex: /\bleft-auto\b/g, replacement: 'start-auto' },
    { regex: /\bright-auto\b/g, replacement: 'end-auto' },
    // Borders
    { regex: /\bborder-l\b/g, replacement: 'border-s' },
    { regex: /\bborder-r\b/g, replacement: 'border-e' },
    { regex: /\bborder-l-([\w-]+)\b/g, replacement: 'border-s-$1' },
    { regex: /\bborder-r-([\w-]+)\b/g, replacement: 'border-e-$1' },
    // Rounded corners
    { regex: /\brounded-l\b/g, replacement: 'rounded-s' },
    { regex: /\brounded-r\b/g, replacement: 'rounded-e' },
    { regex: /\brounded-l-([\w-]+)\b/g, replacement: 'rounded-s-$1' },
    { regex: /\brounded-r-([\w-]+)\b/g, replacement: 'rounded-e-$1' },
    { regex: /\brounded-tl\b/g, replacement: 'rounded-ts' },
    { regex: /\brounded-tr\b/g, replacement: 'rounded-te' },
    { regex: /\brounded-bl\b/g, replacement: 'rounded-bs' },
    { regex: /\brounded-br\b/g, replacement: 'rounded-be' },
    { regex: /\brounded-tl-([\w-]+)\b/g, replacement: 'rounded-ts-$1' },
    { regex: /\brounded-tr-([\w-]+)\b/g, replacement: 'rounded-te-$1' },
    { regex: /\brounded-bl-([\w-]+)\b/g, replacement: 'rounded-bs-$1' },
    { regex: /\brounded-br-([\w-]+)\b/g, replacement: 'rounded-be-$1' },
    // Text Alignment
    { regex: /\btext-left\b/g, replacement: 'text-start' },
    { regex: /\btext-right\b/g, replacement: 'text-end' },
    // Floats
    { regex: /\bfloat-left\b/g, replacement: 'float-start' },
    { regex: /\bfloat-right\b/g, replacement: 'float-end' },
    // Clear
    { regex: /\bclear-left\b/g, replacement: 'clear-start' },
    { regex: /\bclear-right\b/g, replacement: 'clear-end' },
    // Margin auto
    { regex: /\bml-auto\b/g, replacement: 'ms-auto' },
    { regex: /\bmr-auto\b/g, replacement: 'me-auto' },
];

let filesModified = 0;

walkDir('./src', (filePath) => {
    if (!filePath.endsWith('.vue')) return;
    
    let content = fs.readFileSync(filePath, 'utf8');
    let newContent = content;
    
    replaceRules.forEach(rule => {
        newContent = newContent.replace(rule.regex, rule.replacement);
    });
    
    if (content !== newContent) {
        fs.writeFileSync(filePath, newContent, 'utf8');
        console.log(`Updated ${filePath}`);
        filesModified++;
    }
});

console.log(`Total files modified: ${filesModified}`);
