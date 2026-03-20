# TikTok/Instagram Posting + Tracking Plan

## Ziel
Karussell als Entwurf posten → Tracking aktivieren → A/B Tests → Optimierung

---

## Phase 1: Upload Setup

### Option A: TikTok API (Offiziell)
- **Vorteil:** Direkter API-Zugriff, Analytics
- **Nachteil:** Business Account nötig, Approval-Prozess
- **Kosten:** Kostenlos aber limitiert

### Option B: Instagram Basic Display API
- **Vorteil:** Meta-API, Content Publishing
- **Nachteil:** Nur Business/Creator Accounts
- **Kosten:** Kostenlos

### Option C: Playwright Automation (Empfohlen)
- **Vorteil:** Funktioniert sofort, keine API-Approvals
- **Nachteil:** Kann brechen wenn UI sich ändert
- **Kosten:** Kostenlos

---

## Phase 2: Tracking Setup

### Was tracken?
1. **Views** (Aufrufe)
2. **Likes** 
3. **Comments** (vor allem "GUIDE" Kommentare)
4. **Shares**
5. **CTR** (Link-Klicks via Shortlink)

### Tracking-Methoden:
- **TikTok Analytics API** (wenn API-Zugriff)
- **Playwright Scraping** (tägliche Abfrage)
- **Shortlink Tracking** (für Link-in-Bio)

---

## Phase 3: A/B Testing

### Variablen zum Testen:
1. **Hook Text** (3 Fehler vs. 5 Fehler vs. "Stop")
2. **Thumbnail** (Slide 1 vs. Slide 5)
3. **Posting Zeit** (Morgen vs. Abend)
4. **Caption** (Lang vs. Kurz)

### Test-Setup:
- 2 Varianten parallel posten
- 48h Laufzeit
- Gewinner weiter skalieren

---

## Nächste Schritte

1. [ ] Credentials für TikTok/Instagram Account
2. [ ] Shortlink-Service (für Link-Tracking)
3. [ ] Upload-Methode wählen (API vs. Automation)
4. [ ] Tracking-Dashboard aufsetzen
5. [ ] Ersten Post als Entwurf erstellen

---

## Fragen an Master Albert:

1. **Hast du TikTok Business Account?** (für API-Zugriff)
2. **Hast du Instagram Business/Creator Account?**
3. **Welche Shortlink-Services nutzen wir?** (bit.ly, tinyurl, eigener?)
4. **Soll ich Playwright Automation bauen?** (funktioniert sofort)
5. **Welche Caption willst du testen?** (ich kann 3 Varianten erstellen)

---

**Timeline:** 
- Setup: Heute
- Erster Post: Morgen
- Erste Daten: +24h
- Erste Optimierung: +48h
