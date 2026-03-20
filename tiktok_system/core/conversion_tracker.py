#!/usr/bin/env python3
"""
Conversion Tracker - Tracking von Link-Klicks bis Verkauf
Integration mit Stripe + Landing Page
"""

import os
import sqlite3
import logging
import json
from datetime import datetime
from typing import Dict, Optional
from dataclasses import dataclass, asdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('ConversionTracker')

DB_PATH = 'tiktok_system/content_db.sqlite'

@dataclass
class ConversionEvent:
    """Ein Tracking-Event"""
    event_id: str
    event_type: str  # click, page_view, add_to_cart, purchase
    request_id: Optional[str]  # Verknüpfung mit GUIDE Request
    post_id: Optional[str]
    source: str  # tiktok, organic, email
    timestamp: str
    metadata: Dict  # UTM, Device, etc.
    value: float = 0.0  # Für purchases

class ConversionTracker:
    """End-to-End Conversion Tracking"""
    
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversion_events (
                event_id TEXT PRIMARY KEY,
                event_type TEXT,
                request_id TEXT,
                post_id TEXT,
                source TEXT,
                timestamp TIMESTAMP,
                metadata TEXT,
                value REAL DEFAULT 0,
                FOREIGN KEY (request_id) REFERENCES guide_requests(id)
            )
        ''')
        
        # Tägliche Aggregierung für schnelle Reports
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_stats (
                date TEXT PRIMARY KEY,
                post_id TEXT,
                impressions INTEGER DEFAULT 0,
                clicks INTEGER DEFAULT 0,
                guide_requests INTEGER DEFAULT 0,
                link_clicks INTEGER DEFAULT 0,
                add_to_carts INTEGER DEFAULT 0,
                purchases INTEGER DEFAULT 0,
                revenue REAL DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def track_event(self, event: ConversionEvent):
        """Tracke ein Event"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO conversion_events
            (event_id, event_type, request_id, post_id, source, timestamp, metadata, value)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            event.event_id, event.event_type, event.request_id,
            event.post_id, event.source, event.timestamp,
            json.dumps(event.metadata), event.value
        ))
        
        conn.commit()
        conn.close()
        
        logger.info(f"📊 Event: {event.event_type} | Source: {event.source} | Value: €{event.value}")
    
    def track_link_click(self, request_id: str, post_id: str, utm_data: Dict):
        """Track wenn User auf GUIDE Link klickt"""
        event = ConversionEvent(
            event_id=f"click_{request_id}_{int(datetime.now().timestamp())}",
            event_type='link_click',
            request_id=request_id,
            post_id=post_id,
            source='tiktok',
            timestamp=datetime.now().isoformat(),
            metadata=utm_data
        )
        self.track_event(event)
        
        # Update request in comment_tracker
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('UPDATE guide_requests SET clicked = 1 WHERE id = ?', (request_id,))
        conn.commit()
        conn.close()
    
    def track_purchase(self, request_id: str, amount: float, post_id: Optional[str] = None):
        """Track Verkauf von Stripe Webhook"""
        event = ConversionEvent(
            event_id=f"purchase_{request_id}_{int(datetime.now().timestamp())}",
            event_type='purchase',
            request_id=request_id,
            post_id=post_id,
            source='tiktok',
            timestamp=datetime.now().isoformat(),
            metadata={'amount': amount, 'currency': 'EUR'},
            value=amount
        )
        self.track_event(event)
        
        # Update guide_requests
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE guide_requests 
            SET converted = 1, revenue = ? 
            WHERE id = ?
        ''', (amount, request_id))
        conn.commit()
        conn.close()
        
        logger.info(f"💰 VERKAUF! €{amount} | Request: {request_id}")
    
    def get_funnel_stats(self, post_id: Optional[str] = None, days: int = 30) -> Dict:
        """Funnel-Statistiken für Dashboard"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        since = datetime.now().timestamp() - (days * 86400)
        
        if post_id:
            cursor.execute('''
                SELECT 
                    event_type,
                    COUNT(*) as count,
                    SUM(value) as total_value
                FROM conversion_events
                WHERE post_id = ? AND datetime(timestamp) > datetime(?, 'unixepoch')
                GROUP BY event_type
            ''', (post_id, since))
        else:
            cursor.execute('''
                SELECT 
                    event_type,
                    COUNT(*) as count,
                    SUM(value) as total_value
                FROM conversion_events
                WHERE datetime(timestamp) > datetime(?, 'unixepoch')
                GROUP BY event_type
            ''', (since,))
        
        results = cursor.fetchall()
        conn.close()
        
        stats = {
            'link_clicks': 0,
            'page_views': 0,
            'add_to_carts': 0,
            'purchases': 0,
            'revenue': 0
        }
        
        for row in results:
            event_type, count, value = row
            if event_type == 'link_click':
                stats['link_clicks'] = count
            elif event_type == 'page_view':
                stats['page_views'] = count
            elif event_type == 'add_to_cart':
                stats['add_to_carts'] = count
            elif event_type == 'purchase':
                stats['purchases'] = count
                stats['revenue'] = value or 0
        
        # Berechne Conversion Rates
        if stats['link_clicks'] > 0:
            stats['cart_rate'] = (stats['add_to_carts'] / stats['link_clicks']) * 100
            stats['purchase_rate'] = (stats['purchases'] / stats['link_clicks']) * 100
        else:
            stats['cart_rate'] = 0
            stats['purchase_rate'] = 0
        
        return stats
    
    def get_post_performance(self) -> list:
        """Performance pro Post für Optimierung"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                c.id,
                c.hook,
                c.theme,
                c.views,
                c.likes,
                c.comments,
                COUNT(gr.id) as guide_requests,
                SUM(gr.clicked) as link_clicks,
                SUM(gr.converted) as conversions,
                SUM(gr.revenue) as revenue
            FROM carousels c
            LEFT JOIN guide_requests gr ON c.id = gr.post_id
            WHERE c.status = 'posted'
            GROUP BY c.id
            ORDER BY revenue DESC
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        return [{
            'post_id': r[0],
            'hook': r[1],
            'theme': r[2],
            'views': r[3] or 0,
            'likes': r[4] or 0,
            'comments': r[5] or 0,
            'guide_requests': r[6] or 0,
            'link_clicks': r[7] or 0,
            'conversions': r[8] or 0,
            'revenue': r[9] or 0
        } for r in results]

# Webhook Handler für Stripe
class StripeWebhookHandler:
    """Verarbeitet Stripe Webhooks für Conversion Tracking"""
    
    def __init__(self, tracker: ConversionTracker):
        self.tracker = tracker
    
    def handle_checkout_complete(self, event_data: Dict):
        """Verarbeite successful payment"""
        # Extrahiere Referrer aus metadata
        metadata = event_data.get('metadata', {})
        request_id = metadata.get('tiktok_request_id')
        post_id = metadata.get('tiktok_post_id')
        
        amount = event_data.get('amount_total', 0) / 100  # Cent zu Euro
        
        if request_id:
            self.tracker.track_purchase(request_id, amount, post_id)
            return True
        
        return False

if __name__ == '__main__':
    # Test
    tracker = ConversionTracker()
    
    # Simuliere Events
    tracker.track_link_click(
        request_id='test_001',
        post_id='awareness_w1_A',
        utm_data={'utm_source': 'tiktok', 'utm_campaign': 'w1'}
    )
    
    tracker.track_purchase('test_001', 19.0, 'awareness_w1_A')
    
    # Stats
    stats = tracker.get_funnel_stats()
    print(f"\n📊 Funnel: {stats}")
