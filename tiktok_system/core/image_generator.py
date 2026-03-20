#!/usr/bin/env python3
"""
Image Generator für TikTok Karussells
Nutzt Pollinations (kostenlos) oder DALL-E
"""

import os
import requests
import base64
import json
import logging
from pathlib import Path
from typing import Optional, List
from PIL import Image, ImageDraw, ImageFont
import io

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('ImageGenerator')

OUTPUT_DIR = Path('tiktok_system/images')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

class ImageGenerator:
    """Generiert Karussell-Bilder mit AI + Overlay"""
    
    def __init__(self):
        self.output_dir = OUTPUT_DIR
        self.style_presets = {
            'minimal': {
                'bg_colors': ['#E8F4F8', '#FFF5E6', '#F0F8E8', '#F8E8F0'],
                'text_color': '#2C3E50',
                'accent_color': '#FF6B6B',
                'font_size_title': 48,
                'font_size_body': 28
            },
            'warm': {
                'bg_colors': ['#FFE4C4', '#FFDAB9', '#F5DEB3', '#FFEFD5'],
                'text_color': '#4A3728',
                'accent_color': '#D2691E',
                'font_size_title': 48,
                'font_size_body': 28
            },
            'calm': {
                'bg_colors': ['#E0F2F1', '#B2DFDB', '#80CBC4', '#4DB6AC'],
                'text_color': '#004D40',
                'accent_color': '#00897B',
                'font_size_title': 48,
                'font_size_body': 28
            }
        }
    
    def generate_fal_ai(self, prompt: str, width: int = 1080, height: int = 1350) -> Optional[bytes]:
        """Generiere Bild mit fal.ai FLUX Dev (Premium Qualität)"""
        
        import fal_client
        import urllib.request
        
        try:
            result = fal_client.subscribe(
                "fal-ai/flux/dev",
                arguments={
                    "prompt": prompt,
                    "image_size": "portrait_4_3",
                    "num_inference_steps": 50,
                    "guidance_scale": 4.0,
                    "enable_safety_checker": False,
                },
                with_logs=False
            )
            
            image_url = result["images"][0]["url"]
            
            # Download image
            req = urllib.request.Request(
                image_url,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            with urllib.request.urlopen(req, timeout=60) as response:
                img_data = response.read()
                logger.info(f"✅ fal.ai Bild generiert: {prompt[:50]}...")
                return img_data
                
        except Exception as e:
            logger.error(f"❌ fal.ai Fehler: {e}")
            return None
    
    def create_carousel_slide(self, 
                             slide_number: int,
                             headline: str, 
                             body_text: str,
                             visual_prompt: str,
                             style: str = 'minimal',
                             cta: Optional[str] = None) -> Path:
        """Erstelle komplette Karussell-Seite"""
        
        # Generiere Hintergrundbild
        img_data = self.generate_pollinations(visual_prompt)
        
        if img_data:
            # Lade AI-generiertes Bild
            bg_image = Image.open(io.BytesIO(img_data))
            bg_image = bg_image.resize((1080, 1350))  # Instagram/TikTok Format
        else:
            # Fallback: Farbiger Hintergrund
            bg_image = self._create_gradient_background(style)
        
        # Füge Text-Overlay hinzu
        final_image = self._add_text_overlay(
            bg_image, headline, body_text, cta, style, slide_number
        )
        
        # Speichere
        filename = f"slide_{slide_number:02d}_{headline.replace(' ', '_')[:20]}.png"
        filepath = self.output_dir / filename
        final_image.save(filepath, 'PNG', quality=95)
        
        logger.info(f"💾 Slide gespeichert: {filepath}")
        return filepath
    
    def _create_gradient_background(self, style: str) -> Image.Image:
        """Erstelle Farbverlauf Hintergrund"""
        preset = self.style_presets.get(style, self.style_presets['minimal'])
        
        img = Image.new('RGB', (1080, 1350), preset['bg_colors'][0])
        draw = ImageDraw.Draw(img)
        
        # Einfacher Farbverlauf
        for y in range(1350):
            ratio = y / 1350
            color_idx = int(ratio * len(preset['bg_colors'])) % len(preset['bg_colors'])
            # (Vereinfacht - nur erste Farbe)
        
        return img
    
    def _add_text_overlay(self, 
                         image: Image.Image,
                         headline: str,
                         body: str,
                         cta: Optional[str],
                         style: str,
                         slide_number: int) -> Image.Image:
        """Füge Text über Bild hinzu"""
        
        preset = self.style_presets.get(style, self.style_presets['minimal'])
        draw = ImageDraw.Draw(image)
        
        # Lade Font (System Font als Fallback)
        try:
            font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", preset['font_size_title'])
            font_body = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", preset['font_size_body'])
            font_cta = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
        except:
            font_title = ImageFont.load_default()
            font_body = ImageFont.load_default()
            font_cta = ImageFont.load_default()
        
        # Semi-transparentes Overlay für bessere Lesbarkeit
        overlay = Image.new('RGBA', image.size, (255, 255, 255, 180))
        image = Image.alpha_composite(image.convert('RGBA'), overlay)
        draw = ImageDraw.Draw(image)
        
        # Zeichne Headline
        margin = 80
        y_pos = 150
        
        # Headline mit Umbruch
        words = headline.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            bbox = draw.textbbox((0, 0), ' '.join(current_line), font=font_title)
            if bbox[2] - bbox[0] > 920:  # Max Breite
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]
        lines.append(' '.join(current_line))
        
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font_title)
            x_pos = (1080 - (bbox[2] - bbox[0])) // 2
            draw.text((x_pos, y_pos), line, fill=preset['accent_color'], font=font_title)
            y_pos += preset['font_size_title'] + 10
        
        # Body Text
        y_pos += 40
        body_words = body.split()
        body_lines = []
        current_line = []
        
        for word in body_words:
            current_line.append(word)
            bbox = draw.textbbox((0, 0), ' '.join(current_line), font=font_body)
            if bbox[2] - bbox[0] > 920:
                current_line.pop()
                body_lines.append(' '.join(current_line))
                current_line = [word]
        body_lines.append(' '.join(current_line))
        
        for line in body_lines[:6]:  # Max 6 Zeilen
            bbox = draw.textbbox((0, 0), line, font=font_body)
            x_pos = (1080 - (bbox[2] - bbox[0])) // 2
            draw.text((x_pos, y_pos), line, fill=preset['text_color'], font=font_body)
            y_pos += preset['font_size_body'] + 8
        
        # CTA Button
        if cta:
            y_pos = 1150
            
            # Button Hintergrund
            button_margin = 100
            draw.rounded_rectangle(
                [button_margin, y_pos, 1080 - button_margin, y_pos + 80],
                radius=40,
                fill=preset['accent_color']
            )
            
            # CTA Text
            bbox = draw.textbbox((0, 0), cta, font=font_cta)
            x_pos = (1080 - (bbox[2] - bbox[0])) // 2
            draw.text((x_pos, y_pos + 18), cta, fill='white', font=font_cta)
        
        # Slide Nummer
        draw.text((50, 50), f"{slide_number}/5", fill=preset['text_color'], font=font_body)
        
        return image.convert('RGB')
    
    def generate_carousel_set(self, post_data: dict) -> List[Path]:
        """Generiere alle Slides für einen Post"""
        
        slides = post_data.get('slides', [])
        generated = []
        
        logger.info(f"🎨 Generiere {len(slides)} Slides für {post_data.get('id', 'unknown')}")
        
        for i, slide in enumerate(slides, 1):
            filepath = self.create_carousel_slide(
                slide_number=i,
                headline=slide.get('headline', ''),
                body_text=slide.get('body_text', ''),
                visual_prompt=slide.get('visual_prompt', ''),
                style=post_data.get('style', 'minimal'),
                cta=slide.get('cta') if i == len(slides) else None
            )
            generated.append(filepath)
        
        return generated

# Schnelle Test-Funktion
def test_generate():
    """Teste Bildgenerierung"""
    gen = ImageGenerator()
    
    test_slide = {
        'headline': '5 Warnsignale',
        'body_text': 'Die meisten Eltern übersehen diese kritischen Anzeichen von Schulstress bei ihren Kindern.',
        'visual_prompt': 'Worried mother looking at child doing homework, soft lighting, warm colors, emotional connection, professional photography style',
        'cta': 'Kommentiere "GUIDE"'
    }
    
    filepath = gen.create_carousel_slide(
        slide_number=1,
        headline=test_slide['headline'],
        body_text=test_slide['body_text'],
        visual_prompt=test_slide['visual_prompt'],
        cta=test_slide['cta']
    )
    
    print(f"✅ Test-Bild erstellt: {filepath}")
    return filepath

if __name__ == '__main__':
    test_generate()
