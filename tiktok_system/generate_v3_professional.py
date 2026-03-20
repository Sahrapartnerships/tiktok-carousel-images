#!/usr/bin/env python3
"""
Generate 5 PROFESSIONAL TikTok Carousel Images
HIGHEST QUALITY - Sharp images, perfect text placement
"""

import os
import re
import urllib.request
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

# Setup
OUTPUT_DIR = Path('/root/life/elternratgeber-system/tiktok_system/images/carousel_3_fehler_v3')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load credentials
with open(os.path.expanduser('~/.fal-credentials')) as f:
    content = f.read()
    match = re.search(r'export FAL_KEY="([^"]+)"', content)
    if match:
        os.environ['FAL_KEY'] = match.group(1)

import fal_client

# PROFESSIONAL Prompts - Maximum quality, sharp details
SLIDES = [
    {
        'filename': 'slide_01_hook.png',
        'prompt': '3D rendered illustration, Pixar style characters, ultra sharp 8k quality. A cute stylized child character with big expressive eyes sitting at a modern desk, hands on cheeks looking worried at homework papers. Concerned parent figure in background near window. Soft coral pink and mint green color palette, cinematic lighting, depth of field, bokeh background. Clean composition with EMPTY SPACE at top for text overlay. Trendy 3D art like premium mobile app illustrations, smooth surfaces, rounded forms, high detail. Professional render, octane quality.',
        'overlay_type': 'hook',
        'text_zone': 'top'  # Text goes at top where background is cleaner
    },
    {
        'filename': 'slide_02_fehler_1.png', 
        'prompt': '3D rendered illustration, Pixar style, ultra sharp 8k. Split composition with clear vertical divider. Left side: child looking down sadly, parent distracted by smartphone. Right side: same child looking hopeful, parent giving full attention. Characters have smooth stylized features, soft lighting. Color palette: warm coral left, cool teal right. EMPTY SPACE in upper third for text. Trendy 3D aesthetic like Apple product illustrations, clean minimal background, professional render quality.',
        'overlay_type': 'fehler',
        'text_zone': 'top'
    },
    {
        'filename': 'slide_03_fehler_2.png',
        'prompt': '3D rendered illustration, Pixar style character, ultra sharp 8k quality. Cute stylized child character holding a school report card with disappointed expression, big soulful eyes. Modern cozy bedroom with bookshelf, soft morning light from window. Color palette: soft blue and warm peach. EMPTY SPACE at top for text overlay. Trendy 3D art style like premium app illustrations, smooth surfaces, cinematic lighting, depth of field, professional octane render.',
        'overlay_type': 'fehler',
        'text_zone': 'top'
    },
    {
        'filename': 'slide_04_fehler_3.png',
        'prompt': '3D rendered illustration, Pixar style, ultra sharp 8k. Happy confident child character organizing colorful school planner and calendar, looking proud. Supportive parent watching from background with laptop. Modern bright bedroom with plants, warm sunlight. Mint green and golden yellow palette. EMPTY SPACE in upper area for text. Trendy 3D aesthetic like high-end app illustrations, smooth rounded forms, professional lighting, octane quality render.',
        'overlay_type': 'fehler',
        'text_zone': 'top'
    },
    {
        'filename': 'slide_05_cta.png',
        'prompt': '3D rendered illustration, Pixar style family, ultra sharp 8k quality. Happy scene: confident child studying at desk with smile, two proud parents in background. Warm golden hour lighting, cozy modern home office. Color palette: golden yellow, soft coral, mint accents. EMPTY SPACE at very top for headline text. Trendy 3D art like premium product illustrations, cinematic composition, depth of field, smooth stylized characters, professional octane render.',
        'overlay_type': 'cta',
        'text_zone': 'top'
    }
]

STYLE = {
    'text_color': '#2D3436',
    'accent_color': '#E17055',
    'accent_green': '#00B894',
    'white': '#FFFFFF',
    'shadow': '#00000040'
}

def generate_image(prompt, output_path):
    print(f'🎨 Generating: {output_path.name}')
    result = fal_client.subscribe(
        'fal-ai/flux/dev',
        arguments={
            'prompt': prompt,
            'image_size': 'portrait_4_3',
            'num_inference_steps': 50,  # Maximum for FLUX Dev
            'guidance_scale': 4.5,  # Higher for more prompt adherence
            'enable_safety_checker': False,
        },
        with_logs=False
    )
    
    image_url = result['images'][0]['url']
    req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=120) as response:
        with open(output_path, 'wb') as f:
            f.write(response.read())
    print(f'✅ Saved: {output_path.name}')
    return output_path

