import sqlite3
import json
from datetime import datetime
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, asdict


@dataclass
class Post:
    """Repräsentiert einen TikTok Post"""
    id: Optional[int] = None
    blotato_post_id: Optional[str] = None
    platform: str = "tiktok"
    content_pillar: str = ""
    hook: str = ""
    caption: str = ""
    hashtags: str = ""
    image_paths: str = ""  # JSON list
    status: str = "draft"  # draft, scheduled, published, failed
    scheduled_time: Optional[str] = None
    published_time: Optional[str] = None
    created_at: str = ""
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()


@dataclass
class Analytics:
    """Analytics Daten für einen Post"""
    id: Optional[int] = None
    post_id: int = 0
    views: int = 0
    likes: int = 0
    comments: int = 0
    shares: int = 0
    profile_visits: int = 0
    link_clicks: int = 0  # Wichtig für Conversion!
    saved: int = 0
    recorded_at: str = ""
    
    def __post_init__(self):
        if not self.recorded_at:
            self.recorded_at = datetime.now().isoformat()


@dataclass
class Conversion:
    """Verkaufs/Conversion Tracking"""
    id: Optional[int] = None
    source: str = ""  # z.B. "tiktok_carousel_123"
    utm_campaign: str = ""
    utm_content: str = ""  # Post ID oder Hook
    revenue: float = 0.0
    product: str = "elternratgeber"
    timestamp: str = ""
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()


class Database:
    """SQLite Database für alle Daten"""
    
    def __init__(self, db_path: str = "elternratgeber.db"):
        self.db_path = db_path
        self.init_db()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def init_db(self):
        """Initialisiert alle Tabellen"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Posts Tabelle
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    blotato_post_id TEXT,
                    platform TEXT DEFAULT 'tiktok',
                    content_pillar TEXT,
                    hook TEXT,
                    caption TEXT,
                    hashtags TEXT,
                    image_paths TEXT,
                    status TEXT DEFAULT 'draft',
                    scheduled_time TEXT,
                    published_time TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Analytics Tabelle
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS analytics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    post_id INTEGER,
                    views INTEGER DEFAULT 0,
                    likes INTEGER DEFAULT 0,
                    comments INTEGER DEFAULT 0,
                    shares INTEGER DEFAULT 0,
                    profile_visits INTEGER DEFAULT 0,
                    link_clicks INTEGER DEFAULT 0,
                    saved INTEGER DEFAULT 0,
                    recorded_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (post_id) REFERENCES posts (id)
                )
            """)
            
            # Conversions Tabelle
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source TEXT,
                    utm_campaign TEXT,
                    utm_content TEXT,
                    revenue REAL DEFAULT 0,
                    product TEXT DEFAULT 'elternratgeber',
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Settings Tabelle
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
    
    # Posts CRUD
    def create_post(self, post: Post) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO posts 
                (blotato_post_id, platform, content_pillar, hook, caption, 
                 hashtags, image_paths, status, scheduled_time, published_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                post.blotato_post_id, post.platform, post.content_pillar,
                post.hook, post.caption, post.hashtags, post.image_paths,
                post.status, post.scheduled_time, post.published_time
            ))
            conn.commit()
            return cursor.lastrowid
    
    def get_post(self, post_id: int) -> Optional[Post]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
            row = cursor.fetchone()
            if row:
                return Post(*row)
            return None
    
    def get_all_posts(self, status: Optional[str] = None) -> List[Post]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if status:
                cursor.execute("SELECT * FROM posts WHERE status = ? ORDER BY created_at DESC", (status,))
            else:
                cursor.execute("SELECT * FROM posts ORDER BY created_at DESC")
            rows = cursor.fetchall()
            return [Post(*row) for row in rows]
    
    def update_post_status(self, post_id: int, status: str):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if status == "published":
                cursor.execute(
                    "UPDATE posts SET status = ?, published_time = ? WHERE id = ?",
                    (status, datetime.now().isoformat(), post_id)
                )
            else:
                cursor.execute(
                    "UPDATE posts SET status = ? WHERE id = ?",
                    (status, post_id)
                )
            conn.commit()
    
    # Analytics
    def record_analytics(self, analytics: Analytics):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO analytics 
                (post_id, views, likes, comments, shares, profile_visits, link_clicks, saved)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                analytics.post_id, analytics.views, analytics.likes,
                analytics.comments, analytics.shares, analytics.profile_visits,
                analytics.link_clicks, analytics.saved
            ))
            conn.commit()
    
    def get_latest_analytics(self, post_id: int) -> Optional[Analytics]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM analytics 
                WHERE post_id = ? 
                ORDER BY recorded_at DESC 
                LIMIT 1
            """, (post_id,))
            row = cursor.fetchone()
            if row:
                return Analytics(*row)
            return None
    
    def get_analytics_history(self, post_id: int, days: int = 30) -> List[Analytics]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM analytics 
                WHERE post_id = ? 
                AND recorded_at > datetime('now', '-{} days')
                ORDER BY recorded_at ASC
            """.format(days))
            rows = cursor.fetchall()
            return [Analytics(*row) for row in rows]
    
    # Conversions
    def record_conversion(self, conversion: Conversion):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO conversions (source, utm_campaign, utm_content, revenue, product)
                VALUES (?, ?, ?, ?, ?)
            """, (
                conversion.source, conversion.utm_campaign,
                conversion.utm_content, conversion.revenue, conversion.product
            ))
            conn.commit()
    
    def get_conversions(self, days: int = 30) -> List[Conversion]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM conversions 
                WHERE timestamp > datetime('now', '-{} days')
                ORDER BY timestamp DESC
            """.format(days))
            rows = cursor.fetchall()
            return [Conversion(*row) for row in rows]
    
    def get_total_revenue(self, days: int = 30) -> float:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COALESCE(SUM(revenue), 0) FROM conversions 
                WHERE timestamp > datetime('now', '-{} days')
            """.format(days))
            return cursor.fetchone()[0]
    
    # Dashboard Stats
    def get_dashboard_stats(self) -> Dict[str, Any]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Post Stats
            cursor.execute("SELECT COUNT(*) FROM posts")
            total_posts = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM posts WHERE status = 'published'")
            published_posts = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM posts WHERE status = 'draft'")
            draft_posts = cursor.fetchone()[0]
            
            # Analytics Summen
            cursor.execute("""
                SELECT 
                    COALESCE(SUM(views), 0),
                    COALESCE(SUM(likes), 0),
                    COALESCE(SUM(comments), 0),
                    COALESCE(SUM(shares), 0),
                    COALESCE(SUM(link_clicks), 0)
                FROM analytics
                WHERE recorded_at > datetime('now', '-30 days')
            """)
            views, likes, comments, shares, clicks = cursor.fetchone()
            
            # Revenue
            revenue = self.get_total_revenue(30)
            
            return {
                "posts": {
                    "total": total_posts,
                    "published": published_posts,
                    "draft": draft_posts
                },
                "engagement_30d": {
                    "views": views,
                    "likes": likes,
                    "comments": comments,
                    "shares": shares,
                    "link_clicks": clicks
                },
                "revenue_30d": revenue,
                "conversion_rate": (clicks / views * 100) if views > 0 else 0
            }


if __name__ == "__main__":
    # Test
    db = Database()
    stats = db.get_dashboard_stats()
    print(json.dumps(stats, indent=2))
