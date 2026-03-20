#!/usr/bin/env python3
"""
Generate 5 TikTok Carousel Images with IDEOGRAM V3
Best for illustrations, posters, social media graphics
"""

import os
import re
import urllib.request
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

# Setup
OUTPUT_DIR = Path('/root/life/elternratgeber-system/tiktok_system/images/carousel_3_fehler_v6_ideogram')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load credentials
with open(os.path.expanduser('~/.fal-credentials')) as f:
    content = f.read()
    match = re.search(r'export FAL_KEY="([^"]+)"', content)
    if match:
        os.environ['FAL_KEY'] = match.group(1)

import fal_client

# IDEOGRAM V3 Prompts - Optimized for illustration style
SLIDES = [
    {
        'filename': 'slide_01_hook.png',
        'prompt': 'Illustration, modern flat design with subtle 3D depth. A cute stylized child character sitting at a desk, hands on cheeks looking worried at homework papers. Parent figure in background looking concerned. Soft coral pink, mint green and cream color palette. Warm cozy home setting with soft lighting. Clean composition with empty space at top for text. Trendy social media illustration style, smooth gradients, friendly characters. No text in image.',
    },
    {
        'filename': 'slide_02_fehler_1.png', 
        'prompt': 'Split-screen illustration, modern flat design. Left side (coral tint): child looking sad at desk, parent distracted by phone. Right side (teal tint): same child looking hopeful, parent giving full attention. Cute stylized characters, clean minimalist style, soft studio lighting. Empty space at top for text overlay. Social media graphic style, smooth surfaces, trendy illustration aesthetic. No text.',
    },
    {
        'filename': 'slide_03_fehler_2.png',
        'prompt': 'Illustration, modern flat design with depth. Cute child character holding a school report card with disappointed expression, big expressive eyes. Cozy bedroom with bookshelf, soft morning light from window. Soft blue, peach and cream palette. Empty space at top for text. Trendy social media illustration style, smooth gradients, emotional storytelling. No text in image.',
    },
    {
        'filename': 'slide_04_fehler_3.png',
        'prompt': 'Illustration, modern flat design with subtle 3D. Happy confident child character organizing colorful school planner, looking proud and capable. Supportive parent watching from background with smile. Modern bright bedroom with plants, warm sunlight. Mint green and golden yellow palette. Empty space at top for text. Trendy social media graphic style, uplifting mood. No text.',
    },
    {
        'filename': 'slide_05_cta.png',
        'prompt': 'Illustration, modern flat design with depth. Happy family scene: confident child studying at desk with smile, two proud parents in background. Warm golden lighting, cozy modern home office. Golden yellow, soft coral and mint accents. Empty space at top for headline. Trendy social media illustration style, harmonious composition, success and transformation theme. No text.',
    }
]

STYLE = {
    'text_color': '#2D3436',
    'accent_color': '#E17055',
    'accent_green': '#00B894',
}

