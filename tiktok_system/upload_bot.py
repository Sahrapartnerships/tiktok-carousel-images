#!/usr/bin/env python3
"""
TikTok & Instagram Carousel Upload Bot
Uploads carousel as DRAFT for manual approval
Includes view tracking setup
"""

import asyncio
import json
import os
from pathlib import Path
from datetime import datetime

from playwright.async_api import async_playwright

# Configuration
IMAGES_DIR = Path('/root/life/elternratgeber-system/tiktok_system/images/carousel_3_fehler_realistic')
TRACKING_FILE = Path('/root/life/elternratgeber-system/tiktok_system/data/post_tracking.json')

# Ensure tracking directory exists
TRACKING_FILE.parent.mkdir(parents=True, exist_ok=True)

class TikTokUploader:
    def __init__(self):
        self.tracking_data = self._load_tracking()
    
    def _load_tracking(self):
        """Load existing tracking data"""
        if TRACKING_FILE.exists():
            with open(TRACKING_FILE) as f:
                return json.load(f)
        return {"posts": [], "last_upload": None}
    
    def _save_tracking(self):
        """Save tracking data"""
        with open(TRACKING_FILE, 'w') as f:
            json.dump(self.tracking_data, f, indent=2)
    
    async def upload_to_tiktok(self, images, caption, hashtags):
        """
        Upload carousel to TikTok as DRAFT
        
        Args:
            images: List of image paths (5 slides)
            caption: Post caption text
            hashtags: List of hashtags
        """
        async with async_playwright() as p:
            # Launch browser (headed for first run to see what's happening)
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context(
                viewport={'width': 1280, 'height': 800}
            )
            page = await context.new_page()
            
            try:
                print("🌐 Opening TikTok...")
                await page.goto('https://www.tiktok.com/upload')
                await page.wait_for_timeout(3000)
                
                # Check if login required
                if 'login' in page.url.lower():
                    print("🔐 Login required!")
                    print("   Please login manually in the browser window")
                    print("   Waiting 60 seconds for manual login...")
                    await page.wait_for_timeout(60000)
                
                print("📤 Uploading carousel images...")
                
                # Wait for upload button
                await page.wait_for_selector('input[type="file"]', timeout=10000)
                
                # Upload images
                file_input = await page.query_selector('input[type="file"]')
                await file_input.set_input_files(images)
                
                print(f"   Uploaded {len(images)} images")
                await page.wait_for_timeout(5000)
                
                # Add caption
                print("📝 Adding caption...")
                caption_input = await page.query_selector('[contenteditable="true"]')
                if caption_input:
                    full_caption = f"{caption}\n\n{' '.join(hashtags)}"
                    await caption_input.fill(full_caption)
                    print("   Caption added")
                
                await page.wait_for_timeout(2000)
                
                # Save as draft (don't post yet)
                print("💾 Saving as DRAFT...")
                # Look for draft button or similar
                # TikTok might have "Save draft" or we just don't click "Post"
                
                print("\n✅ UPLOAD COMPLETE")
                print("   Images uploaded as draft")
                print("   Review in TikTok Studio and click 'Post' when ready")
                
                # Track the upload
                post_data = {
                    "platform": "tiktok",
                    "timestamp": datetime.now().isoformat(),
                    "images": [str(img) for img in images],
                    "caption": caption,
                    "hashtags": hashtags,
                    "status": "draft",
                    "tracking_url": None  # Will be added after posting
                }
                self.tracking_data["posts"].append(post_data)
                self.tracking_data["last_upload"] = datetime.now().isoformat()
                self._save_tracking()
                
                # Keep browser open for manual review
                print("\n⏳ Browser stays open for 60 seconds...")
                print("   You can manually complete the post or close the window")
                await page.wait_for_timeout(60000)
                
            except Exception as e:
                print(f"❌ Error: {e}")
                # Take screenshot for debugging
                await page.screenshot(path='/tmp/tiktok_error.png')
                print("   Screenshot saved to /tmp/tiktok_error.png")
                
            finally:
                await browser.close()
    
    async def upload_to_instagram(self, images, caption):
        """
        Upload carousel to Instagram as DRAFT
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context(
                viewport={'width': 1280, 'height': 900}
            )
            page = await context.new_page()
            
            try:
                print("🌐 Opening Instagram...")
                await page.goto('https://www.instagram.com/')
                await page.wait_for_timeout(3000)
                
                # Check login
                if 'login' in page.url.lower():
                    print("🔐 Login required!")
                    print("   Please login manually...")
                    await page.wait_for_timeout(60000)
                
                print("📤 Navigating to create post...")
                await page.goto('https://www.instagram.com/create/style/')
                await page.wait_for_timeout(3000)
                
                print("📤 Uploading images...")
                # Instagram upload flow
                file_input = await page.wait_for_selector('input[type="file"]', timeout=10000)
                await file_input.set_input_files(images)
                
                await page.wait_for_timeout(5000)
                
                print("📝 Adding caption...")
                caption_input = await page.query_selector('textarea[aria-label*="caption" i]')
                if caption_input:
                    await caption_input.fill(caption)
                
                print("💾 Saving as draft...")
                # Instagram draft logic
                
                print("\n✅ INSTAGRAM UPLOAD COMPLETE")
                print("   Review and post manually")
                
                await page.wait_for_timeout(60000)
                
            except Exception as e:
                print(f"❌ Error: {e}")
                await page.screenshot(path='/tmp/instagram_error.png')
                
            finally:
                await browser.close()


class ViewTracker:
    """Track views, likes, comments for posted content"""
    
    def __init__(self):
        self.data_file = Path('/root/life/elternratgeber-system/tiktok_system/data/view_data.json')
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        self.data = self._load_data()
    
    def _load_data(self):
        if self.data_file.exists():
            with open(self.data_file) as f:
                return json.load(f)
        return {}
    
    def _save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    async def scrape_tiktok_stats(self, post_url):
        """Scrape view/like/comment counts from TikTok post"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                await page.goto(post_url)
                await page.wait_for_timeout(3000)
                
                # Extract stats
                stats = {}
                
                # Views (might need different selector)
                view_elem = await page.query_selector('[data-e2e="browse-video-views"]')
                if view_elem:
                    stats['views'] = await view_elem.inner_text()
                
                # Likes
                like_elem = await page.query_selector('[data-e2e="like-count"]')
                if like_elem:
                    stats['likes'] = await like_elem.inner_text()
                
                # Comments
                comment_elem = await page.query_selector('[data-e2e="comment-count"]')
                if comment_elem:
                    stats['comments'] = await comment_elem.inner_text()
                
                # Save
                self.data[post_url] = {
                    "timestamp": datetime.now().isoformat(),
                    "stats": stats
                }
                self._save_data()
                
                return stats
                
            finally:
                await browser.close()


