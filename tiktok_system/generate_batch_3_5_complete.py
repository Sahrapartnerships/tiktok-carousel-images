#!/usr/bin/env python3
"""
Generate TikTok Carousel Images - Batch 3-5 Combined (Themes 11-20)
50 images total: 10 themes × 5 slides each
Uses fal.ai FLUX Dev API (cost: $1.25 total for 50 images)

Themes:
11: "5 Erziehungsfehler die Konzentration zerstören"
12: "Warum Kinder beim Lernen träumen"
13: "Der 5-Minuten-Trick für mehr Fokus"
14: "Wie du dein Kind für Lernen begeisterst"
15: "Der ideale Lernplatz zu Hause"
16: "Wann ist das Gehirn am leistungsfähigsten"
17: "Warum Pausen beim Lernen wichtig sind"
18: "Wie du Lernstress erkennst"
19: "Die beste Tageszeit für Hausaufgaben"
20: "5 Sätze die motivieren statt drängen"
"""

import os
import re
import urllib.request
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

# Setup
BASE_DIR = Path('/root/life/elternratgeber-system/tiktok_carousels')
OUTPUT_DIRS = {
    'batch_3': BASE_DIR / 'batch_3',
    'batch_4': BASE_DIR / 'batch_4',
    'batch_5': BASE_DIR / 'batch_5'
}
for d in OUTPUT_DIRS.values():
    d.mkdir(parents=True, exist_ok=True)

# Load FAL credentials
with open(os.path.expanduser('~/.fal-credentials')) as f:
    content = f.read()
    match = re.search(r'export FAL_KEY="([^"]+)"', content)
    if match:
        os.environ['FAL_KEY'] = match.group(1)

import fal_client

# Style Constants
STYLE = {
    'text_color': '#2D3436',
    'accent_color': '#E17055',
    'accent_green': '#00B894',
    'accent_blue': '#0984E3',
    'accent_purple': '#6C5CE7',
    'accent_teal': '#00CEC9',
    'accent_pink': '#FD79A8',
    'white': '#FFFFFF',
    'shadow': '#00000040'
}

# Style prompt for flat vector illustration with warm pastel colors
STYLE_PREFIX = "Flat vector illustration, warm pastel colors, minimalist editorial style, soft lighting, clean composition, professional graphic design"
STYLE_SUFFIX = "Generous empty space at top for text overlay, warm beige and soft coral color palette, modern minimalist aesthetic"

# ============================================================
# THEME 11: "5 Erziehungsfehler die Konzentration zerstören"
# ============================================================
THEME_11_SLIDES = [
    {
        'filename': '11_fehler_01_hook.png',
        'prompt': f'{STYLE_PREFIX}. A concerned parent watching child struggling to focus on homework, surrounded by digital distractions like phone notifications and TV. Emotional but hopeful atmosphere. {STYLE_SUFFIX}',
        'theme': '11_fehler',
        'slide_num': 1,
        'batch': 'batch_3',
        'text': {
            'headline': ['5 Erziehungsfehler', 'die Konzentration zerstören'],
            'body': 'Vermeide diese häufigen Fehler',
            'body2': 'für mehr Fokus beim Lernen!'
        }
    },
    {
        'filename': '11_fehler_02_multitasking.png',
        'prompt': f'{STYLE_PREFIX}. Visual metaphor of multitasking chaos - child trying to do homework while eating, watching TV, and phone buzzing. Fragmented attention concept. {STYLE_SUFFIX}',
        'theme': '11_fehler',
        'slide_num': 2,
        'batch': 'batch_3',
        'text': {
            'headline': ['Fehler #1: Multitasking', '📱💻📺'],
            'body': 'Zu viele Reize auf einmal',
            'body2': 'zerstreuen den Fokus komplett'
        }
    },
    {
        'filename': '11_fehler_03_zeitdruck.png',
        'prompt': f'{STYLE_PREFIX}. Parent looking at watch with worried expression while child struggles with homework, clock showing late hour, stress atmosphere. {STYLE_SUFFIX}',
        'theme': '11_fehler',
        'slide_num': 3,
        'batch': 'batch_3',
        'text': {
            'headline': ['Fehler #2: Zeitdruck', '⏰😰'],
            'body': '"Beeil dich!" blockiert',
            'body2': 'das Gehirn statt es zu aktivieren'
        }
    },
    {
        'filename': '11_fehler_04_vergleich.png',
        'prompt': f'{STYLE_PREFIX}. Child looking sad while parent compares them to sibling or classmate, speech bubbles showing comparison text, emotional impact. {STYLE_SUFFIX}',
        'theme': '11_fehler',
        'slide_num': 4,
        'batch': 'batch_3',
        'text': {
            'headline': ['Fehler #3: Vergleiche', '🙅‍♀️'],
            'body': '"Warum schafft Anna das?"',
            'body2': 'untergräbt Selbstvertrauen'
        }
    },
    {
        'filename': '11_fehler_05_loesung.png',
        'prompt': f'{STYLE_PREFIX}. Positive scene: Parent and child working together peacefully, organized desk, focused atmosphere, warm supportive interaction. {STYLE_SUFFIX}',
        'theme': '11_fehler',
        'slide_num': 5,
        'batch': 'batch_3',
        'text': {
            'headline': ['Die Lösung ✨', 'Bewusst anders machen'],
            'body': 'Eine Sache nach der anderen',
            'body2': 'Ruhig bleiben & ermutigen!'
        }
    }
]

