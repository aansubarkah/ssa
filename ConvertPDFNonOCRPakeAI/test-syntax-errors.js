const { chromium } = require('playwright');

async function testSyntaxErrors() {
    console.log('🔍 Testing for specific JavaScript syntax errors...\n');
    
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext();
    const page = await context.newPage();
    
    // Collect all errors and messages
    const errors = [];
    const consoleMessages = [];
    
    page.on('console', msg => {
        consoleMessages.push({
            type: msg.type(),
            text: msg.text(),
            location: msg.location()
        });
    });
    
    page.on('pageerror', error => {
        errors.push({
            message: error.message,
            stack: error.stack,
            name: error.name
        });
    });
    
    try {
        const filePath = 'file:///D:/OneDriveAanSubarkahOutlook/OneDrive/SekolahSabtuAuditor/ssa/ConvertPDFNonOCRPakeAI/dist/index-offline.html';
        console.log(`🔗 Loading: ${filePath}`);
        
        await page.goto(filePath, { waitUntil: 'domcontentloaded', timeout: 30000 });
        
        // Wait for potential lazy-loaded errors
        await page.waitForTimeout(3000);
        
        console.log('\n📋 Detailed Error Analysis:');
        console.log('='.repeat(60));
        
        if (errors.length === 0) {
            console.log('✅ No JavaScript errors detected!');
        } else {
            console.log(`❌ Found ${errors.length} JavaScript error(s):\n`);
            
            errors.forEach((error, index) => {
                console.log(`Error ${index + 1}:`);
                console.log(`  Name: ${error.name}`);
                console.log(`  Message: ${error.message}`);
                if (error.stack) {
                    console.log(`  Stack: ${error.stack.split('\n')[0]}`);
                }
                
                // Analyze common error patterns
                if (error.message.includes('Invalid or unexpected token')) {
                    console.log('  🔍 Analysis: This usually indicates malformed JavaScript, possibly in base64 encoding');
                }
                if (error.message.includes('missing ) after argument list')) {
                    console.log('  🔍 Analysis: Unclosed parentheses, likely in function calls or base64 worker creation');
                }
                if (error.message.includes('pdfjsLib is not defined')) {
                    console.log('  🔍 Analysis: PDF.js library not loaded properly');
                }
                
                console.log('');
            });
        }
        
        console.log('\n📋 Console Messages:');
        console.log('='.repeat(60));
        
        const errorMessages = consoleMessages.filter(msg => msg.type === 'error');
        const warningMessages = consoleMessages.filter(msg => msg.type === 'warning');
        
        console.log(`Errors: ${errorMessages.length}`);
        console.log(`Warnings: ${warningMessages.length}`);
        console.log(`Total: ${consoleMessages.length}`);
        
        if (errorMessages.length > 0) {
            console.log('\nError Messages:');
            errorMessages.forEach((msg, index) => {
                console.log(`  ${index + 1}. ${msg.text}`);
            });
        }
        
        if (warningMessages.length > 0) {
            console.log('\nWarning Messages:');
            warningMessages.forEach((msg, index) => {
                console.log(`  ${index + 1}. ${msg.text}`);
            });
        }
        
        // Test if we can access basic page elements despite errors
        console.log('\n📋 Element Accessibility Test:');
        console.log('='.repeat(60));
        
        try {
            const fileInput = await page.locator('input[type="file"]').count();
            console.log(`File input elements found: ${fileInput}`);
            
            const buttons = await page.locator('button').count();
            console.log(`Button elements found: ${buttons}`);
            
            const inputs = await page.locator('input').count();
            console.log(`Total input elements found: ${inputs}`);
            
            // Try to evaluate a simple JavaScript expression
            const canEvalJS = await page.evaluate(() => {
                try {
                    return typeof window !== 'undefined' && typeof document !== 'undefined';
                } catch (e) {
                    return false;
                }
            });
            console.log(`Basic JavaScript evaluation: ${canEvalJS ? '✅ Working' : '❌ Failed'}`);
            
        } catch (evalError) {
            console.log(`❌ Element test failed: ${evalError.message}`);
        }
        
        // Final assessment
        console.log('\n🎯 SUMMARY:');
        console.log('='.repeat(60));
        
        if (errors.length === 0) {
            console.log('🎉 SUCCESS: No JavaScript syntax errors found!');
            console.log('The base64 worker encoding appears to be working correctly.');
        } else {
            console.log('⚠️  ISSUES FOUND:');
            console.log('- JavaScript syntax errors are preventing proper functionality');
            console.log('- The base64 worker encoding needs to be fixed');
            console.log('- Recommend checking the build script base64 encoding logic');
        }
        
    } catch (error) {
        console.log(`❌ Test failed: ${error.message}`);
    } finally {
        await browser.close();
    }
}

testSyntaxErrors().catch(console.error);