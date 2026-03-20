#!/usr/bin/env python3
"""
Generate TikTok Carousel Images - Batch 3 (Themes 11-15)
Themen: Lernplanung, Fachwechsel, Prüfungsangst, Eltern-Gespräch, Schulstress
Nutzt fal.ai FLUX Dev API
Bereit für Style-Entscheidung (Ideogram V3 vs FLUX-Pro)
"""

import os
import re
import urllib.request
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

# Setup
OUTPUT_DIR = Path('/root/life/elternratgeber-system/tiktok_system/images/batch_3')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load FAL credentials
with open(os.path.expanduser('~/.fal-credentials')) as f:
    content = f.read()
    match = re.search(r'export FAL_KEY="([^"]+)"', content)
    if match:
        os.environ['FAL_KEY'] = match.group(1)

import fal_client

# STYLE SELECTION - Master Albert muss entscheiden:
# Option 1: "ideogram_v3" - Flat editorial design, $0.04/image
# Option 2: "flux_pro" - 3D Pixar cinematic, $0.03-0.05/image  
# Option 3: "flux_dev" - Balance quality/cost, $0.025/image
SELECTED_STYLE = "flux_dev"  # DEFAULT - kann geändert werden

# Style-specific prompts
STYLE_PROMPTS = {
    "ideogram_v3": {
        "prefix": "Editorial flat design illustration, warm pastel colors, soft gradients,",
        "suffix": "Modern minimalist style, clean composition, generous empty space at top for text overlay, professional graphic design aesthetic like top-tier editorial illustrations."
    },
    "flux_pro": {
        "prefix": "3D rendered illustration, Pixar style characters, ultra sharp 8k quality,",
        "suffix": "Trendy 3D aesthetic like premium app illustrations, clean modern style, cinematic lighting, professional octane render, EMPTY SPACE at top for text."
    },
    "flux_dev": {
        "prefix": "3D rendered illustration, soft Pixar-inspired style, high quality,",
        "suffix": "Clean modern aesthetic, soft lighting, professional render, EMPTY SPACE at top for headline text."
    }
}

def get_prompt(base_description, style):
    """Generate prompt based on selected style"""
    style_config = STYLE_PROMPTS[style]
    return f"{style_config['prefix']} {base_description} {style_config['suffix']}"

# Theme 11: Wochen-Lernplanung
THEME_11 = [
    {"filename": "11_lernplan_01_hook.png", "desc": "Child looking at a colorful weekly study schedule on wall, organized with subjects in different colors, sense of structure and planning.", "slide": 1},
    {"filename": "11_lernplan_02_tage.png", "desc": "Calendar layout showing Monday to Friday with subject blocks, visual representation of balanced study time.", "slide": 2},
    {"filename": "11_lernplan_03_pausen.png", "desc": "Child taking a healthy break, stretching, drinking water, showing importance of rest between study sessions.", "slide": 3},
    {"filename": "11_lernplan_04_flexibel.png", "desc": "Plan being adjusted with flexibility, showing adaptation when things don't go as expected, resilient mindset.", "slide": 4},
    {"filename": "11_lernplan_05_erfolg.png", "desc": "Child ticking off completed tasks with satisfaction, sense of accomplishment, parent giving approving nod.", "slide": 5},
]

# Theme 12: Fachwechsel-Strategie  
THEME_12 = [
    {"filename": "12_wechsel_01_hook.png", "desc": "Child transitioning between different school subjects, visual metaphor of switching gears, colorful subject icons.", "slide": 1},
    {"filename": "12_wechsel_02_mental.png", "desc": "Child taking a deep breath, closing eyes momentarily, mental reset between subjects, mindfulness practice.", "slide": 2},
    {"filename": "12_wechsel_03_material.png", "desc": "Organized desk with different subject materials neatly separated, preparation for subject switch.", "slide": 3},
    {"filename": "12_wechsel_04_review.png", "desc": "Quick 2-minute review of previous subject before starting new one, bridging technique visualization.", "slide": 4},
    {"filename": "12_wechsel_05_flow.png", "desc": "Child smoothly transitioning between subjects with confidence, flow state, productive momentum.", "slide": 5},
]

# Theme 13: Prüfungsangst überwinden
THEME_13 = [
    {"filename": "13_angst_01_hook.png", "desc": "Child feeling anxious about upcoming test, worried expression, but then finding a solution, hope emerging.", "slide": 1},
    {"filename": "13_angst_02_atmung.png", "desc": "Child practicing 4-7-8 breathing technique, calm and centered, anxiety management visualization.", "slide": 2},
    {"filename": "13_angst_03_vorbereitung.png", "desc": "Thorough exam preparation spread out, organized notes, practice tests, building confidence through readiness.", "slide": 3},
    {"filename": "13_angst_04_gedanken.png", "desc": "Positive self-talk visualization, thought bubbles showing encouraging messages replacing negative ones.", "slide": 4},
    {"filename": "13_angst_05_erfolg.png", "desc": "Child walking into exam room confident and prepared, parent supporting from background, success mindset.", "slide": 5},
]

# Theme 14: Eltern-Lehrer Gespräch
THEME_14 = [
    {"filename": "14_gespraech_01_hook.png", "desc": "Parent and teacher meeting, friendly professional atmosphere, child shown in middle connecting both worlds.", "slide": 1},
    {"filename": "14_gespraech_02_vorbereitung.png", "desc": "Parent preparing questions, taking notes, organized folder with child's work samples, proactive approach.", "slide": 2},
    {"filename": "14_gespraech_03_gespräch.png", "desc": "Positive conversation scene, constructive dialogue, both parties engaged and solution-oriented.", "slide": 3},
    {"filename": "14_gespraech_04_notizen.png", "desc": "Taking notes during meeting, action items being recorded, follow-up plan emerging.", "slide": 4},
    {"filename": "14_gespraech_05_umsetzung.png", "desc": "Child benefiting from parent-teacher collaboration, improved performance, supportive triangle of communication.", "slide": 5},
]

