#!/usr/bin/env python3
"""
Generate 5 TikTok Carousel Images for "3 Eltern-Fehler bei Schulstress"
Using fal.ai FLUX Dev - HIGH QUALITY
"""

import os
import sys
import json
import urllib.request
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Setup paths
OUTPUT_DIR = Path("/root/life/elternratgeber-system/tiktok_system/images/carousel_3_fehler")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load fal credentials from bash-style file
with open(os.path.expanduser("~/.fal-credentials")) as f:
    content = f.read()
    # Parse export FAL_KEY="value"
    import re
    match = re.search(r'export FAL_KEY="([^"]+)"', content)
    if match:
        os.environ["FAL_KEY"] = match.group(1)
    else:
        raise ValueError("FAL_KEY not found in credentials file")

import fal_client

# HIGH QUALITY Config
CONFIG = {
    "image_size": "portrait_4_3",
    "num_inference_steps": 50,  # High quality!
    "guidance_scale": 4.0,
    "enable_safety_checker": False,
}

# 5 Slides - OPTIMIZED for viral performance
SLIDES = [
    {
        "filename": "slide_01_hook.png",
        "prompt": """Flat vector illustration, warm pastel color palette with soft peach, coral, mint green and lavender tones. 
A worried child sitting at a desk with homework, head in hands looking stressed and overwhelmed. 
Parents visible in background looking concerned but unsure how to help. 
Cozy modern living room setting with warm lighting. 
Minimalist style, clean lines, gentle shadows, no text in image. 
Emotional, relatable parenting scene showing family stress. Professional illustration quality like in modern children's books.""",
        "overlay": {
            "headline": "3 Fehler, die dein Kind",
            "subheadline": "NOCH gestresster machen 😰",
            "subtext": "Nr. 2 sagst du bestimmt täglich..."
        }
    },
    {
        "filename": "slide_02_fehler_1.png", 
        "prompt": """Flat vector illustration, warm pastel colors (soft peach, coral, cream, light blue). 
Split-screen composition showing emotional contrast: 
LEFT: Child looking sad at desk, parent in background on smartphone appearing distracted and dismissive, 
RIGHT: Same child at desk, parent actively listening, making eye contact, being supportive and present. 
Cozy home interior with soft lighting. Clean minimalist style, no text in image. 
Emotional storytelling showing disconnection vs connection. Professional children's book illustration quality, Scandinavian design aesthetic.""",
        "overlay": {
            "headline": "❌ \"Das schaffst du schon!\"",
            "body": 'Dein Kind hört:\n"Mein Stress ist nicht wichtig."',
            "solution": '✅ "Das klingt wirklich\nstressig für dich."'
        }
    },
    {
        "filename": "slide_03_fehler_2.png",
        "prompt": """Flat vector illustration, warm pastel palette (soft blues, peaches, cream, lavender). 
Child looking at school report card with sad, disappointed expression. 
Visual metaphor showing comparison: shadowy silhouette of "perfect" student on one side, supportive encouraging figure on other side. 
Cozy bedroom or study setting with desk and books. 
Minimalist clean design, gentle shadows, no text in image. 
Emotional school stress scene, empathy-focused. Professional editorial illustration quality.""",
        "overlay": {
            "headline": '❌ "Warum kann Maria das\nund du nicht?"',
            "body": "Vergleiche zerstören das\nSelbstwertgefühl!",
            "solution": '✅ "Jeder lernt anders.\nWas brauchst DU gerade?"'
        }
    },
    {
        "filename": "slide_04_fehler_3.png",
        "prompt": """Flat vector illustration, warm pastel tones (mint green, peach, soft yellow, coral). 
Positive empowering scene: Child independently organizing school materials using colorful wall calendar and personal planner on desk, looking proud and capable. 
Parent standing nearby in background watching supportively with smile but NOT intervening or taking over. 
Scene shows developing independence and confidence. 
Clean modern bedroom/study setting with natural light. 
Minimalist style, no text in image. Professional children's illustration quality, uplifting mood.""",
        "overlay": {
            "headline": '❌ "Ich mach das schon\nfür dich..."',
            "body": "Überorganisation nimmt die\nChance auf Selbstständigkeit.",
            "solution": '✅ "Ich zeig dir, wie du\ndas selbst planst."'
        }
    },
    {
        "filename": "slide_05_cta.png",
        "prompt": """Flat vector illustration, warm pastel colors (golden yellow, soft coral, mint green, peach). 
Happy transformed family scene: relaxed child studying at desk with confident smile, organized materials, parents in background looking peaceful, proud and harmonious. 
Warm golden sunlight streaming through window. 
Visual transformation from stress to harmony, success and relief. 
Cozy modern home interior. 
Minimalist clean design, uplifting optimistic mood, no text in image. 
Professional editorial illustration quality like in premium parenting magazines.""",
        "overlay": {
            "headline": "Willst du mehr bewährte\nStrategien? 🎯",
            "benefits": [
                "✓ Morgenroutine ohne Drama",
                "✓ Gespräche, die wirklich helfen", 
                "✓ Hausaufgaben-Strategien",
                "✓ Selbstständigkeit fördern"
            ],
            "price_old": "Statt 49,90€",
            "price_new": "NUR 19€",
            "cta": "🔗 Link in Bio"
        }
    }
]