# ============================================================
# THEME 12: "Warum Kinder beim Lernen träumen"
# ============================================================
THEME_12_SLIDES = [
    {
        'filename': '12_traeumen_01_hook.png',
        'prompt': f'{STYLE_PREFIX}. Child staring out window daydreaming instead of doing homework, dreamy expression, thought bubbles showing imagination, soft lighting. {STYLE_SUFFIX}',
        'theme': '12_traeumen',
        'slide_num': 1,
        'batch': 'batch_3',
        'text': {
            'headline': ['Warum Kinder beim', 'Lernen träumen 🌤️'],
            'body': 'Das Gehirn braucht Pausen',
            'body2': 'um Informationen zu verarbeiten'
        }
    },
    {
        'filename': '12_traeumen_02_gehirn.png',
        'prompt': f'{STYLE_PREFIX}. Stylized brain illustration showing active and resting zones, neural connections, daydreaming mode visualization, scientific but warm. {STYLE_SUFFIX}',
        'theme': '12_traeumen',
        'slide_num': 2,
        'batch': 'batch_3',
        'text': {
            'headline': ['Das Gehirn arbeitet', 'auch in der Pause 🧠'],
            'body': 'Tagträumen = aktive',
            'body2': 'Verarbeitungsphase!'
        }
    },
    {
        'filename': '12_traeumen_03_kreativ.png',
        'prompt': f'{STYLE_PREFIX}. Child having creative ideas while daydreaming, lightbulb moments, imagination and creativity flowing, positive visualization. {STYLE_SUFFIX}',
        'theme': '12_traeumen',
        'slide_num': 3,
        'batch': 'batch_3',
        'text': {
            'headline': ['Kreativität braucht', 'Raum 💡'],
            'body': 'Träumen fördert',
            'body2': 'kreative Problemlösung'
        }
    },
    {
        'filename': '12_traeumen_04_erholung.png',
        'prompt': f'{STYLE_PREFIX}. Child taking a proper break, looking out window peacefully, recharging energy, balanced study rhythm visualization. {STYLE_SUFFIX}',
        'theme': '12_traeumen',
        'slide_num': 4,
        'batch': 'batch_3',
        'text': {
            'headline': ['Geplante Pausen', 'statt Ablenkung ☕'],
            'body': '5 Minuten weggucken',
            'body2': 'ist erlaubt & wichtig!'
        }
    },
    {
        'filename': '12_traeumen_05_balance.png',
        'prompt': f'{STYLE_PREFIX}. Balanced scene showing focused work and peaceful breaks in harmony, child productive and happy, ideal learning rhythm. {STYLE_SUFFIX}',
        'theme': '12_traeumen',
        'slide_num': 5,
        'batch': 'batch_3',
        'text': {
            'headline': ['Die perfekte Balance ⚖️', 'Fokus + Pausen'],
            'body': '25 Min Arbeit, 5 Min Pause',
            'body2': 'Pomodoro-Technik!'
        }
    }
]

