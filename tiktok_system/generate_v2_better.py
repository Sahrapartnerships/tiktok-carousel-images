#!/usr/bin/env python3
"""
Generate 5 BEAUTIFUL TikTok Carousel Images with fal.ai
Better style: Modern 3D illustration, vibrant colors, TikTok aesthetic
"""

import os
import re
import urllib.request
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Setup
OUTPUT_DIR = Path('/root/life/elternratgeber-system/tiktok_system/images/carousel_3_fehler_v2')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load credentials
with open(os.path.expanduser('~/.fal-credentials')) as f:
    content = f.read()
    match = re.search(r'export FAL_KEY="([^"]+)"', content)
    if match:
        os.environ['FAL_KEY'] = match.group(1)

import fal_client

# MUCH BETTER Prompts - Modern 3D style, vibrant, eye-catching
SLIDES = [
    {
        'filename': 'slide_01_hook.png',
        'prompt': '3D rendered illustration, modern aesthetic, soft gradients in coral pink and mint green. A cute stylized child character sitting at a desk with head in hands looking stressed, homework scattered. Concerned parent characters in background. Warm cozy lighting, depth of field, soft shadows. Trendy 3D art style like Apple design or modern app illustrations, rounded shapes, smooth surfaces. No text. 8k quality, professional render.',
        'overlay_type': 'hook'
    },
    {
        'filename': 'slide_02_fehler_1.png', 
        'prompt': '3D rendered illustration split composition, modern aesthetic. Left side: child looking sad at desk, parent distracted looking at smartphone. Right side: same child, parent giving full attention, making eye contact warmly. Soft coral and teal color palette, smooth 3D characters with rounded features, warm lighting. Trendy 3D art style, emotional storytelling. No text. 8k quality render.',
        'overlay_type': 'fehler'
    },
    {
        'filename': 'slide_03_fehler_2.png',
        'prompt': '3D rendered illustration, modern aesthetic, soft blue and peach color palette. Child character looking at school report card with disappointed expression. Visual metaphor with shadowy "perfect student" figure vs supportive mentor figure. Cozy bedroom with desk, books, warm lighting. Trendy 3D art style, smooth rounded shapes, emotional scene. No text. 8k quality professional render.',
        'overlay_type': 'fehler'
    },
    {
        'filename': 'slide_04_fehler_3.png',
        'prompt': '3D rendered illustration, modern aesthetic, mint green and warm yellow palette. Happy child character independently organizing school supplies with colorful planner and calendar, looking proud and confident. Supportive parent watching from background with smile, NOT taking over. Modern bedroom with natural light. Trendy 3D art style, rounded shapes, uplifting mood. No text. 8k quality render.',
        'overlay_type': 'fehler'
    },
    {
        'filename': 'slide_05_cta.png',
        'prompt': '3D rendered illustration, modern aesthetic, golden yellow and coral gradient background. Happy family scene: confident relaxed child studying, organized materials on desk, parents looking peaceful and proud in background. Warm sunlight streaming through window, harmony and success atmosphere. Trendy 3D art style like premium app illustrations, rounded shapes, smooth surfaces, warm lighting. No text. 8k quality professional render.',
        'overlay_type': 'cta'
    }
]

STYLE = {
    'text_color': '#2D3436',
    'accent_color': '#E17055',
    'accent_green': '#00B894',
    'bg_light': '#FFF9F5'
}

