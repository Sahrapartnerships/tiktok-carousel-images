#!/usr/bin/env python3
"""
Instagram Performance Tracker
Manuelle Eingabe von Instagram Insights für Analyse
"""

import json
from datetime import datetime
from pathlib import Path

class InstagramTracker:
    def __init__(self):
        self.data_file = Path("/root/life/elternratgeber-system/marketing/instagram_performance.json")
        self.data = self._load_data()
    
    def _load_data(self):
        if self.data_file.exists():
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return {"posts": [], "summary": {}}
    
    def _save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def add_post(self, post_id, caption, post_type, hashtags, timestamp):
        """Fügt neuen Post hinzu (wird nach Upload aufgerufen)"""
        post = {
            "id": post_id,
            "caption": caption[:100] + "..." if len(caption) > 100 else caption,
            "type": post_type,  # carousel, single_image, reel
            "hashtags": hashtags,
            "posted_at": timestamp,
            "metrics": {},
            "updated_at": None
        }
        self.data["posts"].append(post)
        self._save_data()
        print(f"✅ Post {post_id} zum Tracking hinzugefügt")
    
    def update_metrics(self, post_id, likes, comments, shares, saves, reach, impressions):
        """Manuelle Aktualisierung durch Master Albert (aus Instagram Insights kopieren)"""
        for post in self.data["posts"]:
            if post["id"] == post_id:
                post["metrics"] = {
                    "likes": likes,
                    "comments": comments,
                    "shares": shares,
                    "saves": saves,
                    "reach": reach,
                    "impressions": impressions,
                    "engagement_rate": round((likes + comments + shares + saves) / reach * 100, 2) if reach > 0 else 0,
                    "updated_at": datetime.now().isoformat()
                }
                self._save_data()
                print(f"✅ Metrics für {post_id} aktualisiert")
                self._analyze_post(post)
                return
        print(f"❌ Post {post_id} nicht gefunden")
    
    def _analyze_post(self, post):
        """Gibt Analyse und Optimierungsvorschläge"""
        m = post["metrics"]
        engagement = m.get("engagement_rate", 0)
        
        print(f"\n📊 ANALYSE: {post['id']}")
        print(f"   Engagement Rate: {engagement}%")
        print(f"   Reach: {m.get('reach', 0):,}")
        print(f"   Likes: {m.get('likes', 0):,}")
        
        # Benchmarks für Instagram
        if engagement >= 3:
            print("   🟢 EXCELLENT — Top 10% Performance")
            suggestion = "Scale this format! Mehr davon erstellen."
        elif engagement >= 1.5:
            print("   🟡 GOOD — Durchschnitt übertroffen")
            suggestion = "Teste leichte Variationen (andere Hashtags, Caption-Hook)"
        else:
            print("   🔴 NEEDS IMPROVEMENT — Unterdurchschnittlich")
            suggestion = "Ändere: Erster Slide Hook, Caption ersten 2 Zeilen, Hashtag-Set"
        
        print(f"   💡 Tipp: {suggestion}")
    
    def get_summary(self):
        """Übersicht aller Posts"""
        if not self.data["posts"]:
            print("Noch keine Posts getrackt")
            return
        
        print("\n📈 INSTAGRAM PERFORMANCE ÜBERSICHT")
        print("=" * 60)
        for post in self.data["posts"]:
            m = post.get("metrics", {})
            engagement = m.get("engagement_rate", "N/A")
            status = "✅" if m else "⏳"
            print(f"{status} {post['id']} | {post['type']} | Engagement: {engagement}%")
        print("=" * 60)

# Post-Daten aus dem Launch
tracker = InstagramTracker()

# Post 1: Launch Carousel (bereits live)
tracker.add_post(
    post_id="DWJoHb5DI-F",
    caption="🚀 ENDLICH LIVE! 🚀 Nach Monaten der Arbeit ist er da...",
    post_type="carousel",
    hashtags=["#schulstress", "#elternratgeber", "#lernmethoden", "#konzentration", "#elternsein"],
    timestamp="2026-03-21T20:30:00"
)

print("\n📝 SO FÜGST DU PERFORMANCE-DATEN HINZU:")
print("1. Öffne Instagram → Profil → Post → 'Weitere Optionen' → 'Insights'")
print("2. Kopiere die Zahlen (Likes, Comments, Shares, Saves, Reach, Impressions)")
print("3. Führe aus:")
print("   python3 instagram_tracker.py")
print("   → Dann update_metrics() mit den Werten aufrufen")

print("\n🔍 AKTUELLER STATUS:")
tracker.get_summary()
