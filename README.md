# Elternratgeber TikTok Automation System

**Direkte TikTok API Integration** für maximale Kontrolle und echte Analytics.

## 🚀 Quick Start

```bash
# Dependencies installieren
pip install -r requirements.txt

# Dashboard starten
streamlit run dashboard.py
```

## 📁 Struktur

```
elternratgeber-system/
├── tiktok_client.py         # Direkte TikTok API Integration
├── link_tracker.py          # Eigener Link Tracking (für CTR)
├── database.py              # SQLite Datenbank
├── dashboard.py             # Streamlit Dashboard
├── automation.py            # Cron-Jobs
├── TIKTOK_SETUP.md          # Detaillierte TikTok Setup Anleitung
└── elternratgeber.db        # Datenbank
```

## 🎯 Features

### Direkte TikTok API
- ✅ Carousel Uploads als Draft
- ✅ Echte TikTok Analytics (Views, Likes, Shares, Comments)
- ✅ Video Liste & Status
- ✅ Keine Middleware nötig

### Link Tracking
- ⚠️ TikTok zeigt KEINE Link-Clicks in der API an!
- ✅ Eigener Shortlink Tracker (SQLite-basiert)
- ✅ Optional: Bitly Integration
- ✅ CTR Berechnung pro Post

### Content System
- ✅ 4 Content Pillars (Awareness → Value → Social Proof → Conversion)
- ✅ Auto-Generierung von Hooks & Captions
- ✅ Weekly Schedule (Mo/Mi/Fr/So um 19:00)
- ✅ UTM Parameter Tracking

### Dashboard
- 📊 Übersicht: Views, Likes, Link-Clicks, Revenue
- 📝 Content Planer mit TikTok Draft Upload
- 📈 Analytics: Post Performance über Zeit
- 💰 Conversions: Sales Tracking, ROI Berechnung

## 🔧 Setup

### 1. TikTok Developer Account (erforderlich!)

Siehe **[TIKTOK_SETUP.md](TIKTOK_SETUP.md)** für detaillierte Schritte.

**Kurzfassung:**
1. [developers.tiktok.com](https://developers.tiktok.com) → Account erstellen
2. App mit "Content Posting API" + "Display API" erstellen
3. OAuth Scopes beantragen: `user.info.basic`, `video.upload`, `video.publish`
4. Access Token generieren (läuft nach 24h ab!)

### 2. Environment Variables

```bash
# .env Datei erstellen
TIKTOK_ACCESS_TOKEN=dein_token_hier
TIKTOK_REFRESH_TOKEN=dein_refresh_token
```

### 3. Link Tracking Setup

Für Link-Clicks brauchst du einen Redirect-Server:

```python
# Beispiel: Flask Redirect Server
from flask import Flask, redirect
from link_tracker import LinkTracker

app = Flask(__name__)
tracker = LinkTracker()

@app.route('/r/<short_code>')
def redirect_link(short_code):
    # Track click
    link_id = tracker.track_click(
        short_code=short_code,
        ip=request.remote_addr,
        user_agent=request.user_agent.string,
        referrer=request.referrer
    )
    
    # Get original URL and redirect
    links = tracker.get_all_links()
    for link in links:
        if link.short_code == short_code:
            return redirect(link.original_url)
    
    return "Link not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

**Alternative:** Nutze Bitly (einfacher, aber kostenpflichtig).

## 📊 Verwendung

### 1. Dashboard öffnen

```bash
streamlit run dashboard.py
```

### 2. Content generieren

- Sidebar → "📝 Content Planer"
- Pillar auswählen (Awareness, Value, Social Proof, Conversion)
- "🎲 Carousel-Idee generieren"
- Shortlink wird automatisch erstellt

### 3. Zu TikTok hochladen

- Draft auswählen
- "🚀 Als Draft zu TikTok hochladen"
- Post landet als Entwurf in deiner TikTok App
- Dort kannst du Musik hinzufügen und veröffentlichen

### 4. Analytics tracken

- Täglich: "📊 Analytics" → TikTok Stats aktualisieren
- Conversions manuell eintragen (oder Stripe Webhook)
- Dashboard zeigt CTR, Conversion Rate, ROI

## 🔄 Automation

### Cron Jobs einrichten

```bash
# Content Generierung (Sonntag 18:00)
0 18 * * 0 cd ~/life/elternratgeber-system && python automation.py generate

# Analytics Sync (täglich 09:00)  
0 9 * * * cd ~/life/elternratgeber-system && python automation.py analytics

# Täglicher Report (20:00)
0 20 * * * cd ~/life/elternratgeber-system && python automation.py report
```

## 📈 Content Strategie

### Posting Zeiten (optimiert für Eltern)

| Tag | Zeit | Pillar | Ziel |
|-----|------|--------|------|
| Montag | 19:00 | Awareness | Reichweite aufbauen |
| Mittwoch | 19:00 | Value | Vertrauen aufbauen |
| Freitag | 19:00 | Social Proof | Überzeugen |
| Sonntag | 19:00 | Conversion | Verkaufen |

### Slide Struktur (pro Carousel)

1. **Hook** - Scroll-stopper (0-1 Sekunden entscheidend!)
2. **Problem** - Relatable Pain Point
3. **Lösung** - Konkreter Tipp/Technik
4. **Beweis** - Statistik oder Case Study
5. **CTA** - Link in Bio + Dringlichkeit

## 💰 Conversion Tracking

### UTM Parameter

Jeder Link enthält automatisch:
```
utm_source=tiktok
utm_medium=social
utm_campaign=elternratgeber
utm_content=post_ID_oder_hook
```

### Metrics

| Metric | Berechnung | Ziel |
|--------|------------|------|
| CTR | Link-Clicks / Views | >3% |
| Conversion Rate | Sales / Link-Clicks | >5% |
| Revenue per Post | Sales × 19€ | >€50 |
| ROI | (Revenue - Cost) / Cost | >200% |

## ⚠️ Wichtige Hinweise

### TikTok API Limitierungen
- Access Token läuft nach **24 Stunden** ab → Refresh Token implementieren!
- Max 20 Video IDs pro Analytics Request
- Upload dauert 1-5 Minuten (asynchron)
- Keine Link-Click Daten (daher eigener Tracker)

### Content Guidelines
- Nicht als medizinischer Rat verkaufen
- Disclaimer: "Kein Ersatz für professionelle Beratung"
- Impressum in Bio verlinken
- Community Guidelines beachten

## 🛠️ Troubleshooting

### "invalid_access_token"
```python
# Token refresh implementieren
new_token = client.refresh_token(refresh_token)
```

### "rate_limit exceeded"
- Weniger Requests pro Minute
- Caching implementieren

### Upload bleibt bei "PROCESSING"
- Normal, kann 1-5 Minuten dauern
- Status regelmäßig prüfen

## 📚 Ressourcen

- [TikTok Content Posting API Docs](https://developers.tiktok.com/doc/content-posting-api-get-started)
- [TikTok Display API Docs](https://developers.tiktok.com/doc/tiktok-api-v2-get-started)
- [TikTok Developer Portal](https://developers.tiktok.com/)

## 🎯 Roadmap

- [ ] Auto-Refresh für Access Tokens
- [ ] Stripe Webhook für automatische Conversions
- [ ] Bildgenerierung mit AI
- [ ] A/B Testing für Hooks
- [ ] Competitor Analysis
- [ ] Telegram Bot für Alerts

---

**Built by Robofabio 🤖 for Master Albert 👑**

*Let's make some money!* 💰🦾
