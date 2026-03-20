const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const IMAGES_DIR = '/root/life/elternratgeber-system/tiktok_system/images/carousel_3_fehler_realistic';
const DATA_DIR = '/root/life/elternratgeber-system/tiktok_system/data';

async function main() {
    console.log('='.repeat(60));
    console.log('🌐 ÖFFNE TIKTOK');
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
    
    // Öffne TikTok Upload
    console.log('\n📱 Öffne TikTok Upload...');
    await page.goto('https://www.tiktok.com/upload');
    await page.waitForTimeout(3000);
    
    console.log('\n📱 Schritte:');
    console.log('   1. Logge dich in TikTok ein (im Browser-Fenster)');
    console.log('   2. Warte bis die Upload-Seite lädt');
    console.log('   3. Drücke ENTER hier im Terminal wenn eingeloggt');
    console.log('\n⏳ Warte auf Login...');
    
    // Warte auf ENTER
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
    
    console.log('\n💾 Speichere Session...');
    const storageState = await context.storageState();
    
    if (!fs.existsSync(DATA_DIR)) {
        fs.mkdirSync(DATA_DIR, { recursive: true });
    }
    
    fs.writeFileSync(
        path.join(DATA_DIR, 'tiktok_session.json'),
        JSON.stringify(storageState, null, 2)
    );
    
    console.log('   ✅ Session gespeichert!');
    
    // Navigiere zu Upload
    await page.goto('https://www.tiktok.com/upload');
    await page.waitForTimeout(5000);
    
    // Finde Bilder
    const images = fs.readdirSync(IMAGES_DIR)
        .filter(f => f.endsWith('.png'))
        .sort()
        .slice(0, 5)
        .map(f => path.join(IMAGES_DIR, f));
    
    console.log(`\n📤 ${images.length} Bilder gefunden`);
    
    // Upload
    console.log('\n📤 Starte Upload...');
    const fileInput = await page.waitForSelector('input[type="file"]', { timeout: 30000 });
    await fileInput.setInputFiles(images);
    
    console.log('   ✅ Bilder hochgeladen');
    await page.waitForTimeout(8000);
    
    // Caption
    console.log('📝 Füge Caption hinzu...');
    const caption = `3 Fehler, die fast alle Eltern machen – ohne es zu merken

Schulstress ist kein „Phase" – er wird oft durch die eigene Kommunikation verstärkt.

Hier sind die 3 größten Fehler und wie du sie vermeidest 👇

#schulstress #eltern #erziehung #psychologie #familie #tipps #mutter #vater #schule #lernen`;
    
    const captionInput = await page.$('[contenteditable="true"], textarea, div[contenteditable]');
    if (captionInput) {
        await captionInput.click();
        await captionInput.fill(caption);
        console.log('   ✅ Caption hinzugefügt');
    }
    
    console.log('\n' + '='.repeat(60));
    console.log('✅ UPLOAD BEREIT!');
    console.log('='.repeat(60));
    console.log('\n📝 NÄCHSTE SCHRITTE:');
    console.log('   1. Prüfe das Karussell im Browser');
    console.log('   2. Klicke auf "Posten" wenn alles passt');
    console.log('   3. ODER schließe das Fenster für später');
    console.log('\n⏳ Browser bleibt offen...');
    
    // Halte Browser offen
    await new Promise(() => {});
}

main().catch(console.error);