def generate_image(prompt, output_path):
    print(f'🎨 Generating: {output_path.name}')
    result = fal_client.subscribe(
        'fal-ai/flux/dev',
        arguments={
            'prompt': prompt,
            'image_size': 'portrait_4_3',
            'num_inference_steps': 50,
            'guidance_scale': 4.0,
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

def add_overlay(img_path, slide_num):
    img = Image.open(img_path).convert('RGBA')
    draw = ImageDraw.Draw(img)
    
    # Semi-transparent overlay - lighter for better image visibility
    overlay = Image.new('RGBA', img.size, (255, 255, 255, 100))
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)
    
    # Load fonts
    try:
        font_title = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 52)
        font_body = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 28)
        font_small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 24)
        font_cta = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 38)
    except:
        font_title = font_body = font_small = font_cta = ImageFont.load_default()
    
    # SLIDE 1: HOOK
    if slide_num == 1:
        lines = [
            ('3 Fehler, die dein Kind', STYLE['accent_color'], font_title, 60),
            ('NOCH gestresster machen 😰', STYLE['text_color'], font_title, 130),
            ('Nr. 2 sagst du bestimmt täglich...', STYLE['text_color'], font_body, 1150),
        ]
        for text, color, font, y in lines:
            bbox = draw.textbbox((0,0), text, font=font)
            x = (1080 - (bbox[2]-bbox[0])) // 2
            draw.text((x, y), text, fill=color, font=font)
        draw.text((40, 40), '1/5', fill=STYLE['text_color'], font=font_small)
    
    # SLIDE 2-4: FEHLER
    elif slide_num in [2,3,4]:
        fehler_texts = {
            2: ('❌ "Das schaffst du schon!"', 'Dein Kind hört:', '"Mein Stress ist nicht wichtig."', 
                '✅ "Das klingt wirklich', 'stressig für dich."'),
            3: ('❌ "Warum kann Maria das\nund du nicht?"', 'Vergleiche zerstören das', 'Selbstwertgefühl!',
                '✅ "Jeder lernt anders.', 'Was brauchst DU gerade?"'),
            4: ('❌ "Ich mach das schon\nfür dich..."', 'Überorganisation nimmt die', 'Chance auf Selbstständigkeit.',
                '✅ "Ich zeig dir, wie du', 'das selbst planst."')
        }
        t = fehler_texts[slide_num]
        
        # Headline
        y = 50
        for line in t[0].split('\n'):
            bbox = draw.textbbox((0,0), line, font=font_title)
            x = (1080 - (bbox[2]-bbox[0])) // 2
            draw.text((x, y), line, fill=STYLE['accent_color'], font=font_title)
            y += 55
        
        # Body
        y = 180
        for line in [t[1], t[2]]:
            bbox = draw.textbbox((0,0), line, font=font_body)
            x = (1080 - (bbox[2]-bbox[0])) // 2
            draw.text((x, y), line, fill=STYLE['text_color'], font=font_body)
            y += 40
        
        # Solution at bottom
        y = 1070
        for line in [t[3], t[4]]:
            bbox = draw.textbbox((0,0), line, font=font_body)
            x = (1080 - (bbox[2]-bbox[0])) // 2
            draw.text((x, y), line, fill=STYLE['accent_green'], font=font_body)
            y += 40
        
        draw.text((40, 40), f'{slide_num}/5', fill=STYLE['text_color'], font=font_small)
    
    # SLIDE 5: CTA
    elif slide_num == 5:
        lines = [
            ('Willst du mehr bewährte', 40),
            ('Strategien? 🎯', 100),
        ]
        for text, y in lines:
            bbox = draw.textbbox((0,0), text, font=font_title)
            x = (1080 - (bbox[2]-bbox[0])) // 2
            draw.text((x, y), text, fill=STYLE['text_color'], font=font_title)
        
        benefits = ['✓ Morgenroutine ohne Drama', '✓ Gespräche, die wirklich helfen', 
                   '✓ Hausaufgaben-Strategien', '✓ Selbstständigkeit fördern']
        y = 200
        for benefit in benefits:
            bbox = draw.textbbox((0,0), benefit, font=font_body)
            x = (1080 - (bbox[2]-bbox[0])) // 2
            draw.text((x, y), benefit, fill=STYLE['text_color'], font=font_body)
            y += 50
        
        # Price
        y += 20
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
        y += 90
        draw.rounded_rectangle([280, y, 800, y+65], radius=32, fill=STYLE['accent_color'])
        bbox = draw.textbbox((0,0), '🔗 Link in Bio', font=font_cta)
        x = (1080 - (bbox[2]-bbox[0])) // 2
        draw.text((x, y+12), '🔗 Link in Bio', fill='white', font=font_cta)
        
        draw.text((40, 40), '5/5', fill=STYLE['text_color'], font=font_small)
    
    # Save final
    final_path = img_path.parent / f'{img_path.stem}_final.png'
    img.convert('RGB').save(final_path, 'PNG', quality=95)
    print(f'✅ Final: {final_path.name}')
    return final_path

def main():
    print('🚀 Generating 5 BEAUTIFUL TikTok Carousel Images')
    print(f'📁 Output: {OUTPUT_DIR}')
    print('🎨 Style: Modern 3D illustration (much better!)\n')
    
    for i, slide in enumerate(SLIDES, 1):
        try:
            output_path = OUTPUT_DIR / slide['filename']
            generate_image(slide['prompt'], output_path)
            add_overlay(output_path, i)
        except Exception as e:
            print(f'❌ Error on slide {i}: {e}')
    
    print('\n🎉 All done! Check the results:')
    for f in OUTPUT_DIR.glob('*_final.png'):
        print(f'   • {f.name}')

if __name__ == '__main__':
    main()
