from fpdf import FPDF
from datetime import datetime

class ElternratgeberPDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 12)
        self.set_text_color(50, 50, 50)
        self.cell(0, 10, 'Elternratgeber PLUS: Schulstress befreit + Lern-Erfolg', new_x="RIGHT", new_y="TOP")
        self.cell(0, 10, f'Seite {self.page_no()}', new_x="RIGHT", new_y="TOP", align='R')
        self.ln(15)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, 'Copyright 2026 Elternratgeber - Alle Rechte vorbehalten', align='C')
    
    def chapter_title(self, title):
        self.set_font('helvetica', 'B', 18)
        self.set_text_color(0, 102, 204)
        self.cell(0, 15, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(5)
    
    def chapter_subtitle(self, subtitle):
        self.set_font('helvetica', 'B', 14)
        self.set_text_color(51, 51, 51)
        self.cell(0, 10, subtitle, new_x="LMARGIN", new_y="NEXT")
        self.ln(3)
    
    def body_text(self, text):
        self.set_font('helvetica', '', 11)
        self.set_text_color(51, 51, 51)
        self.multi_cell(0, 6, text)
        self.ln(5)
    
    def bullet_point(self, text):
        self.set_font('helvetica', '', 11)
        self.set_text_color(51, 51, 51)
        start_x = self.get_x()
        self.cell(5, 6, '-', new_x="RIGHT", new_y="TOP")
        self.multi_cell(self.w - self.r_margin - start_x - 10, 6, text)
        self.ln(2)
    
    def highlight_box(self, text):
        self.set_fill_color(240, 248, 255)
        self.set_draw_color(0, 102, 204)
        self.set_line_width(0.5)
        self.set_font('helvetica', 'I', 11)
        self.set_text_color(0, 51, 102)
        self.multi_cell(0, 8, text, border=1, fill=True)
        self.ln(10)

def create_pdf():
    pdf = ElternratgeberPDF()
    
    # === TITELSEITE ===
    pdf.add_page()
    pdf.set_font('helvetica', 'B', 26)
    pdf.set_text_color(0, 102, 204)
    pdf.ln(50)
    pdf.cell(0, 20, 'SCHULSTRESS BEFREIT', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.set_font('helvetica', 'B', 20)
    pdf.set_text_color(255, 152, 0)
    pdf.cell(0, 15, '+ LERN-ERFOLG', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.set_font('helvetica', 'B', 16)
    pdf.set_text_color(51, 51, 51)
    pdf.cell(0, 12, 'Die Komplettloesung fuer Eltern', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    pdf.set_font('helvetica', '', 13)
    pdf.set_text_color(102, 102, 102)
    pdf.cell(0, 10, 'Kommunikation + Lernmethoden + Konzentration', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, 'Fuer entspannte Eltern und erfolgreiche Kinder', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(25)
    pdf.set_font('helvetica', 'I', 12)
    pdf.cell(0, 10, 'NEU: Erweiterte Edition mit Praxis-Guide fuer besseres Lernen', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_font('helvetica', 'I', 11)
    pdf.set_text_color(128, 128, 128)
    pdf.cell(0, 10, 'Copyright 2026 - Alle Rechte vorbehalten', align='C', new_x="LMARGIN", new_y="NEXT")
    
    # === INHALTSVERZEICHNIS ===
    pdf.add_page()
    pdf.chapter_title('Inhaltsverzeichnis')
    
    sections = [
        ('TEIL 1: Kommunikation', [
            'Einleitung',
            'Fehler #1: "Das schaffst du schon!"',
            'Fehler #2: "Warum kann Maria das?"',
            'Fehler #3: "Ich mach das schon"',
            '7-Tage Praxis-Plan'
        ]),
        ('TEIL 2: Lernmethoden', [
            'Wie das Gehirn wirklich lernt',
            'Die 5 besten Lernmethoden fuer Kinder',
            'Lernplan erstellen - Schritt fuer Schritt',
            'Pruefungsvorbereitung ohne Stress'
        ]),
        ('TEIL 3: Konzentration', [
            'Fokus staerken: Die 4-P-S-Formel',
            'Ablenkungen eliminieren',
            'Der perfekte Lernplatz',
            'Pausen richtig nutzen: Pomodoro fuer Kids'
        ]),
        ('TEIL 4: Tools \u0026 Templates', [
            'Wochen-Lernplan Template',
            'Tagesplan fuer Konzentration',
            'Belohnungssystem zum Ausdrucken'
        ])
    ]
    
    for part_title, chapters in sections:
        pdf.set_font('helvetica', 'B', 13)
        pdf.set_text_color(0, 102, 204)
        pdf.cell(0, 10, part_title, new_x="LMARGIN", new_y="NEXT")
        pdf.set_font('helvetica', '', 11)
        pdf.set_text_color(51, 51, 51)
        for chapter in chapters:
            pdf.cell(10)
            pdf.cell(0, 7, f'- {chapter}', new_x="LMARGIN", new_y="NEXT")
        pdf.ln(3)
    
    # === EINLEITUNG ===
    pdf.add_page()
    pdf.chapter_title('Einleitung')
    pdf.body_text(
        'Liebe Eltern,\n\n'
        'Schulstress ist kein "Schoenheitsfehler" der modernen Zeit - er ist ein echtes Problem, '
        'das die Gesundheit und Entwicklung unserer Kinder beeintraechtigt. Als Eltern wollen wir '
        'das Beste fuer unsere Kinder, doch oft machen wir unbewusst Fehler, die den Stress '
        'noch verstaerken.\n\n'
        'Diese erweiterte Edition geht noch einen Schritt weiter: Wir zeigen dir nicht nur, '
        'wie du Kommunikationsfehler vermeidest, sondern auch, wie du deinem Kind konkrete '
        'Lern- und Konzentrationsstrategien an die Hand gibst - fuer nachhaltigen Erfolg '
        'und weniger Stress fuer die ganze Familie.'
    )
    
    pdf.highlight_box(
        'Fakt: 65% aller Schueler geben an, regelmaessig unter Schulstress zu leiden. '
        'Kinder mit guten Lernstrategien und Konzentrationstechniken erleben bis zu 40% '
        'weniger Stress und verbessern ihre Noten signifikant.'
    )
    
    # === TEIL 1: FEHLER 1 ===
    pdf.add_page()
    pdf.chapter_title('TEIL 1: Kommunikation')
    pdf.chapter_subtitle('Fehler #1: "Das schaffst du schon!" - Der Ueberzeugungs-Fehler')
    
    pdf.body_text(
        'Dieser Satz klingt harmlos, ist aber ein Trojanisches Pferd. Wenn wir sagen '
        '"Das schaffst du schon", meinen wir es ermutigend. Aber was unser Kind hoert, '
        'ist: "Ich bin nicht gut genug, solange ich es nicht geschafft habe."\n\n'
        'Der Druck steigt. Das Kind fuehlt sich alleingelassen mit seinen Aengsten. '
        'Und genau das fuehrt zu Ueberforderung und Stress.'
    )
    
    pdf.chapter_subtitle('Was stattdessen hilft:')
    pdf.bullet_point('Validierung: "Ich sehe, dass du das schwierig findest."')
    pdf.bullet_point('Unterstuetzung anbieten: "Wie kann ich dir helfen?"')
    pdf.bullet_point('Gemeinsame Loesung finden: "Lass uns zusammen schauen, was wir tun koennen."')
    pdf.ln(10)
    
    pdf.highlight_box(
        'Tipp: Validation bedeutet nicht Zustimmung. Du bestaetigst die Gefuehle deines '
        'Kindes, nicht unbedingt seine Einschaetzung der Situation.'
    )
    
    # === FEHLER 2 ===
    pdf.add_page()
    pdf.chapter_subtitle('Fehler #2: "Warum kann Maria das?" - Der Vergleichs-Fehler')
    
    pdf.body_text(
        'Vergleiche mit anderen Kindern sind Gift fuer das Selbstwertgefuehl. Jedes Kind '
        'hat seinen eigenen Rhythmus, seine eigenen Staerken und Herausforderungen. '
        'Wenn wir sagen "Maria schafft das auch", setzen wir unser Kind unter Leistungsdruck '
        'und lassen es sich minderwertig fuehlen.'
    )
    
    pdf.chapter_subtitle('Was stattdessen hilft:')
    pdf.bullet_point('Individuellen Fortschritt wuerdigen: "Du hast dich so sehr verbessert!"')
    pdf.bullet_point('Eigene Staerken betonen: "Du bist besonders gut in..."')
    pdf.bullet_point('Wachstumsdenken foerdern: "Jeder lernt in seinem eigenen Tempo."')
    
    # === FEHLER 3 ===
    pdf.add_page()
    pdf.chapter_subtitle('Fehler #3: "Ich mach das schon" - Die Uebernahme-Fehler')
    
    pdf.body_text(
        'Als Eltern wollen wir unsere Kinder entlasten. Doch wenn wir staendig Aufgaben '
        'uebernehmen, nehmen wir ihnen die Chance, Selbstwirksamkeit zu entwickeln. '
        'Das Kind lernt: "Ich bin nicht faehig, das alleine zu schaffen."'
    )
    
    pdf.chapter_subtitle('Was stattdessen hilft:')
    pdf.bullet_point('Begleiten statt uebernehmen: "Ich bin da, wenn du Fragen hast."')
    pdf.bullet_point('Eigenverantwortung foerdern: "Was planst du als Naechstes?"')
    pdf.bullet_point('Fehler erlauben: "Es ist okay, wenn nicht alles perfekt ist."')
    
    # === TEIL 2: LERNMETHODEN ===
    pdf.add_page()
    pdf.chapter_title('TEIL 2: Lernmethoden')
    pdf.chapter_subtitle('Wie das Gehirn wirklich lernt')
    
    pdf.body_text(
        'Das Gehirn ist kein Computer, der Informationen einfach speichert. Es ist ein '
        'komplexes Netzwerk, das durch Verbindungen lernt. Das bedeutet: \n\n'
        'Wichtiger als "viel lernen" ist "richtig lernen". Qualitaet schlaegt Quantitaet. '
        'Ein Kind, das 30 Minuten fokussiert und effektiv lernt, lernt mehr als ein Kind, '
        'das 2 Stunden planlos vor sich hin lernt.'
    )
    
    pdf.highlight_box(
        'Wissenschaftlich bewiesen: Das Gehirn bildet staerkere Verbindungen, wenn wir '
        'aktiv mit dem Stoff umgehen statt nur passiv zu lesen. Das nennt man "aktives Lernen".'
    )
    
    pdf.add_page()
    pdf.chapter_subtitle('Die 5 besten Lernmethoden fuer Kinder')
    
    methods = [
        ('1. Die Cornell-Methode', 
         'Unterteile das Blatt in drei Bereiche: Notizen, Stichwoerter, Zusammenfassung. '
         'Dies fordert strukturiertes Denken und aktive Verarbeitung.'),
        ('2. Mind Mapping', 
         'Visuelle Darstellung von Zusammenhaengen. Besonders gut fuer visuelle Lerner. '
         'Nutze Farben, Bilder, Symbole - je kreativer, desto besser.'),
        ('3. Lernkarten (Karteikarten)', 
         'Perfekt fuer Vokabeln, Definitionen, Formeln. Das Selbsttesten aktiviert '
         'das aktive Abrufen und festigt das Wissen.'),
        ('4. Feynman-Technik', 
         'Erklaere den Stoff einfach, als wuerdest du es einem 6-Jaehrigen erklaeren. '
         'Wenn du es nicht einfach erklaeren kannst, hast du es nicht verstanden.'),
        ('5. Das Leitner-System', 
         'Karteikarten in Faecher einteilen nach Schwierigkeitsgrad. Haeufiger wiederholen, '
         'was schwer faellt, seltener das, was sitzt. Effizient und nachweislich wirksam.')
    ]
    
    for title, desc in methods:
        pdf.set_font('helvetica', 'B', 12)
        pdf.set_text_color(0, 102, 204)
        pdf.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        pdf.set_font('helvetica', '', 11)
        pdf.set_text_color(51, 51, 51)
        pdf.multi_cell(0, 6, desc)
        pdf.ln(3)
    
    pdf.add_page()
    pdf.chapter_subtitle('Lernplan erstellen - Schritt fuer Schritt')
    
    pdf.body_text(
        'Ein guter Lernplan ist das Fundament fuer Lernerfolg ohne Stress. '
        'So erstellst du gemeinsam mit deinem Kind einen Plan, der funktioniert:'
    )
    
    pdf.chapter_subtitle('Schritt-fuer-Schritt Lernplan:')
    pdf.bullet_point('Gemeinsam alle anstehenden Aufgaben auflisten')
    pdf.bullet_point('Schaetze: Wie lange braucht jede Aufgabe? (Zeitpuffer einplanen!)')
    pdf.bullet_point('Priorisiere: Was ist dringend? Was ist wichtig?')
    pdf.bullet_point('Verteile die Aufgaben auf die Woche (nicht alles auf einen Tag!)')
    pdf.bullet_point('Plane Pausen ein - mindestens 10 Minuten pro Stunde')
    pdf.bullet_point('Schreibe den Plan auf (sichtbar aufhaengen)')
    pdf.bullet_point('Am Ende der Woche: Gemeinsam reflektieren und anpassen')
    
    pdf.highlight_box(
        'Goldene Regel: Der Plan muss realistisch sein! Besser weniger Aufgaben '
        'erfolgreich schaffen als viele Aufgaben halbherzig erledigen.'
    )
    
    # === TEIL 3: KONZENTRATION ===
    pdf.add_page()
    pdf.chapter_title('TEIL 3: Konzentration')
    pdf.chapter_subtitle('Fokus staerken: Die 4-P-S-Formel')
    
    pdf.body_text(
        'Konzentration ist trainierbar - wie ein Muskel. Mit der richtigen Strategie '
        'kann jedes Kind seinen Fokus verbessern. Die 4-P-S-Formel hilft dabei:'
    )
    
    four_ps = [
        ('PLATZ', 'Ein fester, ruhiger Lernplatz ohne Ablenkungen. Nicht am Kuechentisch, '
         'nicht vor dem Fernseher. Ein eigener "Lern-Tempel".'),
        ('PLAN', 'Klare Zeitfenster fuer Lernen. Das Gehirn gewoehnt sich an Routinen. '
         'Gleiche Zeit = gleicher Ort = automatischer Fokus.'),
        ('PAUSE', 'Regelmaessige Pausen sind Pflicht, nicht optional. Ohne Pause sinkt '
         'die Konzentration dramatisch.'),
        ('PRAEMIE', 'Belohnungen motivieren. Nicht nur am Ende, sondern auch fuer '
         'Zwischenziele. Kleine Siege feiern!')
    ]
    
    for title, desc in four_ps:
        pdf.set_font('helvetica', 'B', 12)
        pdf.set_text_color(255, 152, 0)
        pdf.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        pdf.set_font('helvetica', '', 11)
        pdf.set_text_color(51, 51, 51)
        pdf.multi_cell(0, 6, desc)
        pdf.ln(3)
    
    pdf.add_page()
    pdf.chapter_subtitle('Ablenkungen eliminieren')
    
    pdf.body_text(
        'Smartphones, Tablets, Fernseher - die modernen Konzentrationskiller. '
        'So schaffst du ein ablenkungsfreies Lernumfeld:'
    )
    
    pdf.chapter_subtitle('Ablenkungen beseitigen:')
    pdf.bullet_point('Handy auf Flugmodus und ausser Reichweite')
    pdf.bullet_point('Tablet nur bei Bedarf, sonst weg')
    pdf.bullet_point('Fernseher aus - nicht nur stumm')
    pdf.bullet_point('Laptop: Nur Lern-Websites erlauben (Apps wie Cold Turkey)')
    pdf.bullet_point('Tuere schliessen (wenn moeglich)')
    pdf.bullet_point('Geschwister informieren: "Ich lerne jetzt"')
    pdf.bullet_point('Stille ODER ruhige Hintergrundmusik (keine Lyrics!)')
    
    pdf.highlight_box(
        'Studie: Es dauert durchschnittlich 23 Minuten, bis man nach einer Unterbrechung '
        'wieder voll konzentriert ist. Ein einziges Handy-Signal kann den ganzen Lernflow zerstoeren!'
    )
    
    pdf.add_page()
    pdf.chapter_subtitle('Pomodoro fuer Kids - Das perfekte Pausensystem')
    
    pdf.body_text(
        'Die Pomodoro-Technik funktioniert hervorragend fuer Kinder - mit kleinen Anpassungen:\n\n'
        'Standard-Pomodoro: 25 Minuten Arbeit, 5 Minuten Pause\n'
        'Fuer Kinder: 15-20 Minuten Arbeit, 5-10 Minuten Pause\n\n'
        'Nach 4 Runden: Eine laengere Pause (20-30 Minuten)'
    )
    
    pdf.chapter_subtitle('Pomodoro mit Kindern umsetzen:')
    pdf.bullet_point('Timer sichtbar stellen (Eieruhr, App, oder Sanduhr)')
    pdf.bullet_point('Waehrend der Pause: Bewegung, Wasser trinken, frische Luft')
    pdf.bullet_point('NICHT waehrend der Pause: Handy, Gaming, Fernsehen')
    pdf.bullet_point('Nach jedem Pomodoro: Haekchen setzen oder Aufkleber')
    pdf.bullet_point('4 Pomodoros = Belohnung (nicht materiell, sondern Erlebnis)')
    
    pdf.highlight_box(
        'Tipp fuer kleine Kinder: Mache es zu einem Spiel. "Wir schauen, wie viele '
        'Pomodoros wir heute schaffen!" Wettbewerb mit sich selbst - nicht mit anderen.'
    )
    
    # === TEIL 4: TOOLS ===
    pdf.add_page()
    pdf.chapter_title('TEIL 4: Tools \u0026 Templates')
    
    pdf.body_text(
        'Umsetzung ist alles. Nutze diese Templates, um das Gelernte sofort in die Tat umzusetzen. '
        'Du kannst sie ausdrucken oder digital nutzen.'
    )
    
    pdf.chapter_subtitle('Wochen-Lernplan Template')
    
    pdf.set_font('helvetica', '', 10)
    pdf.set_fill_color(245, 245, 245)
    
    days = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
    for day in days:
        pdf.cell(40, 8, day, border=1, fill=True)
        pdf.cell(0, 8, '__________________________________________', border=1)
        pdf.ln(8)
    
    pdf.ln(10)
    pdf.chapter_subtitle('Tagesplan fuer maximale Konzentration')
    
    schedule_items = [
        'Uhrzeit: _____________ Lern-Thema: ________________________',
        'Lernmethode: ________________ Dauer: _______ Minuten',
        'Pausen-Plan: Nach ____ Minuten ____ Minuten Pause',
        'Belohnung danach: _________________________________________',
        'Hilfsmittel: ______________________________________________'
    ]
    
    for item in schedule_items:
        pdf.cell(0, 10, item, border=1)
        pdf.ln(10)
    
    pdf.ln(10)
    pdf.chapter_subtitle('Belohnungssystem zum Ausdrucken')
    
    pdf.body_text(
        'Motive dein Kind mit einem visuellen Belohnungssystem. Jeder erfolgreiche '
        'Lerntag bringt einen Stern - gesammelt koennen diese in Belohnungen umgewandelt werden.'
    )
    
    pdf.set_font('helvetica', '', 12)
    for i in range(1, 6):
        for j in range(1, 6):
            pdf.cell(20, 12, '*', border=1, align='C')
        pdf.ln(12)
    
    pdf.ln(10)
    pdf.set_font('helvetica', 'I', 10)
    pdf.multi_cell(0, 6, 
        'Belohnungs-Ideen (nicht materiell): Spieleabend, Ausflug, Eisessen, '
        'spaeter ins Bett duerfen, extra Kuscheleinheit, gemeinsam kochen...'
    )
    
    # === ABSCHLUSS ===
    pdf.add_page()
    pdf.chapter_title('Zusammenfassung \u0026 Naechste Schritte')
    
    pdf.body_text(
        'Du hast jetzt ein komplettes Toolkit zur Hand:\n\n'
        '1. Bessere Kommunikation ohne Stress\n'
        '2. Effektive Lernmethoden, die wirklich funktionieren\n'
        '3. Konzentrationstechniken fuer mehr Fokus\n'
        '4. Praktische Templates fuer sofortige Umsetzung\n\n'
        'Denke daran: Nicht alles auf einmal umsetzen. Waehle einen Bereich, '
        'fange klein an, und feiere jeden Erfolg. Dein Kind wird es dir danken.'
    )
    
    pdf.chapter_subtitle('Dein Aktionsplan fuer die naechsten 7 Tage:')
    pdf.bullet_point('Tag 1: Lies Teil 1 nochmal durch und waehle einen Kommunikationsfehler')
    pdf.bullet_point('Tag 2-3: Uebe die neue Kommunikation (bewusst darauf achten)')
    pdf.bullet_point('Tag 4: Sprich mit deinem Kind ueber Lernmethoden (zeige Mind-Mapping)')
    pdf.bullet_point('Tag 5: Erstelle gemeinsam den ersten Lernplan')
    pdf.bullet_point('Tag 6: Testet Pomodoro mit einem einfachen Thema')
    pdf.bullet_point('Tag 7: Reflektiert gemeinsam: Was hat gut funktioniert?')
    
    pdf.ln(20)
    pdf.set_font('helvetica', 'B', 14)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(0, 10, 'Du schaffst das - gemeinsam!', align='C', new_x="LMARGIN", new_y="NEXT")
    
    pdf.ln(10)
    pdf.set_font('helvetica', 'I', 10)
    pdf.set_text_color(128, 128, 128)
    pdf.multi_cell(0, 5, 
        'Hinweis: Dieser Ratgeber ersetzt keine professionelle Beratung bei '
        'akuten psychischen Problemen. Bei ernsthaften Belastungen wende dich '
        'bitte an einen Kinder- und Jugendpsychotherapeuten.'
    )
    
    # Save PDF
    output_path = '/root/life/elternratgeber-system/pdf/Elternratgeber_PLUS_Lern_Erfolg.pdf'
    pdf.output(output_path)
    print(f"✅ PDF created: {output_path}")
    
    # Check file size
    import os
    size = os.path.getsize(output_path)
    print(f"📄 File size: {size/1024:.1f} KB")
    print(f"📑 Pages: {pdf.page_no()}")

if __name__ == '__main__':
    create_pdf()
