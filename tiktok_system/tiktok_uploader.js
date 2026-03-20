const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const IMAGES_DIR = '/root/life/elternratgeber-system/tiktok_system/images/carousel_3_fehler_realistic';
const DATA_DIR = '/root/life/elternratgeber-system/tiktok_system/data';

async function main() {
    console.log('='.repeat(60));
    console.log('🎵 TIKTOK UPLOAD BOT');
    console.log('='.repeat(60));
    
    // Nutze bestehenden VNC Display
    process.env.DISPLAY = ':1';
    
    const browser = await chromium.launch({
        headless: false,
        args: [
            '--disable-blink-features=AutomationControlled',
            '--no-sandbox',
            '--disable-setuid-sandbox'
        ]
    });
    
    const context = await browser.newContext({
        viewport: { width: 1280, height: 900 }
    });
    
    const page = await context.newPage();
    
    // Check for saved session
    const sessionFile = path.join(DATA_DIR, 'tiktok_session.json');
    let hasSession = false;
    
    if (fs.existsSync(sessionFile)) {
        console.log('\n📂 Loading saved session...');
        const storageState = JSON.parse(fs.readFileSync(sessionFile));
        await context.addCookies(storageState.cookies || []);
        hasSession = true;
    }
    
    // Öffne TikTok Upload
    console.log('\n🌐 Opening TikTok...');
    await page.goto('https://www.tiktok.com/upload');
    await page.waitForTimeout(3000);
    
    // Check if logged in
    const loginForm = await page.$('input[name="username"], input[placeholder*="username" i]');
    if (loginForm) {
        console.log('\n🔐 LOGIN REQUIRED');
        console.log('   Please login manually in the browser window.');
        console.log('   Press ENTER here when logged in...\n');
        
        // Wait for ENTER
        await new Promise((resolve) => {
            process.stdin.setRawMode(true);
            process.stdin.resume();
            process.stdin.on('data', (data) => {
                if (data[0] === 13 || data[0] === 10) {
                    process.stdin.setRawMode(false);
                    process.stdin.pause();
                    resolve();
                }
            });
        });
        
        // Save session
        console.log('\n💾 Saving session...');
        const storageState = await context.storageState();
        if (!fs.existsSync(DATA_DIR)) {
            fs.mkdirSync(DATA_DIR, { recursive: true });
        }
        fs.writeFileSync(sessionFile, JSON.stringify(storageState, null, 2));
        console.log('   ✅ Session saved!');
    } else {
        console.log('   ✅ Already logged in!');
    }
    
    // Navigate to upload
    await page.goto('https://www.tiktok.com/upload');
    await page.waitForTimeout(5000);
    
    // Upload images
    const images = fs.readdirSync(IMAGES_DIR)
        .filter(f => f.endsWith('.png'))
        .sort()
        .slice(0, 5)
        .map(f => path.join(IMAGES_DIR, f));
    
    console.log(`\n📤 Uploading ${images.length} images...`);
    
    const fileInput = await page.waitForSelector('input[type="file"]', { timeout: 30000 });
    await fileInput.setInputFiles(images);
    
    console.log('   ✅ Images uploaded');
    await page.waitForTimeout(8000);
    
    // Add caption
    console.log('📝 Adding caption...');
    const caption = `3 Fehler, die fast alle Eltern machen – ohne es zu merken

Schulstress ist kein „Phase" – er wird oft durch die eigene Kommunikation verstärkt.

Hier sind die 3 größten Fehler und wie du sie vermeidest 👇

#schulstress #eltern #erziehung #psychologie #familie #tipps #mutter #vater #schule #lernen`;
    
    const captionInput = await page.$('[contenteditable="true"], textarea, div[contenteditable]');
    if (captionInput) {
        await captionInput.click();
        await captionInput.fill(caption);
        console.log('   ✅ Caption added');
    }
    
    console.log('\n' + '='.repeat(60));
    console.log('✅ READY TO POST!');
    console.log('='.repeat(60));
    console.log('\n📝 NEXT STEPS:');
    console.log('   1. Check the carousel in the browser');
    console.log('   2. Click "Post" when ready');
    console.log('   3. Or close the browser to save as draft');
    console.log('\n⏳ Browser stays open...');
    
    // Keep browser open
    await new Promise(() => {});
}

main().catch(console.error);
