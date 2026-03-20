#!/usr/bin/env python3
"""
Generate TikTok Carousel Images - Batch 2 (Themes 6-10)
Themen: Cornell-Methode, Mind Mapping, Pomodoro Kids, Belohnungssystem, Konzentration
Nutzt fal.ai FLUX Dev API
"""

import os
import re
import urllib.request
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

# Setup
OUTPUT_DIR = Path('/root/life/elternratgeber-system/tiktok_system/images/batch_2')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

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
    'white': '#FFFFFF',
    'shadow': '#00000040'
}

# Theme 6: Cornell-Methode Deep Dive
CORNELL_SLIDES = [
    {
        'filename': '06_cornell_01_hook.png',
        'prompt': '3D rendered illustration, Pixar style characters, ultra sharp 8k quality. A happy child sitting at a desk showing an organized notebook with the Cornell note-taking system layout. The notebook has three clear sections - cues, notes, and summary. Warm study room with soft golden lighting, bookshelves in background. Color palette: soft coral pink, mint green accents, warm beige. EMPTY SPACE at top for text. Trendy 3D aesthetic like premium app illustrations, clean modern style, cinematic lighting, professional octane render.',
        'theme': 'cornell',
        'slide_num': 1
    },
    {
        'filename': '06_cornell_02_setup.png',
        'prompt': '3D rendered illustration, Pixar style, ultra sharp 8k. Clean visual diagram of a page divided into three sections: narrow left column labeled "Stichwörter", large right area labeled "Notizen", and bottom strip labeled "Zusammenfassung". Stylized paper texture, soft shadows. Modern minimalist study desk scene. Color palette: soft blue #74B9FF, white, light gray. EMPTY SPACE at top for text. Trendy 3D art like Apple product illustrations, clean professional style.',
        'theme': 'cornell',
        'slide_num': 2
    },
    {
        'filename': '06_cornell_03_notizen.png',
        'prompt': '3D rendered illustration, Pixar style character, ultra sharp 8k. Cute child writing concentrated in the main notes section, using colorful pens. Close-up view of hands writing keywords and bullet points. Warm cozy atmosphere, soft morning light from window. Color palette: warm peach, soft mint, golden yellow. EMPTY SPACE at top for text. Trendy 3D aesthetic like premium app illustrations, smooth rounded forms, professional lighting.',
        'theme': 'cornell',
        'slide_num': 3
    },
    {
        'filename': '06_cornell_04_fragen.png',
        'prompt': '3D rendered illustration, Pixar style, ultra sharp 8k. Child looking thoughtful, writing questions in the left cue column. Visual representation of question marks and key terms floating gently. Modern bright study space with plants. Color palette: teal #00CEC9, soft coral, cream white. EMPTY SPACE at top for text. Trendy 3D art style, clean composition, professional octane quality.',
        'theme': 'cornell',
        'slide_num': 4
    },
    {
        'filename': '06_cornell_05_summary.png',
        'prompt': '3D rendered illustration, Pixar style, ultra sharp 8k. Proud child showing completed Cornell notes with summary section highlighted. Parent giving thumbs up in background. Success and achievement mood, warm golden hour lighting. Color palette: success green #00B894, warm gold, soft pink. EMPTY SPACE at top for headline text. Trendy 3D aesthetic like high-end app illustrations, cinematic composition, professional render.',
        'theme': 'cornell',
        'slide_num': 5
    }
]

