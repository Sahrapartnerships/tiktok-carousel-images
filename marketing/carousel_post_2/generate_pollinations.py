#!/usr/bin/env python3
"""
Generate Instagram Carousel Images for Post 2
Using Pollinations.ai (fallback method)
"""

import requests
import os
from pathlib import Path

def generate_image(prompt, filename):
    """Generate image using Pollinations.ai"""
    
    # Encode prompt for URL
    encoded_prompt = requests.utils.quote(prompt)
    
    # Pollinations.ai endpoint
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1080&height=1350&seed=42&nologo=true"
    
    print(f"🎨 Generating: {filename}")
    print(f"   Prompt: {prompt[:80]}...")
    
    try:
        response = requests.get(url, timeout=120)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"   ✅ Saved: {filename}")
            return True
        else:
            print(f"   ❌ Error: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    output_dir = Path("/root/life/elternratgeber-system/marketing/carousel_post_2")
    output_dir.mkdir(exist_ok=True)
    
    # Image prompts for each slide
    slides = [
        {
            "filename": "slide_1_cover.png",
            "prompt": "Flat vector illustration, warm orange and yellow gradient background, friendly cartoon parent and child having peaceful conversation, large text space at top for '3 Sätze für weniger Schulstress', hearts and stars decorative elements, clean modern Instagram carousel cover design, portrait format 1080x1350, professional social media graphic style"
        },
        {
            "filename": "slide_2_problem.png",
            "prompt": "Split screen flat illustration, left side shows worried parent with speech bubbles, right side shows sad child with thought bubbles, soft pink and blue pastel colors, emotional but gentle, educational infographic style, modern clean design, parent saying encouraging words but child hears pressure, Instagram carousel format"
        },
        {
            "filename": "slide_3_solution1.png",
            "prompt": "Warm cozy illustration, mother hugging and comforting child at home, living room setting with soft lighting, peaceful atmosphere, child feeling understood and safe, yellow orange warm tones, supportive parenting moment, flat illustration style, emotional connection, Instagram carousel"
        },
        {
            "filename": "slide_4_solutions.png",
            "prompt": "Clean modern checklist design, mint green and white color scheme, two large checkmarks, parenting tips layout, friendly icons, educational content design, organized professional look, space for text, flat design style, Instagram carousel infographic"
        },
        {
            "filename": "slide_5_cta.png",
            "prompt": "Instagram call-to-action design, gradient purple to pink background, large bookmark icon, follow button graphic, arrows and engagement elements, modern flat social media style, professional CTA layout, clean finish, space for profile link text, portrait format"
        }
    ]
    
    print("=" * 60)
    print("🚀 Generating Instagram Carousel Post 2 Images")
    print("=" * 60)
    
    success_count = 0
    for slide in slides:
        filepath = output_dir / slide["filename"]
        if generate_image(slide["prompt"], str(filepath)):
            success_count += 1
        print()
    
    print("=" * 60)
    print(f"✅ Complete: {success_count}/{len(slides)} images generated")
    print(f"📁 Location: {output_dir}")
    print("=" * 60)
    
    # List generated files
    print("\nGenerated files:")
    for f in output_dir.glob("*.png"):
        size_kb = f.stat().st_size / 1024
        print(f"  • {f.name} ({size_kb:.1f} KB)")

if __name__ == "__main__":
    main()