# ============================================================
# THEME 13: "Der 5-Minuten-Trick für mehr Fokus"
# ============================================================
THEME_13_SLIDES = [
    {
        'filename': '13_5min_01_hook.png',
        'prompt': f'{STYLE_PREFIX}. Giant number "5" as hero element, child starting homework with timer, sense of beginning small, motivational atmosphere. {STYLE_SUFFIX}',
        'theme': '13_5min',
        'slide_num': 1,
        'batch': 'batch_3',
        'text': {
            'headline': ['Der 5-Minuten-Trick', 'für mehr Fokus ⏱️'],
            'body': 'Nur 5 Minuten anfangen',
            'body2': 'Der Rest kommt von allein!'
        }
    },
    {
        'filename': '13_5min_02_start.png',
        'prompt': f'{STYLE_PREFIX}. Child setting a small timer for 5 minutes, minimal commitment, easy start concept, overcoming procrastination. {STYLE_SUFFIX}',
        'theme': '13_5min',
        'slide_num': 2,
        'batch': 'batch_3',
        'text': {
            'headline': ['Schritt 1:', 'Timer auf 5 Min 🎯'],
            'body': '"Nur 5 Minuten, das',
            'body2': 'schaffe ich locker!"'
        }
    },
    {
        'filename': '13_5min_03_flow.png',
        'prompt': f'{STYLE_PREFIX}. Child continuing past the 5 minutes, getting into flow state, momentum building, focused and engaged. {STYLE_SUFFIX}',
        'theme': '13_5min',
        'slide_num': 3,
        'batch': 'batch_3',
        'text': {
            'headline': ['Schritt 2:', 'Flow übernehmt 🌊'],
            'body': 'Nach 5 Minuten läuft es',
            'body2': 'oft von allein weiter'
        }
    },
    {
        'filename': '13_5min_04_fertig.png',
        'prompt': f'{STYLE_PREFIX}. Child completing homework with satisfaction, checkmarks and progress visible, sense of accomplishment. {STYLE_SUFFIX}',
        'theme': '13_5min',
        'slide_num': 4,
        'batch': 'batch_3',
        'text': {
            'headline': ['Schritt 3:', 'Aufgabe erledigt ✅'],
            'body': 'Der schwierigste Teil?',
            'body2': 'Der Anfang!'
        }
    },
    {
        'filename': '13_5min_05_gewohnheit.png',
        'prompt': f'{STYLE_PREFIX}. Child building a habit chain, multiple 5-minute sessions connected, consistency visualization, habit formation concept. {STYLE_SUFFIX}',
        'theme': '13_5min',
        'slide_num': 5,
        'batch': 'batch_3',
        'text': {
            'headline': ['Gewohnheit bilden 🔄', 'Jeden Tag 5 Minuten'],
            'body': 'Kleine Schritte führen',
            'body2': 'zu großen Erfolgen!'
        }
    }
]

# ============================================================
# THEME 14: "Wie du dein Kind für Lernen begeisterst"
# ============================================================
THEME_14_SLIDES = [
    {
        'filename': '14_begeistern_01_hook.png',
        'prompt': f'{STYLE_PREFIX}. Excited child discovering something interesting in a book, spark of curiosity, magical moment of learning, warm atmosphere. {STYLE_SUFFIX}',
        'theme': '14_begeistern',
        'slide_num': 1,
        'batch': 'batch_3',
        'text': {
            'headline': ['Wie du dein Kind', 'für Lernen begeisterst 🚀'],
            'body': 'Neugier wecken statt',
            'body2': 'Zwang ausüben'
        }
    },
    {
        'filename': '14_begeistern_02_neugier.png',
        'prompt': f'{STYLE_PREFIX}. Parent asking open questions, child thinking with curious expression, question marks floating, inquiry-based learning. {STYLE_SUFFIX}',
        'theme': '14_begeistern',
        'slide_num': 2,
        'batch': 'batch_3',
        'text': {
            'headline': ['Fragen statt', 'Erklären ❓'],
            'body': '"Was glaubst du,',
            'body2': 'warum das so ist?"'
        }
    },
    {
        'filename': '14_begeistern_03_verknuepfen.png',
        'prompt': f'{STYLE_PREFIX}. Child connecting learning to real world - math in cooking, science in nature, practical applications visualization. {STYLE_SUFFIX}',
        'theme': '14_begeistern',
        'slide_num': 3,
        'batch': 'batch_3',
        'text': {
            'headline': ['Mit dem Alltag', 'verknüpfen 🌍'],
            'body': 'Mathe beim Backen,',
            'body2': 'Physik beim Sport'
        }
    },
    {
        'filename': '14_begeistern_04_erfolg.png',
        'prompt': f'{STYLE_PREFIX}. Child celebrating small learning wins, progress visible, parent acknowledging effort not just results, positive reinforcement. {STYLE_SUFFIX}',
        'theme': '14_begeistern',
        'slide_num': 4,
        'batch': 'batch_3',
        'text': {
            'headline': ['Kleine Erfolge', 'feiern 🎉'],
            'body': 'Auf Anstrengung achten',
            'body2': 'nicht nur auf Ergebnisse'
        }
    },
    {
        'filename': '14_begeistern_05_autonomie.png',
        'prompt': f'{STYLE_PREFIX}. Child choosing what to learn, autonomy and self-direction, empowered student making choices, independence visualization. {STYLE_SUFFIX}',
        'theme': '14_begeistern',
        'slide_num': 5,
        'batch': 'batch_3',
        'text': {
            'headline': ['Wahl geben 🎯', 'Autonomie stärkt'],
            'body': '"Welches Fach zuerst?"',
            'body2': 'Selbst entscheiden lassen!'
        }
    }
]

