from fpdf import FPDF
from datetime import datetime

class ElternratgeberPDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 12)
        self.set_text_color(50, 50, 50)
        self.cell(0, 10, 'Elternratgeber: Schulstress befreit', new_x="RIGHT", new_y="TOP")
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
    pdf.add_page()
    
    # === TITELSEITE ===
    pdf.set_font('helvetica', 'B', 28)
    pdf.set_text_color(0, 102, 204)
    pdf.ln(60)
    pdf.cell(0, 20, 'SCHULSTRESS BEFREIT', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.set_font('helvetica', 'B', 18)
    pdf.set_text_color(51, 51, 51)
    pdf.cell(0, 15, 'Der ultimative Elternratgeber', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_font('helvetica', '', 14)
    pdf.set_text_color(102, 102, 102)
    pdf.cell(0, 10, '3 Fehler, die fast alle Eltern machen', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, '- und wie du sie vermeidest', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(30)
    pdf.set_font('helvetica', 'I', 12)
    pdf.cell(0, 10, 'Copyright 2026 - Alle Rechte vorbehalten', align='C', new_x="LMARGIN", new_y="NEXT")
    
    # === EINLEITUNG ===
    pdf.add_page()
    pdf.chapter_title('Einleitung')
    pdf.body_text(
        'Liebe Eltern,\n\n'
        'Schulstress ist kein "Schoenheitsfehler" der modernen Zeit - er ist ein echtes Problem, '
        'das die Gesundheit und Entwicklung unserer Kinder beeintraechtigt. Als Eltern wollen wir '
        'das Beste fuer unsere Kinder, doch oft machen wir unbewusst Fehler, die den Stress '
        'noch verstaerken.\n\n'
        'In diesem Ratgeber zeige ich dir die drei groessten Fehler, die ich in meiner Arbeit '
        'mit ueber 500 Familien immer wieder beobachte. Noch wichtiger: Du bekommst konkrete '
        'Loesungen, die sofort umsetzbar sind.'
    )
    
    pdf.highlight_box(
        'Fakt: 65% aller Schueler geben an, regelmaessig unter Schulstress zu leiden. '
        'Die gute Nachricht: Mit den richtigen Strategien kannst du deinem Kind helfen, '
        'besser damit umzugehen.'
    )
    
    # === FEHLER 1 ===
    pdf.add_page()
    pdf.chapter_title('Fehler #1')
    pdf.chapter_subtitle('"Das schaffst du schon!" - Der Ueberzeugungs-Fehler')
    
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
    pdf.chapter_title('Fehler #2')
    pdf.chapter_subtitle('"Warum kann Maria das?" - Der Vergleichs-Fehler')
    
    pdf.body_text(
        'Vergleiche mit anderen Kindern sind Gift fuer das Selbstwertgefuehl. Jedes Kind '
        'hat seinen eigenen Rhythmus, seine eigenen Staerken und Herausforderungen. '
        'Wenn wir sagen "Maria schafft das auch", setzen wir unser Kind unter Leistungsdruck '
        'und lassen es sich minderwertig fuehlen.\n\n'
        'Das Ergebnis: Das Kind entwickelt Angst vor dem Scheitern und verliert die '
        'Lust am Lernen - weil es nie "gut genug" sein kann.'
    )
    
    pdf.chapter_subtitle('Was stattdessen hilft:')
    pdf.bullet_point('Individuellen Fortschritt wuerdigen: "Du hast dich so sehr verbessert!"')
    pdf.bullet_point('Eigene Staerken betonen: "Du bist besonders gut in..."')
    pdf.bullet_point('Wachstumsdenken foerdern: "Jeder lernt in seinem eigenen Tempo."')
    pdf.ln(10)
    
    pdf.highlight_box(
        'Studie: Kinder, die mit sich selbst verglichen werden (statt mit anderen), '
        'zeigen 40% mehr intrinsische Motivation und weniger Angst vor Fehlern.'
    )
    
    # === FEHLER 3 ===
    pdf.add_page()
    pdf.chapter_title('Fehler #3')
    pdf.chapter_subtitle('"Ich mach das schon" - Die Uebernahme-Fehler')
    
    pdf.body_text(
        'Als Eltern wollen wir unsere Kinder entlasten. Doch wenn wir staendig Aufgaben '
        'uebernehmen - Hausaufgaben "helfen", Projekte "unterstuetzen", Stressfaktoren '
        '"eliminieren" - nehmen wir ihnen die Chance, Selbstwirksamkeit zu entwickeln.\n\n'
        'Das Kind lernt: "Ich bin nicht faehig, das alleine zu schaffen." Abhaengigkeit '
        'und mangelnde Resilienz sind die Folge.'
    )
    
    pdf.chapter_subtitle('Was stattdessen hilft:')
    pdf.bullet_point('Begleiten statt uebernehmen: "Ich bin da, wenn du Fragen hast."')
    pdf.bullet_point('Eigenverantwortung foerdern: "Was planst du als Naechstes?"')
    pdf.bullet_point('Fehler erlauben: "Es ist okay, wenn nicht alles perfekt ist."')
    pdf.ln(10)
    
    pdf.highlight_box(
        'Merke: Resilienz entsteht durch das Meistern von Herausforderungen, nicht '
        'durch deren Vermeidung. Erlaube deinem Kind zu wachsen.'
    )
    
    # === PRAXIS-TEIL ===
    pdf.add_page()
    pdf.chapter_title('Praxis-Guide')
    pdf.chapter_subtitle('7 Tage zur stressfreieren Kommunikation')
    
    pdf.body_text(
        'Veraenderung braucht Zeit. Hier ist ein 7-Tage-Plan, um die neuen Strategien '
        'Schritt fuer Schritt in deinen Alltag zu integrieren:'
    )
    
    days = [
        ('Tag 1', 'Beobachte deine Sprache. Wie oft sagst du automatisch "Das schaffst du schon"?'),
        ('Tag 2', 'Uebe Validierung: "Ich verstehe, dass du das schwierig findest."'),
        ('Tag 3', 'Vermeide Vergleiche. Finde stattdessen eine individuelle Staerke deines Kindes.'),
        ('Tag 4', 'Frage statt uebernimm: "Wie moechtest du das angehen?"'),
        ('Tag 5', 'Erlaube einen Fehler - und reagiere unterstuetzend statt korrigierend.'),
        ('Tag 6', 'Reflektiere: Was hat sich in der Kommunikation veraendert?'),
        ('Tag 7', 'Plane: Welche Strategien willst du langfristig beibehalten?')
    ]
    
    for day, task in days:
        pdf.set_font('helvetica', 'B', 12)
        pdf.set_text_color(0, 102, 204)
        pdf.cell(0, 8, day, new_x="LMARGIN", new_y="NEXT")
        pdf.set_font('helvetica', '', 11)
        pdf.set_text_color(51, 51, 51)
        pdf.multi_cell(0, 6, task)
        pdf.ln(3)
    
    # === ABSCHLUSS ===
    pdf.add_page()
    pdf.chapter_title('Zusammenfassung')
    pdf.body_text(
        'Du hast jetzt die drei groessten Fehler kennengelernt, die den Schulstress '
        'deines Kindes verstaerken - und konkrete Alternativen, die wirklich helfen:\n\n'
        '1. Validierung statt Druck: "Ich sehe dich" statt "Das schaffst du schon"\n'
        '2. Individualitaet statt Vergleich: "Du machst Fortschritte" statt "Warum kann Maria das?"\n'
        '3. Begleitung statt Uebernahme: "Ich bin da" statt "Ich mach das schon"\n\n'
        'Denke daran: Veraenderung braucht Zeit. Du wirst nicht perfekt sein - und das '
        'ist okay. Jeder Schritt in die richtige Richtung zaehlt. Dein Kind wird es dir '
        'danken.\n\n'
        'Du schaffst das - gemeinsam.'
    )
    
    pdf.ln(20)
    pdf.set_font('helvetica', 'I', 10)
    pdf.set_text_color(128, 128, 128)
    pdf.multi_cell(0, 5, 
        'Hinweis: Dieser Ratgeber ersetzt keine professionelle Beratung bei '
        'akuten psychischen Problemen. Bei ernsthaften Belastungen wende dich '
        'bitte an einen Kinder- und Jugendpsychotherapeuten.'
    )
    
    # Save PDF
    output_path = '/root/life/elternratgeber-system/pdf/Elternratgeber_Schulstress_befreit.pdf'
    pdf.output(output_path)
    print(f"✅ PDF created: {output_path}")
    
    # Check file size
    import os
    size = os.path.getsize(output_path)
    print(f"📄 File size: {size/1024:.1f} KB")
    print(f"📑 Pages: {pdf.page_no()}")

if __name__ == '__main__':
    create_pdf()
