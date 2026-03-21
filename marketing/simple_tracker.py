#!/usr/bin/env python3
"""
Instagram Performance Tracker - Zero-Tool Solution
Nutzt nur manuelle Datenerfassung und einfache Python-Analyse
Keine externen APIs, keine kostenpflichtigen Tools
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

class SimpleInstagramTracker:
    """
    Manuelles Tracking-System für Instagram-Performance
    
    VERWENDUNG:
    1. Post auf Instagram veröffentlichen
    2. Nach 24h/48h/7 Tage in Instagram App öffnen
    3. Insights checken (Likes, Comments, Saves, Shares, Reach, Impressions)
    4. Daten in tracker_input.txt eintragen
    5. Dieses Script ausführen für Analyse
    """
    
    def __init__(self):
        self.data_file = Path("/root/life/elternratgeber-system/marketing/instagram_data.json")
        self.input_file = Path("/root/life/elternratgeber-system/marketing/tracker_input.txt")
        self.analysis_file = Path("/root/life/elternratgeber-system/marketing/performance_analysis.md")
        self.data = self._load_data()
    
    def _load_data(self):
        if self.data_file.exists():
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "posts": [],
            "summary": {
                "total_posts": 0,
                "avg_engagement_rate": 0,
                "best_performing_post": None,
                "last_updated": None
            }
        }
    
    def _save_data(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def add_post(self, post_id, caption, post_type, hashtags, posted_date):
        """Fügt neuen Post zum Tracking hinzu"""
        post = {
            "id": post_id,
            "caption": caption[:100] + "..." if len(caption) > 100 else caption,
            "type": post_type,  # carousel, single, reel
            "hashtags": hashtags,
            "posted_date": posted_date,
            "metrics": {
                "24h": {},
                "48h": {},
                "7d": {},
                "final": {}
            },
            "engagement_rate": 0,
            "performance_score": 0
        }
        self.data["posts"].append(post)
        self._save_data()
        print(f"✅ Post {post_id} zum Tracking hinzugefügt")
        return post
    
    def update_metrics(self, post_id, metrics, timeframe="final"):
        """
        Aktualisiert Metrics für einen Post
        
        metrics = {
            "likes": 150,
            "comments": 12,
            "saves": 45,
            "shares": 8,
            "reach": 1200,
            "impressions": 2400,
            "profile_visits": 80,
            "follows": 5
        }
        """
        for post in self.data["posts"]:
            if post["id"] == post_id:
                post["metrics"][timeframe] = metrics
                post["metrics"]["last_updated"] = datetime.now().isoformat()
                
                # Engagement Rate berechnen
                if metrics.get("reach", 0) > 0:
                    engagement = (
                        metrics.get("likes", 0) +
                        metrics.get("comments", 0) +
                        metrics.get("saves", 0) +
                        metrics.get("shares", 0)
                    )
                    post["engagement_rate"] = round((engagement / metrics["reach"]) * 100, 2)
                    
                    # Performance Score (0-100)
                    # Gewichtung: Saves (40%), Shares (30%), Comments (20%), Likes (10%)
                    post["performance_score"] = min(100, round(
                        (metrics.get("saves", 0) / max(metrics["reach"], 1) * 100 * 0.4) +
                        (metrics.get("shares", 0) / max(metrics["reach"], 1) * 100 * 0.3) +
                        (metrics.get("comments", 0) / max(metrics["reach"], 1) * 100 * 0.2) +
                        (metrics.get("likes", 0) / max(metrics["reach"], 1) * 100 * 0.1)
                    , 2))
                
                self._save_data()
                print(f"✅ Metrics für {post_id} ({timeframe}) aktualisiert")
                self._show_post_analysis(post)
                return
        
        print(f"❌ Post {post_id} nicht gefunden")
    
    def _show_post_analysis(self, post):
        """Zeigt Analyse für einen einzelnen Post"""
        print(f"\n📊 POST-ANALYSE: {post['id']}")
        print("=" * 50)
        print(f"Type: {post['type']}")
        print(f"Posted: {post['posted_date']}")
        print(f"Engagement Rate: {post['engagement_rate']}%")
        print(f"Performance Score: {post['performance_score']}/100")
        
        # Benchmark-Vergleich
        if post['engagement_rate'] >= 3:
            print("🟢 EXCELLENT — Top 10% Performance")
        elif post['engagement_rate'] >= 1.5:
            print("🟡 GOOD — Über dem Durchschnitt")
        else:
            print("🔴 NEEDS IMPROVEMENT — Unterdurchschnittlich")
        
        print("\n💡 EMPFEHLUNG:")
        self._generate_recommendation(post)
    
    def _generate_recommendation(self, post):
        """Generiert Handlungsempfehlung basierend auf Performance"""
        score = post.get("performance_score", 0)
        saves = post["metrics"].get("final", {}).get("saves", 0)
        comments = post["metrics"].get("final", {}).get("comments", 0)
        
        if score >= 70:
            print("  • Dieses Format funktioniert! Skaliere es.")
            print("  • Ähnliche Themen/Captions für nächste Posts nutzen")
            print("  • Zeitpunkt dokumentieren und wiederholen")
        elif saves > comments * 2:
            print("  • Hohe Save-Rate = Wertvoller Content")
            print("  • Mehr 'Speichern'-CTAs in Captions einbauen")
            print("  • Educational Content erweitern")
        elif comments > 10:
            print("  • Gute Diskussion! Engagement anregt weiteren Reach")
            print("  • Ähnliche Fragen in Captions stellen")
        else:
            print("  • Hook (erster Satz) verbessern")
            print("  • Hashtags testen (verschiedene Sets)")
            print("  • Posting-Zeitpunkt variieren")
    
    def show_dashboard(self):
        """Zeigt Übersicht aller Posts"""
        print("\n" + "=" * 60)
        print("📈 INSTAGRAM PERFORMANCE DASHBOARD")
        print("=" * 60)
        
        if not self.data["posts"]:
            print("\nNoch keine Posts getrackt.")
            print(f"\nFüge Post hinzu mit: tracker.add_post('POST_ID', 'Caption', 'carousel', ['#tag'], '2026-03-22')")
            return
        
        print(f"\nInsgesamt: {len(self.data['posts'])} Posts")
        print("-" * 60)
        
        for post in self.data["posts"]:
            status = "✅" if post["metrics"].get("final") else "⏳"
            engagement = f"{post['engagement_rate']}%" if post["engagement_rate"] else "N/A"
            score = f"{post['performance_score']}/100" if post["performance_score"] else "N/A"
            print(f"{status} {post['id'][:15]:<15} | {post['type']:<10} | {engagement:<8} | Score: {score}")
        
        print("-" * 60)
        
        # Beste Posts
        if len(self.data["posts"]) > 1:
            best = max(self.data["posts"], key=lambda x: x.get("performance_score", 0))
            print(f"\n🏆 Bester Post: {best['id']}")
            print(f"   Score: {best['performance_score']}/100 | Engagement: {best['engagement_rate']}%")
    
    def generate_analysis_report(self):
        """Generiert Markdown-Report mit Analysen"""
        report = []
        report.append("# Instagram Performance Report")
        report.append(f"\nErstellt: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        report.append(f"\n## Übersicht")
        report.append(f"\n- **Gesamt Posts:** {len(self.data['posts'])}")
        
        if self.data["posts"]:
            avg_engagement = sum(p.get("engagement_rate", 0) for p in self.data["posts"]) / len(self.data["posts"])
            report.append(f"- **Durchschn. Engagement:** {avg_engagement:.2f}%")
            
            best = max(self.data["posts"], key=lambda x: x.get("performance_score", 0))
            report.append(f"- **Bester Post:** {best['id']} (Score: {best['performance_score']}/100)")
        
        report.append(f"\n## Post Details")
        report.append("")
        
        for post in self.data["posts"]:
            report.append(f"### {post['id']}")
            report.append(f"- **Type:** {post['type']}")
            report.append(f"- **Posted:** {post['posted_date']}")
            report.append(f"- **Engagement Rate:** {post['engagement_rate']}%")
            report.append(f"- **Performance Score:** {post['performance_score']}/100")
            
            if post["metrics"].get("final"):
                m = post["metrics"]["final"]
                report.append(f"- **Likes:** {m.get('likes', 0)}")
                report.append(f"- **Comments:** {m.get('comments', 0)}")
                report.append(f"- **Saves:** {m.get('saves', 0)}")
                report.append(f"- **Reach:** {m.get('reach', 0)}")
            
            report.append("")
        
        # Save report
        with open(self.analysis_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
        
        print(f"\n✅ Report gespeichert: {self.analysis_file}")
    
    def create_input_template(self):
        """Erstellt Template-Datei für Dateneingabe"""
        template = """# Instagram Performance Tracker - Dateneingabe