# Theme 15: Schulstress erkennen & abbauen
THEME_15 = [
    {"filename": "15_stress_01_hook.png", "desc": "Visual representation of school stress signs - tired child, messy room, changed appetite, parent noticing with concern.", "slide": 1},
    {"filename": "15_stress_02_signale.png", "desc": "Infographic-style showing stress signals: sleep problems, irritability, avoidance, physical symptoms.", "slide": 2},
    {"filename": "15_stress_03_gespräch.png", "desc": "Parent having open conversation with child, safe space, listening with empathy, non-judgmental support.", "slide": 3},
    {"filename": "15_stress_04_aktivitäten.png", "desc": "Stress-relief activities: outdoor play, creative hobbies, family time, balancing academic pressure.", "slide": 4},
    {"filename": "15_stress_05_profis.png", "desc": "Knowing when to seek professional help, school counselor or therapist as positive support resource.", "slide": 5},
]

ALL_SLIDES = THEME_11 + THEME_12 + THEME_13 + THEME_14 + THEME_15

def generate_image(prompt, output_path):
    """Generate image using fal.ai"""
    try:
        result = fal_client.subscribe(
            "fal-ai/flux/dev",
            arguments={
                "prompt": prompt,
                "image_size": "portrait_4_3",
                "num_inference_steps": 28,
                "guidance_scale": 3.5,
                "num_images": 1,
                "enable_safety_checker": False
            },
            with_logs=False
        )
        
        image_url = result['images'][0]['url']
        urllib.request.urlretrieve(image_url, output_path)
        return True
    except Exception as e:
        print(f"Error generating {output_path}: {e}")
        return False

def add_text_overlay(image_path, output_path, theme, slide_num):
    """Add German text overlay to image"""
    # Text content for each slide
    TEXT_CONTENT = {
        "11_lernplan": ["So erstellst du einen Wochen-Lernplan", "Die Tage strukturieren", "Pausen einplanen", "Flexibel bleiben", "Erfolg feiern"],
        "12_wechsel": ["Fachwechsel ohne Stress", "Mental reset", "Material organisieren", "2-Min Review", "Flow finden"],
        "13_angst": ["Prüfungsangst besiegen", "Atemtechnik", "Gründlich vorbereiten", "Positive Gedanken", "Mit Selbstvertrauen"],
        "14_gespraech": ["Eltern-Lehrer Gespräch", "Gut vorbereiten", "Konstruktiver Dialog", "Notizen machen", "Gemeinsam umsetzen"],
        "15_stress": ["Schulstress erkennen", "Warnsignale", "Gespräch suchen", "Ausgleich schaffen", "Profis einbeziehen"]
    }
    
    try:
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)
        
        # Try to load font
        try:
            font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
            font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 48)
        except:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Get text for this slide
        theme_key = image_path.stem.split('_01_')[0].split('_02_')[0].split('_03_')[0].split('_04_')[0].split('_05_')[0]
        if theme_key in TEXT_CONTENT:
            texts = TEXT_CONTENT[theme_key]
            slide_idx = slide_num - 1
            if slide_idx < len(texts):
                text = texts[slide_idx]
                
                # Add text at top with background
                overlay = Image.new('RGBA', img.size, (255, 255, 255, 0))
                overlay_draw = ImageDraw.Draw(overlay)
                overlay_draw.rectangle([0, 0, img.width, 200], fill=(255, 255, 255, 220))
                img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
                draw = ImageDraw.Draw(img)
                
                # Center text
                bbox = draw.textbbox((0, 0), text, font=font_large)
                text_width = bbox[2] - bbox[0]
                x = (img.width - text_width) // 2
                draw.text((x, 60), text, font=font_large, fill='#2D3436')
        
        img.save(output_path, 'PNG', quality=95)
        return True
    except Exception as e:
        print(f"Error adding text to {image_path}: {e}")
        return False

# Main generation
if __name__ == "__main__":
    print(f"🎨 Generating Batch 3 with style: {SELECTED_STYLE}")
    print(f"📊 Total slides to generate: {len(ALL_SLIDES)}")
    print("-" * 50)
    
    for i, slide in enumerate(ALL_SLIDES, 1):
        output_path = OUTPUT_DIR / slide['filename']
        final_path = OUTPUT_DIR / slide['filename'].replace('.png', '_final.png')
        
        if final_path.exists():
            print(f"✅ {i}/{len(ALL_SLIDES)}: {slide['filename']} (already exists)")
            continue
        
        print(f"🔄 {i}/{len(ALL_SLIDES)}: Generating {slide['filename']}...")
        
        # Generate with selected style
        prompt = get_prompt(slide['desc'], SELECTED_STYLE)
        if generate_image(prompt, output_path):
            # Add text overlay
            theme = slide['filename'].split('_')[0]
            if add_text_overlay(output_path, final_path, theme, slide['slide']):
                print(f"   ✅ Complete: {final_path.name}")
            else:
                print(f"   ⚠️  Generated but text overlay failed")
        else:
            print(f"   ❌ Generation failed")
    
    print("-" * 50)
    print("✨ Batch 3 generation complete!")
