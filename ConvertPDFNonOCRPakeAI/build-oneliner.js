const fs = require('fs');
const path = require('path');

/**
 * Build script to create a one-liner HTML file
 * Combines HTML with compiled CSS and minifies everything
 */

function minifyHTML(html) {
    return html
        // Remove comments
        .replace(/<!--[\s\S]*?-->/g, '')
        // Remove extra whitespace between tags
        .replace(/>\s+</g, '><')
        // Remove whitespace at start/end of lines
        .replace(/\s+/g, ' ')
        // Remove quotes from simple attributes
        .replace(/="([a-zA-Z0-9-_]+)"/g, '=$1')
        // Trim
        .trim();
}

function inlineCSS(html, css) {
    // Find the <style> tag and replace it with the compiled CSS
    const styleRegex = /<style[^>]*>[\s\S]*?<\/style>/;
    const inlinedCSS = `<style>${css}</style>`;
    
    if (styleRegex.test(html)) {
        return html.replace(styleRegex, inlinedCSS);
    } else {
        // If no style tag, add CSS before closing head
        return html.replace('</head>', `${inlinedCSS}</head>`);
    }
}

function buildOneLiner() {
    try {
        console.log('🚀 Building one-liner HTML...');
        
        // Check if dist directory exists
        if (!fs.existsSync('./dist')) {
            fs.mkdirSync('./dist');
        }
        
        // Read the source HTML
        const htmlPath = './index.html';
        if (!fs.existsSync(htmlPath)) {
            console.error('❌ index.html not found!');
            return;
        }
        
        let html = fs.readFileSync(htmlPath, 'utf8');
        console.log('✅ Read index.html');
        
        // Read the compiled CSS if it exists
        const cssPath = './dist/style.css';
        if (fs.existsSync(cssPath)) {
            const css = fs.readFileSync(cssPath, 'utf8');
            html = inlineCSS(html, css);
            console.log('✅ Inlined compiled CSS');
        } else {
            console.log('⚠️  No compiled CSS found, using existing styles');
        }
        
        // Minify the HTML
        const minified = minifyHTML(html);
        console.log('✅ Minified HTML');
        
        // Write the one-liner file
        fs.writeFileSync('./dist/index-oneliner.html', minified);
        console.log('✅ Created dist/index-oneliner.html');
        
        // Also create a regular minified version (multi-line)
        const prettyMinified = html
            .replace(/<!--[\s\S]*?-->/g, '')
            .replace(/\s+/g, ' ')
            .trim();
        fs.writeFileSync('./dist/index-minified.html', prettyMinified);
        console.log('✅ Created dist/index-minified.html');
        
        // Show file sizes
        const originalSize = fs.statSync(htmlPath).size;
        const minifiedSize = fs.statSync('./dist/index-oneliner.html').size;
        const reduction = ((originalSize - minifiedSize) / originalSize * 100).toFixed(1);
        
        console.log('\n📊 Build Statistics:');
        console.log(`Original size: ${originalSize} bytes`);
        console.log(`Minified size: ${minifiedSize} bytes`);
        console.log(`Size reduction: ${reduction}%`);
        console.log('\n🎉 Build complete!');
        
    } catch (error) {
        console.error('❌ Build failed:', error.message);
    }
}

// Run the build
buildOneLiner();