# Stripe Integration für Elternratgeber

## Zusammenfassung Research (20.03.2026)

### Empfohlene Lösung: Stripe Payment Links + Zapier

**Vorteile:**
- Setup: ~30 Minuten
- Kein Code nötig für Basis-Funktion
- Automatische PDF-Auslieferung per Email
- Kosten: ~0€ bis Significant Volume

### Setup Schritte:

1. **Stripe Account erstellen**
   - Test-Modus: Sofort verfügbar
   - Live-Modus: Verifizierung nötig

2. **Payment Link erstellen**
   - Produkt: "Elternratgeber PDF"
   - Preis: 19€ (einmalig)
   - Metadata: `product_id: elternratgeber_19`

3. **Zapier Automation**
   - Trigger: Stripe `checkout.session.completed`
   - Action: Email mit PDF-Download-Link

4. **PDF Hosting**
   - Cloudflare R2 / AWS S3 / Google Drive
   - Zeitlich begrenzter Download-Link

### Alternative: Selbstgehosteter Webhook

Siehe `webhook_server.py` für Python-Implementation.

### Nächste Schritte:
- [ ] Stripe Test-Account erstellen
- [ ] Payment Link konfigurieren
- [ ] Zapier Workflow einrichten
- [ ] PDF auf CDN hochladen
