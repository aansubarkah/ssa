const fs = require('fs');
const path = require('path');
const https = require('https');

/**
 * Build script to create one-liner HTML files
 * - Creates online and offline versions from ./index.html
 * - Downloads CDN JS locally for offline build (dist/*.js)
 * - Removes external trackers (GA/Grow.me) for offline build
 * - Rewrites script tags and pdf.workerSrc to local dist/*
 * - Outputs:
 *    dist/index-oneliner.html            (online, minified)
 *    dist/index-offline.html             (offline, minified)
 *    dist/index-offline-debug.html       (offline, non-minified for debug)
 *    dist/index-minified.html            (pretty minified original)
 */

function ensureDir(p) {
  if (!fs.existsSync(p)) fs.mkdirSync(p, { recursive: true });
}

function downloadFile(url) {
  return new Promise((resolve, reject) => {
    https
      .get(url, (res) => {
        if (res.statusCode !== 200) {
          reject(new Error(`HTTP ${res.statusCode} for ${url}`));
          res.resume();
          return;
        }
        const data = [];
        res.on('data', (chunk) => data.push(chunk));
        res.on('end', () => resolve(Buffer.concat(data)));
      })
      .on('error', reject);
  });
}

function inlineCSS(html, css) {
  if (/<\/head>/.test(html)) {
    return html.replace('</head>', `<style>${css}</style></head>`);
  }
  return `<style>${css}</style>${html}`;
}

function minifyHTML(html) {
  return html
    .replace(/<!--[\s\S]*?-->/g, '')
    .replace(/\n+/g, ' ')
    .replace(/\s{2,}/g, ' ')
    .trim();
}

function stripTrackers(html) {
  // Remove Google Analytics loader and inline gtag config
  html = html.replace(
    /<script async src="https:\/\/www\.googletagmanager\.com\/gtag\/js[^"]*"><\/script>/g,
    '<!-- GA removed -->'
  );
  html = html.replace(
    /<script>\s*window\.dataLayer[\s\S]*?<\/script>/g,
    '<!-- GA inline removed -->'
  );

  // Remove Grow.me widget block
  html = html.replace(
    /<script[^>]*data-grow-initializer[^>]*>[\s\S]*?<\/script>/g,
    '<!-- Grow.me removed -->'
  );

  return html;
}

async function createOfflineVersion(html) {
  // CDN libraries used by the app
  const cdnFiles = [
    {
      url: 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js',
      filename: 'pdf.min.js',
      matcher:
        /<script src="https:\/\/cdnjs\.cloudflare\.com\/ajax\/libs\/pdf\.js\/3\.11\.174\/pdf\.min\.js"><\/script>/g,
      replacement: '<script src="dist/pdf.min.js"></script>',
    },
    {
      url: 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js',
      filename: 'pdf.worker.min.js',
      matcher: null, // referenced via workerSrc; handled via code replacement
      replacement: null,
    },
    {
      url: 'https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js',
      filename: 'xlsx.full.min.js',
      matcher:
        /<script src="https:\/\/cdnjs\.cloudflare\.com\/ajax\/libs\/xlsx\/0\.18\.5\/xlsx\.full\.min\.js"><\/script>/g,
      replacement: '<script src="dist/xlsx.full.min.js"></script>',
    },
  ];

  ensureDir('./dist');

  // Download CDN files to dist
  for (const file of cdnFiles) {
    try {
      console.log(`  Downloading ${file.url} ...`);
      const buf = await downloadFile(file.url);
      fs.writeFileSync(path.join('./dist', file.filename), buf);
      console.log(`  ✓ Saved dist/${file.filename}`);
    } catch (e) {
      console.error(`  ✗ Failed to download ${file.url}: ${e.message}`);
    }
  }

  // Replace script tags pointing to CDN with local dist/* files
  let offline = html;
  for (const file of cdnFiles) {
    if (file.matcher && file.replacement) {
      offline = offline.replace(file.matcher, file.replacement);
    }
  }

  // Make sure pdf.js worker points to local file
  offline = offline.replace(
    /pdfjsLib\.GlobalWorkerOptions\.workerSrc\s*=\s*['"][^'"]+['"]/g,
    'pdfjsLib.GlobalWorkerOptions.workerSrc = "dist/pdf.worker.min.js"'
  );

  // Remove GA and Grow.me for offline privacy
  offline = stripTrackers(offline);

  // Sanity warnings if CDN refs still present
  if (offline.includes('https://cdnjs.cloudflare.com/ajax/libs/pdf.js')) {
    console.warn('  ⚠ PDF.js CDN reference still present after replacement');
  }
  if (offline.includes('https://cdnjs.cloudflare.com/ajax/libs/xlsx')) {
    console.warn('  ⚠ XLSX CDN reference still present after replacement');
  }

  console.log('  ✓ Offline HTML prepared');
  return offline;
}