STYLE_PRESET = {
    'bg_colors': ['#FFE4C4', '#FFDAB9', '#F5DEB3', '#FFEFD5'],
    'text_color': '#4A3728',
    'accent_color': '#E74C3C',
    'accent_green': '#27AE60',
    'font_size_title': 56,
    'font_size_body': 32,
    'font_size_small': 26
}

def generate_fal_image(prompt: str, output_path: Path):
    """Generate image using fal.ai FLUX Dev"""
    print(f"🎨 Generating: {output_path.name}")
    
    result = fal_client.subscribe(
        "fal-ai/flux/dev",
        arguments={
            "prompt": prompt,
            **CONFIG
        },
        with_logs=False
    )
    
    # Download image
    image_url = result["images"][0]["url"]
    req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=120) as response:
        img_data = response.read()
    
    with open(output_path, 'wb') as f:
        f.write(img_data)
    
    print(f"✅ Saved: {output_path}")
    return output_path

def add_text_overlay(image_path: Path, overlay_data: dict, slide_num: int) -> Path:
    """Add German text overlay to image"""
    
    # Load image
    img = Image.open(image_path).convert('RGBA')
    draw = ImageDraw.Draw(img)
    
    # Load fonts
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", STYLE_PRESET['font_size_title'])
        font_body = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", STYLE_PRESET['font_size_body'])
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", STYLE_PRESET['font_size_small'])
        font_cta = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
    except:
        font_title = ImageFont.load_default()
        font_body = ImageFont.load_default()
        font_small = ImageFont.load_default()
        font_cta = ImageFont.load_default()
    
    # Semi-transparent overlay for readability
    overlay = Image.new('RGBA', img.size, (255, 248, 240, 160))
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)
    
    margin = 60
    y_pos = 80
    
    # Slide 1: Hook
    if slide_num == 1:
        # Headline
        headline = overlay_data['headline']
        bbox = draw.textbbox((0, 0), headline, font=font_title)
        x_pos = (1080 - (bbox[2] - bbox[0])) // 2
        draw.text((x_pos, y_pos), headline, fill=STYLE_PRESET['accent_color'], font=font_title)
        
        # Subheadline
        y_pos += 80
        sub = overlay_data['subheadline']
        bbox = draw.textbbox((0, 0), sub, font=font_title)
        x_pos = (1080 - (bbox[2] - bbox[0])) // 2
        draw.text((x_pos, y_pos), sub, fill=STYLE_PRESET['text_color'], font=font_title)
        
        # Subtext at bottom
        y_pos = 1100
        subtext = overlay_data['subtext']
        bbox = draw.textbbox((0, 0), subtext, font=font_body)
        x_pos = (1080 - (bbox[2] - bbox[0])) // 2
        draw.text((x_pos, y_pos), subtext, fill=STYLE_PRESET['text_color'], font=font_body)
    
    # Slides 2-4: Fehler + Lösung
    elif slide_num in [2, 3, 4]:
        # Headline (Fehler)
        headline = overlay_data['headline']
        y_pos = 60
        bbox = draw.textbbox((0, 0), headline, font=font_title)
        x_pos = (1080 - (bbox[2] - bbox[0])) // 2
        draw.text((x_pos, y_pos), headline, fill=STYLE_PRESET['accent_color'], font=font_title)
        
        # Body text
        y_pos += 100
        body = overlay_data['body']
        for line in body.split('\n'):
            bbox = draw.textbbox((0, 0), line, font=font_body)
            x_pos = (1080 - (bbox[2] - bbox[0])) // 2
            draw.text((x_pos, y_pos), line, fill=STYLE_PRESET['text_color'], font=font_body)
            y_pos += 45
        
        # Solution at bottom
        y_pos = 1050
        solution = overlay_data['solution']
        for line in solution.split('\n'):
            bbox = draw.textbbox((0, 0), line, font=font_body)
            x_pos = (1080 - (bbox[2] - bbox[0])) // 2
            draw.text((x_pos, y_pos), line, fill=STYLE_PRESET['accent_green'], font=font_body)
            y_pos += 45
    
    # Slide 5: CTA
    elif slide_num == 5:
        # Headline
        headline = overlay_data['headline']
        y_pos = 50
        bbox = draw.textbbox((0, 0), headline, font=font_title)
        x_pos = (1080 - (bbox[2] - bbox[0])) // 2
        draw.text((x_pos, y_pos), headline, fill=STYLE_PRESET['text_color'], font=font_title)
        
        # Benefits
        y_pos += 120
        for benefit in overlay_data['benefits']:
            bbox = draw.textbbox((0, 0), benefit, font=font_body)
            x_pos = (1080 - (bbox[2] - bbox[0])) // 2
            draw.text((x_pos, y_pos), benefit, fill=STYLE_PRESET['text_color'], font=font_body)
            y_pos += 55
        
        # Price anchor
        y_pos += 40
        price_old = overlay_data['price_old']
        bbox = draw.textbbox((0, 0), price_old, font=font_small)
        x_pos = (1080 - (bbox[2] - bbox[0])) // 2
        # Strikethrough
        draw.text((x_pos, y_pos), price_old, fill='#888888', font=font_small)
        line_y = y_pos + 18
        draw.line([(x_pos, line_y), (x_pos + bbox[2] - bbox[0], line_y)], fill='#888888', width=2)
        
        # New price
        y_pos += 50
        price_new = overlay_data['price_new']
        bbox = draw.textbbox((0, 0), price_new, font=font_title)
        x_pos = (1080 - (bbox[2] - bbox[0])) // 2
        draw.text((x_pos, y_pos), price_new, fill=STYLE_PRESET['accent_color'], font=font_title)
        
        # CTA Button
        y_pos += 100
        cta = overlay_data['cta']
        button_margin = 250
        draw.rounded_rectangle(
            [button_margin, y_pos, 1080 - button_margin, y_pos + 70],
            radius=35,
            fill=STYLE_PRESET['accent_color']
        )
        bbox = draw.textbbox((0, 0), cta, font=font_cta)
        x_pos = (1080 - (bbox[2] - bbox[0])) // 2
        draw.text((x_pos, y_pos + 15), cta, fill='white', font=font_cta)
    
    # Slide number
    draw.text((40, 40), f"{slide_num}/5", fill=STYLE_PRESET['text_color'], font=font_small)
    
    # Save final
    final_path = image_path.parent / f"{image_path.stem}_final.png"
    img.convert('RGB').save(final_path, 'PNG', quality=95)
    print(f"✅ Text overlay added: {final_path.name}")
    return final_path

def main():
    print("🚀 Generating 5 TikTok Carousel Images with fal.ai FLUX")
    print(f"📁 Output: {OUTPUT_DIR}")
    print(f"⚙️  Quality: {CONFIG['num_inference_steps']} inference steps\n")
    
    generated = []
    
    for i, slide in enumerate(SLIDES, 1):
        try:
            # Generate base image
            base_path = OUTPUT_DIR / slide['filename']
            generate_fal_image(slide['prompt'], base_path)
            
            # Add text overlay
            final_path = add_text_overlay(base_path, slide['overlay'], i)
            generated.append(final_path)
            
        except Exception as e:
            print(f"❌ Error on slide {i}: {e}")
    
    print(f"\n🎉 Complete! Generated {len(generated)}/5 images")
    print(f"💰 Estimated cost: ${len(generated) * 0.036:.2f}")
    print(f"\nFiles:")
    for img in generated:
        print(f"   • {img.name}")
    
    return generated

if __name__ == "__main__":
    main()
