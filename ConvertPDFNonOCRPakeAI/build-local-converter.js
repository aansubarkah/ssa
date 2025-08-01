const fs = require('fs');
const path = require('path');

/**
 * Build script to create production version of local converter
 * Creates minified HTML files in a separate dist-local folder
 */

function minifyHTML(html) {
    // First, preserve script and style content by replacing them temporarily
    const scriptContentMap = new Map();
    const styleContentMap = new Map();
    let scriptCounter = 0;
    let styleCounter = 0;

    // Preserve script contents
    html = html.replace(/<script[^>]*>([\s\S]*?)<\/script>/g, (match, content) => {
        const placeholder = `__SCRIPT_PLACEHOLDER_${scriptCounter}__`;
        scriptContentMap.set(placeholder, match);
        scriptCounter++;
        return placeholder;
    });

    // Preserve style contents
    html = html.replace(/<style[^>]*>([\s\S]*?)<\/style>/g, (match, content) => {
        const placeholder = `__STYLE_PLACEHOLDER_${styleCounter}__`;
        styleContentMap.set(placeholder, match);
        styleCounter++;
        return placeholder;
    });

    // Now minify the HTML structure
    html = html
        // Remove comments (but preserve conditional comments)
        .replace(/<!--(?!\[if)[\s\S]*?-->/g, '')
        // Remove extra whitespace between tags
        .replace(/>\s+</g, '><')
        // Remove whitespace at start/end of lines
        .replace(/\s+/g, ' ')
        // Remove quotes from simple attributes (but be careful)
        .replace(/="([a-zA-Z0-9-_]+)"/g, '=$1')
        // Trim
        .trim();

    // Restore script contents
    scriptContentMap.forEach((content, placeholder) => {
        html = html.replace(placeholder, content);
    });

    // Restore style contents
    styleContentMap.forEach((content, placeholder) => {
        html = html.replace(placeholder, content);
    });

    return html;
}

function minifyJS(js) {
    return js
        // Remove single-line comments (but be careful with URLs and regexes)
        .replace(/\/\/(?![^\r\n]*["'`]).*$/gm, '')
        // Remove multi-line comments (but preserve those inside strings)
        .replace(/\/\*[\s\S]*?\*\//g, '')
        // Remove extra whitespace but preserve line breaks after certain tokens
        .replace(/\s+/g, ' ')
        // Be more conservative with whitespace removal around operators
        .replace(/\s*([{}();,])\s*/g, '$1')
        // Preserve spaces around operators that need them
        .replace(/\s*([=+\-*/<>!&|])\s*/g, ' $1 ')
        // Clean up double spaces
        .replace(/\s+/g, ' ')
        // Trim
        .trim();
}

function optimizeForProduction(html, minifyJS = false) {
    // Remove development-specific elements
    html = html.replace(/data-grow-initializer[^>]*>[\s\S]*?<\/script>/g, '');
    
    // Remove Google Analytics for local version
    html = html.replace(/<!-- Google tag \(gtag\.js\) -->[\s\S]*?gtag\('config'[^}]+\};\s*<\/script>/g, '');
    
    // Update title and meta for local version
    html = html.replace(
        /<title>[^<]*<\/title>/, 
        '<title>Local PDF to Excel Converter - Ollama AI Powered</title>'
    );

    // Conditionally minify inline JavaScript only for certain builds
    if (minifyJS) {
        html = html.replace(/<script[^>]*>([\s\S]*?)<\/script>/g, (match, jsContent) => {
            if (jsContent.trim() && !match.includes('src=')) {
                const minifiedJS = minifyJS(jsContent);
                return `<script>${minifiedJS}</script>`;
            }
            return match;
        });
    }

    return html;
}

function buildLocalConverter() {
    try {
        console.log('🚀 Building Local PDF to Excel Converter production version...');
        
        // Create dist-local directory
        const distDir = './dist-local';
        if (!fs.existsSync(distDir)) {
            fs.mkdirSync(distDir);
            console.log('✅ Created dist-local directory');
        }
        
        // Read the local converter HTML
        const htmlPath = './local_converter.html';
        if (!fs.existsSync(htmlPath)) {
            console.error('❌ local_converter.html not found!');
            return;
        }
        
        let html = fs.readFileSync(htmlPath, 'utf8');
        console.log('✅ Read local_converter.html');
        
        // Create different versions with varying levels of optimization
        
        // 1. One-liner minified version (HTML only, preserve JS)
        const htmlForOneliner = optimizeForProduction(html, false); // Don't minify JS
        const oneliner = minifyHTML(htmlForOneliner);
        fs.writeFileSync(path.join(distDir, 'local-converter-oneliner.html'), oneliner);
        console.log('✅ Created dist-local/local-converter-oneliner.html');
        
        // 2. Pretty minified version (multi-line but optimized)
        const htmlForMinified = optimizeForProduction(html, false); // Don't minify JS
        const prettyMinified = htmlForMinified
            .replace(/<!--(?!\[if)[\s\S]*?-->/g, '')
            .replace(/\s+/g, ' ')
            .trim();
        fs.writeFileSync(path.join(distDir, 'local-converter-minified.html'), prettyMinified);
        console.log('✅ Created dist-local/local-converter-minified.html');
        
        // 3. Development version (with better formatting, no JS minification)
        const htmlForDev = optimizeForProduction(html, false); // Don't minify JS
        const development = htmlForDev
            .replace(/<!--(?!\[if)[\s\S]*?-->/g, '')
            .replace(/>\s+</g, '>\n<')
            .split('\n')
            .map(line => line.trim())
            .filter(line => line.length > 0)
            .join('\n');
        fs.writeFileSync(path.join(distDir, 'local-converter-dev.html'), development);
        console.log('✅ Created dist-local/local-converter-dev.html');
        
        console.log('✅ All versions created with preserved JavaScript syntax');
        
        // Show file sizes
        const originalSize = fs.statSync(htmlPath).size;
        const onelinerSize = fs.statSync(path.join(distDir, 'local-converter-oneliner.html')).size;
        const minifiedSize = fs.statSync(path.join(distDir, 'local-converter-minified.html')).size;
        const devSize = fs.statSync(path.join(distDir, 'local-converter-dev.html')).size;
        
        const onelinerReduction = ((originalSize - onelinerSize) / originalSize * 100).toFixed(1);
        const minifiedReduction = ((originalSize - minifiedSize) / originalSize * 100).toFixed(1);
        const devReduction = ((originalSize - devSize) / originalSize * 100).toFixed(1);
        
        console.log('\n📊 Build Statistics:');
        console.log(`Original size:           ${originalSize.toLocaleString()} bytes`);
        console.log(`One-liner size:          ${onelinerSize.toLocaleString()} bytes (${onelinerReduction}% reduction)`);
        console.log(`Minified size:           ${minifiedSize.toLocaleString()} bytes (${minifiedReduction}% reduction)`);
        console.log(`Development size:        ${devSize.toLocaleString()} bytes (${devReduction}% reduction)`);
        
        // Create a README for the dist-local folder
        const readmeContent = `# Local PDF to Excel Converter - Production Builds

This folder contains production-ready versions of the Local PDF to Excel Converter.

## Files:

- **local-converter-oneliner.html** - Ultra-compressed single-line version for minimal file size
- **local-converter-minified.html** - Minified but readable version
- **local-converter-dev.html** - Development-optimized version with better formatting

## Features:

- Complete local processing using Ollama AI
- No external API calls or data transmission
- Offline PDF to Excel conversion
- Privacy-focused design
- Batch processing support

## Requirements:

- Ollama installed locally (https://ollama.com/)
- Vision model downloaded (e.g., \`ollama pull llava\`)
- Modern web browser with JavaScript enabled

## Usage:

1. Install Ollama and download a vision model
2. Open any of the HTML files in your browser
3. Select your Ollama model from the dropdown
4. Upload PDF files and convert to Excel

Built on: ${new Date().toISOString()}
Original size: ${originalSize.toLocaleString()} bytes
Optimized sizes: ${onelinerSize.toLocaleString()} - ${devSize.toLocaleString()} bytes
`;
        
        fs.writeFileSync(path.join(distDir, 'README.md'), readmeContent);
        console.log('✅ Created dist-local/README.md');
        
        console.log('\n🎉 Local converter build complete!');
        console.log(`📁 Files created in: ${path.resolve(distDir)}`);
        
    } catch (error) {
        console.error('❌ Build failed:', error.message);
        process.exit(1);
    }
}

// Run the build
buildLocalConverter();