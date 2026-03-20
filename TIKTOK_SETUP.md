# TikTok Direct API Integration - Setup Guide

## 🎯 Übersicht

Dieses System nutzt die **offizielle TikTok Content Posting API** direkt - keine Middleware mehr nötig!

**Vorteile:**
- ✅ Direkte Kontrolle über Uploads
- ✅ Echte TikTok Analytics (Views, Likes, Shares)
- ✅ Draft-Mode: Post landet als Entwurf in deiner TikTok App
- ✅ Keine zusätzlichen Kosten für Drittanbieter

**Einschränkungen:**
- ❌ Link-Clicks werden NICHT von TikTok getrackt → Wir nutzen eigene Shortlinks
- ❌ Setup ist komplexer (Developer Account nötig)

---

## 🔧 Setup Schritt-für-Schritt

### 1. TikTok Developer Account

1. Gehe zu [developers.tiktok.com](https://developers.tiktok.com)
2. Melde dich mit deinem TikTok Account an
3. Verifiziere deine Email

### 2. App Erstellen

1. "My Apps" → "Connect an App"
2. Wähle: **"Content Posting API"** und **"Display API"**
3. App Name: "Elternratgeber Marketing"
4. Kategorie: "Business"

### 3. OAuth Scopes anfordern

Du brauchst diese Berechtigungen:
- `user.info.basic` - User Info abrufen
- `video.upload` - Videos hochladen
- `video.publish` - Videos veröffentlichen
- `video.list` - Video Liste abrufen

**Wichtig:** TikTok prüft manuell! Beschreibe deinen Use Case detailliert:

```
"We are a digital marketing agency managing content for our 
parenting guide product. We need to upload educational carousel 
posts about school stress relief for parents. All content is 
original and complies with TikTok's community guidelines."
```

### 4. Access Token generieren

Nach Approval:
1. In deiner App → "Products" → "Content Posting API"
2. "Generate Access Token"
3. Token kopieren und sicher speichern

**Token läuft ab nach 24 Stunden!** Du brauchst Refresh Token Logic.

### 5. System konfigurieren

Erstelle `.env` Datei:

```bash
# ~/life/elternratgeber-system/.env
TIKTOK_ACCESS_TOKEN=dein_access_token_hier
TIKTOK_REFRESH_TOKEN=dein_refresh_token_hier
TIKTOK_CLIENT_KEY=dein_client_key
TIKTOK_CLIENT_SECRET=dein_client_secret
```

---

## 🚀 Verwendung

### Carousel als Draft hochladen

```python
from tiktok_client import TikTokAPIClient

client = TikTokAPIClient(access_token="dein_token")

# Carousel hochladen
result = client.upload_carousel_draft(
    image_paths=["slide1.jpg", "slide2.jpg", "slide3.jpg"],
    title="5 Anzeichen für Schulstress 🚨 #eltern #schulstress",
    privacy_level="SELF_ONLY",  # Als Draft speichern
    auto_add_music=True
)

print(f"Publish ID: {result['publish_id']}")

# Status prüfen
status = client.check_upload_status(result['publish_id'])
print(f"Status: {status['status']}")  # PROCESSING, PUBLISH_COMPLETE, FAILED
```

### Analytics abrufen

```python
# Deine Video IDs (aus publish result oder video list)
video_ids = ["v1234567890", "v0987654321"]

analytics = client.get_video_analytics(video_ids)

for video in analytics:
    print(f"Video: {video['id']}")
    print(f"  Views: {video['view_count']}")
    print(f"  Likes: {video['like_count']}")
    print(f"  Comments: {video['comment_count']}")
    print(f"  Shares: {video['share_count']}")
```

---

## 📊 Link Tracking Setup

Da TikTok keine Link-Clicks zeigt, nutzen wir eigenen Tracker:

### Option A: Eigener Shortlink Service (einfach)

```python
from link_tracker import LinkTracker

tracker = LinkTracker()

# Link erstellen
link = tracker.create_link(
    original_url="https://elternratgeber-deploy.vercel.app/",
    post_id=1,
    utm_content="hook_001"
)

# In Caption verwenden:
caption = f"Link in Bio ⬆️ oder: {tracker.get_short_url(link.short_code, 'https://deine-domain.com/r')}"
```

### Option B: Bitly Integration (profi)

```python
from link_tracker import BitlyIntegration

bitly = BitlyIntegration(api_key="dein_bitly_key")
short_url = bitly.shorten_url(
    "https://elternratgeber-deploy.vercel.app/?utm_source=tiktok"
)
```

---

## 🔄 Automation

### Wöchentlicher Workflow

```bash
# Sonntag: Content generieren
python automation_tiktok.py generate

# Montag-Freitag: Analytics aktualisieren
python automation_tiktok.py analytics

# Täglich: Report senden
python automation_tiktok.py report
```

### Cron Jobs

```bash
# Content Generierung (Sonntag 18:00)
0 18 * * 0 cd ~/life/elternratgeber-system && python automation_tiktok.py generate

# Analytics Sync (täglich 09:00)
0 9 * * * cd ~/life/elternratgeber-system && python automation_tiktok.py analytics

# Reports (täglich 20:00)
0 20 * * * cd ~/life/elternratgeber-system && python automation_tiktok.py report
```

---

## 📋 Content Strategie

### Posting-Zeiten (optimiert für Eltern)

| Tag | Zeit | Pillar |
|-----|------|--------|
| Montag | 19:00 | Awareness |
| Mittwoch | 19:00 | Value |
| Freitag | 19:00 | Social Proof |
| Sonntag | 19:00 | Conversion |

### Slide-Struktur pro Carousel

1. **Hook Slide** - Aufmerksamkeit fangen
2. **Problem Slide** - Relatable Pain Point
3. **Lösung Slide** - Tipp/Technik
4. **Beweis Slide** - Statistik/Case Study
5. **CTA Slide** - Link in Bio + Urgency

---

## ⚠️ Wichtige Hinweise

### Rate Limits
- Max 20 Video IDs pro Analytics Request
- Uploads: 1 pro Minute empfohlen
- Keine harten Limits dokumentiert, aber konservativ bleiben

### Token Refresh
Access Token läuft nach 24h ab! Implementiere Refresh:

```python
def refresh_token(self, refresh_token: str) -> str:
    response = requests.post(
        "https://open.tiktokapis.com/v2/oauth/token/",
        data={
            "client_key": self.client_key,
            "client_secret": self.client_secret,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
    )
    return response.json()["access_token"]
```

### Content Guidelines
- Keine medizinischen Ratschläge ohne Disclaimer
- "Kein Ersatz für professionelle Beratung" hinzufügen
- Impressum/Datenschutz in Bio verlinken

---

## 🆘 Troubleshooting

### "invalid_access_token"
- Token abgelaufen → Refresh nötig
- Falsche Scopes → App neu genehmigen lassen

### "video upload failed"
- Video zu groß (max 4GB)
- Falsches Format (nur MP4/MOV)
- Dauer zu lang (max 10 Minuten)

### "rate limit exceeded"
- Warte 1 Minute zwischen Requests
- Reduziere Analytics Abfragen

---

**Fragen? Check die TikTok API Doku:**
https://developers.tiktok.com/doc/content-posting-api-get-started

**Let's make some money, Capo!** 🦾💰