# ============================================================
# THEME 15: "Der ideale Lernplatz zu Hause"
# ============================================================
THEME_15_SLIDES = [
    {
        'filename': '15_lernplatz_01_hook.png',
        'prompt': f'{STYLE_PREFIX}. Perfect home study setup overview, organized desk in quiet corner, good lighting, plants, ideal learning environment. {STYLE_SUFFIX}',
        'theme': '15_lernplatz',
        'slide_num': 1,
        'batch': 'batch_3',
        'text': {
            'headline': ['Der ideale Lernplatz', 'zu Hause 🏠'],
            'body': 'So schaffst du den',
            'body2': 'perfekten Lern-Spot!'
        }
    },
    {
        'filename': '15_lernplatz_02_licht.png',
        'prompt': f'{STYLE_PREFIX}. Study area with excellent lighting, natural light from window plus desk lamp, bright but not glaring, eye-friendly setup. {STYLE_SUFFIX}',
        'theme': '15_lernplatz',
        'slide_num': 2,
        'batch': 'batch_3',
        'text': {
            'headline': ['Tipp 1: Gutes Licht 💡', 'Augenschonend'],
            'body': 'Tageslicht + Lampe links',
            'body2': '(für Rechtshänder)'
        }
    },
    {
        'filename': '15_lernplatz_03_geraeusche.png',
        'prompt': f'{STYLE_PREFIX}. Quiet study zone, noise-cancelling concept, peaceful atmosphere, visual representation of silence and focus. {STYLE_SUFFIX}',
        'theme': '15_lernplatz',
        'slide_num': 3,
        'batch': 'batch_3',
        'text': {
            'headline': ['Tipp 2: Ruhe 🤫', 'Abgeschotteter Bereich'],
            'body': 'Kein TV, kein Trubel',
            'body2': 'Kopfhörer optional'
        }
    },
    {
        'filename': '15_lernplatz_04_material.png',
        'prompt': f'{STYLE_PREFIX}. Organized study materials, pens in cups, books on shelf, everything in its place, tidy but accessible, minimal clutter. {STYLE_SUFFIX}',
        'theme': '15_lernplatz',
        'slide_num': 4,
        'batch': 'batch_3',
        'text': {
            'headline': ['Tipp 3: Ordnung 📚', 'Alles griffbereit'],
            'body': 'Nur notwendiges Material',
            'body2': 'Ablenkung wegräumen'
        }
    },
    {
        'filename': '15_lernplatz_05_persoenlich.png',
        'prompt': f'{STYLE_PREFIX}. Personalized study space with childs own touches, favorite colors, motivation quotes, sense of ownership and comfort. {STYLE_SUFFIX}',
        'theme': '15_lernplatz',
        'slide_num': 5,
        'batch': 'batch_3',
        'text': {
            'headline': ['Tipp 4: Persönlich 🎨', 'Eigener Stil'],
            'body': 'Lieblingsfarbe, Pflanze,',
            'body2': 'Motivationsbild'
        }
    }
]

# ============================================================
# THEME 16: "Wann ist das Gehirn am leistungsfähigsten"
# ============================================================
THEME_16_SLIDES = [
    {
        'filename': '16_gehirn_01_hook.png',
        'prompt': f'{STYLE_PREFIX}. Brain as hero element, clock showing different times, peak performance concept, biological rhythms visualization. {STYLE_SUFFIX}',
        'theme': '16_gehirn',
        'slide_num': 1,
        'batch': 'batch_4',
        'text': {
            'headline': ['Wann ist das Gehirn', 'am leistungsfähigsten? 🧠'],
            'body': 'Nutze die natürlichen',
            'body2': 'Hochleistungszeiten!'
        }
    },
    {
        'filename': '16_gehirn_02_morgen.png',
        'prompt': f'{STYLE_PREFIX}. Morning scene with child alert and focused, sunrise, fresh energy, cortisol peak concept, optimal morning brain state. {STYLE_SUFFIX}',
        'theme': '16_gehirn',
        'slide_num': 2,
        'batch': 'batch_4',
        'text': {
            'headline': ['Morgens: 9-11 Uhr 🌅', 'Höchste Wachheit'],
            'body': 'Schwierige Aufgaben',
            'body2': 'am besten Vormittags!'
        }
    },
    {
        'filename': '16_gehirn_03_mittag.png',
        'prompt': f'{STYLE_PREFIX}. Midday slump visualization, tired child, yawn, clock showing 2-3 PM, dip in energy curve, need for break. {STYLE_SUFFIX}',
        'theme': '16_gehirn',
        'slide_num': 3,
        'batch': 'batch_4',
        'text': {
            'headline': ['Mittagstief: 13-15 Uhr 😴', 'Leistungstief normal'],
            'body': 'Leichte Aufgaben oder Pause',
            'body2': 'Schlafenszeit-Mittagessen!'
        }
    },
    {
        'filename': '16_gehirn_04_nachmittag.png',
        'prompt': f'{STYLE_PREFIX}. Afternoon recovery, child getting second wind, productivity rising again, moderate energy for routine tasks. {STYLE_SUFFIX}',
        'theme': '16_gehirn',
        'slide_num': 4,
        'batch': 'batch_4',
        'text': {
            'headline': ['Nachmittag: 16-18 Uhr 📈', 'Zweite Welle'],
            'body': 'Gut für Wiederholung',
            'body2': '& Routine-Aufgaben'
        }
    },
    {
        'filename': '16_gehirn_05_individuell.png',
        'prompt': f'{STYLE_PREFIX}. Different chronotypes visualization, morning lark vs night owl concept, individual differences in peak times. {STYLE_SUFFIX}',
        'theme': '16_gehirn',
        'slide_num': 5,
        'batch': 'batch_4',
        'text': {
            'headline': ['Individuell wichtig 🎯', 'Typ bedenken'],
            'body': 'Eule oder Lerche?',
            'body2': 'Eigenen Rhythmus finden!'
        }
    }
]

