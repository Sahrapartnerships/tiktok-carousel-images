#!/usr/bin/env python3
"""
TikTok & Instagram Carousel Upload Bot mit PERSISTENTEM LOGIN
Speichert Session-Daten, damit du nicht jedes Mal neu einloggen musst
"""

import asyncio
import json
import os
from pathlib import Path
from datetime import datetime

from playwright.async_api import async_playwright

# Configuration
IMAGES_DIR = Path('/root/life/elternratgeber-system/tiktok_system/images/carousel_3_fehler_realistic')
DATA_DIR = Path('/root/life/elternratgeber-system/tiktok_system/data')
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Session files
TIKTOK_SESSION = DATA_DIR / 'tiktok_session.json'
INSTAGRAM_SESSION = DATA_DIR / 'instagram_session.json'
TRACKING_FILE = DATA_DIR / 'post_tracking.json'


class PersistentUploader:
    """Uploader mit persistenter Session"""
    
    def __init__(self):
        self.tracking_data = self._load_tracking()
    
    def _load_tracking(self):
        if TRACKING_FILE.exists():
            with open(TRACKING_FILE) as f:
                return json.load(f)
        return {"posts": [], "last_upload": None}
    
    def _save_tracking(self):
        with open(TRACKING_FILE, 'w') as f:
            json.dump(self.tracking_data, f, indent=2)
    
    async def _get_browser_context(self, playwright, session_file):
        """Get or create browser context with saved session"""
        browser = await playwright.chromium.launch(
            headless=False,  # Visible for user interaction
            args=['--disable-blink-features=AutomationControlled']
        )
        
        # Load existing session if available
        if session_file.exists():
            print(f"   📂 Loading saved session from {session_file.name}")
            with open(session_file) as f:
                storage_state = json.load(f)
            context = await browser.new_context(
                storage_state=storage_state,
                viewport={'width': 1280, 'height': 900}
            )
            return browser, context, True  # True = has existing session
        else:
            print(f"   🆕 No session found - new login required")
            context = await browser.new_context(
                viewport={'width': 1280, 'height': 900}
            )
            return browser, context, False
    
    async def _save_session(self, context, session_file):
        """Save current browser session"""
        storage_state = await context.storage_state()
        with open(session_file, 'w') as f:
            json.dump(storage_state, f)
        print(f"   💾 Session saved to {session_file.name}")
    
    async def upload_to_tiktok(self, images, caption, hashtags):
        """Upload to TikTok with persistent session"""
        async with async_playwright() as p:
            browser, context, has_session = await self._get_browser_context(p, TIKTOK_SESSION)
            page = await context.new_page()
            
            try:
                print("🌐 Opening TikTok...")
                await page.goto('https://www.tiktok.com/upload')
                await page.wait_for_timeout(3000)
                
                # Check if we're logged in
                if 'login' in page.url.lower() or await page.query_selector('input[name="username"]'):
                    print("🔐 Login required!")
                    print("   Please login manually in the browser window...")
                    print("   Waiting up to 120 seconds for login...")
                    
                    # Wait for redirect away from login page
                    for i in range(120):
                        await page.wait_for_timeout(1000)
                        if 'login' not in page.url.lower():
                            print("   ✅ Login detected!")
                            break
                        if i == 30:
                            print("   ⏳ Still waiting... (30s)")
                        if i == 60:
                            print("   ⏳ Still waiting... (60s)")
                    
                    # Save the new session
                    await self._save_session(context, TIKTOK_SESSION)
                else:
                    print("   ✅ Already logged in!")
                
                # Navigate to upload page
                print("📤 Opening upload interface...")
                await page.goto('https://www.tiktok.com/upload')
                await page.wait_for_timeout(5000)
                
                # Handle "Upload Studio" vs direct upload
                # Try to find file upload input
                print("📤 Uploading carousel images...")
                
                # Wait for and click "Upload" button if needed
                upload_btn = await page.query_selector('text=/upload|Upload/i')
                if upload_btn:
                    await upload_btn.click()
                    await page.wait_for_timeout(2000)
                
                # Find file input
                file_input = await page.wait_for_selector('input[type="file"]', timeout=10000)
                
                # Upload all 5 images
                print(f"   Uploading {len(images)} images...")
                await file_input.set_input_files(images[:5])  # Max 5 images
                await page.wait_for_timeout(8000)  # Wait for processing
                
                # Add caption
                print("📝 Adding caption...")
                caption_input = await page.query_selector('[contenteditable="true"], textarea[data-testid*="caption"], div[contenteditable]')
                
                if caption_input:
                    full_text = f"{caption}\n\n{' '.join(hashtags)}"
                    await caption_input.click()
                    await caption_input.fill(full_text)
                    print("   ✅ Caption added")
                else:
                    print("   ⚠️  Caption input not found - you may need to add manually")
                
                await page.wait_for_timeout(3000)
                
                # Important: Save session again after successful upload flow
                await self._save_session(context, TIKTOK_SESSION)
                
                # Track upload
                post_data = {
                    "platform": "tiktok",
                    "timestamp": datetime.now().isoformat(),
                    "images": [str(img) for img in images[:5]],
                    "caption": caption[:100],
                    "status": "draft_ready",
                    "tracking_url": None
                }
                self.tracking_data["posts"].append(post_data)
                self.tracking_data["last_upload"] = datetime.now().isoformat()
                self._save_tracking()
                
                print("\n" + "="*60)
                print("✅ UPLOAD BEREIT!")
                print("="*60)
                print("\n📝 NÄCHSTE SCHRITTE:")
                print("   1. Review das Karussell im Browser")
                print("   2. Klicke 'Post' wenn alles passt")
                print("   3. ODER schließe das Fenster für später")
                print("\n💾 Session gespeichert - beim nächsten Mal")
                print("   bist du automatisch eingeloggt!")
                print("\n⏳ Browser bleibt offen (schließe manuell wenn fertig)")
                
                # Keep browser open indefinitely
                while True:
                    await page.wait_for_timeout(10000)
                    # Check if page is still open
                    try:
                        await page.evaluate('1')
                    except:
                        print("\n   Browser wurde geschlossen")
                        break
                
            except Exception as e:
                print(f"\n❌ Error: {e}")
                await page.screenshot(path='/tmp/tiktok_error.png')
                print("   Screenshot: /tmp/tiktok_error.png")
                
            finally:
                await browser.close()
    
    async def upload_to_instagram(self, images, caption):
        """Upload to Instagram with persistent session"""
        async with async_playwright() as p:
            browser, context, has_session = await self._get_browser_context(p, INSTAGRAM_SESSION)
            page = await context.new_page()
            
            try:
                print("🌐 Opening Instagram...")
                await page.goto('https://www.instagram.com/')
                await page.wait_for_timeout(3000)
                
                # Check login
                login_form = await page.query_selector('input[name="username"]')
                if login_form:
                    print("🔐 Instagram login required!")
                    print("   Please login manually...")
                    
                    for i in range(120):
                        await page.wait_for_timeout(1000)
                        login_form = await page.query_selector('input[name="username"]')
                        if not login_form:
                            print("   ✅ Login detected!")
                            break
                    
                    await self._save_session(context, INSTAGRAM_SESSION)
                else:
                    print("   ✅ Already logged in!")
                
                # Navigate to create post
                print("📤 Opening create post...")
                await page.goto('https://www.instagram.com/create/select/')
                await page.wait_for_timeout(5000)
                
                # Upload images
                print("📤 Uploading images...")
                file_input = await page.wait_for_selector('input[type="file"]', timeout=10000)
                await file_input.set_input_files(images[:10])  # Instagram allows up to 10
                await page.wait_for_timeout(8000)
                
                # Click through to caption
                next_btn = await page.query_selector('text=/next|weiter/i')
                if next_btn:
                    await next_btn.click()
                    await page.wait_for_timeout(2000)
                
                # Add caption
                print("📝 Adding caption...")
                caption_input = await page.query_selector('textarea[aria-label*="caption" i], textarea[placeholder*="caption" i]')
                if caption_input:
                    await caption_input.fill(caption)
                    print("   ✅ Caption added")
                
                await self._save_session(context, INSTAGRAM_SESSION)
                
                print("\n✅ INSTAGRAM UPLOAD BEREIT!")
                print("   Review und poste manuell, oder schließe das Fenster")
                
                # Keep open
                while True:
                    await page.wait_for_timeout(10000)
                    try:
                        await page.evaluate('1')
                    except:
                        break
                
            except Exception as e:
                print(f"❌ Error: {e}")
                await page.screenshot(path='/tmp/instagram_error.png')
                
            finally:
                await browser.close()