# Kopiere die Werte aus Instagram Insights hier ein

POST_ID: DWJoHb5DI-F
TIMEFRAME: final  # Optionen: 24h, 48h, 7d, final

METRICS:
likes: 0
comments: 0
saves: 0
shares: 0
reach: 0
impressions: 0
profile_visits: 0
follows: 0

# So fügst du Daten hinzu:
# 1. Öffne Instagram App → Profil → Post → "Insights"
# 2. Kopiere die Zahlen in die Zeilen oben
# 3. Speichern und Script ausführen: python3 simple_tracker.py
"""
        with open(self.input_file, 'w', encoding='utf-8') as f:
            f.write(template)
        
        print(f"✅ Template erstellt: {self.input_file}")
        print("  Bearbeite diese Datei und führe dann das Script aus")

def main():
    tracker = SimpleInstagramTracker()
    
    print("🚀 Instagram Performance Tracker (Zero-Tools)")
    print("=" * 50)
    
    # Zeige aktuellen Status
    tracker.show_dashboard()
    
    # Post 1 hinzufügen (wenn noch nicht vorhanden)
    post_id = "DWJoHb5DI-F"
    if not any(p["id"] == post_id for p in tracker.data["posts"]):
        tracker.add_post(
            post_id=post_id,
            caption="🚀 ENDLICH LIVE! 🚀 Nach Monaten der Arbeit ist er da...",
            post_type="carousel",
            hashtags=["#schulstress", "#elternratgeber", "#lernmethoden"],
            posted_date="2026-03-21"
        )
    
    # Erstelle Input-Template wenn nicht vorhanden
    if not tracker.input_file.exists():
        tracker.create_input_template()
    
    print("\n" + "=" * 50)
    print("📋 NÄCHSTE SCHRITTE:")
    print("=" * 50)
    print("1. Öffne Instagram → Dein Post → Insights")
    print("2. Bearbeite: marketing/tracker_input.txt")
    print("3. Trage die Zahlen ein")
    print("4. Führe aus: python3 simple_tracker.py")
    print("\nFür Analyse ohne neue Daten:")
    print("  python3 -c \"from simple_tracker import SimpleInstagramTracker; t=SimpleInstagramTracker(); t.generate_analysis_report()\"")

if __name__ == "__main__":
    main()