function validateHTML(html, filename) {
  try {
    const open = (html.match(/<[^/][^>]*>/g) || []).length;
    const close = (html.match(/<\/[^>]*>/g) || []).length;
    if (Math.abs(open - close) > 5) {
      console.warn(
        `  ⚠ Potential tag imbalance in ${filename} (${open} open vs ${close} close)`
      );
    }
    if (html.includes('pdfjsLib') && html.includes('XLSX')) {
      console.log(`  ✓ PDF.js and XLSX detected in ${filename}`);
    } else {
      console.warn(`  ⚠ Missing PDF.js or XLSX in ${filename}`);
    }
    return true;
  } catch (e) {
    console.error(`  ✗ Validation failed for ${filename}: ${e.message}`);
    return false;
  }
}

async function buildOneLiner() {
  try {
    console.log('🚀 Building one-liner HTML files...');
    ensureDir('./dist');

    const htmlPath = './index.html';
    if (!fs.existsSync(htmlPath)) {
      console.error('✗ index.html not found');
      return;
    }

    let html = fs.readFileSync(htmlPath, 'utf8');
    console.log('✓ Loaded index.html');

    // Inline compiled CSS if present
    const cssPath = './dist/style.css';
    if (fs.existsSync(cssPath)) {
      const css = fs.readFileSync(cssPath, 'utf8');
      html = inlineCSS(html, css);
      console.log('✓ Inlined compiled CSS');
    } else {
      console.log('• No compiled CSS found, continuing');
    }

    // Online one-liner (keep external links as-is)
    const onlineMin = minifyHTML(html);
    fs.writeFileSync('./dist/index-oneliner.html', onlineMin);
    console.log('✓ Wrote dist/index-oneliner.html');

    // Offline version (download CDN and rewrite)
    const offlineHtml = await createOfflineVersion(html);

    console.log('🔍 Validating offline HTML...');
    const ok = validateHTML(offlineHtml, 'index-offline.html');

    if (ok) {
      const offlineMin = minifyHTML(offlineHtml);
      fs.writeFileSync('./dist/index-offline.html', offlineMin);
      console.log('✓ Wrote dist/index-offline.html');
      fs.writeFileSync('./dist/index-offline-debug.html', offlineHtml);
      console.log('✓ Wrote dist/index-offline-debug.html');
    } else {
      fs.writeFileSync('./dist/index-offline-debug.html', offlineHtml);
      console.log(
        '• Wrote dist/index-offline-debug.html (validation failed, not minified)'
      );
    }

    // Pretty minified multi-line version of original
    const prettyMin = html.replace(/<!--[\s\S]*?-->/g, '').replace(/\s+/g, ' ').trim();
    fs.writeFileSync('./dist/index-minified.html', prettyMin);
    console.log('✓ Wrote dist/index-minified.html');

    // Stats
    const originalSize = fs.statSync(htmlPath).size;
    const onlineSize = fs.statSync('./dist/index-oneliner.html').size;
    let offlineSize = 0;
    try {
      offlineSize = fs.statSync('./dist/index-offline.html').size;
    } catch {}

    console.log('\n📊 Build Statistics:');
    console.log(`Original: ${originalSize} bytes`);
    console.log(
      `Online:   ${onlineSize} bytes (${(
        ((originalSize - onlineSize) / originalSize) *
        100
      ).toFixed(1)}% reduction)`
    );
    if (offlineSize) {
      const pct = (
        ((originalSize - offlineSize) / originalSize) *
        100
      ).toFixed(1);
      console.log(
        `Offline:  ${offlineSize} bytes (${pct}% ${
          offlineSize > originalSize ? 'increase' : 'reduction'
        })`
      );
    }
    console.log('\n🎯 Files created:');
    console.log('  • dist/index-oneliner.html (online)');
    console.log('  • dist/index-offline.html (offline, local JS, trackers removed)');
    console.log('  • dist/index-offline-debug.html (debug)');
    console.log('  • dist/index-minified.html');
    console.log('✅ Build complete');
  } catch (e) {
    console.error('✗ Build failed:', e.message);
  }
}

// Execute
(async () => {
  await buildOneLiner();
})();