def generate_ideogram(prompt, output_path):
    """Generate with Ideogram V3"""
    print(f'🎨 Generating: {output_path.name}')
    
    result = fal_client.subscribe(
        'fal-ai/ideogram/v3',
        arguments={
            'prompt': prompt,
            'aspect_ratio': '3:4',  # Portrait for TikTok
            'guidance_scale': 3.5,
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

def add_overlay(img_path, slide_num):
    """Add text overlay"""
    img = Image.open(img_path).convert('RGBA')
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(1.1)
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 54)
        font_body = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 28)
        font_small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 24)
        font_cta = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 38)
    except:
        font_title = font_body = font_small = font_cta = ImageFont.load_default()
    
    # Overlay at top for text
    overlay = Image.new('RGBA', (1080, 280), (255, 255, 255, 210))
    img.paste(overlay, (0, 0), overlay)
    draw = ImageDraw.Draw(img)
    
    # SLIDE 1: HOOK
    if slide_num == 1:
        y = 30
        lines = [
            ('3 Fehler, die dein Kind', STYLE['accent_color']),
            ('NOCH gestresster machen 😰', STYLE['text_color']),
        ]
        for text, color in lines:
            bbox = draw.textbbox((0,0), text, font=font_title)
            x = (1080 - (bbox[2]-bbox[0])) // 2
            draw.text((x, y), text, fill=color, font=font_title)
            y += 65
        
        # Subtext at bottom
        y = 1180
        subtext = 'Nr. 2 sagst du bestimmt täglich...'
        bbox = draw.textbbox((0,0), subtext, font=font_body)
        x = (1080 - (bbox[2]-bbox[0])) // 2
        draw.rounded_rectangle([x-40, y-10, x+bbox[2]-bbox[0]+40, y+45], radius=20, fill=(255,255,255,180))
        draw.text((x, y), subtext, fill=STYLE['text_color'], font=font_body)
        draw.text((40, 1160), '1/5', fill=STYLE['text_color'], font=font_small)
    
    # SLIDES 2-4
    elif slide_num in [2, 3, 4]:
        fehler_texts = {
            2: (('❌ "Das schaffst du schon!"',), ('Dein Kind hört:', '"Mein Stress ist nicht wichtig."'), 
                ('✅ "Das klingt wirklich', 'stressig für dich."')),
            3: (('❌ "Warum kann Maria das"', 'und du nicht?"'), ('Vergleiche zerstören das', 'Selbstwertgefühl!'),
                ('✅ "Jeder lernt anders."', 'Was brauchst DU gerade?"')),
            4: (('❌ "Ich mach das schon"', 'für dich..."'), ('Überorganisation nimmt die', 'Chance auf Selbstständigkeit.'),
                ('✅ "Ich zeig dir, wie du"', 'das selbst planst."')),
        }
        t = fehler_texts[slide_num]
        
        y = 25
        for line in t[0]:
            bbox = draw.textbbox((0,0), line, font=font_title)
            x = (1080 - (bbox[2]-bbox[0])) // 2
            draw.text((x, y), line, fill=STYLE['accent_color'], font=font_title)
            y += 60
        
        y = 160
        for line in t[1]:
            bbox = draw.textbbox((0,0), line, font=font_body)
            x = (1080 - (bbox[2]-bbox[0])) // 2
            draw.text((x, y), line, fill=STYLE['text_color'], font=font_body)
            y += 40
        
        # Solution at bottom
        y = 1120
        pill = Image.new('RGBA', (1080, 130), (255, 255, 255, 230))
        img.paste(pill, (0, y-20), pill)
        draw = ImageDraw.Draw(img)
        for line in t[2]:
            bbox = draw.textbbox((0,0), line, font=font_body)
            x = (1080 - (bbox[2]-bbox[0])) // 2
            draw.text((x, y), line, fill=STYLE['accent_green'], font=font_body)
            y += 42
        
        draw.text((40, 1160), f'{slide_num}/5', fill=STYLE['text_color'], font=font_small)
    
    # SLIDE 5: CTA
    elif slide_num == 5:
        y = 25
        for text in ['Willst du mehr bewährte', 'Strategien? 🎯']:
            bbox = draw.textbbox((0,0), text, font=font_title)
            x = (1080 - (bbox[2]-bbox[0])) // 2
            draw.text((x, y), text, fill=STYLE['text_color'], font=font_title)
            y += 60
        
        # Benefits
        benefits_y = 340
        bg = Image.new('RGBA', (1080, 220), (255, 255, 255, 200))
        img.paste(bg, (0, benefits_y), bg)
        draw = ImageDraw.Draw(img)
        
        benefits = ['✓ Morgenroutine ohne Drama', '✓ Gespräche, die wirklich helfen', 
                   '✓ Hausaufgaben-Strategien', '✓ Selbstständigkeit fördern']
        y = benefits_y + 15
        for benefit in benefits:
            bbox = draw.textbbox((0,0), benefit, font=font_body)
            x = (1080 - (bbox[2]-bbox[0])) // 2
            draw.text((x, y), benefit, fill=STYLE['text_color'], font=font_body)
            y += 50
        
        # Price
        price_y = 1040
        bg2 = Image.new('RGBA', (1080, 190), (255, 248, 240, 240))
        img.paste(bg2, (0, price_y), bg2)
        draw = ImageDraw.Draw(img)
        
        y = price_y + 15
        bbox = draw.textbbox((0,0), 'Statt 49,90€', font=font_small)
        x = (1080 - (bbox[2]-bbox[0])) // 2
        draw.text((x, y), 'Statt 49,90€', fill='#888888', font=font_small)
        line_y = y + 16
        draw.line([(x, line_y), (x + bbox[2]-bbox[0], line_y)], fill='#888888', width=2)
        
        y += 45
        bbox = draw.textbbox((0,0), 'NUR 19€', font=font_title)
        x = (1080 - (bbox[2]-bbox[0])) // 2
        draw.text((x, y), 'NUR 19€', fill=STYLE['accent_color'], font=font_title)
        
        # CTA Button
        y += 85
        draw.rounded_rectangle([280, y, 800, y+65], radius=32, fill=STYLE['accent_color'])
        bbox = draw.textbbox((0,0), '🔗 Link in Bio', font=font_cta)
        x = (1080 - (bbox[2]-bbox[0])) // 2
        draw.text((x, y+13), '🔗 Link in Bio', fill='white', font=font_cta)
        
        draw.text((40, 1160), '5/5', fill=STYLE['text_color'], font=font_small)
    
    final_path = img_path.parent / f'{img_path.stem}_final.png'
    img.convert('RGB').save(final_path, 'PNG', quality=95)
    print(f'✅ Final: {final_path.name}')
    return final_path

def main():
    print('🚀 Generating 5 TikTok Carousel Images with IDEOGRAM V3')
    print(f'📁 Output: {OUTPUT_DIR}')
    print('🎨 Model: Ideogram V3 (perfect for illustrations)')
    print('💰 Est. cost: ~$0.20 for 5 images ($0.04 each)\n')
    
    for i, slide in enumerate(SLIDES, 1):
        try:
            output_path = OUTPUT_DIR / slide['filename']
            generate_ideogram(slide['prompt'], output_path)
            add_overlay(output_path, i)
        except Exception as e:
            print(f'❌ Error on slide {i}: {e}')
    
    print('\n🎉 Complete! Files:')
    for f in sorted(OUTPUT_DIR.glob('*_final.png')):
        print(f'   • {f.name}')

if __name__ == '__main__':
    main()
