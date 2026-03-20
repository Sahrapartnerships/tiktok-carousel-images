# Blotato TikTok Automation System
# Für Elternratgeber "Schulstress befreit"

import requests
import json
import os
from typing import Optional, List, Dict, Any
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BlotatoClient:
    """Blotato API Client für TikTok Automation"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.blotato.com"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def upload_carousel_draft(
        self,
        images: List[str],
        caption: str,
        hashtags: List[str],
        account_id: str,
        schedule_time: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Lädt einen TikTok Carousel als Draft hoch
        
        Args:
            images: Liste der Bildpfade (max 10)
            caption: Post Caption
            hashtags: Liste der Hashtags
            account_id: TikTok Account ID in Blotato
            schedule_time: Optional - wann gepostet werden soll
        """
        if len(images) > 10:
            raise ValueError("Max 10 Bilder für TikTok Carousel")
        
        payload = {
            "platform": "tiktok",
            "account_id": account_id,
            "content_type": "carousel",
            "caption": caption,
            "hashtags": hashtags,
            "images": images,
            "status": "draft",  # Wichtig: als Draft hochladen
            "auto_add_music": True
        }
        
        if schedule_time:
            payload["scheduled_time"] = schedule_time.isoformat()
        
        try:
            response = requests.post(
                f"{self.base_url}/v1/posts",
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            logger.info(f"✅ Carousel Draft erstellt: {response.json().get('post_id')}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Upload fehlgeschlagen: {e}")
            raise
    
    def get_post_analytics(self, post_id: str) -> Dict[str, Any]:
        """Holt Analytics für einen Post"""
        try:
            response = requests.get(
                f"{self.base_url}/v1/posts/{post_id}/analytics",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Analytics Fehler: {e}")
            raise
    
    def get_account_stats(self, account_id: str) -> Dict[str, Any]:
        """Holt Account-übergreifende Stats"""
        try:
            response = requests.get(
                f"{self.base_url}/v1/accounts/{account_id}/stats",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Account Stats Fehler: {e}")
            raise
    
    def list_scheduled_posts(self, account_id: str) -> List[Dict]:
        """Liste aller geplanten Posts"""
        try:
            response = requests.get(
                f"{self.base_url}/v1/accounts/{account_id}/posts",
                headers=self.headers,
                params={"status": "scheduled,draft"}
            )
            response.raise_for_status()
            return response.json().get("posts", [])
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Liste Fehler: {e}")
            raise


class CarouselGenerator:
    """Generiert TikTok Carousels für Elternratgeber"""
    
    # Themen-Pipeline für "Schulstress befreit"
    CONTENT_PILLARS = {
        "awareness": {
            "title": "Erkennungszeichen",
            "hooks": [
                "5 Zeichen, dass dein Kind unter Schulstress leidet 🚨",
                "Das sagt dein Kind, wenn es überfordert ist...",
                "Warum gute Schüler plötzlich schlechte Noten bekommen",
                "Der Fehler, den 90% der Eltern machen",
            ],
            "ctas": [
                "Swipe für die Lösung →",
                "Speichern für später 💾",
                "Teile mit anderen Eltern",
            ]
        },
        "value": {
            "title": "Tipps & Tricks",
            "hooks": [
                "3 Minuten-Technik gegen Prüfungsangst ✨",
                "So hilfst du beim Lernen OHNE zu nerven",
                "Der beste Lerntipp aus der Harvard-Studie",
                "Morgenroutine für stressfreie Schulwege",
            ],
            "ctas": [
                "Link in Bio für den kompletten Ratgeber",
                "Kennst du das auch? Kommentar! 👇",
                "Folge für mehr Eltern-Tipps",
            ]
        },
        "social_proof": {
            "title": "Erfolgsgeschichten",
            "hooks": [
                "Von 4 auf 1 in Mathe - so ging's 🚀",
                "Mama erzählt: Das hat unserem Sohn geholfen",
                "Vorher/Nachher: Keine Hausaufgaben-Stress mehr",
                "Warum diese 3 Dinge WIRKLICH funktionieren",
            ],
            "ctas": [
                "Kostenloser Ratgeber - Link in Bio",
                "Verändere dein Familienleben heute",
                "Jetzt 19€ statt 49,90€",
            ]
        },
        "conversion": {
            "title": "Direct CTA",
            "hooks": [
                "Endlich Schluss mit Schulstress 📚✨",
                "Der Ratgeber, den Eltern lieben",
                "30-Tage Geld-zurück-Garantie",
                "Warum warten? Der perfekte Moment ist JETZT",
            ],
            "ctas": [
                "🔥 Link in Bio - Nur 19€",
                "Swipe Up für sofortigen Zugang",
                "Letzte Chance: Angebot läuft aus",
            ]
        }
    }
    
    HASHTAG_POOL = [
        "#eltern", "#elternleben", "#schulstress", "#prüfungsangst",
        "#lernen", "#schule", "#mama", "#papa", "#familie",
        "#erziehung", "#elterntipps", "#familienleben", "#grundschule",
        "#gymnasium", "#hausaufgaben", "#lernmotivation"
    ]
    
    def __init__(self):
        self.used_hooks = set()
    
    def generate_carousel_data(
        self,
        pillar: str = None,
        custom_hook: str = None
    ) -> Dict[str, Any]:
        """Generiert Carousel-Daten"""
        
        if pillar is None:
            # Rotiere durch die Pillars
            pillars = list(self.CONTENT_PILLARS.keys())
            pillar = pillars[datetime.now().weekday() % len(pillars)]
        
        content = self.CONTENT_PILLARS[pillar]
        
        # Wähle unbenutzten Hook
        available_hooks = [h for h in content["hooks"] if h not in self.used_hooks]
        if not available_hooks:
            self.used_hooks.clear()
            available_hooks = content["hooks"]
        
        hook = custom_hook or available_hooks[0]
        self.used_hooks.add(hook)
        
        # Wähle zufälligen CTA
        cta = content["ctas"][hash(hook) % len(content["ctas"])]
        
        # Generiere Caption
        caption = f"""{hook}

{cta}

{" ".join(self.HASHTAG_POOL[:8])}"""
        
        return {
            "pillar": pillar,
            "hook": hook,
            "cta": cta,
            "caption": caption,
            "hashtags": self.HASHTAG_POOL[:8],
            "slide_structure": [
                "Hook-Slide (Aufmerksamkeit)",
                "Problem (Relatable)",
                "Lösung/Tipp (Value)",
                "Beweis/Social Proof",
                "CTA + Link in Bio"
            ]
        }


if __name__ == "__main__":
    # Test
    gen = CarouselGenerator()
    data = gen.generate_carousel_data("value")
    print(json.dumps(data, indent=2, ensure_ascii=False))
