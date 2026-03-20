#!/usr/bin/env python3
"""
Comment Tracker - Überwacht "GUIDE" Kommentare auf TikTok
Sendet automatisch Links + Trackt Konversionen
"""

import os
import sqlite3
import logging
import re
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('CommentTracker')

DB_PATH = 'tiktok_system/content_db.sqlite'

@dataclass
class GuideRequest:
    """Ein GUIDE Kommentar"""
    id: str
    post_id: str
    username: str
    comment_text: str
    detected_at: str
    link_sent: bool = False
    link_sent_at: Optional[str] = None
    clicked: bool = False
    converted: bool = False

class CommentTracker:
    """Trackt und verwaltet GUIDE Kommentare"""
    
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS guide_requests (
                id TEXT PRIMARY KEY,
                post_id TEXT,
                username TEXT,
                comment_text TEXT,
                detected_at TIMESTAMP,
                link_sent BOOLEAN DEFAULT 0,
                link_sent_at TIMESTAMP,
                clicked BOOLEAN DEFAULT 0,
                converted BOOLEAN DEFAULT 0,
                revenue REAL DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def detect_guide_comments(self, comments: List[Dict], post_id: str) -> List[GuideRequest]:
        """Erkenne GUIDE Kommentare aus TikTok API Response"""
        
        guide_pattern = re.compile(r'\bguide\b', re.IGNORECASE)
        requests = []
        
        for comment in comments:
            text = comment.get('text', '')
            
            if guide_pattern.search(text):
                request = GuideRequest(
                    id=f"{post_id}_{comment['username']}_{int(datetime.now().timestamp())}",
                    post_id=post_id,
                    username=comment['username'],
                    comment_text=text,
                    detected_at=datetime.now().isoformat()
                )
                requests.append(request)
                self._save_request(request)
                logger.info(f"🎯 GUIDE erkannt von @{request.username} auf {post_id}")
        
        return requests
    
    def _save_request(self, request: GuideRequest):
        """Speichere Request in DB"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR IGNORE INTO guide_requests 
            (id, post_id, username, comment_text, detected_at, link_sent, clicked, converted)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (request.id, request.post_id, request.username, request.comment_text,
              request.detected_at, request.link_sent, request.clicked, request.converted))
        
        conn.commit()
        conn.close()
    
    def send_link(self, request_id: str, link: str) -> bool:
        """Markiere Link als gesendet (würde TikTok DM/Reply API nutzen)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        sent_at = datetime.now().isoformat()
        
        cursor.execute('''
            UPDATE guide_requests 
            SET link_sent = 1, link_sent_at = ?
            WHERE id = ?
        ''', (sent_at, request_id))
        
        conn.commit()
        conn.close()
        
        logger.info(f"✅ Link gesendet für {request_id}")
        return True
    
    def track_click(self, request_id: str):
        """Track wenn User auf Link klickt"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE guide_requests SET clicked = 1 WHERE id = ?
        ''', (request_id,))
        
        conn.commit()
        conn.close()
    
    def track_conversion(self, request_id: str, revenue: float = 19.0):
        """Track wenn User kauft"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE guide_requests SET converted = 1, revenue = ? WHERE id = ?
        ''', (revenue, request_id))
        
        conn.commit()
        conn.close()
        
        logger.info(f"💰 Conversion! {request_id} - €{revenue}")
    
    def get_stats(self, post_id: Optional[str] = None) -> Dict:
        """Statistiken für Dashboard"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if post_id:
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_requests,
                    SUM(link_sent) as links_sent,
                    SUM(clicked) as clicks,
                    SUM(converted) as conversions,
                    SUM(revenue) as total_revenue
                FROM guide_requests
                WHERE post_id = ?
            ''', (post_id,))
        else:
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_requests,
                    SUM(link_sent) as links_sent,
                    SUM(clicked) as clicks,
                    SUM(converted) as conversions,
                    SUM(revenue) as total_revenue
                FROM guide_requests
            ''')
        
        row = cursor.fetchone()
        conn.close()
        
        total = row[0] or 0
        sent = row[1] or 0
        clicks = row[2] or 0
        conversions = row[3] or 0
        revenue = row[4] or 0
        
        return {
            'total_requests': total,
            'links_sent': sent,
            'clicks': clicks,
            'conversions': conversions,
            'revenue': revenue,
            'click_rate': (clicks / sent * 100) if sent > 0 else 0,
            'conversion_rate': (conversions / clicks * 100) if clicks > 0 else 0
        }

# Auto-Reply Bot (Simuliert bis TikTok API verfügbar)
class AutoReplyBot:
    """Automatische Antworten auf GUIDE Kommentare"""
    
    def __init__(self, tracker: CommentTracker):
        self.tracker = tracker
        self.reply_templates = [
            "Danke für dein Interesse! 💙 Ich habe dir den Link zur Landing Page geschickt. Check deine DMs!",
            "Gerne! 📚 Der Guide ist auf dem Weg zu dir - schau in deine Direktnachrichten!",
            "Super! 💪 Hier ist dein Zugang: [LINK] - Viel Erfolg beim Umsetzen!"
        ]
    
    def process_new_comments(self, post_id: str, comments: List[Dict]):
        """Verarbeite neue Kommentare"""
        requests = self.tracker.detect_guide_comments(comments, post_id)
        
        for request in requests:
            # Generiere personalisierter Link
            personalized_link = f"https://elternratgeber.vercel.app/?ref={request.id}"
            
            # Sende Reply (simuliert)
            reply_text = f"@{request.username} {self.reply_templates[0]}"
            logger.info(f"🤖 Würde antworten: {reply_text[:80]}...")
            
            # Markiere als gesendet
            self.tracker.send_link(request.id, personalized_link)

if __name__ == '__main__':
    # Test
    tracker = CommentTracker()
    
    # Simuliere Kommentare
    test_comments = [
        {'username': 'mama123', 'text': 'Ich brauche den Guide bitte!'},
        {'username': 'peter_m', 'text': 'GUIDE'},
        {'username': 'susanne', 'text': 'Super Content! GUIDE bitte 🙏'}
    ]
    
    bot = AutoReplyBot(tracker)
    bot.process_new_comments('test_post_001', test_comments)
    
    # Stats
    stats = tracker.get_stats()
    print(f"\n📊 Stats: {stats}")
