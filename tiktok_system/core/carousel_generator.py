#!/usr/bin/env python3
"""
TikTok Carousel Generator für Elternratgeber
Erstellt Karussell-Bilder + Texte für TikTok
Modular für Selbst-Überwachung & -Verbesserung
"""

import os
import json
import sqlite3
import logging
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path

# Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('CarouselGenerator')

# Konstanten
DB_PATH = 'tiktok_system/content_db.sqlite'
TEMPLATE_DIR = 'tiktok_system/templates'
IMAGE_DIR = 'tiktok_system/images'

@dataclass
class CarouselSlide:
    """Einzelne Karussell-Seite"""
    slide_number: int
    headline: str
    body_text: str
    visual_prompt: str  # Für Bildgenerierung
    cta: Optional[str] = None

@dataclass
class CarouselPost:
    """Kompletter Karussell-Post"""
    id: str
    theme: str
    target_week: int
    slides: List[CarouselSlide]
    caption: str
    hashtags: List[str]
    hook: str  # Erster Text-Hook
    guide_link: str
    status: str = 'draft'  # draft, ready, posted, optimized
    performance_score: float = 0.0
    created_at: str = None
    ab_test_variant: str = 'A'  # Für A/B Testing
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()

class CarouselDatabase:
    """Datenbank für Content & Performance"""
    
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS carousels (
                id TEXT PRIMARY KEY,
                theme TEXT,
                target_week INTEGER,
                hook TEXT,
                caption TEXT,
                hashtags TEXT,
                guide_link TEXT,
                status TEXT,
                performance_score REAL,
                created_at TIMESTAMP,
                posted_at TIMESTAMP,
                views INTEGER DEFAULT 0,
                likes INTEGER DEFAULT 0,
                comments INTEGER DEFAULT 0,
                shares INTEGER DEFAULT 0,
                guide_clicks INTEGER DEFAULT 0,
                conversions INTEGER DEFAULT 0,
                ab_test_variant TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS slides (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                carousel_id TEXT,
                slide_number INTEGER,
                headline TEXT,
                body_text TEXT,
                visual_prompt TEXT,
                cta TEXT,
                FOREIGN KEY (carousel_id) REFERENCES carousels(id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                carousel_id TEXT,
                metric_name TEXT,
                metric_value REAL,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_carousel(self, post: CarouselPost):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO carousels 
            (id, theme, target_week, hook, caption, hashtags, guide_link, status, performance_score, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            post.id, post.theme, post.target_week, post.hook, post.caption,
            json.dumps(post.hashtags), post.guide_link, post.status,
            post.performance_score, post.created_at
        ))
        
        for slide in post.slides:
            cursor.execute('''
                INSERT OR REPLACE INTO slides
                (carousel_id, slide_number, headline, body_text, visual_prompt, cta)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (post.id, slide.slide_number, slide.headline, slide.body_text, 
                  slide.visual_prompt, slide.cta))
        
        conn.commit()
        conn.close()
    
    def get_carousel(self, carousel_id: str) -> Optional[CarouselPost]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM carousels WHERE id = ?', (carousel_id,))
        row = cursor.fetchone()
        
        if not row:
            return None
        
        cursor.execute('SELECT * FROM slides WHERE carousel_id = ? ORDER BY slide_number', (carousel_id,))
        slide_rows = cursor.fetchall()
        
        slides = [CarouselSlide(
            slide_number=s[2],
            headline=s[3],
            body_text=s[4],
            visual_prompt=s[5],
            cta=s[6]
        ) for s in slide_rows]
        
        post = CarouselPost(
            id=row[0],
            theme=row[1],
            target_week=row[2],
            slides=slides,
            caption=row[4],
            hashtags=json.loads(row[5]),
            hook=row[3],
            guide_link=row[6],
            status=row[7],
            performance_score=row[8],
            created_at=row[9]
        )
        
        conn.close()
        return post

class CarouselGenerator:
    """Generiert Karussell-Content basierend auf Templates"""
    
    def __init__(self, db: CarouselDatabase = None):
        self.db = db or CarouselDatabase()
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict:
        """Lade Content-Templates"""
        return {
            'awareness': {
                'hook_templates': [
                    "Dein Kind zeigt diese 5 Zeichen? 🚨",
                    "Warum 73% der Eltern das übersehen...",
                    "Schulstress ist nicht normal - hier ist der Beweis"
                ],
                'slide_structure': [
                    {'type': 'hook', 'headline': 'Das Problem', 'body': 'Viele Eltern denken...'},
                    {'type': 'symptom1', 'headline': 'Zeichen #1', 'body': 'Morgendliche Bauchschmerzen...'},
                    {'type': 'symptom2', 'headline': 'Zeichen #2', 'body': 'Schlafstörungen vor Schultagen...'},
                    {'type': 'symptom3', 'headline': 'Zeichen #3', 'body': 'Vermeidungsverhalten...'},
                    {'type': 'solution', 'headline': 'Die Lösung', 'body': 'Kommentiere GUIDE für die komplette Methode'},
                ]
            },
            'value': {
                'hook_templates': [
                    "3 Kommunikationsfehler die Schulstress verstärken",
                    "Was du NIEMALS zu einem gestressten Kind sagen solltest",
                    "Diese Sätze machen alles schlimmer..."
                ],
                'slide_structure': [
                    {'type': 'problem', 'headline': 'Fehler #1', 'body': '"Sei nicht so ängstlich"...'},
                    {'type': 'why_bad', 'headline': 'Warum das schadet', 'body': 'Das Kind fühlt sich nicht verstanden...'},
                    {'type': 'better', 'headline': 'Besser so', 'body': '"Ich sehe du hast Angst..."'},
                    {'type': 'cta', 'headline': 'Willst mehr?', 'body': 'Kommentiere GUIDE'},
                ]
            }
        }
    
    def generate_carousel(self, theme: str, week: int, variant: str = 'A') -> CarouselPost:
        """Generiere einen neuen Karussell-Post"""
        template = self.templates.get(theme, self.templates['awareness'])
        
        post_id = f"{theme}_w{week}_{variant}_{datetime.now().strftime('%Y%m%d')}"
        
        # Wähle Hook basierend auf Variant für A/B Testing
        hooks = template['hook_templates']
        hook = hooks[hash(variant) % len(hooks)]
        
        slides = []
        for i, slide_tmpl in enumerate(template['slide_structure']):
            slide = CarouselSlide(
                slide_number=i + 1,
                headline=slide_tmpl['headline'],
                body_text=slide_tmpl['body'],
                visual_prompt=self._generate_visual_prompt(slide_tmpl, theme),
                cta='Kommentiere "GUIDE"' if i == len(template['slide_structure']) - 1 else None
            )
            slides.append(slide)
        
        post = CarouselPost(
            id=post_id,
            theme=theme,
            target_week=week,
            slides=slides,
            caption=self._generate_caption(hook, theme),
            hashtags=self._generate_hashtags(theme),
            hook=hook,
            guide_link=f"https://elternratgeber.vercel.app/?ref={post_id}",
            ab_test_variant=variant
        )
        
        self.db.save_carousel(post)
        logger.info(f"✅ Karussell generiert: {post_id}")
        
        return post
    
    def _generate_visual_prompt(self, slide: Dict, theme: str) -> str:
        """Generiere Bild-Prompt für DALL-E/AI"""
        base_style = "Minimalistisches Instagram-Karussell Design, sanfte Farben (mint, beige, soft blue), moderne Typography, Eltern-Kind Thema, professionell, clean"
        
        prompts = {
            'problem': f"Besorgte Mutter mit Kind, Schule im Hintergrund, {base_style}",
            'symptom1': f"Kind mit Bauchschmerzen am Morgen, bett, {base_style}",
            'symptom2': f"Kind kann nicht schlafen, Uhr zeigt spät, {base_style}",
            'solution': f"Glückliche Mutter und Kind, entspannt, {base_style}",
        }
        
        return prompts.get(slide['type'], f"Eltern-Kind Beziehung, positiv, {base_style}")
    
    def _generate_caption(self, hook: str, theme: str) -> str:
        """Generiere TikTok Caption"""
        captions = {
            'awareness': f"{hook}\n\nWenn du das bei deinem Kind erkennst, ist es Zeit zu handeln. 💙\n\nKommentiere \"GUIDE\" und ich schicke dir die komplette Methode, mit der du deinem Kind helfen kannst, Schulstress endlich hinter sich zu lassen.\n\n#Schulstress #ElternRatgeber #KinderPsyche",
            'value': f"{hook}\n\nDiese kleinen Änderungen machen einen riesigen Unterschied. 🎯\n\nWillst du die komplette Kommunikations-Anleitung? Kommentiere \"GUIDE\"!\n\n#ElternTipps #Kommunikation #SchulstressBefreit"
        }
        return captions.get(theme, captions['awareness'])
    
    def _generate_hashtags(self, theme: str) -> List[str]:
        """Generiere Hashtags"""
        base = ["ElternRatgeber", "SchulstressBefreit", "KinderPsyche", "ElternTipps", "MamaLeben", "PapaTipps"]
        theme_tags = {
            'awareness': ["Schulstress", "KindHilfe", "ElternSein"],
            'value': ["Kommunikation", "Erziehung", "Familie"]
        }
        return base + theme_tags.get(theme, [])

# Self-Monitoring & Improvement
class CarouselAnalyzer:
    """Analysiert Performance für Selbst-Verbesserung"""
    
    def __init__(self, db: CarouselDatabase):
        self.db = db
    
    def get_best_performing(self, limit: int = 5) -> List[Dict]:
        """Finde beste Karussells für Pattern-Erkennung"""
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, theme, hook, views, likes, comments, guide_clicks, conversions
            FROM carousels 
            WHERE status = 'posted'
            ORDER BY conversions DESC, guide_clicks DESC
            LIMIT ?
        ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        return [{
            'id': r[0], 'theme': r[1], 'hook': r[2],
            'views': r[3], 'likes': r[4], 'comments': r[5],
            'guide_clicks': r[6], 'conversions': r[7]
        } for r in results]
    
    def suggest_improvements(self, carousel_id: str) -> List[str]:
        """Schlage Verbesserungen vor"""
        post = self.db.get_carousel(carousel_id)
        if not post:
            return []
        
        suggestions = []
        
        # Analysiere Hook
        if '?' not in post.hook:
            suggestions.append("Hook enthält keine Frage - Teste Frage-Format (höhere CTR)")
        
        if len(post.hook) > 60:
            suggestions.append("Hook zu lang - Kürze auf 40-50 Zeichen für bessere Lesbarkeit")
        
        # Analysiere CTA
        last_slide = post.slides[-1] if post.slides else None
        if last_slide and 'GUIDE' not in (last_slide.cta or ''):
            suggestions.append("CTA fehlt oder enthält nicht 'GUIDE' - Einheitlicher CTA wichtig für Tracking")
        
        return suggestions

if __name__ == '__main__':
    # Test
    db = CarouselDatabase()
    generator = CarouselGenerator(db)
    
    # Generiere Test-Karussell
    post = generator.generate_carousel('awareness', week=1, variant='A')
    print(f"\n🎯 Karussell: {post.id}")
    print(f"Hook: {post.hook}")
    print(f"Slides: {len(post.slides)}")
    
    # Analysiere
    analyzer = CarouselAnalyzer(db)
    print(f"\n📊 Beste Karussells: {len(analyzer.get_best_performing())}")
