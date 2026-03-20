# 🤖 TikTok/Instagram Upload Bot (Persistent Login)

Automatisiertes Upload-System mit **gespeicherter Login-Session**.
Einmal einloggen, danach automatisch eingeloggt bleiben.

---

## ✨ Features

✅ **Persistenter Login** - Session wird gespeichert  
✅ **Einmal einloggen** - Danach automatisch eingeloggt  
✅ **Session-Manager** - Status prüfen, Sessions löschen  
✅ **Auto-Upload** - Bilder + Caption + Hashtags  
✅ **Draft-Modus** - Du entscheidest wann gepostet wird  
✅ **Tracking** - Views, Likes, Comments tracken  

---

## 🚀 Schnellstart

### 1. Erster Upload (Login erforderlich)

```bash
cd /root/life/elternratgeber-system/tiktok_system
python3 upload_bot_persistent.py
```

**Was passiert:**
1. Browser öffnet TikTok
2. Du loggst dich EINMAL ein (manuell)
3. Bot speichert die Session
4. Karussell wird hochgeladen
5. Session bleibt gespeichert für nächstes Mal

### 2. Jeder weitere Upload (Auto-Login)

```bash
python3 upload_bot_persistent.py
```

**Was passiert:**
1. Browser öffnet TikTok
2. ✅ Bereits eingeloggt (Session geladen)
3. Direkt zum Upload
4. Kein erneuter Login nötig!

---

## 📊 Session Manager

### Status prüfen
```bash
python3 session_manager.py status
```

### Testen ob Session noch gültig
```bash
python3 session_manager.py test tiktok
python3 session_manager.py test instagram
```

### Session löschen (neuer Login nötig)
```bash
python3 session_manager.py delete tiktok
python3 session_manager.py delete instagram
python3 session_manager.py delete all
```

---

## 📁 Dateistruktur

```
data/
├── tiktok_session.json        # TikTok Login-Session
├── instagram_session.json     # Instagram Login-Session
├── post_tracking.json         # Upload-History
└── post_analytics.json        # Performance-Daten
```

**⚠️ Wichtig:** Session-Files enthalten Login-Cookies. Nicht öffentlich teilen!

---

## 🔄 Workflow

### Erstmalig (Einrichtung)

```bash
# 1. Upload starten
python3 upload_bot_persistent.py

# 2. Im Browser:
#    - TikTok öffnet sich
#    - Einloggen mit deinen Daten
#    - Warten bis Upload fertig ist
#    - Browser schließen

# 3. Session ist jetzt gespeichert!
```

### Regulärer Gebrauch

```bash
# Einfach starten - automatisch eingeloggt
python3 upload_bot_persistent.py

# Bilder werden hochgeladen
# Du prüfst und postest manuell
```

### Nach Problemen

```bash
# Session prüfen
python3 session_manager.py status

# Wenn Session ungültig:
python3 session_manager.py delete tiktok

# Neu einloggen
python3 upload_bot_persistent.py
```

---

## 📈 Tracking

### Nach dem Posten (URL eintragen)

```bash
# Performance tracken
python3 analytics_dashboard.py track https://tiktok.com/@name/video/123 post_001

# Report anzeigen
python3 analytics_dashboard.py report
```

---

## ⚠️ Session-Haltbarkeit

| Plattform | Hält typischerweise | Nach Ablauf |
|-----------|---------------------|-------------|
| TikTok | 7-30 Tage | Neuer Login |
| Instagram | 14-60 Tage | Neuer Login |

**Warum läuft sie ab?**
- Sicherheits-Logouts
- Cookie-Ablauf
- "Verdächtige Aktivität" Erkennung

**Lösung:** Einfach neu einloggen mit `delete` → Upload

---

## 🛠️ Troubleshooting

### "Login erforderlich" obwohl Session existiert
```bash
# Session testen
python3 session_manager.py test tiktok

# Falls ungültig - löschen und neu
python3 session_manager.py delete tiktok
python3 upload_bot_persistent.py
```

### "Element not found" Error
- TikTok/Instagram UI hat sich geändert
- Selector muss angepasst werden
- Screenshot wird gespeichert unter `/tmp/tiktok_error.png`

### Upload funktioniert nicht
- Max 5 Bilder für TikTok
- Max 10 Bilder für Instagram
- Bilder prüfen: `ls images/carousel_3_fehler_realistic/`

---

## 📝 Anpassungen

### Bilder ändern
```python
# In upload_bot_persistent.py
IMAGES_DIR = Path('.../carousel_3_fehler_premium')  # oder realistic
```

### Caption ändern
```python
caption = """Dein Text hier..."""
hashtags = ["#tag1", "#tag2"]
```

---

## 🎯 Sicherheit

✅ Sessions werden lokal gespeichert  
✅ Keine Daten werden versendet  
✅ Du behältst volle Kontrolle  
⚠️ Session-Files nicht teilen (enthalten Login-Info)  

---

**Version:** 2.0 (Persistent Login)  
**Letztes Update:** 2026-03-20  
