#!/usr/bin/env python3
"""
Generate 5-slide TikTok carousel - REALISTIC STYLE
Theme: 3 Fehler bei Schulstress
"""

import os
import re
import urllib.request
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = Path('/root/life/elternratgeber-system/tiktok_system/images/carousel_3_fehler_realistic')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load credentials
with open(os.path.expanduser('~/.fal-credentials')) as f:
    content = f.read()
    match = re.search(r'export FAL_KEY="([^"]+)"', content)
    if match:
        os.environ['FAL_KEY'] = match.group(1)

import fal_client

# Realistic prompts for each slide
slides = [
    {
        'file': 'slide_01_hook.png',
        'prompt': 'Professional lifestyle photography, photorealistic. A stressed 10-year-old child sitting at a wooden desk, hands covering face in overwhelm, homework papers scattered. Parent standing in background with concerned expression. Soft natural window light from the left, shallow depth of field. Warm interior with coral and sage green accents. Shot on Canon EOS R5, 85mm f/1.8 lens, editorial family photography style, authentic emotional moment, high detail skin texture, magazine quality.',
        'text': '3 Fehler, die dein Kind\nNOCH gestresster machen 😰',
        'text_pos': 'top'
    },
    {
        'file': 'slide_02_fehler_1.png',
        'prompt': 'Split composition lifestyle photography. Left side: distracted parent looking at smartphone, child sad and ignored at desk. Right side: attentive parent engaged with child, both smiling. Soft natural lighting, warm home interior with mint green and coral accents. Documentary photography style, authentic family moment, emotional storytelling. Shot on Sony A7IV, 35mm lens, photorealistic, magazine quality.',
        'text': '❌ FEHLER #1:\n"Das schaffst du schon!"\n\n✅ Stattdessen:\nValidation & aktives Zuhören',
        'text_pos': 'center'
    },
    {
        'file': 'slide_03_fehler_2.png',
        'prompt': 'Candid lifestyle photography. Disappointed child holding school report card with sad expression, sitting on bed in cozy bedroom. Bookshelf and study materials in background. Soft diffused window light, warm earth tones with soft blue and peach accents. Documentary family photography, authentic emotion, photorealistic skin texture. Shot on Canon R5, 50mm f/1.4 lens, editorial quality.',
        'text': '❌ FEHLER #2:\n"Warum kann Maria das?"\n\n✅ Stattdessen:\nIndividualität respektieren',
        'text_pos': 'center'
    },
    {
        'file': 'slide_04_fehler_3.png',
        'prompt': 'Warm lifestyle photography. Proud independent child organizing school planner at desk, looking confident. Supportive parent watching from a distance with smile. Bright bedroom with houseplants, natural morning light. Mint green and yellow color accents, harmonious family scene. Documentary style, authentic moment, photorealistic. Shot on Sony A7IV, 35mm lens, magazine quality.',
        'text': '❌ FEHLER #3:\n"Ich mach das schon"\n\n✅ Stattdessen:\nSelbstständigkeit fördern',
        'text_pos': 'center'
    },
    {
        'file': 'slide_05_cta.png',
        'prompt': 'Happy family lifestyle photography. Confident teenager studying at desk with focused expression, proud parents in soft-focus background. Warm golden hour lighting through window, harmonious home atmosphere. Golden, coral and mint color palette, success and educational achievement theme. Professional editorial photography, authentic family moment. Shot on Canon EOS R5, 85mm f/1.8 lens, photorealistic, magazine cover quality.',
        'text': '📘 DER KOMPLETTE GUIDE\n"SCHULSTRESS BEFREIT"\n\n✅ Praktische Strategien\n✅ Sofort umsetzbar\n\n🔥 Nur 19€ statt 49,90€\n📲 Link in Bio',
        'text_pos': 'top'
    }
]

print('=' * 60)
print('🎬 Generating 5-Slide Carousel - REALISTIC STYLE')
print('=' * 60)

for i, slide in enumerate(slides, 1):
    print(f'\n📸 Slide {i}/5: {slide["file"]}')
    print('-' * 50)
    
    # Generate image
    result = fal_client.subscribe(
        'fal-ai/flux-pro',
        arguments={
            'prompt': slide['prompt'],
            'aspect_ratio': '3:4',
        },
        with_logs=False
    )
    
    image_url = result['images'][0]['url']
    req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=120) as response:
        img_data = response.read()
    
    base_path = OUTPUT_DIR / slide['file']
    with open(base_path, 'wb') as f:
        f.write(img_data)
    print(f'✅ Base image: {len(img_data)/1024:.1f} KB')
    
    # Add text overlay
    img = Image.open(base_path)
    draw = ImageDraw.Draw(img)
    
    # Try to load a nice font, fallback to default
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
        font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
    except:
        font_large = ImageFont.load_default()
        font_medium = font_large
        font_small = font_large
    
    width, height = img.size
    
    # Draw text with background for readability
    lines = slide['text'].split('\n')
    y_offset = 80 if slide['text_pos'] == 'top' else height // 3
    
    for line in lines:
        if not line.strip():
            y_offset += 20
            continue
            
        # Determine font size based on line content
        if 'FEHLER' in line or '📘' in line or 'Nur 19€' in line:
            font = font_large
            fill_color = '#FF6B6B' if 'FEHLER' in line else '#4ECDC4' if '19€' in line else '#FFFFFF'
        elif line.startswith('✅') or line.startswith('❌'):
            font = font_medium
            fill_color = '#FFFFFF'
        else:
            font = font_medium
            fill_color = '#FFFFFF'
        
        # Get text bbox
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (width - text_width) // 2
        
        # Draw semi-transparent background pill
        padding = 20
        draw.rounded_rectangle(
            [x - padding, y_offset - padding, x + text_width + padding, y_offset + text_height + padding],
            radius=15,
            fill=(0, 0, 0, 180)
        )
        
        # Draw text
        draw.text((x, y_offset), line, font=font, fill=fill_color)
        y_offset += text_height + 40
    
    # Save final
    final_path = OUTPUT_DIR / f"{slide['file'].replace('.png', '_final.png')}"
    img.save(final_path, 'PNG')
    print(f'✅ Final with text: {final_path.name}')

print('\n' + '=' * 60)
print('🎉 ALL 5 SLIDES COMPLETE!')
print(f'📁 Location: {OUTPUT_DIR}')
print('=' * 60)
