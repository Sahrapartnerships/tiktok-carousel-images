#!/usr/bin/env python3
"""
Playwright TikTok Upload - Browser Automation
Öffnet TikTok im sichtbaren Browser für Login
"""

import asyncio
from playwright.async_api import async_playwright
from pathlib import Path

# Bilder-Pfade
IMAGES_DIR = Path('/root/life/elternratgeber-system/tiktok_system/images/carousel_3_fehler_realistic')

async def main():
    async with async_playwright() as p:
        # Browser im sichtbaren Modus starten
        browser = await p.chromium.launch(
            headless=False,  # SICHTBAR für Login
            args=['--disable-blink-features=AutomationControlled']
        )
        
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 900}
        )
        
        page = await context.new_page()
        
        print("="*60)
        print("🌐 ÖFFNE TIKTOK")
        print("="*60)
        
        # TikTok Upload Seite öffnen
        await page.goto('https://www.tiktok.com/upload')
        await page.wait_for_timeout(3000)
        
        print("\n📱 Schritte:")
        print("   1. Logge dich in TikTok ein (im Browser-Fenster)")
        print("   2. Warte bis die Upload-Seite lädt")
        print("   3. Drücke ENTER hier im Terminal wenn eingeloggt")
        print("\n⏳ Warte auf Login...")
        
        # Warte auf Benutzereingabe
        input("\n🔐 Drücke ENTER wenn du eingeloggt bist...")
        
        # Speichere Session
        print("\n💾 Speichere Session...")
        storage_state = await context.storage_state()
        
        import json
        session_file = Path('/root/life/elternratgeber-system/tiktok_system/data/tiktok_session.json')
        session_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(session_file, 'w') as f:
            json.dump(storage_state, f)
        
        print("   ✅ Session gespeichert!")
        
        # Navigiere zu Upload
        await page.goto('https://www.tiktok.com/upload')
        await page.wait_for_timeout(5000)
        
        # Finde Bilder
        images = sorted([str(f) for f in IMAGES_DIR.glob('*.png')])[:5]
        print(f"\n📤 {len(images)} Bilder gefunden")
        
        # Upload durchführen
        print("\n📤 Starte Upload...")
        
        # Warte auf File Input
        file_input = await page.wait_for_selector('input[type="file"]', timeout=30000)
        await file_input.set_input_files(images)
        
        print("   ✅ Bilder hochgeladen")
        await page.wait_for_timeout(8000)
        
        # Caption hinzufügen
        print("📝 Füge Caption hinzu...")
        caption = """3 Fehler, die fast alle Eltern machen – ohne es zu merken

Schulstress ist kein „Phase" – er wird oft durch die eigene Kommunikation verstärkt.

Hier sind die 3 größten Fehler und wie du sie vermeidest 👇

#schulstress #eltern #erziehung #psychologie #familie #tipps #mutter #vater #schule #lernen"""
        
        caption_input = await page.query_selector('[contenteditable="true"], textarea, div[contenteditable]')
        if caption_input:
            await caption_input.click()
            await caption_input.fill(caption)
            print("   ✅ Caption hinzugefügt")
        
        print("\n" + "="*60)
        print("✅ UPLOAD BEREIT!")
        print("="*60)
        print("\n📝 NÄCHSTE SCHRITTE:")
        print("   1. Prüfe das Karussell im Browser")
        print("   2. Klicke auf 'Posten' wenn alles passt")
        print("   3. ODER schließe das Fenster für später")
        print("\n⏳ Browser bleibt offen...")
        
        # Halte Browser offen
        while True:
            await page.wait_for_timeout(10000)
            try:
                await page.evaluate('1')
            except:
                print("\n   Browser geschlossen")
                break
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