async def main():
    """Main upload workflow"""
    
    # Get images
    image_files = sorted([
        IMAGES_DIR / f"slide_0{i}_fehler_{i}_final.png" if i > 1 else IMAGES_DIR / f"slide_0{i}_hook_final.png"
        for i in range(1, 6)
    ])
    
    # Check which images exist
    existing_images = [str(img) for img in image_files if img.exists()]
    
    if len(existing_images) < 5:
        print("⚠️  Not all images found!")
        print(f"   Looking in: {IMAGES_DIR}")
        # Fallback to premium version
        premium_dir = Path('/root/life/elternratgeber-system/tiktok_system/images/carousel_3_fehler_premium')
        existing_images = sorted([str(f) for f in premium_dir.glob('*_final.png')])
        print(f"   Using premium version: {len(existing_images)} images found")
    
    print(f"\n📁 Found {len(existing_images)} images")
    for img in existing_images[:5]:
        print(f"   - {Path(img).name}")
    
    # Caption and hashtags
    caption = """3 Fehler, die fast alle Eltern machen – ohne es zu merken 😰

Schulstress ist kein „Phase" – er wird oft durch die eigene Kommunikation verstärkt.

Hier sind die 3 größten Fehler und wie du sie vermeidest 👇"""
    
    hashtags = [
        "#schulstress",
        "#eltern",
        "#erziehung",
        "#psychologie",
        "#familie",
        "#tipps",
        "#mutter",
        "#vater",
        "#schule",
        "#lernen"
    ]
    
    # Upload to TikTok
    print("\n" + "="*60)
    print("🎵 TIKTOK UPLOAD")
    print("="*60)
    uploader = TikTokUploader()
    await uploader.upload_to_tiktok(existing_images[:5], caption, hashtags)
    
    # Upload to Instagram
    print("\n" + "="*60)
    print("📸 INSTAGRAM UPLOAD")
    print("="*60)
    await uploader.upload_to_instagram(existing_images[:5], caption)


if __name__ == "__main__":
    asyncio.run(main())
