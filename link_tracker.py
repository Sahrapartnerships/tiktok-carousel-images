"""
Link Tracking System für TikTok Marketing
Wichtig: TikTok zeigt keine Link-Clicks in der API an!
Daher tracken wir selbst mit Shortlinks.
"""

import sqlite3
import hashlib
import json
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass
import requests


@dataclass
class TrackedLink:
    """Ein getrackter Link"""
    id: Optional[int] = None
    original_url: str = ""
    short_code: str = ""
    post_id: int = 0  # Referenz zu unserem Post
    utm_source: str = "tiktok"
    utm_medium: str = "social"
    utm_campaign: str = "elternratgeber"
    utm_content: str = ""  # Post ID oder Hook
    clicks: int = 0
    unique_clicks: int = 0
    created_at: str = ""
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.short_code:
            # Generiere kurzen Code aus URL + Timestamp
            data = f"{self.original_url}{datetime.now().timestamp()}"
            self.short_code = hashlib.md5(data.encode()).hexdigest()[:8]


@dataclass
class LinkClick:
    """Ein einzelner Link Click"""
    id: Optional[int] = None
    link_id: int = 0
    ip_address: str = ""
    user_agent: str = ""
    referrer: str = ""
    country: str = ""
    timestamp: str = ""
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()