# Theme 7: Mind Mapping Guide
MINDMAP_SLIDES = [
    {
        'filename': '07_mindmap_01_hook.png',
        'prompt': '3D rendered illustration, Pixar style, ultra sharp 8k. Child creating a colorful mind map on a large sheet of paper, with the main topic in center and branches spreading out in rainbow colors. Creative explosion of ideas visualized as glowing nodes. Modern creative space with art supplies. Color palette: vibrant but soft - purple #A29BFE, pink #FD79A8, blue #74B9FF. EMPTY SPACE at top for text. Trendy 3D art like premium app illustrations, professional render.',
        'theme': 'mindmap',
        'slide_num': 1
    },
    {
        'filename': '07_mindmap_02_center.png',
        'prompt': '3D rendered illustration, Pixar style, ultra sharp 8k. Close-up of a mind map center with "Hauptthema" written in bold, colorful circle in middle. Child drawing the first main branches with thick marker. Creative desk with colorful pens scattered. Color palette: energetic orange #FDCB6E, teal #00CEC9, soft white. EMPTY SPACE at top for text. Trendy 3D aesthetic, smooth stylized, professional lighting.',
        'theme': 'mindmap',
        'slide_num': 2
    },
    {
        'filename': '07_mindmap_03_branches.png',
        'prompt': '3D rendered illustration, Pixar style, ultra sharp 8k. Mind map with main branches extending outward, each branch a different color representing different subtopics. Child connecting related ideas with curved lines. Birds-eye view angle. Color palette: rainbow pastels - soft red, blue, green, yellow, purple. EMPTY SPACE at top for text. Trendy 3D art like Apple product illustrations, clean professional quality.',
        'theme': 'mindmap',
        'slide_num': 3
    },
    {
        'filename': '07_mindmap_04_keywords.png',
        'prompt': '3D rendered illustration, Pixar style, ultra sharp 8k. Child drawing simple icons and keywords on mind map branches - small doodles of lightbulbs, stars, and symbols instead of long text. Visual thinking concept. Creative workspace with natural light. Color palette: warm yellow #FFEAA7, mint #55EFC4, soft gray. EMPTY SPACE at top for text. Trendy 3D aesthetic, playful and creative, professional render.',
        'theme': 'mindmap',
        'slide_num': 4
    },
    {
        'filename': '07_mindmap_05_complete.png',
        'prompt': '3D rendered illustration, Pixar style, ultra sharp 8k. Complete colorful mind map on wall/poster, child and parent admiring the finished work together. Sense of accomplishment and creativity. Warm cozy room with the mind map as centerpiece. Color palette: full spectrum soft rainbow, warm gold accents. EMPTY SPACE at top for text. Trendy 3D art like premium app illustrations, cinematic depth, professional octane render.',
        'theme': 'mindmap',
        'slide_num': 5
    }
]

# Theme 8: Pomodoro für Kids
POMODORO_SLIDES = [
    {
        'filename': '08_pomodoro_01_hook.png',
        'prompt': '3D rendered illustration, Pixar style, ultra sharp 8k. Cute animated tomato-shaped timer (Pomodoro) on desk next to a child ready to study. Playful friendly design, the timer has a smiley face. Study materials neatly arranged. Color palette: tomato red #FF7675, fresh green #55EFC4, warm cream. EMPTY SPACE at top for text. Trendy 3D aesthetic like premium app illustrations, professional render quality.',
        'theme': 'pomodoro',
        'slide_num': 1
    },
    {
        'filename': '08_pomodoro_02_timer.png',
        'prompt': '3D rendered illustration, Pixar style, ultra sharp 8k. Child setting a fun colorful timer, 25 minutes displayed digitally. Visual emphasis on the time concept with soft clock elements floating. Modern clean desk setup. Color palette: bright blue #74B9FF, orange #FDCB6E, white. EMPTY SPACE at top for text. Trendy 3D art like Apple product illustrations, clean minimal background, professional render.',
        'theme': 'pomodoro',
        'slide_num': 2
    },
    {
        'filename': '08_pomodoro_03_focus.png',
        'prompt': '3D rendered illustration, Pixar style character, ultra sharp 8k. Child in deep focus mode, concentrated expression, writing or reading with complete attention. Visual "focus zone" effect with soft glow around child. Distractions blurred in background. Color palette: deep teal #00B894, soft gold, lavender #A29BFE. EMPTY SPACE at top for text. Trendy 3D aesthetic, cinematic depth of field, professional lighting.',
        'theme': 'pomodoro',
        'slide_num': 3
    },
    {
        'filename': '08_pomodoro_04_pause.png',
        'prompt': '3D rendered illustration, Pixar style, ultra sharp 8k. Happy child taking a break, stretching, looking out window, or having a healthy snack. 5-minute break visualization with playful elements. Bright cheerful room with plants. Color palette: sunshine yellow #FDCB6E, fresh mint #55EFC4, soft pink. EMPTY SPACE at top for text. Trendy 3D art like premium app illustrations, joyful mood, professional render.',
        'theme': 'pomodoro',
        'slide_num': 4
    },
    {
        'filename': '08_pomodoro_05_checkmarks.png',
        'prompt': '3D rendered illustration, Pixar style, ultra sharp 8k. Child proudly checking off completed pomodoros on a chart, multiple tomato stickers or checkmarks visible. Progress tracker with 4 slots, 3 already checked. Sense of achievement and motivation. Warm room with progress chart on wall. Color palette: success green #00B894, tomato red, golden yellow. EMPTY SPACE at top for text. Trendy 3D aesthetic, celebratory mood, professional octane render.',
        'theme': 'pomodoro',
        'slide_num': 5
    }
]