# ============================================================
# THEME 17: "Warum Pausen beim Lernen wichtig sind"
# ============================================================
THEME_17_SLIDES = [
    {
        'filename': '17_pausen_01_hook.png',
        'prompt': f'{STYLE_PREFIX}. Tired exhausted child vs refreshed child after break, comparison visualization, importance of rest, before/after concept. {STYLE_SUFFIX}',
        'theme': '17_pausen',
        'slide_num': 1,
        'batch': 'batch_4',
        'text': {
            'headline': ['Warum Pausen beim', 'Lernen wichtig sind ☕'],
            'body': 'Ohne Pause sinkt',
            'body2': 'die Leistung drastisch!'
        }
    },
    {
        'filename': '17_pausen_02_konzentration.png',
        'prompt': f'{STYLE_PREFIX}. Concentration curve graph showing decline over time and recovery with breaks, data visualization, productivity science. {STYLE_SUFFIX}',
        'theme': '17_pausen',
        'slide_num': 2,
        'batch': 'batch_4',
        'text': {
            'headline': ['Konzentrationskurve 📉', 'Nach 25 Min sinkt sie'],
            'body': 'Ununterbrochenes Lernen',
            'body2': '= schlechte Aufnahme'
        }
    },
    {
        'filename': '17_pausen_03_verarbeitung.png',
        'prompt': f'{STYLE_PREFIX}. Brain processing information during rest, neural pathways consolidating, memory formation visualization, active recovery. {STYLE_SUFFIX}',
        'theme': '17_pausen',
        'slide_num': 3,
        'batch': 'batch_4',
        'text': {
            'headline': ['Das Gehirn arbeitet', 'weiter 🧠'],
            'body': 'In der Pause wird',
            'body2': 'das Gelernte verankert'
        }
    },
    {
        'filename': '17_pausen_04_bewegung.png',
        'prompt': f'{STYLE_PREFIX}. Child moving during break, stretching, walking, physical activity boosting brain, active rest concept. {STYLE_SUFFIX}',
        'theme': '17_pausen',
        'slide_num': 4,
        'batch': 'batch_4',
        'text': {
            'headline': ['Aktive Pausen 🏃', 'Bewegung statt Handy'],
            'body': '5 Minuten hochkommen,',
            'body2': 'Wasser holen, strecken!'
        }
    },
    {
        'filename': '17_pausen_05_25_5.png',
        'prompt': f'{STYLE_PREFIX}. Pomodoro cycle visualization, 25-5 rhythm, timer concept, balanced work-rest pattern, sustainable learning. {STYLE_SUFFIX}',
        'theme': '17_pausen',
        'slide_num': 5,
        'batch': 'batch_4',
        'text': {
            'headline': ['Die 25/5-Regel ⏱️', 'Pomodoro-Technik'],
            'body': '25 Min lernen,',
            'body2': '5 Min Pause - wiederholen!'
        }
    }
]

