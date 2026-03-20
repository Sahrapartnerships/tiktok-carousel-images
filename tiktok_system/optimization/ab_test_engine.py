#!/usr/bin/env python3
"""
A/B Testing Engine für TikTok Karussells
Automatische Optimierung basierend auf Performance
"""

import os
import sqlite3
import logging
import random
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('ABTestEngine')

DB_PATH = 'tiktok_system/content_db.sqlite'

@dataclass
class ABTest:
    """A/B Test Definition"""
    test_id: str
    post_id: str
    element: str  # hook, cta, image_style
    variant_a: str
    variant_b: str
    traffic_split: float = 0.5  # 50/50
    status: str = 'running'  # running, completed, winner_a, winner_b
    start_date: str = None
    end_date: Optional[str] = None
    
    def __post_init__(self):
        if not self.start_date:
            self.start_date = datetime.now().isoformat()

class ABTestEngine:
    """Automatische A/B Test Verwaltung"""
    
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self.init_db()
        self.confidence_threshold = 0.95  # 95% confidence
        self.min_sample_size = 100  # Mindestens 100 pro Variante
    
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ab_tests (
                test_id TEXT PRIMARY KEY,
                post_id TEXT,
                element TEXT,
                variant_a TEXT,
                variant_b TEXT,
                traffic_split REAL,
                status TEXT,
                start_date TIMESTAMP,
                end_date TIMESTAMP,
                winner TEXT,
                confidence_level REAL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ab_test_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                test_id TEXT,
                variant TEXT,  # A oder B
                impressions INTEGER DEFAULT 0,
                clicks INTEGER DEFAULT 0,
                conversions INTEGER DEFAULT 0,
                revenue REAL DEFAULT 0,
                recorded_date DATE
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_test(self, post_id: str, element: str, variant_a: str, variant_b: str) -> ABTest:
        """Erstelle neuen A/B Test"""
        test_id = f"ab_{post_id}_{element}_{datetime.now().strftime('%Y%m%d')}"
        
        test = ABTest(
            test_id=test_id,
            post_id=post_id,
            element=element,
            variant_a=variant_a,
            variant_b=variant_b
        )
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO ab_tests 
            (test_id, post_id, element, variant_a, variant_b, traffic_split, status, start_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (test.test_id, test.post_id, test.element, test.variant_a, 
              test.variant_b, test.traffic_split, test.status, test.start_date))
        
        conn.commit()
        conn.close()
        
        logger.info(f"🧪 A/B Test erstellt: {test_id} | Element: {element}")
        return test
    
    def assign_variant(self, test_id: str, user_id: str) -> str:
        """Weise User zu Variante zu (consistent hashing)"""
        # Nutze user_id für konsistente Zuweisung
        hash_val = hash(f"{test_id}_{user_id}")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT traffic_split FROM ab_tests WHERE test_id = ?', (test_id,))
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            return 'A'
        
        split = result[0]
        
        # 50/50 Split (oder wie definiert)
        if (hash_val % 100) < (split * 100):
            return 'A'
        return 'B'
    
    def record_result(self, test_id: str, variant: str, metric: str, value: int = 1):
        """Tracke Ergebnis für Variante"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        today = datetime.now().date().isoformat()
        
        # Update oder Insert
        cursor.execute('''
            INSERT INTO ab_test_results (test_id, variant, recorded_date, {0})
            VALUES (?, ?, ?, ?)
            ON CONFLICT DO UPDATE SET {0} = {0} + ?
            WHERE test_id = ? AND variant = ? AND recorded_date = ?
        '''.format(metric), (test_id, variant, today, value, value, test_id, variant, today))
        
        conn.commit()
        conn.close()
    
    def get_test_results(self, test_id: str) -> Dict:
        """Aggregiere Test-Ergebnisse"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                variant,
                SUM(impressions) as total_impressions,
                SUM(clicks) as total_clicks,
                SUM(conversions) as total_conversions,
                SUM(revenue) as total_revenue
            FROM ab_test_results
            WHERE test_id = ?
            GROUP BY variant
        ''', (test_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        data = {}
        for row in results:
            variant = row[0]
            data[variant] = {
                'impressions': row[1] or 0,
                'clicks': row[2] or 0,
                'conversions': row[3] or 0,
                'revenue': row[4] or 0,
                'ctr': (row[2] / row[1] * 100) if row[1] else 0,
                'conv_rate': (row[3] / row[2] * 100) if row[2] else 0
            }
        
        return data
    
    def check_significance(self, test_id: str) -> Optional[str]:
        """Prüfe ob Test signifikant ist"""
        results = self.get_test_results(test_id)
        
        if 'A' not in results or 'B' not in results:
            return None
        
        a = results['A']
        b = results['B']
        
        # Mindest-Sample-Size
        if a['impressions'] < self.min_sample_size or b['impressions'] < self.min_sample_size:
            return None
        
        # Einfache Signifikanz-Prüfung (z-Test Approximation)
        # Für Conversion Rate
        if a['clicks'] > 0 and b['clicks'] > 0:
            p1 = a['conversions'] / a['clicks']
            p2 = b['conversions'] / b['clicks']
            n1 = a['clicks']
            n2 = b['clicks']
            
            # Pooled probability
            p_pooled = (a['conversions'] + b['conversions']) / (n1 + n2)
            
            # Standard error
            se = (p_pooled * (1 - p_pooled) * (1/n1 + 1/n2)) ** 0.5
            
            if se > 0:
                z_score = abs(p1 - p2) / se
                
                # Z-Score für 95% confidence ≈ 1.96
                if z_score > 1.96:
                    winner = 'A' if p1 > p2 else 'B'
                    self._end_test(test_id, winner, z_score)
                    return winner
        
        return None
    
    def _end_test(self, test_id: str, winner: str, confidence: float):
        """Beende Test mit Gewinner"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        end_date = datetime.now().isoformat()
        status = f'winner_{winner.lower()}'
        
        cursor.execute('''
            UPDATE ab_tests 
            SET status = ?, end_date = ?, winner = ?, confidence_level = ?
            WHERE test_id = ?
        ''', (status, end_date, winner, confidence, test_id))
        
        conn.commit()
        conn.close()
        
        logger.info(f"🏆 Test beendet: {test_id} | Gewinner: {winner} | Confidence: {confidence:.2f}")
    
    def get_active_tests(self) -> List[ABTest]:
        """Liste aktive Tests"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT test_id, post_id, element, variant_a, variant_b, 
                   traffic_split, status, start_date, end_date
            FROM ab_tests
            WHERE status = 'running'
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        return [ABTest(*row) for row in rows]
    
    def suggest_tests(self, post_id: str) -> List[Dict]:
        """Schlage A/B Tests vor basierend auf Post-Typ"""
        suggestions = [
            {
                'element': 'hook',
                'variant_a': 'Dein Kind zeigt diese 5 Zeichen? 🚨',
                'variant_b': '73% der Eltern übersehen diese Warnsignale...',
                'reason': 'Frage vs. Statistik - Teste welcher Hook mehr Aufmerksamkeit erzeugt'
            },
            {
                'element': 'cta',
                'variant_a': 'Kommentiere "GUIDE"',
                'variant_b': 'Schreib "JA" für den kostenlosen Guide',
                'reason': 'Verschiedene CTA-Formulierungen testen'
            },
            {
                'element': 'slide_count',
                'variant_a': '5 Slides',
                'variant_b': '7 Slides',
                'reason': 'Optimale Länge für Completion Rate'
            }
        ]
        
        return suggestions

# Auto-Optimizer
class AutoOptimizer:
    """Automatische Optimierung basierend auf Performance"""
    
    def __init__(self, engine: ABTestEngine):
        self.engine = engine
    
    def analyze_and_optimize(self):
        """Analysiere alle laufenden Tests und Posts"""
        # 1. Prüfe aktive Tests auf Signifikanz
        active_tests = self.engine.get_active_tests()
        
        for test in active_tests:
            winner = self.engine.check_significance(test.test_id)
            if winner:
                logger.info(f"✅ Signifikanter Gewinner gefunden: {test.element} = {winner}")
        
        # 2. Suggestiere neue Tests für unterperformende Posts
        # (würde aus DB geladen werden)
        
        return True
    
    def generate_optimized_version(self, post_id: str, winning_elements: Dict) -> Dict:
        """Generiere neue Version mit Gewinner-Elementen"""
        optimized = {
            'post_id': f"{post_id}_v2",
            'hook': winning_elements.get('hook', 'Original'),
            'cta': winning_elements.get('cta', 'Original'),
            'improvements': list(winning_elements.keys())
        }
        
        return optimized

if __name__ == '__main__':
    # Test
    engine = ABTestEngine()
    
    # Erstelle Test
    test = engine.create_test(
        post_id='awareness_w1',
        element='hook',
        variant_a='Dein Kind zeigt diese 5 Zeichen?',
        variant_b='73% der Eltern übersehen das...'
    )
    
    # Simuliere Ergebnisse
    for i in range(150):
        variant = engine.assign_variant(test.test_id, f'user_{i}')
        engine.record_result(test.test_id, variant, 'impressions')
        
        # Simuliere unterschiedliche Conversion Rates
        if variant == 'A':
            if random.random() < 0.05:  # 5% CTR
                engine.record_result(test.test_id, variant, 'clicks')
        else:
            if random.random() < 0.08:  # 8% CTR (besser)
                engine.record_result(test.test_id, variant, 'clicks')
    
    # Prüfe Signifikanz
    winner = engine.check_significance(test.test_id)
    print(f"\n🏆 Gewinner: {winner}")
    print(f"Ergebnisse: {engine.get_test_results(test.test_id)}")