# Theme 9: Belohnungssystem
BELOHNUNG_SLIDES = [
    {
        'filename': '09_belohnung_01_hook.png',
        'prompt': '3D rendered illustration, Pixar style, ultra sharp 8k. Child excitedly placing a star sticker on a colorful reward chart on the wall. Chart shows progress toward a goal with multiple star slots. Bedroom or study area with motivational decor. Color palette: golden yellow #FDCB6E, star gold, soft blue #74B9FF. EMPTY SPACE at top for text. Trendy 3D art like premium app illustrations, professional render quality.',
        'theme': 'belohnung',
        'slide_num': 1
    },
    {
        'filename': '09_belohnung_02_chart.png',
        'prompt': '3D rendered illustration, Pixar style, ultra sharp 8k. Detailed view of a weekly reward chart with days of the week, task categories (homework, reading, practice), and star slots. Clean organized design on wall or clipboard. Color palette: soft purple #A29BFE, mint #55EFC4, warm beige. EMPTY SPACE at top for text. Trendy 3D aesthetic like Apple product illustrations, clean professional style.',
        'theme': 'belohnung',
        'slide_num': 2
    },
    {
        'filename': '09_belohnung_03_stars.png',
        'prompt': '3D rendered illustration, Pixar style, ultra sharp 8k. Close-up of child earning a golden star sticker for completed task, proud expression. Sparkle and glow effects around the star moment. Soft warm lighting emphasizing achievement. Color palette: gold #FDCB6E, success green #00B894, soft pink. EMPTY SPACE at top for text. Trendy 3D art, celebratory mood, professional render.',
        'theme': 'belohnung',
        'slide_num': 3
    },
    {
        'filename': '09_belohnung_04_ziel.png',
        'prompt': '3D rendered illustration, Pixar style, ultra sharp 8k. Child reaching a goal on the reward chart - chart shows full stars and child receives a small reward (book, activity, or experience, not material). Happy parent celebrating with child. Color palette: victory gold, warm orange #E17055, soft teal. EMPTY SPACE at top for text. Trendy 3D aesthetic like premium app illustrations, joyful cinematic lighting.',
        'theme': 'belohnung',
        'slide_num': 4
    },
    {
        'filename': '09_belohnung_05_routine.png',
        'prompt': '3D rendered illustration, Pixar style, ultra sharp 8k. Child independently checking the reward chart and starting homework without prompting, self-motivated. Parent observing proudly from background. Morning routine visualization. Color palette: fresh morning blue #74B9FF, energizing yellow #FDCB6E, soft white. EMPTY SPACE at top for text. Trendy 3D art, sense of independence and growth, professional octane render.',
        'theme': 'belohnung',
        'slide_num': 5
    }
]