# ============================================================
# THEME 18: "Wie du Lernstress erkennst"
# ============================================================
THEME_18_SLIDES = [
    {
        'filename': '18_stress_01_hook.png',
        'prompt': f'{STYLE_PREFIX}. Parent observing child with concern, subtle stress signals, observational perspective, early warning signs concept. {STYLE_SUFFIX}',
        'theme': '18_stress',
        'slide_num': 1,
        'batch': 'batch_4',
        'text': {
            'headline': ['Wie du Lernstress', 'früh erkennst 🚨'],
            'body': 'Achte auf diese',
            'body2': 'Warnsignale!'
        }
    },
    {
        'filename': '18_stress_02_koerper.png',
        'prompt': f'{STYLE_PREFIX}. Physical stress symptoms visualization - headache, stomach ache, sleep problems, tension, body showing stress signals. {STYLE_SUFFIX}',
        'theme': '18_stress',
        'slide_num': 2,
        'batch': 'batch_4',
        'text': {
            'headline': ['Körperliche Signale 🤒', 'Bauchschmerzen'],
            'body': 'Schlafstörungen, Kopfweh,',
            'body2': 'Appetitlosigkeit'
        }
    },
    {
        'filename': '18_stress_03_verhalten.png',
        'prompt': f'{STYLE_PREFIX}. Behavioral changes - avoidance, procrastination, irritability, mood swings, emotional stress indicators. {STYLE_SUFFIX}',
        'theme': '18_stress',
        'slide_num': 3,
        'batch': 'batch_4',
        'text': {
            'headline': ['Verhaltensänderungen 😤', 'Auffälligkeiten'],
            'body': 'Reizbar, Vermeidung,',
            'body2': 'plötzliches Zögern'
        }
    },
    {
        'filename': '18_stress_04_schule.png',
        'prompt': f'{STYLE_PREFIX}. School performance decline, grades dropping, lack of interest, academic stress manifestation, worried student. {STYLE_SUFFIX}',
        'theme': '18_stress',
        'slide_num': 4,
        'batch': 'batch_4',
        'text': {
            'headline': ['Schulische Anzeichen 📉', 'Leistungsabfall'],
            'body': 'Noten sinken, Unlust,',
            'body2': 'Schwänzen, Verspätungen'
        }
    },
    {
        'filename': '18_stress_05_reaktion.png',
        'prompt': f'{STYLE_PREFIX}. Supportive parent helping stressed child, calming presence, solution-oriented approach, help and support. {STYLE_SUFFIX}',
        'theme': '18_stress',
        'slide_num': 5,
        'batch': 'batch_4',
        'text': {
            'headline': ['Richtig reagieren 💙', 'Gespräch suchen'],
            'body': 'Ohne Druck, mit Empathie',
            'body2': 'Bei Bedarf: Profis holen'
        }
    }
]

# ============================================================
# THEME 19: "Die beste Tageszeit für Hausaufgaben"
# ============================================================
THEME_19_SLIDES = [
    {
        'filename': '19_zeit_01_hook.png',
        'prompt': f'{STYLE_PREFIX}. Clock showing different times of day, homework being done at optimal moment, time optimization concept. {STYLE_SUFFIX}',
        'theme': '19_zeit',
        'slide_num': 1,
        'batch': 'batch_5',
        'text': {
            'headline': ['Die beste Tageszeit', 'für Hausaufgaben ⏰'],
            'body': 'Wann ist dein Kind',
            'body2': 'am produktivsten?'
        }
    },
    {
        'filename': '19_zeit_02_direkt.png',
        'prompt': f'{STYLE_PREFIX}. Child doing homework right after school, fresh from learning, materials still out, immediate start concept. {STYLE_SUFFIX}',
        'theme': '19_zeit',
        'slide_num': 2,
        'batch': 'batch_5',
        'text': {
            'headline': ['Option 1: Direkt nach', 'der Schule 🎒'],
            'body': 'Stoff noch frisch,',
            'body2': 'Energie vorhanden'
        }
    },
    {
        'filename': '19_zeit_03_pause.png',
        'prompt': f'{STYLE_PREFIX}. Child having break first, snack, rest, then starting homework refreshed, balance approach. {STYLE_SUFFIX}',
        'theme': '19_zeit',
        'slide_num': 3,
        'batch': 'batch_5',
        'text': {
            'headline': ['Option 2: Erst Pause ☕', 'Dann Hausaufgaben'],
            'body': '30 Min runterkommen,',
            'body2': 'dann fokussiert ran'
        }
    },
    {
        'filename': '19_zeit_04_abend.png',
        'prompt': f'{STYLE_PREFIX}. Evening study scene, some children work better at night, individual differences, night owl concept. {STYLE_SUFFIX}',
        'theme': '19_zeit',
        'slide_num': 4,
        'batch': 'batch_5',
        'text': {
            'headline': ['Option 3: Abends 🌙', 'Nicht für alle geeignet'],
            'body': 'Müdigkeit macht es',
            'body2': 'schwieriger, testen!'
        }
    },
    {
        'filename': '19_zeit_05_routine.png',
        'prompt': f'{STYLE_PREFIX}. Consistent daily routine visualization, same time every day, habit formation, structured approach. {STYLE_SUFFIX}',
        'theme': '19_zeit',
        'slide_num': 5,
        'batch': 'batch_5',
        'text': {
            'headline': ['Wichtig: Routine 🔄', 'Täglich gleiche Zeit'],
            'body': 'Gewohnheit stärkt',
            'body2': 'den Lern-Erfolg!'
        }
    }
]

