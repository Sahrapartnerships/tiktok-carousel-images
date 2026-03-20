"""
TikTok API Client - Direkte Integration
Für Elternratgeber Marketing System

Offizielle TikTok Content Posting API + Display API
"""

import requests
import json
import os
from typing import Optional, List, Dict, Any
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TikTokAPIClient:
    """
    TikTok Content Posting API Client
    
    Erfordert:
    - TikTok Developer Account
    - App mit Content Posting API Produkten
    - OAuth Access Token (user.info.basic, video.upload, video.publish scopes)
    """
    
    BASE_URL = "https://open.tiktokapis.com/v2"
    
    def __init__(self, access_token: str, refresh_token: Optional[str] = None):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    
    # ═══════════════════════════════════════════════════════════
    # UPLOAD ENDPOINTS
    # ═══════════════════════════════════════════════════════════
    
    def upload_carousel_draft(
        self,
        image_paths: List[str],
        title: str,
        privacy_level: str = "SELF_ONLY",  # Als Draft speichern
        disable_comment: bool = False,
        auto_add_music: bool = True,
        photo_cover_index: int = 0,
        brand_content_toggle: bool = False
    ) -> Dict[str, Any]:
        """
        Lädt einen TikTok Carousel (Photo Slideshow) als Draft hoch
        
        Args:
            image_paths: Liste der Bildpfade (1-10 Bilder)
            title: Caption/Title (max 2200 Zeichen)
            privacy_level: PUBLIC_TO_EVERYONE, MUTUAL_FOLLOW_FRIENDS, 
                          FOLLOWER_OF_CREATOR, SELF_ONLY
            disable_comment: Kommentare deaktivieren
            auto_add_music: Automatisch Musik hinzufügen
            photo_cover_index: Welches Bild als Cover (0-basiert)
            brand_content_toggle: Als gesponsorter Content markieren
        
        Returns:
            Dict mit publish_id und upload_url für Chunked Upload
        """
        if len(image_paths) > 10:
            raise ValueError("Maximal 10 Bilder für TikTok Carousel")
        
        if len(image_paths) < 1:
            raise ValueError("Mindestens 1 Bild erforderlich")
        
        # Source info für Photo Upload
        source_info = {
            "source": "FILE_UPLOAD",
            "photo_images": [
                {
                    "file_name": os.path.basename(path),
                    "file_size": os.path.getsize(path)
                }
                for path in image_paths
            ]
        }
        
        payload = {
            "source_info": source_info,
            "title": title,
            "privacy_level": privacy_level,
            "disable_comment": disable_comment,
            "auto_add_music": auto_add_music,
            "photo_cover_index": photo_cover_index,
            "brand_content_toggle": brand_content_toggle,
            "post_mode": "DIRECT_POST"  # Wird zu Draft wenn privacy_level = SELF_ONLY
        }
        
        try:
            response = requests.post(
                f"{self.BASE_URL}/post/publish/content/init/",
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get("error", {}).get("code") != "ok":
                raise Exception(f"TikTok API Error: {data.get('error')}")
            
            logger.info(f"✅ Carousel Upload initiiert: {data.get('data', {}).get('publish_id')}")
            return data.get("data", {})
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Upload Init fehlgeschlagen: {e}")
            raise
    
    def upload_video_draft(
        self,
        video_path: str,
        title: str,
        privacy_level: str = "SELF_ONLY",
        video_cover_timestamp_ms: int = 0,
        disable_duet: bool = False,
        disable_stitch: bool = False,
        disable_comment: bool = False
    ) -> Dict[str, Any]:
        """
        Lädt ein TikTok Video als Draft hoch
        
        Args:
            video_path: Pfad zur Video-Datei
            title: Caption/Title
            privacy_level: Sichtbarkeit
            video_cover_timestamp_ms: Timestamp für Thumbnail (ms)
            disable_duet: Duet deaktivieren
            disable_stitch: Stitch deaktivieren
            disable_comment: Kommentare deaktivieren
        
        Returns:
            Dict mit publish_id und upload_url
        """
        file_size = os.path.getsize(video_path)
        chunk_size = 10 * 1024 * 1024  # 10MB chunks
        total_chunk_count = (file_size + chunk_size - 1) // chunk_size
        
        source_info = {
            "source": "FILE_UPLOAD",
            "video_size": file_size,
            "chunk_size": chunk_size,
            "total_chunk_count": total_chunk_count
        }
        
        payload = {
            "source_info": source_info,
            "title": title,
            "privacy_level": privacy_level,
            "video_cover_timestamp_ms": video_cover_timestamp_ms,
            "disable_duet": disable_duet,
            "disable_stitch": disable_stitch,
            "disable_comment": disable_comment
        }
        
        try:
            response = requests.post(
                f"{self.BASE_URL}/post/publish/video/init/",
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get("error", {}).get("code") != "ok":
                raise Exception(f"TikTok API Error: {data.get('error')}")
            
            logger.info(f"✅ Video Upload initiiert: {data.get('data', {}).get('publish_id')}")
            return data.get("data", {})
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Video Upload Init fehlgeschlagen: {e}")
            raise
    
    def upload_file_chunk(
        self,
        upload_url: str,
        file_path: str,
        chunk_index: int,
        total_chunks: int
    ) -> bool:
        """
        Lädt einen Chunk der Datei hoch (für große Videos)
        
        Args:
            upload_url: URL aus upload_carousel/video_draft
            file_path: Pfad zur Datei
            chunk_index: Index des aktuellen Chunks (0-basiert)
            total_chunks: Gesamtzahl der Chunks
        
        Returns:
            True bei Erfolg
        """
        chunk_size = 10 * 1024 * 1024  # 10MB
        
        with open(file_path, 'rb') as f:
            f.seek(chunk_index * chunk_size)
            chunk_data = f.read(chunk_size)
        
        content_range = f"bytes {chunk_index * chunk_size}-{chunk_index * chunk_size + len(chunk_data) - 1}/{os.path.getsize(file_path)}"
        
        headers = {
            "Content-Range": content_range,
            "Content-Type": "application/octet-stream"
        }
        
        try:
            response = requests.put(
                upload_url,
                headers=headers,
                data=chunk_data
            )
            response.raise_for_status()
            logger.info(f"✅ Chunk {chunk_index + 1}/{total_chunks} hochgeladen")
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Chunk Upload fehlgeschlagen: {e}")
            raise
    
    def check_upload_status(self, publish_id: str) -> Dict[str, Any]:
        """
        Prüft den Status eines Uploads
        
        Args:
            publish_id: ID aus dem Upload-Init Response
        
        Returns:
            Status Info (PROCESSING, PUBLISH_COMPLETE, FAILED)
        """
        try:
            response = requests.post(
                f"{self.BASE_URL}/post/publish/status/fetch/",
                headers=self.headers,
                json={"publish_id": publish_id}
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get("error", {}).get("code") != "ok":
                raise Exception(f"TikTok API Error: {data.get('error')}")
            
            status = data.get("data", {}).get("status")
            logger.info(f"📊 Upload Status für {publish_id}: {status}")
            return data.get("data", {})
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Status Check fehlgeschlagen: {e}")
            raise
    
    def delete_video(self, video_id: str) -> bool:
        """
        Löscht ein veröffentlichtes Video
        
        Args:
            video_id: TikTok Video ID
        
        Returns:
            True bei Erfolg
        """
        try:
            response = requests.post(
                f"{self.BASE_URL}/video/delete/",
                headers=self.headers,
                json={"video_id": video_id}
            )
            response.raise_for_status()
            data = response.json()
            
            success = data.get("error", {}).get("code") == "ok"
            if success:
                logger.info(f"✅ Video {video_id} gelöscht")
            return success
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Löschen fehlgeschlagen: {e}")
            raise
    
    # ═══════════════════════════════════════════════════════════
    # ANALYTICS ENDPOINTS (Display API)
    # ═══════════════════════════════════════════════════════════
    
    def get_video_analytics(
        self,
        video_ids: List[str],
        fields: List[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Holt Analytics für eigene Videos
        
        Args:
            video_ids: Liste der TikTok Video IDs (max 20)
            fields: Welche Felder abrufen (default: alle verfügbaren)
        
        Returns:
            Liste der Video Analytics
        """
        if len(video_ids) > 20:
            raise ValueError("Maximal 20 Video IDs pro Request")
        
        if fields is None:
            fields = [
                "id",
                "create_time",
                "username",
                "region_code",
                "video_description",
                "music_id",
                "like_count",
                "comment_count",
                "share_count",
                "view_count",
                "duration",
                "video_cover_image_url"
            ]
        
        params = {
            "fields": ",".join(fields)
        }
        
        payload = {
            "filters": {
                "video_ids": video_ids
            }
        }
        
        try:
            response = requests.post(
                f"{self.BASE_URL}/video/query/",
                headers=self.headers,
                params=params,
                json=payload
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get("error", {}).get("code") != "ok":
                raise Exception(f"TikTok API Error: {data.get('error')}")
            
            videos = data.get("data", {}).get("videos", [])
            logger.info(f"✅ Analytics für {len(videos)} Videos abgerufen")
            return videos
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Analytics Abruf fehlgeschlagen: {e}")
            raise
    
    def get_user_info(self, fields: List[str] = None) -> Dict[str, Any]:
        """
        Holt User Info des authentifizierten Accounts
        
        Args:
            fields: Welche Felder abrufen
        
        Returns:
            User Info
        """
        if fields is None:
            fields = ["open_id", "union_id", "avatar_url", "display_name"]
        
        params = {
            "fields": ",".join(fields)
        }
        
        try:
            response = requests.get(
                f"{self.BASE_URL}/user/info/",
                headers=self.headers,
                params=params
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get("error", {}).get("code") != "ok":
                raise Exception(f"TikTok API Error: {data.get('error')}")
            
            return data.get("data", {}).get("user", {})
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ User Info Abruf fehlgeschlagen: {e}")
            raise
    
    def get_video_list(
        self,
        cursor: int = 0,
        max_count: int = 20
    ) -> Dict[str, Any]:
        """
        Holt Liste der Videos des Users
        
        Args:
            cursor: Pagination cursor
            max_count: Max Anzahl Videos (max 20)
        
        Returns:
            Video Liste mit Pagination
        """
        params = {
            "fields": "id,create_time,title,video_description,duration,cover_image_url",
            "cursor": cursor,
            "max_count": min(max_count, 20)
        }
        
        try:
            response = requests.get(
                f"{self.BASE_URL}/video/list/",
                headers=self.headers,
                params=params
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get("error", {}).get("code") != "ok":
                raise Exception(f"TikTok API Error: {data.get('error')}")
            
            return data.get("data", {})
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Video Liste Abruf fehlgeschlagen: {e}")
            raise


class TikTokContentPlanner:
    """
    Content Planer für Elternratgeber TikTok Strategie
    """
    
    CONTENT_PILLARS = {
        "awareness": {
            "title": "Erkennungszeichen",
            "templates": [
                "5 Anzeichen, dass dein Kind unter Schulstress leidet 🚨 #eltern #schulstress",
                "Das sagt dein Kind, wenn es überfordert ist... 👂 #erziehung #elternleben",
                "Warum gute Schüler plötzlich schlechte Noten bekommen 📉 #schule #lernen",
                "Der Fehler, den 90% der Eltern machen ❌ #elterntipps #familie",
            ]
        },
        "value": {
            "title": "Tipps & Tricks",
            "templates": [
                "3-Minuten-Technik gegen Prüfungsangst ✨ Sofort hilfreich! #prüfungsangst #lernen",
                "So hilfst du beim Lernen OHNE zu nerven 🧘‍♀️ #hausaufgaben #eltern",
                "Der beste Lerntipp aus Harvard-Studien 🎓 #lernmethoden #studium",
                "Morgenroutine für stressfreie Schulwege ☀️ #routine #familienleben",
            ]
        },
        "social_proof": {
            "title": "Erfolgsgeschichten",
            "templates": [
                "Von Note 4 auf 1 in Mathe - so ging's! 🚀 #erfolg #motivation",
                "Mama erzählt: Das hat unserem Sohn geholfen 💪 #testimonial #eltern",
                "Vorher/Nachher: Kein Hausaufgaben-Stress mehr ✨ #transformation #schulstress",
                "Warum diese 3 Dinge WIRKLICH funktionieren ✅ #tipps #erziehung",
            ]
        },
        "conversion": {
            "title": "Direct CTA",
            "templates": [
                "Endlich Schluss mit Schulstress! 📚 Der komplette Ratgeber 🔗 Bio #elternratgeber",
                "Der Ratgeber, den Eltern lieben ❤️ Nur 19€ (statt 49,90€) 🔗 Link in Bio",
                "30 Tage Geld-zurück-Garantie 🛡️ Teste den Ratgeber risikofrei! #garantie",
                "Warum warten? Der perfekte Moment ist JETZT ⏰ 🔗 Link in Bio",
            ]
        }
    }
    
    HASHTAGS = [
        "#eltern", "#elternleben", "#schulstress", "#prüfungsangst",
        "#lernen", "#schule", "#mama", "#papa", "#familie",
        "#erziehung", "#elterntipps", "#familienleben", "#grundschule",
        "#gymnasium", "#hausaufgaben", "#lernmotivation", "#elternratgeber"
    ]
    
    def __init__(self):
        self.used_templates = set()
    
    def generate_carousel_post(self, pillar: str = None) -> Dict[str, Any]:
        """Generiert einen neuen Carousel Post"""
        
        if pillar is None:
            pillars = list(self.CONTENT_PILLARS.keys())
            day_of_week = datetime.now().weekday()
            pillar = pillars[day_of_week % len(pillars)]
        
        content = self.CONTENT_PILLARS[pillar]
        
        # Wähle unbenutztes Template
        available = [t for t in content["templates"] if t not in self.used_templates]
        if not available:
            self.used_templates.clear()
            available = content["templates"]
        
        template = available[0]
        self.used_templates.add(template)
        
        return {
            "pillar": pillar,
            "pillar_title": content["title"],
            "title": template,
            "slide_count": 5,  # Standard: Hook, Problem, Lösung, Beweis, CTA
            "suggested_hashtags": self.HASHTAGS[:6],
            "optimal_posting_time": "19:00",  # Peak time für Eltern
            "content_type": "carousel"
        }
    
    def get_weekly_schedule(self) -> List[Dict]:
        """Gibt wöchentlichen Content Plan zurück"""
        schedule = []
        days = ["Montag", "Mittwoch", "Freitag", "Sonntag"]
        pillars = ["awareness", "value", "social_proof", "conversion"]
        
        for day, pillar in zip(days, pillars):
            post = self.generate_carousel_post(pillar)
            post["day"] = day
            schedule.append(post)
        
        return schedule


if __name__ == "__main__":
    # Test
    planner = TikTokContentPlanner()
    
    print("🎯 Wöchentlicher Content Plan:")
    print("=" * 50)
    
    for post in planner.get_weekly_schedule():
        print(f"\n📅 {post['day']} - {post['pillar_title']}")
        print(f"📝 {post['title']}")
        print(f"📊 {post['slide_count']} Slides")