async def main():
    """Main workflow"""
    
    # Find images
    image_files = sorted([
        IMAGES_DIR / f"slide_0{i}_fehler_{i}_final.png" if i > 1 else IMAGES_DIR / f"slide_0{i}_hook_final.png"
        for i in range(1, 6)
    ])
    
    existing_images = [str(img) for img in image_files if img.exists()]
    
    if len(existing_images) < 5:
        # Fallback to premium
        premium_dir = Path('/root/life/elternratgeber-system/tiktok_system/images/carousel_3_fehler_premium')
        existing_images = sorted([str(f) for f in premium_dir.glob('*_final.png')])[:5]
    
    print(f"\n📁 {len(existing_images)} Bilder gefunden")
    
    # Caption
    caption = """3 Fehler, die fast alle Eltern machen – ohne es zu merken

Schulstress ist kein „Phase" – er wird oft durch die eigene Kommunikation verstärkt.

Hier sind die 3 größten Fehler und wie du sie vermeidest 👇"""
    
    hashtags = [
        "#schulstress", "#eltern", "#erziehung", "#psychologie",
        "#familie", "#tipps", "#mutter", "#vater", "#schule", "#lernen"
    ]
    
    uploader = PersistentUploader()
    
    # Check existing sessions
    print("\n" + "="*60)
    print("🔐 SESSION STATUS")
    print("="*60)
    print(f"   TikTok:     {'✅ Gespeichert' if TIKTOK_SESSION.exists() else '❌ Neu einloggen'}")
    print(f"   Instagram:  {'✅ Gespeichert' if INSTAGRAM_SESSION.exists() else '❌ Neu einloggen'}")
    
    # Upload to TikTok
    print("\n" + "="*60)
    print("🎵 TIKTOK UPLOAD")
    print("="*60)
    await uploader.upload_to_tiktok(existing_images, caption, hashtags)
    
    # Upload to Instagram
    print("\n" + "="*60)
    print("📸 INSTAGRAM UPLOAD")
    print("="*60)
    await uploader.upload_to_instagram(existing_images, caption)
    
    print("\n" + "="*60)
    print("✅ ALLE UPLOADS ABGESCHLOSSEN")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