# ============================================================
# THEME 20: "5 Sätze die motivieren statt drängen"
# ============================================================
THEME_20_SLIDES = [
    {
        'filename': '20_saetze_01_hook.png',
        'prompt': f'{STYLE_PREFIX}. Speech bubbles with encouraging words, positive communication, supportive parent-child interaction, motivational atmosphere. {STYLE_SUFFIX}',
        'theme': '20_saetze',
        'slide_num': 1,
        'batch': 'batch_5',
        'text': {
            'headline': ['5 Sätze die motivieren', 'statt drängen 💬'],
            'body': 'So sprichst du',
            'body2': 'ermutigend!'
        }
    },
    {
        'filename': '20_saetze_02_vertrauen.png',
        'prompt': f'{STYLE_PREFIX}. Parent expressing confidence in child, trust visualization, child standing taller with self-belief, empowerment. {STYLE_SUFFIX}',
        'theme': '20_saetze',
        'slide_num': 2,
        'batch': 'batch_5',
        'text': {
            'headline': ['Satz 1: Vertrauen 🤝', '"Ich weiß, du schaffst das!"'],
            'body': 'Selbstwirksamkeit',
            'body2': 'stärken'
        }
    },
    {
        'filename': '20_saetze_03_anerkennung.png',
        'prompt': f'{STYLE_PREFIX}. Parent acknowledging effort, child working hard, process praise not results, growth mindset encouragement. {STYLE_SUFFIX}',
        'theme': '20_saetze',
        'slide_num': 3,
        'batch': 'batch_5',
        'text': {
            'headline': ['Satz 2: Anstrengung 👏', '"Du gibst dir wirklich Mühe!"'],
            'body': 'Prozess loben,',
            'body2': 'nicht nur Ergebnis'
        }
    },
    {
        'filename': '20_saetze_04_hilfe.png',
        'prompt': f'{STYLE_PREFIX}. Parent offering help, supportive presence, partnership in learning, available but not overbearing. {STYLE_SUFFIX}',
        'theme': '20_saetze',
        'slide_num': 4,
        'batch': 'batch_5',
        'text': {
            'headline': ['Satz 3: Unterstützung 🙌', '"Ich bin da, wenn du Hilfe brauchst"'],
            'body': 'Sicherheit geben,',
            'body2': 'nicht übernehmen'
        }
    },
    {
        'filename': '20_saetze_05_wachstum.png',
        'prompt': f'{STYLE_PREFIX}. Growth mindset concept, child facing challenge positively, learning from mistakes, resilience and perseverance. {STYLE_SUFFIX}',
        'theme': '20_saetze',
        'slide_num': 5,
        'batch': 'batch_5',
        'text': {
            'headline': ['Satz 4 & 5: Wachstum 🌱', '"Fehler sind okay" / "Wir üben das"'],
            'body': 'Wachstumsdenken fördern,',
            'body2': 'Druck nehmen!'
        }
    }
]

# Combine all slides
ALL_SLIDES = (THEME_11_SLIDES + THEME_12_SLIDES + THEME_13_SLIDES + 
              THEME_14_SLIDES + THEME_15_SLIDES + THEME_16_SLIDES +
              THEME_17_SLIDES + THEME_18_SLIDES + THEME_19_SLIDES +
              THEME_20_SLIDES)


def generate_image(prompt, output_path):
    """Generate image using fal.ai FLUX Dev"""
    print(f'\n🎨 Generating: {output_path.name}')
    print(f'   Prompt: {prompt[:80]}...')
    
    result = fal_client.subscribe(
        'fal-ai/flux/dev',
        arguments={
            'prompt': prompt,
            'image_size': 'portrait_4_3',
            'num_inference_steps': 50,
            'guidance_scale': 4.5,
            'enable_safety_checker': False,
        },
        with_logs=False
    )
    
    image_url = result['images'][0]['url']
    print(f'   URL: {image_url[:60]}...')
    
    req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=120) as response:
        with open(output_path, 'wb') as f:
            f.write(response.read())
    print(f'   ✅ Saved: {output_path.name}')
    return output_path


