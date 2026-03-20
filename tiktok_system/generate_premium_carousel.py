#!/usr/bin/env python3
"""
Generate 5-slide TikTok carousel - PREMIUM TEXT DESIGN
Modern TikTok aesthetic with gradients, shadows, professional typography
"""

import os
import re
import urllib.request
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUTPUT_DIR = Path('/root/life/elternratgeber-system/tiktok_system/images/carousel_3_fehler_premium')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load credentials
with open(os.path.expanduser('~/.fal-credentials')) as f:
    content = f.read()
    match = re.search(r'export FAL_KEY="([^"]+)"', content)
    if match:
        os.environ['FAL_KEY'] = match.group(1)

import fal_client

def add_gradient_pill(draw, x, y, width, height, color1, color2, radius=25):
    """Draw a gradient pill background"""
    # Create gradient
    for i in range(height):
        ratio = i / height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        draw.line([(x, y + i), (x + width, y + i)], fill=(r, g, b))
    
    # Round corners by drawing circles at edges
    # (Simplified - just return the coords for text)
    return x, y, x + width, y + height

def draw_modern_text_overlay(img, lines, position='bottom'):
    """Draw modern TikTok-style text overlay"""
    draw = ImageDraw.Draw(img)
    width, height = img.size
    
    # Modern font sizes
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 56)
        font_subtitle = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 44)
        font_body = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
        font_price = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 52)
    except:
        font_title = font_subtitle = font_body = font_price = ImageFont.load_default()
    
    # Calculate positions
    padding = 30
    line_spacing = 20
    
    # Calculate total height
    total_height = 0
    for line in lines:
        text, style = line
        if style == 'title':
            font = font_title
        elif style == 'subtitle':
            font = font_subtitle
        elif style == 'price':
            font = font_price
        else:
            font = font_body
        
        bbox = draw.textbbox((0, 0), text, font=font)
        total_height += (bbox[3] - bbox[1]) + line_spacing
    
    # Start position (bottom with padding)
    if position == 'bottom':
        current_y = height - total_height - 80
    else:
        current_y = 100
    
    for line in lines:
        text, style = line
        
        # Select font and colors based on style
        if style == 'title':
            font = font_title
            # Gradient from coral to pink
            bg_color1 = (255, 107, 107)
            bg_color2 = (255, 80, 80)
            text_color = (255, 255, 255)
        elif style == 'subtitle':
            font = font_subtitle
            bg_color1 = (40, 40, 40)
            bg_color2 = (20, 20, 20)
            text_color = (255, 255, 255)
        elif style == 'solution':
            font = font_body
            bg_color1 = (78, 205, 196)
            bg_color2 = (60, 180, 170)
            text_color = (255, 255, 255)
        elif style == 'price':
            font = font_price
            bg_color1 = (255, 217, 61)
            bg_color2 = (255, 190, 40)
            text_color = (0, 0, 0)
        else:  # body
            font = font_body
            bg_color1 = (30, 30, 30)
            bg_color2 = (15, 15, 15)
            text_color = (255, 255, 255)
        
        # Get text dimensions
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Center horizontally
        x = (width - text_width) // 2
        y = current_y
        
        # Draw shadow/glow
        shadow_offset = 4
        for dx in range(-shadow_offset, shadow_offset+1, 2):
            for dy in range(-shadow_offset, shadow_offset+1, 2):
                draw.text((x + dx, y + dy), text, font=font, fill=(0, 0, 0, 100))
        
        # Draw rounded rectangle background
        pill_padding_x = 35
        pill_padding_y = 20
        pill_width = text_width + (pill_padding_x * 2)
        pill_height = text_height + (pill_padding_y * 2)
        pill_x = x - pill_padding_x
        pill_y = y - pill_padding_y + 5
        
        # Draw pill with rounded corners
        corner_radius = 20
        draw.rounded_rectangle(
            [pill_x, pill_y, pill_x + pill_width, pill_y + pill_height],
            radius=corner_radius,
            fill=bg_color1
        )
        
        # Draw text
        draw.text((x, y), text, font=font, fill=text_color)
        
        current_y += text_height + line_spacing + 25
    
    return img

