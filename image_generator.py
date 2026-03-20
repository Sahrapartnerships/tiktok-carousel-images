"""
Image Generation System for TikTok Carousels
Generiert Bilder für die 20 geplanten Carousels
"""

import os
import json
import requests
from typing import List, Dict, Optional
from pathlib import Path
from datetime import datetime

# Content Plan für 20 Carousels
CAROUSEL_CONTENT = [
    # Week 1: Awareness
    {
        "id": 1,
        "pillar": "awareness",
        "title": "3 Anzeichen, dass dein Kind unter Schulstress leidet",
        "slides": [
            "Slide 1: Titelbild - '3 Anzeichen für Schulstress'",
            "Slide 2: Schlafprobleme - Kind liegt wach",
            "Slide 3: Bauchschmerzen vor der Schule",
            "Slide 4: Vermeidungsverhalten - 'Ich bin krank'",
        ],
        "style": "warm, beruhigend, pastel colors",
        "prompts": [
            "A warm, comforting illustration of a worried child lying awake in bed at night, soft pastel colors, gentle lighting, minimalist style, educational infographic aesthetic",
            "Cute cartoon illustration of a child with stomach ache holding their belly, soft colors, empathetic style, simple background, infographic style",
            "Illustration of a child trying to avoid school by pretending to be sick in bed, soft pastel colors, warm style, educational infographic",
        ]
    },
    {
        "id": 2,
        "pillar": "awareness", 
        "title": "Warum gute Noten nicht alles sind",
        "slides": [
            "Slide 1: 'Warum gute Noten nicht alles sind'",
            "Slide 2: Stress verursacht schlechte Noten",
            "Slide 3: Emotionale Intelligenz zählt mehr",
            "Slide 4: Gesunde Kinder lernen besser",
        ],
        "style": "motivierend, positiv",
        "prompts": [
            "Bright, uplifting illustration showing a balance scale with grades on one side and happy child on other, positive colors, motivational infographic style",
            "Illustration comparing stressed vs happy child learning, split screen design, warm colors, educational style",
        ]
    },
    {
        "id": 3,
        "pillar": "value",
        "title": "Die 5-Minuten-Methode gegen Prüfungsangst",
        "slides": [
            "Slide 1: '5-Minuten-Methode' Titel",
            "Slide 2: Atemübung Schritt 1",
            "Slide 3: Positive Visualisierung Schritt 2", 
            "Slide 4: Affirmationen Schritt 3",
            "Slide 5: Ergebnis: entspanntes Kind",
        ],
        "style": "klar, instructiv, beruhigend",
        "prompts": [
            "Clean, calming illustration of a child doing breathing exercises, step-by-step infographic style, soft blue and green colors, educational",
            "Peaceful illustration of child visualizing success with thought bubble, positive imagery, soft pastel colors",
        ]
    },
    {
        "id": 4,
        "pillar": "value",
        "title": "So hilfst du bei Hausaufgaben-Stress",
        "slides": [
            "Slide 1: 'Hausaufgaben ohne Stress'",
            "Slide 2: Rituale schaffen Struktur",
            "Slide 3: Pausen sind wichtig (Pomodoro)",
            "Slide 4: Loben statt kritisieren",
            "Slide 5: Erfolgserlebnis",
        ],
        "style": "strukturiert, produktiv",
        "prompts": [
            "Organized workspace illustration with child doing homework, timer visible, clean aesthetic, productive atmosphere, soft colors",
            "Happy child finishing homework with parent praising them, warm family scene, positive reinforcement illustration",
        ]
    },
    {
        "id": 5,
        "pillar": "social_proof",
        "title": "Was andere Eltern sagen",
        "slides": [
            "Slide 1: 'Echte Erfolgsgeschichten'",
            "Slide 2: Testimonial 1 - Mutter von Max",
            "Slide 3: Testimonial 2 - Vater von Lisa", 
            "Slide 4: Vorher/Nachher Vergleich",
            "Slide 5: 'Auch dein Kind kann das schaffen'",
        ],
        "style": "authentisch, vertrauensvoll",
        "prompts": [
            "Warm illustration of happy mother and child, testimonial style, authentic family moment, soft natural lighting",
            "Before/after comparison illustration showing stressed vs happy child, split screen, hopeful transformation",
        ]
    },
    {
        "id": 6,
        "pillar": "conversion",
        "title": "Der ultimative Elternratgeber",
        "slides": [
            "Slide 1: 'Schulstress befreit' Cover",
            "Slide 2: Was drin ist (Kapitelübersicht)",
            "Slide 3: 50+ Seiten wertvolles Wissen",
            "Slide 4: Sofort umsetzbare Tipps",
            "Slide 5: Jetzt nur 19€ statt 49,90€",
            "Slide 6: CTA - Link in Bio",
        ],
        "style": "professionell, verkaufsstark",
        "prompts": [
            "Professional ebook cover design for parenting guide about school stress, modern typography, calming colors, trustworthy aesthetic",
            "Clean product showcase of digital guide with checkmarks and benefits, professional marketing style, soft professional colors",
        ]
    },
]