def add_text_overlay(img_path, text_data, slide_num):
    """Add professional German text overlay"""
    print(f'   📝 Adding text overlay...')
    img = Image.open(img_path).convert('RGBA')
    
    # Sharpen
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(1.2)
    
    draw = ImageDraw.Draw(img)
    
    # Load fonts
    try:
        font_title = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 54)
        font_body = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 28)
        font_small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 24)
    except:
        font_title = font_body = font_small = ImageFont.load_default()
    
    # White overlay at top for text
    overlay_height = 280
    overlay = Image.new('RGBA', (1080, overlay_height), (255, 255, 255, 230))
    img.paste(overlay, (0, 0), overlay)
    
    # Add gradient fade
    for i in range(30):
        alpha = int(230 - i * 7)
        draw_overlay = ImageDraw.Draw(img)
        draw_overlay.line([(0, overlay_height + i), (1080, overlay_height + i)], 
                          fill=(255, 255, 255, alpha), width=1)
    
    draw = ImageDraw.Draw(img)
    
    # Draw headline
    y = 30
    for line in text_data['headline']:
        bbox = draw.textbbox((0, 0), line, font=font_title)
        x = (1080 - (bbox[2] - bbox[0])) // 2
        draw.text((x, y), line, fill=STYLE['accent_color'], font=font_title)
        y += 62
    
    # Draw body text
    y += 20
    for line in [text_data['body'], text_data['body2']]:
        if line:
            bbox = draw.textbbox((0, 0), line, font=font_body)
            x = (1080 - (bbox[2] - bbox[0])) // 2
            draw.text((x, y), line, fill=STYLE['text_color'], font=font_body)
            y += 40
    
    # Slide number
    draw.text((40, 1180), f'{slide_num}/5', fill=STYLE['text_color'], font=font_small)
    
    # Final sharpening
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(1.1)
    
    # Save
    final_path = img_path.parent / f'{img_path.stem}_final.png'
    img.convert('RGB').save(final_path, 'PNG', quality=95)
    print(f'   ✅ Final: {final_path.name}')
    return final_path


def generate_single_slide(slide):
    """Generate a single slide"""
    try:
        output_dir = OUTPUT_DIRS[slide['batch']]
        output_path = output_dir / slide['filename']
        
        # Skip if already exists
        final_path = output_dir / slide['filename'].replace('.png', '_final.png')
        if final_path.exists():
            print(f'\n✅ [{slide["batch"]}] {slide["filename"]} already exists')
            return True
        
        # Generate image
        generate_image(slide['prompt'], output_path)
        
        # Add text overlay
        add_text_overlay(output_path, slide['text'], slide['slide_num'])
        return True
    except Exception as e:
        print(f'   ❌ Error: {e}')
        import traceback
        traceback.print_exc()
        return False


def main():
    print('='*70)
    print('🚀 TikTok Carousel Generator - Batch 3-5 (Themes 11-20)')
    print('='*70)
    print(f'📁 Output: {BASE_DIR}')
    print(f'🎨 API: fal.ai FLUX Dev ($0.025/image = $1.25 total)')
    print(f'📊 Total slides to generate: {len(ALL_SLIDES)}')
    print('='*70)
    
    # Count existing
    existing = 0
    for slide in ALL_SLIDES:
        final_path = OUTPUT_DIRS[slide['batch']] / slide['filename'].replace('.png', '_final.png')
        if final_path.exists():
            existing += 1
    
    print(f'📊 Already existing: {existing}/{len(ALL_SLIDES)}')
    print(f'📊 Remaining: {len(ALL_SLIDES) - existing}')
    print('='*70)
    
    success_count = 0
    
    for i, slide in enumerate(ALL_SLIDES, 1):
        print(f'\n[{i}/{len(ALL_SLIDES)}] Batch: {slide["batch"]}', end='')
        if generate_single_slide(slide):
            success_count += 1
    
    # Summary
    print('\n' + '='*70)
    print('🎉 BATCH 3-5 COMPLETE!')
    print('='*70)
    print(f'✅ Generated: {success_count}/{len(ALL_SLIDES)} images')
    
    # List all final files
    print('\n📁 Final images:')
    for batch_name, batch_dir in OUTPUT_DIRS.items():
        final_files = sorted(batch_dir.glob('*_final.png'))
        print(f'\n   {batch_name}/ ({len(final_files)} images)')
        for f in final_files[:3]:  # Show first 3
            size_kb = f.stat().st_size / 1024
            print(f'      • {f.name} ({size_kb:.1f} KB)')
        if len(final_files) > 3:
            print(f'      ... and {len(final_files) - 3} more')


if __name__ == '__main__':
    main()