# Theme 10: Konzentrationstechniken
KONZENTRATION_SLIDES = [
    {
        'filename': '10_konzentration_01_hook.png',
        'prompt': '3D rendered illustration, Pixar style, ultra sharp 8k. Child sitting in "focus bubble" - visual representation of concentration with soft glow, distractions bouncing off the bubble surface. Phone and toys trying to enter but being blocked. Color palette: focus blue #0984E3, soft lavender #A29BFE, white. EMPTY SPACE at top for text. Trendy 3D aesthetic like premium app illustrations, professional render quality.',
        'theme': 'konzentration',
        'slide_num': 1
    },
    {
        'filename': '10_konzentration_02_umgebung.png',
        'prompt': '3D rendered illustration, Pixar style, ultra sharp 8k. Clean organized study space with minimal distractions - desk with only necessary items, phone in drawer, calm colors. Before/after subtle contrast possible. Color palette: calming mint #00B894, soft gray, warm wood tones. EMPTY SPACE at top for text. Trendy 3D art like Apple product illustrations, zen minimalism, professional render.',
        'theme': 'konzentration',
        'slide_num': 2
    },
    {
        'filename': '10_konzentration_03_atmung.png',
        'prompt': '3D rendered illustration, Pixar style character, ultra sharp 8k. Child practicing deep breathing exercise, eyes closed, calm peaceful expression. Visual breathing guide - expanding/contracting circle or gentle waves. Meditative atmosphere. Color palette: calming teal #00CEC9, soft blue #74B9FF, peaceful white. EMPTY SPACE at top for text. Trendy 3D aesthetic, serene mood, professional lighting.',
        'theme': 'konzentration',
        'slide_num': 3
    },
    {
        'filename': '10_konzentration_04_aufgaben.png',
        'prompt': '3D rendered illustration, Pixar style, ultra sharp 8k. Child tackling one task at a time, other tasks visually faded/grayed out in background. Single highlighted worksheet/document in focus. Concept of single-tasking vs multitasking. Color palette: focus purple #6C5CE7, soft gray for background tasks, highlight gold #FDCB6E. EMPTY SPACE at top for text. Trendy 3D art, clear visual hierarchy, professional render.',
        'theme': 'konzentration',
        'slide_num': 4
    },
    {
        'filename': '10_konzentration_05_energie.png',
        'prompt': '3D rendered illustration, Pixar style, ultra sharp 8k. Energized child stretching, moving, or doing a quick physical activity between study sessions. Dynamic pose showing energy and readiness. Bright active atmosphere. Color palette: energetic orange #E17055, fresh green #55EFC4, sunshine yellow. EMPTY SPACE at top for text. Trendy 3D aesthetic like premium app illustrations, dynamic composition, professional octane render.',
        'theme': 'konzentration',
        'slide_num': 5
    }
]

# Combine all slides
ALL_SLIDES = CORNELL_SLIDES + MINDMAP_SLIDES + POMODORO_SLIDES + BELOHNUNG_SLIDES + KONZENTRATION_SLIDES

