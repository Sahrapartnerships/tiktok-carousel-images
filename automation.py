#!/usr/bin/env python3
"""
Automation Script für regelmäßige Tasks
Wird via Cron ausgeführt
"""

import os
import sys
import json
from datetime import datetime, timedelta
from database import Database, Post, Analytics
from blotato_client import BlotatoClient, CarouselGenerator


def check_scheduled_posts():
    """Prüft und veröffentlicht geplante Posts"""
    db = Database()
    
    # Hole alle scheduled Posts
    posts = db.get_all_posts(status='scheduled')
    
    now = datetime.now()
    for post in posts:
        if post.scheduled_time:
            scheduled = datetime.fromisoformat(post.scheduled_time)
            if scheduled <= now:
                print(f"🚀 Publishing Post #{post.id}")
                # Hier würde der tatsächliche Blotato Call kommen
                db.update_post_status(post.id, 'published')


def fetch_analytics():
    """Holt Analytics von Blotato für alle published Posts"""
    db = Database()
    api_key = os.getenv('BLOTATO_API_KEY')
    
    if not api_key:
        print("❌ BLOTATO_API_KEY nicht gesetzt")
        return
    
    client = BlotatoClient(api_key)
    posts = db.get_all_posts(status='published')
    
    for post in posts:
        if post.blotato_post_id:
            try:
                stats = client.get_post_analytics(post.blotato_post_id)
                
                analytics = Analytics(
                    post_id=post.id,
                    views=stats.get('views', 0),
                    likes=stats.get('likes', 0),
                    comments=stats.get('comments', 0),
                    shares=stats.get('shares', 0),
                    profile_visits=stats.get('profile_visits', 0),
                    link_clicks=stats.get('link_clicks', 0),
                    saved=stats.get('saved', 0)
                )
                db.record_analytics(analytics)
                print(f"✅ Analytics für Post #{post.id} aktualisiert")
            except Exception as e:
                print(f"❌ Fehler bei Post #{post.id}: {e}")


def generate_weekly_content():
    """Generiert Content für die nächste Woche"""
    db = Database()
    generator = CarouselGenerator()
    
    pillars = ['awareness', 'value', 'social_proof', 'conversion']
    
    for pillar in pillars:
        data = generator.generate_carousel_data(pillar)
        
        post = Post(
            content_pillar=data['pillar'],
            hook=data['hook'],
            caption=data['caption'],
            hashtags=json.dumps(data['hashtags']),
            status='draft'
        )
        
        post_id = db.create_post(post)
        print(f"✅ Post #{post_id} generiert: {data['hook'][:50]}...")


def send_daily_report():
    """Sendet täglichen Report (kann an Telegram/Discord gekoppelt werden)"""
    db = Database()
    stats = db.get_dashboard_stats()
    
    report = f"""
📊 Täglicher Report - {datetime.now().strftime('%Y-%m-%d')}

📈 Engagement (30d):
  • Views: {stats['engagement_30d']['views']:,}
  • Likes: {stats['engagement_30d']['likes']:,}
  • Link Clicks: {stats['engagement_30d']['link_clicks']:,}

💰 Revenue (30d): €{stats['revenue_30d']:.2f}

📝 Posts:
  • Total: {stats['posts']['total']}
  • Published: {stats['posts']['published']}
  • Drafts: {stats['posts']['draft']}

🎯 Conversion Rate: {stats['conversion_rate']:.2f}%
    """
    
    print(report)
    
    # Hier könnte Telegram/Discord Integration kommen
    # send_telegram_message(report)


def main():
    """Hauptfunktion - wählt Task basierend auf Argument"""
    
    if len(sys.argv) < 2:
        print("Verwendung: python automation.py [task]")
        print("Tasks: publish, analytics, generate, report")
        sys.exit(1)
    
    task = sys.argv[1]
    
    tasks = {
        'publish': check_scheduled_posts,
        'analytics': fetch_analytics,
        'generate': generate_weekly_content,
        'report': send_daily_report,
    }
    
    if task in tasks:
        print(f"🚀 Starte Task: {task}")
        tasks[task]()
        print(f"✅ Task {task} abgeschlossen")
    else:
        print(f"❌ Unbekannter Task: {task}")
        print(f"Verfügbar: {', '.join(tasks.keys())}")


if __name__ == "__main__":
    main()