# Better prompts for FLUX-Pro
slides = [
    {
        'file': 'slide_01_hook.png',
        'prompt': 'Cinematic lifestyle photography, professional editorial quality. A distressed teenager sitting at a modern wooden desk, hands covering face, homework papers scattered. Parent silhouette standing worried in background. Soft natural window light from left, shallow depth of field, warm interior with coral and sage accents. Shot on Canon EOS R5, 85mm f/1.4 lens, photorealistic skin texture, magazine cover quality, emotional storytelling.',
        'lines': [
            ('3 FEHLER', 'title'),
            ('die dein Kind', 'subtitle'),
            ('NOCH gestresster machen', 'title'),
        ]
    },
    {
        'file': 'slide_02_fehler_1.png',
        'prompt': 'Split-screen comparison photography. Left: parent distracted on phone, sad child alone at desk. Right: attentive parent helping, happy engaged child. Modern home interior with mint green and coral accents. Soft natural lighting from windows, documentary family photography style, authentic emotions, photorealistic. Canon R5, 35mm lens, editorial quality.',
        'lines': [
            ('FEHLER #1', 'title'),
            ('"Das schaffst du schon!"', 'subtitle'),
            ('Stattdessen:', 'solution'),
            ('Validation & aktives Zuhören', 'body'),
        ]
    },
    {
        'file': 'slide_03_fehler_2.png',
        'prompt': 'Intimate lifestyle photography. Disappointed child sitting on cozy bed holding school paper, curly hair, sad expression. Bookshelf and plants in soft-focus background. Window light creating soft shadows, warm earth tones with blue and peach accents. Documentary style, authentic moment, photorealistic detail. Sony A7IV, 50mm f/1.4 lens.',
        'lines': [
            ('FEHLER #2', 'title'),
            ('"Warum kann Maria das?"', 'subtitle'),
            ('Stattdessen:', 'solution'),
            ('Individualität respektieren', 'body'),
        ]
    },
    {
        'file': 'slide_04_fehler_3.png',
        'prompt': 'Warm lifestyle photography. Confident child independently organizing colorful planner at wooden desk, focused expression. Supportive parent watching proudly from background. Bright bedroom with houseplants, morning sunlight streaming through window. Mint green and yellow accents, harmonious scene. Documentary style, photorealistic. Canon R5, 35mm f/1.8 lens.',
        'lines': [
            ('FEHLER #3', 'title'),
            ('"Ich mach das schon"', 'subtitle'),
            ('Stattdessen:', 'solution'),
            ('Selbstständigkeit fördern', 'body'),
        ]
    },
    {
        'file': 'slide_05_cta.png',
        'prompt': 'Happy family lifestyle photography. Confident teenager studying at desk with focused smile, parents in soft-focus background showing pride. Golden hour sunlight through large window, warm harmonious atmosphere. Professional editorial photography, authentic achievement moment, photorealistic detail. Canon EOS R5, 85mm f/1.8 lens, magazine cover quality.',
        'lines': [
            ('SCHULSTRESS BEFREIT', 'title'),
            ('Der komplette Guide für Eltern', 'subtitle'),
            ('Praktisch • Sofort umsetzbar', 'body'),
            ('NUR 19€ STATT 49,90€', 'price'),
            ('Link in Bio', 'body'),
        ]
    }
]

print('=' * 60)
print('🎨 PREMIUM Carousel - Modern TikTok Design')
print('=' * 60)

for i, slide in enumerate(slides, 1):
    print(f'\\n📸 Slide {i}/5: {slide["file"]}')
    
    # Generate image
    result = fal_client.subscribe(
        'fal-ai/flux-pro',
        arguments={'prompt': slide['prompt'], 'aspect_ratio': '3:4'},
        with_logs=False
    )
    
    image_url = result['images'][0]['url']
    req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=120) as response:
        img_data = response.read()
    
    base_path = OUTPUT_DIR / slide['file']
    with open(base_path, 'wb') as f:
        f.write(img_data)
    print(f'✅ Base: {len(img_data)/1024:.1f} KB')
    
    # Add premium text overlay
    img = Image.open(base_path)
    img = draw_modern_text_overlay(img, slide['lines'], position='bottom')
    
    final_path = OUTPUT_DIR / f"{slide['file'].replace('.png', '_final.png')}"
    img.save(final_path, 'PNG')
    print(f'✅ Premium overlay: {final_path.name}')

print('\\n' + '=' * 60)
print('🎉 ALL DONE - Premium TikTok Design!')
print(f'📁 Location: {OUTPUT_DIR}')
print('=' * 60)
