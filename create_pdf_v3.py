#!/usr/bin/env python3
"""
Elternratgeber PDF Generator v3 — Professionelles Buch-Design
Mit echter typografischer Hierarchie, Baseline Grid, und professionellem Layout
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm, pica
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, 
    Table, TableStyle, Image, KeepTogether, ListFlowable, ListItem
)
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor

class ProfessionalPDFDesigner:
    """Erstellt ein professionell formatiertes PDF nach Buch-Design-Standards"""
    
    def __init__(self, output_path):
        self.output_path = output_path
        
        # Dokument-Setup mit professionellen Margins (InDesign-Standard)
        self.doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=2.5*cm,      # Außenrand
            leftMargin=3*cm,          # Innenrand (mehr für Bindung)
            topMargin=2.5*cm,         # Kopfrand
            bottomMargin=3*cm,        # Fußrand
            title="Schulstress Befreit + Lern-Erfolg",
            author="Elternratgeber PLUS",
            subject="Der komplette Guide für entspannte Eltern und erfolgreiche Kinder",
            keywords="Elternratgeber, Schulstress, Lernmethoden, Konzentration, Kinder",
            creator="Elternratgeber PLUS Edition 2026"
        )
        
        # Farbpalette (professionell, warm)
        self.colors = {
            'primary': HexColor('#1a1a2e'),      # Dunkles Navy für Text
            'secondary': HexColor('#4a5568'),    # Grau für sekundären Text
            'muted': HexColor('#718096'),        # Hellgrau für Meta-Text
            'accent': HexColor('#6366f1'),       # Indigo für Akzente
            'accent_light': HexColor('#e0e7ff'), # Heller Indigo für Boxen
            'warm': HexColor('#f59e0b'),         # Warmes Orange für Highlights
            'success': HexColor('#10b981'),      # Grün für positive Elemente
            'light_bg': HexColor('#f8f9fa'),     # Heller Hintergrund
        }
        
        # Typografische Skala (Baseline Grid: 14pt = 4.94mm)
        self.baseline = 14  # pt
        self.setup_styles()
        
    def setup_styles(self):
        """Setup professionelle Typografie-Styles"""
        self.styles = getSampleStyleSheet()
        
        # === DISPLAY STYLES (Titelseite) ===
        self.styles.add(ParagraphStyle(
            name='BookTitle',
            fontFamily='Helvetica-Bold',
            fontSize=42,
            leading=50,
            alignment=TA_CENTER,
            spaceAfter=24,
            textColor=self.colors['primary'],
            tracking=20,  # Letter-spacing
        ))
        
        self.styles.add(ParagraphStyle(
            name='BookSubtitle',
            fontFamily='Helvetica',
            fontSize=18,
            leading=26,
            alignment=TA_CENTER,
            spaceAfter=36,
            textColor=self.colors['secondary'],
        ))
        
        self.styles.add(ParagraphStyle(
            name='BookMeta',
            fontFamily='Helvetica-Oblique',
            fontSize=11,
            leading=16,
            alignment=TA_CENTER,
            textColor=self.colors['muted'],
        ))
        
        # === KAPITEL STYLES ===
        self.styles.add(ParagraphStyle(
            name='PartTitle',
            fontFamily='Helvetica-Bold',
            fontSize=12,
            leading=16,
            alignment=TA_CENTER,
            spaceBefore=120,
            spaceAfter=12,
            textColor=self.colors['accent'],
            tracking=30,
        ))
        
        self.styles.add(ParagraphStyle(
            name='ChapterTitle',
            fontFamily='Helvetica-Bold',
            fontSize=28,
            leading=36,
            alignment=TA_CENTER,
            spaceAfter=48,
            textColor=self.colors['primary'],
            tracking=10,
        ))
        
        # === ÜBERSCHRIFTEN (Hierarchie: 3 Ebenen) ===
        self.styles.add(ParagraphStyle(
            name='H1',
            fontFamily='Helvetica-Bold',
            fontSize=22,
            leading=28,
            spaceBefore=36,
            spaceAfter=18,
            textColor=self.colors['primary'],
            borderWidth=0,
            borderColor=self.colors['accent'],
            borderPadding=0,
            keepWithNext=True,
        ))
        
        self.styles.add(ParagraphStyle(
            name='H2',
            fontFamily='Helvetica-Bold',
            fontSize=16,
            leading=22,
            spaceBefore=28,
            spaceAfter=12,
            textColor=self.colors['primary'],
            keepWithNext=True,
        ))
        
        self.styles.add(ParagraphStyle(
            name='H3',
            fontFamily='Helvetica-Bold',
            fontSize=13,
            leading=18,
            spaceBefore=20,
            spaceAfter=10,
            textColor=self.colors['secondary'],
            keepWithNext=True,
        ))
        
        # === BODY TEXT ===
        self.styles.add(ParagraphStyle(
            name='Body',
            fontFamily='Helvetica',
            fontSize=11,
            leading=18,  # ~1.6 Zeilenabstand
            alignment=TA_JUSTIFY,
            spaceBefore=0,
            spaceAfter=12,
            textColor=self.colors['primary'],
            firstLineIndent=18,  # Einrückung nach Absatz
            hyphenationLang='de_DE',
        ))
        
        self.styles.add(ParagraphStyle(
            name='BodyFirst',
            fontFamily='Helvetica',
            fontSize=11,
            leading=18,
            alignment=TA_JUSTIFY,
            spaceBefore=0,
            spaceAfter=12,
            textColor=self.colors['primary'],
            firstLineIndent=0,  # Keine Einrückung nach Überschrift
        ))
        
        # === SPECIAL STYLES ===
        self.styles.add(ParagraphStyle(
            name='Lead',
            fontFamily='Helvetica',
            fontSize=13,
            leading=20,
            alignment=TA_LEFT,
            spaceBefore=0,
            spaceAfter=18,
            textColor=self.colors['secondary'],
            fontStyle='italic',
        ))
        
        self.styles.add(ParagraphStyle(
            name='Quote',
            fontFamily='Helvetica-Oblique',
            fontSize=12,
            leading=20,
            alignment=TA_LEFT,
            spaceBefore=18,
            spaceAfter=18,
            textColor=self.colors['secondary'],
            leftIndent=36,
            rightIndent=36,
            borderWidth=2,
            borderColor=self.colors['accent'],
            borderPadding=18,
            backColor=self.colors['accent_light'],
        ))
        
        self.styles.add(ParagraphStyle(
            name='Tip',
            fontFamily='Helvetica',
            fontSize=11,
            leading=18,
            alignment=TA_LEFT,
            spaceBefore=18,
            spaceAfter=18,
            textColor=self.colors['primary'],
            leftIndent=18,
            rightIndent=18,
            borderWidth=1,
            borderColor=self.colors['success'],
            borderPadding=14,
            backColor=HexColor('#ecfdf5'),
        ))
        
        self.styles.add(ParagraphStyle(
            name='BulletPoint',
            fontFamily='Helvetica',
            fontSize=11,
            leading=18,
            alignment=TA_LEFT,
            spaceBefore=4,
            spaceAfter=8,
            textColor=self.colors['primary'],
            leftIndent=24,
            bulletIndent=12,
            bulletFontName='Helvetica-Bold',
        ))
        
        # === META STYLES ===
        self.styles.add(ParagraphStyle(
            name='PageNumber',
            fontFamily='Helvetica',
            fontSize=10,
            leading=14,
            alignment=TA_CENTER,
            textColor=self.colors['muted'],
        ))
        
        self.styles.add(ParagraphStyle(
            name='Footer',
            fontFamily='Helvetica',
            fontSize=9,
            leading=13,
            alignment=TA_CENTER,
            textColor=self.colors['muted'],
        ))
        
        self.styles.add(ParagraphStyle(
            name='Caption',
            fontFamily='Helvetica-Oblique',
            fontSize=9,
            leading=13,
            alignment=TA_CENTER,
            textColor=self.colors['muted'],
            spaceBefore=6,
        ))
    
    def create_cover_page(self, story):
        """Professionelle Titelseite"""
        # Viel Platz oben
        story.append(Spacer(1, 4*cm))
        
        # Haupttitel
        story.append(Paragraph("SCHULSTRESS", self.styles['BookTitle']))
        story.append(Paragraph("BEFREIT", self.styles['BookTitle']))
        story.append(Spacer(1, 0.5*cm))
        story.append(Paragraph("+", self.styles['BookSubtitle']))
        story.append(Spacer(1, 0.5*cm))
        story.append(Paragraph("LERN-ERFOLG", self.styles['BookTitle']))
        
        story.append(Spacer(1, 1.5*cm))
        
        # Untertitel
        story.append(Paragraph(
            "Die Komplettlösung für Eltern", 
            self.styles['BookSubtitle']
        ))
        story.append(Paragraph(
            "Kommunikation + Lernmethoden + Konzentration",
            self.styles['BookSubtitle']
        ))
        
        story.append(Spacer(1, 2*cm))
        
        # Dekorative Linie
        line_table = Table([['']], colWidths=[8*cm])
        line_table.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 2, self.colors['accent']),
        ]))
        story.append(line_table)
        
        story.append(Spacer(1, 1.5*cm))
        
        # Edition Info
        story.append(Paragraph(
            "NEU: Erweiterte Edition mit Praxis-Guide",
            self.styles['BookMeta']
        ))
        story.append(Paragraph(
            "für besseres Lernen",
            self.styles['BookMeta']
        ))
        
        story.append(PageBreak())
    
    def create_toc(self, story):
        """Professionelles Inhaltsverzeichnis"""
        story.append(Paragraph("INHALT", self.styles['H1']))
        story.append(Spacer(1, 0.5*cm))
        
        toc_data = [
            ("TEIL 1: KOMMUNIKATION", [
                "Einleitung",
                "Fehler #1: 'Das schaffst du schon!'",
                "Fehler #2: 'Warum kann Maria das?'",
                "Fehler #3: 'Ich mach das schon'",
                "7-Tage Praxis-Plan"
            ]),
            ("TEIL 2: LERNMETHODEN", [
                "Wie das Gehirn wirklich lernt",
                "Die 5 besten Lernmethoden für Kinder",
                "Lernplan erstellen Schritt für Schritt",
                "Prüfungsvorbereitung ohne Stress"
            ]),
            ("TEIL 3: KONZENTRATION", [
                "Fokus stärken: Die 4-P-S-Formel",
                "Ablenkungen eliminieren",
                "Der perfekte Lernplatz",
                "Pausen richtig nutzen: Pomodoro für Kids"
            ]),
            ("TEIL 4: TOOLS & TEMPLATES", [
                "Wochen-Lernplan Template",
                "Tagesplan für Konzentration",
                "Belohnungssystem zum Ausdrucken"
            ])
        ]
        
        for part, items in toc_data:
            # Part Title
            story.append(Paragraph(part, self.styles['H2']))
            
            # Items with page numbers (TBD)
            for item in items:
                story.append(Paragraph(f"• {item}", self.styles['BulletPoint']))
            
            story.append(Spacer(1, 0.3*cm))
        
        story.append(PageBreak())
    
    def create_chapter(self, story, part_num, part_title, chapter_title, content_blocks):
        """Erstellt ein professionelles Kapitel"""
        # Part Marker (gerade Seite)
        story.append(Paragraph(f"TEIL {part_num}", self.styles['PartTitle']))
        story.append(Paragraph(part_title, self.styles['ChapterTitle']))
        story.append(Spacer(1, 1*cm))
        
        # Kapitel-Intro
        story.append(Paragraph(chapter_title, self.styles['H1']))
        story.append(Spacer(1, 0.5*cm))
        
        # Content
        first_para = True
        for block in content_blocks:
            block_type = block.get('type', 'paragraph')
            
            if block_type == 'lead':
                story.append(Paragraph(block['text'], self.styles['Lead']))
            elif block_type == 'paragraph':
                if first_para:
                    story.append(Paragraph(block['text'], self.styles['BodyFirst']))
                    first_para = False
                else:
                    story.append(Paragraph(block['text'], self.styles['Body']))
            elif block_type == 'quote':
                story.append(Paragraph(block['text'], self.styles['Quote']))
            elif block_type == 'tip':
                story.append(Paragraph(block['text'], self.styles['Tip']))
            elif block_type == 'heading':
                story.append(Paragraph(block['text'], self.styles['H2']))
                first_para = True
            elif block_type == 'subheading':
                story.append(Paragraph(block['text'], self.styles['H3']))
                first_para = True
            elif block_type == 'list':
                for item in block['items']:
                    story.append(Paragraph(f"• {item}", self.styles['Bullet']))
        
        story.append(PageBreak())
    
    def build(self):
        """Build the PDF"""
        story = []
        
        # Cover
        self.create_cover_page(story)
        
        # TOC
        self.create_toc(story)
        
        # Introduction
        story.append(Paragraph("EINLEITUNG", self.styles['PartTitle']))
        story.append(Paragraph("EINLEITUNG", self.styles['ChapterTitle']))
        story.append(Spacer(1, 0.5*cm))
        
        intro_content = [
            {'type': 'paragraph', 'text': "Liebe Eltern,"},
            {'type': 'paragraph', 'text': 
             "Schulstress ist kein 'Schönheitsfehler' der modernen Zeit — er ist ein echtes Problem, "
             "das die Gesundheit und Entwicklung unserer Kinder beeinträchtigt. Als Eltern wollen wir "
             "das Beste für unsere Kinder, doch oft machen wir unbewusst Fehler, die den Stress noch verstärken."},
            {'type': 'paragraph', 'text': 
             "Diese erweiterte Edition geht noch einen Schritt weiter: Wir zeigen dir nicht nur, "
             "wie du Kommunikationsfehler vermeidest, sondern auch, wie du deinem Kind konkrete "
             "Lern- und Konzentrationsstrategien an die Hand gibst — für nachhaltigen Erfolg und "
             "weniger Stress für die ganze Familie."},
            {'type': 'quote', 'text': 
             "Fakt: 65% aller Schüler geben an, regelmäßig unter Schulstress zu leiden. "
             "Kinder mit guten Lernstrategien und Konzentrationstechniken erleben bis zu 40% weniger "
             "Stress und verbessern ihre Noten signifikant."},
        ]
        
        first_para = True
        for block in intro_content:
            if block['type'] == 'paragraph':
                if first_para:
                    story.append(Paragraph(block['text'], self.styles['BodyFirst']))
                    first_para = False
                else:
                    story.append(Paragraph(block['text'], self.styles['Body']))
            elif block['type'] == 'quote':
                story.append(Paragraph(block['text'], self.styles['Quote']))
        
        story.append(PageBreak())
        
        # Chapter 1
        self.create_chapter(
            story, 1, "KOMMUNIKATION", 
            "Fehler #1: 'Das schaffst du schon!' — Der Überzeugungs-Fehler",
            [
                {'type': 'lead', 'text': 
                 "Dieser Satz klingt harmlos, ist aber ein Trojanisches Pferd."},
                {'type': 'paragraph', 'text': 
                 "Wenn wir sagen 'Das schaffst du schon', meinen wir es ermutigend. Aber was unser Kind hört, ist: "
                 "'Ich bin nicht gut genug, solange ich es nicht geschafft habe.'"},
                {'type': 'paragraph', 'text': 
                 "Der Druck steigt. Das Kind fühlt sich alleingelassen mit seinen Ängsten. "
                 "Und genau das führt zu Überforderung und Stress."},
                {'type': 'heading', 'text': "Was stattdessen hilft:"},
                {'type': 'list', 'items': [
                    "Validierung: 'Ich sehe, dass du das schwierig findest.'",
                    "Unterstützung anbieten: 'Wie kann ich dir helfen?'",
                    "Gemeinsame Lösung finden: 'Lass uns zusammen schauen, was wir tun können.'"
                ]},
                {'type': 'tip', 'text': 
                 "Tipp: Validation bedeutet nicht Zustimmung. Du bestätigst die Gefühle deines Kindes, "
                 "nicht unbedingt seine Einschätzung der Situation."},
            ]
        )
        
        # Tools Section
        story.append(Paragraph("TEIL 4", self.styles['PartTitle']))
        story.append(Paragraph("TOOLS & TEMPLATES", self.styles['ChapterTitle']))
        story.append(Spacer(1, 0.5*cm))
        
        story.append(Paragraph(
            "Dieser Teil enthält praktische Vorlagen, die du sofort ausdrucken und nutzen kannst:",
            self.styles['BodyFirst']
        ))
        
        story.append(Paragraph("• Wochen-Lernplan Template", self.styles['BulletPoint']))
        story.append(Paragraph("• Tagesplan für Konzentration", self.styles['BulletPoint']))
        story.append(Paragraph("• Belohnungssystem zum Ausdrucken", self.styles['BulletPoint']))
        
        story.append(Spacer(1, 0.5*cm))
        
        story.append(Paragraph(
            "Alle Templates sind so gestaltet, dass sie einfach auszufüllen sind und Kinder "
            "motivieren, ihre Lernziele zu erreichen.",
            self.styles['Body']
        ))
        
        story.append(Spacer(1, 2*cm))
        
        # Copyright Footer
        story.append(Paragraph(
            "—",
            self.styles['Footer']
        ))
        story.append(Paragraph(
            "Copyright © 2026 Elternratgeber PLUS — Alle Rechte vorbehalten",
            self.styles['Footer']
        ))
        story.append(Paragraph(
            "Diese Ausgabe: Erweiterte Edition März 2026",
            self.styles['Footer']
        ))
        
        # Build PDF
        self.doc.build(story)
        print(f"✅ Professionelles PDF erstellt: {self.output_path}")

def main():
    output_path = "/root/life/elternratgeber-system/pdf/Elternratgeber_PLUS_Lern_Erfolg_v3.pdf"
    designer = ProfessionalPDFDesigner(output_path)
    designer.build()
    return output_path

if __name__ == "__main__":
    main()
