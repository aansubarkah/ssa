const { chromium } = require('playwright');

async function testOfflinePDFConverter() {
    console.log('🚀 Starting Playwright test for offline PDF to Excel converter...');
    
    // Launch browser
    const browser = await chromium.launch({ 
        headless: false, // Set to true for headless mode
        slowMo: 1000 // Add delay between actions for better visibility
    });
    
    const context = await browser.newContext();
    const page = await context.newPage();
    
    // Listen for console messages and errors
    const consoleMessages = [];
    const jsErrors = [];
    
    page.on('console', msg => {
        consoleMessages.push({
            type: msg.type(),
            text: msg.text(),
            location: msg.location()
        });
        console.log(`[CONSOLE ${msg.type().toUpperCase()}] ${msg.text()}`);
    });
    
    page.on('pageerror', error => {
        jsErrors.push(error.message);
        console.error(`[JS ERROR] ${error.message}`);
    });
    
    try {
        console.log('\n📄 Test 1: Navigating to offline converter...');
        // Navigate to the offline converter
        const fileUrl = 'file:///D:/OneDriveAanSubarkahOutlook/OneDrive/SekolahSabtuAuditor/ssa/ConvertPDFNonOCRPakeAI/dist/index-offline.html';
        await page.goto(fileUrl);
        
        // Wait for page to load
        await page.waitForLoadState('networkidle');
        await page.waitForTimeout(2000); // Additional wait for JavaScript execution
        
        console.log('✅ Page loaded successfully');
        
        console.log('\n🔍 Test 2: Checking main interface elements...');
        
        // Check if main elements are visible
        const fileInput = await page.locator('input[type="file"]').first();
        const apiKeyInput = await page.locator('input[placeholder*="API"]').first();
        const convertButton = await page.locator('button').filter({ hasText: /convert/i }).first();
        
        const fileInputVisible = await fileInput.isVisible();
        const apiKeyInputVisible = await apiKeyInput.isVisible();
        const convertButtonVisible = await convertButton.isVisible();
        
        console.log(`File input visible: ${fileInputVisible ? '✅' : '❌'}`);
        console.log(`API key input visible: ${apiKeyInputVisible ? '✅' : '❌'}`);
        console.log(`Convert button visible: ${convertButtonVisible ? '✅' : '❌'}`);
        
        console.log('\n🧪 Test 3: Testing basic functionality - API key modal...');
        
        // Test API key modal functionality
        if (convertButtonVisible) {
            await convertButton.click();
            await page.waitForTimeout(1000);
            
            // Check if modal or alert appears
            const modal = await page.locator('[class*="modal"], [class*="popup"], .modal').first();
            const modalVisible = await modal.isVisible().catch(() => false);
            
            console.log(`API key modal/alert shown: ${modalVisible ? '✅' : '❌'}`);
            
            // Check for any alert dialogs
            let alertShown = false;
            page.on('dialog', dialog => {
                console.log(`Alert dialog shown: ${dialog.message()}`);
                alertShown = true;
                dialog.accept();
            });
            
            if (modalVisible) {
                console.log('✅ Modal functionality working');
            } else if (alertShown) {
                console.log('✅ Alert functionality working');
            }
        }
        
        console.log('\n🔧 Test 4: Checking PDF.js library loading...');
        
        // Check if PDF.js is loaded
        const pdfJsLoaded = await page.evaluate(() => {
            return typeof window.pdfjsLib !== 'undefined';
        });
        
        console.log(`PDF.js library loaded: ${pdfJsLoaded ? '✅' : '❌'}`);
        
        if (pdfJsLoaded) {
            const pdfJsVersion = await page.evaluate(() => {
                return window.pdfjsLib.version || 'version unknown';
            });
            console.log(`PDF.js version: ${pdfJsVersion}`);
        }
        
        console.log('\n🔧 Test 5: Checking XLSX library loading...');
        
        // Check if XLSX is loaded
        const xlsxLoaded = await page.evaluate(() => {
            return typeof window.XLSX !== 'undefined';
        });
        
        console.log(`XLSX library loaded: ${xlsxLoaded ? '✅' : '❌'}`);
        
        console.log('\n📊 Test Results Summary:');
        console.log('========================');
        console.log(`Page loaded: ✅`);
        console.log(`File input visible: ${fileInputVisible ? '✅' : '❌'}`);
        console.log(`API key input visible: ${apiKeyInputVisible ? '✅' : '❌'}`);
        console.log(`Convert button visible: ${convertButtonVisible ? '✅' : '❌'}`);
        console.log(`PDF.js loaded: ${pdfJsLoaded ? '✅' : '❌'}`);
        console.log(`XLSX loaded: ${xlsxLoaded ? '✅' : '❌'}`);
        console.log(`JavaScript errors: ${jsErrors.length === 0 ? '✅ None' : `❌ ${jsErrors.length} errors`}`);
        
        if (jsErrors.length > 0) {
            console.log('\n❌ JavaScript Errors Found:');
            jsErrors.forEach((error, index) => {
                console.log(`${index + 1}. ${error}`);
            });
        }
        
        if (consoleMessages.length > 0) {
            console.log('\n📝 Console Messages:');
            consoleMessages.forEach((msg, index) => {
                if (msg.type === 'error') {
                    console.log(`${index + 1}. [${msg.type.toUpperCase()}] ${msg.text}`);
                }
            });
        }
        
        // Overall assessment
        const allTestsPassed = fileInputVisible && apiKeyInputVisible && convertButtonVisible && 
                              pdfJsLoaded && xlsxLoaded && jsErrors.length === 0;
        
        console.log('\n🎯 Overall Assessment:');
        console.log(`Status: ${allTestsPassed ? '✅ ALL TESTS PASSED' : '❌ SOME TESTS FAILED'}`);
        
        if (allTestsPassed) {
            console.log('🎉 The offline PDF to Excel converter is working properly!');
        } else {
            console.log('⚠️  Some issues were detected. Check the details above.');
        }
        
        // Keep browser open for 5 seconds to observe
        await page.waitForTimeout(5000);
        
    } catch (error) {
        console.error('❌ Test failed with error:', error.message);
        jsErrors.push(error.message);
    } finally {
        await browser.close();
        console.log('\n🏁 Test completed');
    }
}

// Run the test
testOfflinePDFConverter().catch(console.error);