class LinkTracker:
    """
    Eigener Link Tracker für TikTok Clicks
    Nutzt SQLite für Speicherung
    """
    
    def __init__(self, db_path: str = "elternratgeber.db"):
        self.db_path = db_path
        self.init_tables()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def init_tables(self):
        """Initialisiert Tracking Tabellen"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Links Tabelle
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tracked_links (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    original_url TEXT NOT NULL,
                    short_code TEXT UNIQUE NOT NULL,
                    post_id INTEGER,
                    utm_source TEXT DEFAULT 'tiktok',
                    utm_medium TEXT DEFAULT 'social',
                    utm_campaign TEXT DEFAULT 'elternratgeber',
                    utm_content TEXT,
                    clicks INTEGER DEFAULT 0,
                    unique_clicks INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (post_id) REFERENCES posts (id)
                )
            """)
            
            # Clicks Tabelle
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS link_clicks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    link_id INTEGER NOT NULL,
                    ip_address TEXT,
                    user_agent TEXT,
                    referrer TEXT,
                    country TEXT,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (link_id) REFERENCES tracked_links (id)
                )
            """)
            
            conn.commit()
    
    def create_link(
        self,
        original_url: str,
        post_id: int = None,
        utm_content: str = ""
    ) -> TrackedLink:
        """Erstellt einen neuen getrackten Link"""
        
        # Füge UTM Parameter hinzu falls nicht vorhanden
        if "?" not in original_url:
            original_url += "?"
        elif not original_url.endswith("?"):
            original_url += "&"
        
        original_url += f"utm_source=tiktok&utm_medium=social&utm_campaign=elternratgeber"
        if utm_content:
            original_url += f"&utm_content={utm_content}"
        
        link = TrackedLink(
            original_url=original_url,
            post_id=post_id,
            utm_content=utm_content
        )
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO tracked_links 
                (original_url, short_code, post_id, utm_source, utm_medium, utm_campaign, utm_content)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                link.original_url, link.short_code, link.post_id,
                link.utm_source, link.utm_medium, link.utm_campaign, link.utm_content
            ))
            conn.commit()
            link.id = cursor.lastrowid
        
        return link
    
    def get_short_url(self, short_code: str, base_url: str = "https://dein-domain.com/r") -> str:
        """Gibt die kurze URL zurück"""
        return f"{base_url}/{short_code}"
    
    def track_click(self, short_code: str, ip: str = "", user_agent: str = "", referrer: str = ""):
        """Tracked einen Click (wird vom Redirect-Server aufgerufen)"""
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Link finden
            cursor.execute(
                "SELECT id FROM tracked_links WHERE short_code = ?",
                (short_code,)
            )
            row = cursor.fetchone()
            
            if not row:
                return None
            
            link_id = row[0]
            
            # Click speichern
            cursor.execute("""
                INSERT INTO link_clicks (link_id, ip_address, user_agent, referrer)
                VALUES (?, ?, ?, ?)
            """, (link_id, ip, user_agent, referrer))
            
            # Click Counter erhöhen
            cursor.execute(
                "UPDATE tracked_links SET clicks = clicks + 1 WHERE id = ?",
                (link_id,)
            )
            
            conn.commit()
            return link_id
    
    def get_link_stats(self, link_id: int) -> Dict:
        """Holt Stats für einen Link"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    l.*,
                    COUNT(DISTINCT c.ip_address) as unique_clicks,
                    COUNT(c.id) as total_clicks
                FROM tracked_links l
                LEFT JOIN link_clicks c ON l.id = c.link_id
                WHERE l.id = ?
                GROUP BY l.id
            """, (link_id,))
            
            row = cursor.fetchone()
            if not row:
                return {}
            
            return {
                "id": row[0],
                "original_url": row[1],
                "short_code": row[2],
                "post_id": row[3],
                "utm_content": row[7],
                "clicks": row[8],
                "unique_clicks": row[9],
                "created_at": row[10]
            }
    
    def get_all_links(self, post_id: int = None) -> List[TrackedLink]:
        """Holt alle Links (optional gefiltert nach Post)"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            if post_id:
                cursor.execute(
                    "SELECT * FROM tracked_links WHERE post_id = ? ORDER BY created_at DESC",
                    (post_id,)
                )
            else:
                cursor.execute("SELECT * FROM tracked_links ORDER BY created_at DESC")
            
            rows = cursor.fetchall()
            return [TrackedLink(*row) for row in rows]
    
    def get_ctr_by_post(self, post_id: int, views: int = 0) -> float:
        """Berechnet CTR für einen Post"""
        stats = self.get_link_stats_for_post(post_id)
        if views > 0 and stats.get("clicks", 0) > 0:
            return (stats["clicks"] / views) * 100
        return 0.0
    
    def get_link_stats_for_post(self, post_id: int) -> Dict:
        """Aggregierte Stats für alle Links eines Posts"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    COALESCE(SUM(clicks), 0),
                    COALESCE(SUM(unique_clicks), 0),
                    COUNT(id)
                FROM tracked_links
                WHERE post_id = ?
            """, (post_id,))
            
            total_clicks, unique_clicks, link_count = cursor.fetchone()
            
            return {
                "post_id": post_id,
                "total_clicks": total_clicks,
                "unique_clicks": unique_clicks,
                "link_count": link_count
            }
    
    def get_daily_clicks(self, days: int = 30) -> List[Dict]:
        """Tägliche Click-Statistik"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute(f"""
                SELECT 
                    DATE(timestamp) as date,
                    COUNT(*) as clicks
                FROM link_clicks
                WHERE timestamp > datetime('now', '-{days} days')
                GROUP BY DATE(timestamp)
                ORDER BY date ASC
            """)
            
            return [
                {"date": row[0], "clicks": row[1]}
                for row in cursor.fetchall()
            ]


class BitlyIntegration:
    """
    Optional: Bitly Integration für professionelle Shortlinks
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api-ssl.bitly.com/v4"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def shorten_url(self, long_url: str, domain: str = "bit.ly") -> Optional[str]:
        """Erstellt Bitly Shortlink"""
        try:
            response = requests.post(
                f"{self.base_url}/shorten",
                headers=self.headers,
                json={"long_url": long_url, "domain": domain}
            )
            response.raise_for_status()
            data = response.json()
            return data.get("link")
        except requests.exceptions.RequestException as e:
            print(f"Bitly Error: {e}")
            return None
    
    def get_clicks(self, bitlink: str) -> int:
        """Holt Clicks für einen Bitly Link"""
        # Entferne https://
        bitlink_id = bitlink.replace("https://", "").replace("http://", "")
        
        try:
            response = requests.get(
                f"{self.base_url}/bitlinks/{bitlink_id}/clicks/summary",
                headers=self.headers
            )
            response.raise_for_status()
            data = response.json()
            return data.get("total_clicks", 0)
        except requests.exceptions.RequestException as e:
            print(f"Bitly Error: {e}")
            return 0


if __name__ == "__main__":
    # Test
    tracker = LinkTracker()
    
    # Link erstellen
    link = tracker.create_link(
        original_url="https://elternratgeber-deploy.vercel.app/",
        post_id=1,
        utm_content="carousel_hook_001"
    )
    
    print(f"🔗 Short Code: {link.short_code}")
    print(f"🔗 Short URL: {tracker.get_short_url(link.short_code)}")
    print(f"🔗 Original: {link.original_url}")