# Generiere 14 weitere Carousels...
ADDITIONAL_CAROUSELS = [
    {"id": 7, "pillar": "awareness", "title": "Der verborgene Stress: Was Lehrer nicht sehen", "slides": 4},
    {"id": 8, "pillar": "awareness", "title": "Wann ist der Schulstress normal, wann nicht?", "slides": 4},
    {"id": 9, "pillar": "value", "title": "Morgenroutine für stressfreie Schultage", "slides": 5},
    {"id": 10, "pillar": "value", "title": "Die perfekte Lernumgebung zu Hause", "slides": 5},
    {"id": 11, "pillar": "value", "title": "Gespräche führen: Was du NICHT sagen solltest", "slides": 4},
    {"id": 12, "pillar": "value", "title": "Schlafhygiene für bessere Noten", "slides": 5},
    {"id": 13, "pillar": "social_proof", "title": "Vorher/Nachher: 3 echte Veränderungen", "slides": 5},
    {"id": 14, "pillar": "social_proof", "title": "Warum 500+ Eltern uns vertrauen", "slides": 4},
    {"id": 15, "pillar": "social_proof", "title": "Das sagt die Kinderpsychologin", "slides": 4},
    {"id": 16, "pillar": "conversion", "title": "3 Gründe, warum das PDF sich lohnt", "slides": 5},
    {"id": 17, "pillar": "conversion", "title": "30-Tage-Geld-zurück-Garantie", "slides": 4},
    {"id": 18, "pillar": "conversion", "title": "Nur noch 48h: Frühbucher-Rabatt", "slides": 5},
    {"id": 19, "pillar": "awareness", "title": "Langfristige Folgen von Schulstress", "slides": 4},
    {"id": 20, "pillar": "conversion", "title": "Dein Kind verdient ein sorgenfreies Leben", "slides": 6},
]

class ImageGenerator:
    """
    Generiert Bilder für TikTok Carousels
    """
    
    def __init__(self, output_dir: str = "/root/life/elternratgeber-system/images"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # OpenAI API Key aus Umgebung
        self.openai_key = os.getenv('OPENAI_API_KEY', '')
        
    def generate_with_dalle(self, prompt: str, size: str = "1024x1024") -> Optional[str]:
        """
        Generiert ein Bild mit DALL-E 3
        """
        if not self.openai_key:
            print("❌ Kein OPENAI_API_KEY gefunden!")
            return None
            
        url = "https://api.openai.com/v1/images/generations"
        headers = {
            "Authorization": f"Bearer {self.openai_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "dall-e-3",
            "prompt": prompt,
            "size": size,
            "quality": "standard",
            "n": 1
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=120)
            if response.status_code == 200:
                result = response.json()
                image_url = result['data'][0]['url']
                return image_url
            else:
                print(f"❌ DALL-E Error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def download_image(self, url: str, filename: str) -> Optional[str]:
        """
        Lädt ein Bild herunter
        """
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                filepath = self.output_dir / filename
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                return str(filepath)
            return None
        except Exception as e:
            print(f"❌ Download Error: {e}")
            return None
    
    def generate_carousel_images(self, carousel_id: int, prompts: List[str]) -> List[str]:
        """
        Generiert alle Bilder für einen Carousel
        """
        print(f"🎨 Generiere Carousel #{carousel_id}...")
        generated = []
        
        for i, prompt in enumerate(prompts):
            print(f"  Bild {i+1}/{len(prompts)}...")
            
            # Generiere mit DALL-E
            image_url = self.generate_with_dalle(prompt)
            if image_url:
                # Lade herunter
                filename = f"carousel_{carousel_id}_img_{i+1}.png"
                filepath = self.download_image(image_url, filename)
                if filepath:
                    generated.append(filepath)
                    print(f"  ✅ {filename}")
                else:
                    print(f"  ❌ Download fehlgeschlagen")
            else:
                print(f"  ❌ Generierung fehlgeschlagen")
        
        return generated
    
    def generate_all(self, max_carousels: int = 20) -> Dict[int, List[str]]:
        """
        Generiert Bilder für alle Carousels
        """
        results = {}
        
        for carousel in CAROUSEL_CONTENT:
            if carousel['id'] <= max_carousels:
                images = self.generate_carousel_images(
                    carousel['id'], 
                    carousel['prompts']
                )
                results[carousel['id']] = images
        
        return results


if __name__ == "__main__":
    print("🎨 TikTok Carousel Image Generator")
    print("=" * 50)
    
    gen = ImageGenerator()
    
    # Prüfe API Key
    if not gen.openai_key:
        print("\n⚠️  OPENAI_API_KEY nicht gefunden!")
        print("Setze den Key mit: export OPENAI_API_KEY='sk-...'")
    else:
        print(f"\n✅ API Key gefunden")
        print(f"📁 Output: {gen.output_dir}")
        
        # Generiere erstes Carousel als Test
        print("\n🚀 Starte Test-Generierung (Carousel #1)...")
        results = gen.generate_carousel_images(1, CAROUSEL_CONTENT[0]['prompts'])
        
        print(f"\n✅ {len(results)} Bilder generiert!")
        for r in results:
            print(f"   📷 {r}")