# Text overlays for each theme
TEXT_OVERLAYS = {
    'cornell': {
        1: {
            'headline': ['Die Cornell-Methode 📝', 'für perfekte Notizen'],
            'body': 'So merkt sich dein Kind',
            'body2': 'alles effizienter!'
        },
        2: {
            'headline': ['Die 3 Bereiche 📚'],
            'body': '1. Stichwörter (links)',
            'body2': '2. Notizen (Mitte) | 3. Zusammenfassung (unten)'
        },
        3: {
            'headline': ['Bereich 1: Notizen ✏️'],
            'body': 'Hier kommt der Hauptstoff hin',
            'body2': 'in eigenen Worten!'
        },
        4: {
            'headline': ['Bereich 2: Stichwörter 💡'],
            'body': 'Fragen \u0026 Keywords',
            'body2': 'zum schnellen Wiederholen'
        },
        5: {
            'headline': ['Bereich 3: Zusammenfassung ✨'],
            'body': 'Nach dem Lernen:',
            'body2': 'Die wichtigsten Punkte zusammenfassen'
        }
    },
    'mindmap': {
        1: {
            'headline': ['Mind Mapping 🧠', 'für kreatives Lernen'],
            'body': 'Visuell verknüpfen statt',
            'body2': 'stumpf auswendig lernen!'
        },
        2: {
            'headline': ['Schritt 1: Hauptthema 🎯'],
            'body': 'In die Mitte schreiben',
            'body2': 'und einen Kreis drum malen'
        },
        3: {
            'headline': ['Schritt 2: Äste 🌿'],
            'body': 'Hauptzweige in Farben',
            'body2': 'für jedes Unterthema'
        },
        4: {
            'headline': ['Schritt 3: Keywords 🔑'],
            'body': 'Nur Stichwörter \u0026 Symbole',
            'body2': 'keine ganzen Sätze!'
        },
        5: {
            'headline': ['Fertig! 🎨'],
            'body': 'So bleibt das Wissen',
            'body2': 'besser hängen!'
        }
    },
    'pomodoro': {
        1: {
            'headline': ['Pomodoro für Kids 🍅', 'Fokus ohne Frust'],
            'body': '25 Minuten Lernen,',
            'body2': '5 Minuten Pause!'
        },
        2: {
            'headline': ['Schritt 1: Timer stellen ⏱️'],
            'body': '25 Minuten auf die Uhr',
            'body2': 'und los gehts!'
        },
        3: {
            'headline': ['Schritt 2: Voller Fokus 🎯'],
            'body': 'Kein Handy, keine Ablenkung',
            'body2': 'Nur diese eine Aufgabe!'
        },
        4: {
            'headline': ['Schritt 3: Pause machen ☕'],
            'body': '5 Minuten chillen,',
            'body2': 'trinken, strecken, atmen!'
        },
        5: {
            'headline': ['4x wiederholen ✅'],
            'body': 'Nach 4 Pomodoros:',
            'body2': 'Große Pause (15-30 Min)!'
        }
    },
    'belohnung': {
        1: {
            'headline': ['Belohnungssystem ⭐', 'das wirklich funktioniert'],
            'body': 'Motivation durch kleine',
            'body2': 'Erfolge sichtbar machen!'
        },
        2: {
            'headline': ['Die Sternchen-Tafel 📊'],
            'body': 'Wochenplan mit Aufgaben',
            'body2': 'und Sternchen-Slots'
        },
        3: {
            'headline': ['Sterne verdienen 🌟'],
            'body': 'Aufgabe erledigt =',
            'body2': 'Stern aufkleben!'
        },
        4: {
            'headline': ['Ziel erreicht! 🏆'],
            'body': 'Volle Tafel = Belohnung',
            'body2': '(Erlebnis \u003e Geschenk!)'
        },
        5: {
            'headline': ['Selbstmotivation wächst 💪'],
            'body': 'Mit der Zeit:',
            'body2': 'Kind checkt selbst ab!'
        }
    },
    'konzentration': {
        1: {
            'headline': ['Konzentration boosten 🚀', 'ohne Medikamente'],
            'body': '5 Techniken für mehr',
            'body2': 'Fokus beim Lernen!'
        },
        2: {
            'headline': ['Tipp 1: Ablenkung weg 📵'],
            'body': 'Handy weg, Schreibtisch',
            'body2': 'nur mit Notwendigem'
        },
        3: {
            'headline': ['Tipp 2: Atem-Reset 🌬️'],
            'body': '3x tief ein \u0026 ausatmen',
            'body2': 'vor dem Lernstart'
        },
        4: {
            'headline': ['Tipp 3: Single-Tasking 🎯'],
            'body': 'Eine Sache nach der',
            'body2': 'anderen - nicht alles gleichzeitig!'
        },
        5: {
            'headline': ['Tipp 4: Bewegung ⚡'],
            'body': 'Alle 25 Minuten:',
            'body2': 'Aufstehen \u0026 Bewegen!'
        }
    }
}

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

def add_text_overlay(img_path, theme, slide_num):
    """Add professional text overlay"""
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
    
    # Get text for this slide
    text_data = TEXT_OVERLAYS.get(theme, {}).get(slide_num, {
        'headline': ['TikTok Carousel'],
        'body': 'Swipe for more',
        'body2': ''
    })
    
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
        output_path = OUTPUT_DIR / slide['filename']
        generate_image(slide['prompt'], output_path)
        add_text_overlay(output_path, slide['theme'], slide['slide_num'])
        return True
    except Exception as e:
        print(f'   ❌ Error: {e}')
        return False

def main():
    print('='*70)
    print('🚀 TikTok Carousel Generator - Batch 2')
    print('='*70)
    print(f'📁 Output: {OUTPUT_DIR}')
    print(f'🎨 API: fal.ai FLUX Dev')
    print(f'📊 Total slides to generate: {len(ALL_SLIDES)}')
    print('='*70)
    
    success_count = 0
    
    for i, slide in enumerate(ALL_SLIDES, 1):
        print(f'\n[{i}/{len(ALL_SLIDES)}]', end='')
        if generate_single_slide(slide):
            success_count += 1
    
    # Summary
    print('\n' + '='*70)
    print('🎉 BATCH 2 COMPLETE!')
    print('='*70)
    print(f'✅ Generated: {success_count}/{len(ALL_SLIDES)} images')
    
    final_files = sorted(OUTPUT_DIR.glob('*_final.png'))
    print(f'\n📁 Final images in {OUTPUT_DIR}:')
    for f in final_files:
        size_kb = f.stat().st_size / 1024
        print(f'   • {f.name} ({size_kb:.1f} KB)')

if __name__ == '__main__':
    main()