def add_professional_overlay(img_path, slide_num, text_zone):
    """Professional text overlay with better contrast and positioning"""
    img = Image.open(img_path).convert('RGBA')
    
    # Sharpen the image first
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(1.2)
    
    draw = ImageDraw.Draw(img)
    
    # Load fonts - LARGER for better readability
    try:
        font_title = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 58)
        font_body = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 30)
        font_small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 26)
        font_cta = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 42)
    except:
        font_title = font_body = font_small = font_cta = ImageFont.load_default()
    
    # STRONGER overlay at top for text readability
    overlay_height = 350 if slide_num in [2,3,4] else 300
    overlay = Image.new('RGBA', (1080, overlay_height), (255, 255, 255, 220))
    img.paste(overlay, (0, 0), overlay)
    
    # Add subtle shadow strip at bottom of overlay
    for i in range(20):
        alpha = int(100 - i * 5)
        draw.line([(0, overlay_height + i), (1080, overlay_height + i)], 
                  fill=(255, 255, 255, alpha), width=1)
    
    draw = ImageDraw.Draw(img)
    
    # SLIDE 1: HOOK
    if slide_num == 1:
        y = 40
        # Main headline with shadow effect
        headline = "3 Fehler, die dein Kind"
        for dx, dy in [(-2,-2), (2,-2), (-2,2), (2,2)]:
            bbox = draw.textbbox((0,0), headline, font=font_title)
            x = (1080 - (bbox[2]-bbox[0])) // 2 + dx
            draw.text((x, y+dy), headline, fill=STYLE['shadow'], font=font_title)
        bbox = draw.textbbox((0,0), headline, font=font_title)
        x = (1080 - (bbox[2]-bbox[0])) // 2
        draw.text((x, y), headline, fill=STYLE['accent_color'], font=font_title)
        
        y += 70
        headline2 = "NOCH gestresster machen 😰"
        bbox = draw.textbbox((0,0), headline2, font=font_title)
        x = (1080 - (bbox[2]-bbox[0])) // 2
        draw.text((x, y), headline2, fill=STYLE['text_color'], font=font_title)
        
        # Subtext at BOTTOM of image (not over face)
        y = 1200
        subtext = "Nr. 2 sagst du bestimmt täglich..."
        bbox = draw.textbbox((0,0), subtext, font=font_body)
        x = (1080 - (bbox[2]-bbox[0])) // 2
        # White background pill
        pill_margin = 40
        draw.rounded_rectangle([x-pill_margin, y-10, x+bbox[2]-bbox[0]+pill_margin, y+50], 
                               radius=25, fill=(255,255,255,200))
        draw.text((x, y), subtext, fill=STYLE['text_color'], font=font_body)
        
        draw.text((40, 1180), '1/5', fill=STYLE['text_color'], font=font_small)
    
    # SLIDE 2-4: FEHLER
    elif slide_num in [2,3,4]:
        fehler_texts = {
            2: ('❌ "Das schaffst du schon!"', 'Dein Kind hört:', '"Mein Stress ist nicht wichtig."', 
                '✅ "Das klingst wirklich', 'stressig für dich."'),
            3: ('❌ "Warum kann Maria das', 'und du nicht?"', 'Vergleiche zerstören das', 'Selbstwertgefühl!',
                '✅ "Jeder lernt anders.', 'Was brauchst DU gerade?"'),
            4: ('❌ "Ich mach das schon', 'für dich..."', 'Überorganisation nimmt die', 'Chance auf Selbstständigkeit.',
                '✅ "Ich zeig dir, wie du', 'das selbst planst.", ""')
        t = fehler_texts[slide_num]
        
        # Headline at TOP
        y = 30
        for line in [t[0], t[1]] if slide_num in [3,4] else [t[0]]:
            bbox = draw.textbbox((0,0), line, font=font_title)
            x = (1080 - (bbox[2]-bbox[0])) // 2
            draw.text((x, y), line, fill=STYLE['accent_color'], font=font_title)
            y += 65
        
        # Body text below headline
        y = 170
        for line in [t[2], t[3]]:
            bbox = draw.textbbox((0,0), line, font=font_body)
            x = (1080 - (bbox[2]-bbox[0])) // 2
            draw.text((x, y), line, fill=STYLE['text_color'], font=font_body)
            y += 42
        
        # Solution at BOTTOM (white pill background)
        y = 1120
        pill_bg = Image.new('RGBA', (1080, 140), (255, 255, 255, 230))
        img.paste(pill_bg, (0, y-20), pill_bg)
        draw = ImageDraw.Draw(img)
        
        y = 1130
        for line in [t[4], t[5]]:
            bbox = draw.textbbox((0,0), line, font=font_body)
            x = (1080 - (bbox[2]-bbox[0])) // 2
            draw.text((x, y), line, fill=STYLE['accent_green'], font=font_body)
            y += 42
        
        draw.text((40, 1180), f'{slide_num}/5', fill=STYLE['text_color'], font=font_small)
    
    # SLIDE 5: CTA
    elif slide_num == 5:
        # Headline at TOP
        y = 30
        lines = [('Willst du mehr bewährte', 30), ('Strategien? 🎯', 95)]
        for text, y_pos in lines:
            bbox = draw.textbbox((0,0), text, font=font_title)
            x = (1080 - (bbox[2]-bbox[0])) // 2
            draw.text((x, y_pos), text, fill=STYLE['text_color'], font=font_title)
        
        # Benefits in MIDDLE with clean background
        benefits_y = 350
        benefits_bg = Image.new('RGBA', (1080, 240), (255, 255, 255, 200))
        img.paste(benefits_bg, (0, benefits_y), benefits_bg)
        draw = ImageDraw.Draw(img)
        
        benefits = ['✓ Morgenroutine ohne Drama', '✓ Gespräche, die wirklich helfen', 
                   '✓ Hausaufgaben-Strategien', '✓ Selbstständigkeit fördern']
        y = benefits_y + 20
        for benefit in benefits:
            bbox = draw.textbbox((0,0), benefit, font=font_body)
            x = (1080 - (bbox[2]-bbox[0])) // 2
            draw.text((x, y), benefit, fill=STYLE['text_color'], font=font_body)
            y += 52
        
        # Price at BOTTOM
        price_y = 1050
        price_bg = Image.new('RGBA', (1080, 200), (255, 248, 240, 240))
        img.paste(price_bg, (0, price_y), price_bg)
        draw = ImageDraw.Draw(img)
        
        y = price_y + 20
        bbox = draw.textbbox((0,0), 'Statt 49,90€', font=font_small)
        x = (1080 - (bbox[2]-bbox[0])) // 2
        draw.text((x, y), 'Statt 49,90€', fill='#888888', font=font_small)
        line_y = y + 18
        draw.line([(x, line_y), (x + bbox[2]-bbox[0], line_y)], fill='#888888', width=2)
        
        y += 50
        bbox = draw.textbbox((0,0), 'NUR 19€', font=font_title)
        x = (1080 - (bbox[2]-bbox[0])) // 2
        draw.text((x, y), 'NUR 19€', fill=STYLE['accent_color'], font=font_title)
        
        # CTA Button
        y += 90
        draw.rounded_rectangle([280, y, 800, y+70], radius=35, fill=STYLE['accent_color'])
        bbox = draw.textbbox((0,0), '🔗 Link in Bio', font=font_cta)
        x = (1080 - (bbox[2]-bbox[0])) // 2
        draw.text((x, y+14), '🔗 Link in Bio', fill='white', font=font_cta)
        
        draw.text((40, 1180), '5/5', fill=STYLE['text_color'], font=font_small)
    
    # Final sharpening
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(1.1)
    
    # Save final
    final_path = img_path.parent / f'{img_path.stem}_final.png'
    img.convert('RGB').save(final_path, 'PNG', quality=95)
    print(f'✅ Final: {final_path.name}')
    return final_path

def main():
    print('🚀 Generating 5 PROFESSIONAL TikTok Carousel Images')
    print(f'📁 Output: {OUTPUT_DIR}')
    print('🎨 Quality: 60 inference steps + professional text placement\n')
    
    for i, slide in enumerate(SLIDES, 1):
        try:
            output_path = OUTPUT_DIR / slide['filename']
            generate_image(slide['prompt'], output_path)
            add_professional_overlay(output_path, i, slide['text_zone'])
        except Exception as e:
            print(f'❌ Error on slide {i}: {e}')
    
    print('\n🎉 All done! Professional quality images ready:')
    for f in sorted(OUTPUT_DIR.glob('*_final.png')):
        print(f'   • {f.name}')

if __name__ == '__main__':
    main()
