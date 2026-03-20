#!/usr/bin/env python3
"""
Session Manager für TikTok/Instagram Upload Bot
- Testet ob Session noch gültig ist
- Löscht Session (für neuen Login)
- Zeigt Session-Status
"""

import asyncio
import json
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright

DATA_DIR = Path('/root/life/elternratgeber-system/tiktok_system/data')
TIKTOK_SESSION = DATA_DIR / 'tiktok_session.json'
INSTAGRAM_SESSION = DATA_DIR / 'instagram_session.json'


class SessionManager:
    """Manage browser sessions"""
    
    def show_status(self):
        """Show current session status"""
        print("\n" + "="*60)
        print("🔐 SESSION STATUS")
        print("="*60)
        
        # TikTok
        if TIKTOK_SESSION.exists():
            with open(TIKTOK_SESSION) as f:
                data = json.load(f)
            cookies_count = len(data.get('cookies', []))
            origin_count = len(data.get('origins', []))
            modified = datetime.fromtimestamp(TIKTOK_SESSION.stat().st_mtime)
            print(f"\n📱 TikTok:")
            print(f"   ✅ Session vorhanden")
            print(f"   📊 {cookies_count} Cookies, {origin_count} Origins")
            print(f"   🕐 Letztes Update: {modified.strftime('%Y-%m-%d %H:%M')}")
        else:
            print(f"\n📱 TikTok:")
            print(f"   ❌ Keine Session")
            print(f"   📝 Beim nächsten Upload: Login erforderlich")
        
        # Instagram
        if INSTAGRAM_SESSION.exists():
            with open(INSTAGRAM_SESSION) as f:
                data = json.load(f)
            cookies_count = len(data.get('cookies', []))
            origin_count = len(data.get('origins', []))
            modified = datetime.fromtimestamp(INSTAGRAM_SESSION.stat().st_mtime)
            print(f"\n📸 Instagram:")
            print(f"   ✅ Session vorhanden")
            print(f"   📊 {cookies_count} Cookies, {origin_count} Origins")
            print(f"   🕐 Letztes Update: {modified.strftime('%Y-%m-%d %H:%M')}")
        else:
            print(f"\n📸 Instagram:")
            print(f"   ❌ Keine Session")
            print(f"   📝 Beim nächsten Upload: Login erforderlich")
    
    async def test_session(self, platform):
        """Test if session is still valid"""
        session_file = TIKTOK_SESSION if platform == 'tiktok' else INSTAGRAM_SESSION
        
        if not session_file.exists():
            print(f"❌ Keine Session für {platform} gefunden")
            return False
        
        print(f"\n🧪 Teste {platform} Session...")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            
            with open(session_file) as f:
                storage_state = json.load(f)
            
            context = await browser.new_context(storage_state=storage_state)
            page = await context.new_page()
            
            try:
                if platform == 'tiktok':
                    await page.goto('https://www.tiktok.com/upload')
                    await page.wait_for_timeout(3000)
                    
                    # Check if we're on login page
                    if 'login' in page.url.lower():
                        print(f"   ❌ Session ungültig - Login erforderlich")
                        return False
                    else:
                        print(f"   ✅ Session gültig - Bereit zum Upload")
                        return True
                        
                else:  # instagram
                    await page.goto('https://www.instagram.com/')
                    await page.wait_for_timeout(3000)
                    
                    login_form = await page.query_selector('input[name="username"]')
                    if login_form:
                        print(f"   ❌ Session ungültig - Login erforderlich")
                        return False
                    else:
                        print(f"   ✅ Session gültig - Bereit zum Upload")
                        return True
                        
            except Exception as e:
                print(f"   ❌ Fehler beim Testen: {e}")
                return False
            finally:
                await browser.close()
    
    def delete_session(self, platform):
        """Delete session file"""
        session_file = TIKTOK_SESSION if platform == 'tiktok' else INSTAGRAM_SESSION
        
        if session_file.exists():
            session_file.unlink()
            print(f"✅ {platform} Session gelöscht")
            print(f"   Beim nächsten Upload: Neuer Login erforderlich")
        else:
            print(f"ℹ️  Keine Session für {platform} vorhanden")
    
    def delete_all(self):
        """Delete all sessions"""
        deleted = []
        if TIKTOK_SESSION.exists():
            TIKTOK_SESSION.unlink()
            deleted.append("TikTok")
        if INSTAGRAM_SESSION.exists():
            INSTAGRAM_SESSION.unlink()
            deleted.append("Instagram")
        
        if deleted:
            print(f"✅ Sessions gelöscht: {', '.join(deleted)}")
        else:
            print("ℹ️  Keine Sessions vorhanden")


def main():
    import sys
    
    manager = SessionManager()
    
    if len(sys.argv) == 1:
        # Show status
        manager.show_status()
        print("\n" + "="*60)
        print("BEFEHLE:")
        print("="*60)
        print("  python session_manager.py status")
        print("  python session_manager.py test tiktok|instagram")
        print("  python session_manager.py delete tiktok|instagram|all")
        
    elif sys.argv[1] == "status":
        manager.show_status()
        
    elif sys.argv[1] == "test":
        if len(sys.argv) < 3:
            print("Usage: python session_manager.py test tiktok|instagram")
            return
        platform = sys.argv[2].lower()
        if platform not in ['tiktok', 'instagram']:
            print("Platform muss 'tiktok' oder 'instagram' sein")
            return
        asyncio.run(manager.test_session(platform))
        
    elif sys.argv[1] == "delete":
        if len(sys.argv) < 3:
            print("Usage: python session_manager.py delete tiktok|instagram|all")
            return
        target = sys.argv[2].lower()
        
        if target == 'all':
            manager.delete_all()
        elif target in ['tiktok', 'instagram']:
            manager.delete_session(target)
        else:
            print("Target muss 'tiktok', 'instagram' oder 'all' sein")


if __name__ == "__main__":
    main()
