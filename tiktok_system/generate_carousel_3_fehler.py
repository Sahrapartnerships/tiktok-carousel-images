#!/usr/bin/env python3
"""
Generate 5 TikTok Carousel Images for "3 Eltern-Fehler bei Schulstress"
Using fal.ai FLUX Dev for high-quality illustration style
"""

import fal_client
import os
import json
from pathlib import Path

# Output directory
OUTPUT_DIR = Path("/root/life/elternratgeber-system/tiktok_system/images/carousel_3_fehler")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load credentials
with open(os.path.expanduser("~/.fal-credentials")) as f:
    creds = json.load(f)
    os.environ["FAL_KEY"] = f"{creds['key_id']}:{creds['key_secret']}"

# Image generation config - HIGH QUALITY settings
CONFIG = {
    "image_size": "portrait_4_3",  # 1080x1350 for TikTok/Instagram
    "num_inference_steps": 50,     # High quality (was key learning!)
    "guidance_scale": 4.0,
    "enable_safety_checker": False,
}

# 5 Slides with optimized prompts
SLIDES = [
    {
        "name": "slide_01_hook",
        "prompt": """Flat vector illustration, warm pastel color palette with soft peach, coral, mint green and lavender tones. 
A worried child sitting at a desk with homework, head in hands looking stressed. 
Parents visible in background looking concerned. 
Cozy modern living room setting. 
Minimalist style, clean lines, gentle shadows, no text in image. 
Emotional, relatable parenting scene. Professional illustration quality."""
    },
    {
        "name": "slide_02_fehler_1",
        "prompt": """Flat vector illustration, warm pastel colors (soft peach, coral, cream). 
Split-screen composition: LEFT side shows child looking sad with parent in background appearing dismissive while holding phone. 
RIGHT side shows same child with parent actively listening, making eye contact, being supportive. 
Cozy home interior. Clean minimalist style, no text in image. 
Emotional contrast between disconnection and connection. Professional children's book illustration quality."""
    },
    {
        "name": "slide_03_fehler_2",
        "prompt": """Flat vector illustration, warm pastel palette (soft blues, peaches, cream). 
Child looking at report card with sad expression. 
Two speech bubbles floating above: one with shadowy comparison figure, one with supportive figure. 
Cozy bedroom or study setting. 
Minimalist clean design, gentle shadows, no text in image. 
Emotional school stress scene. Professional illustration style."""
    },
    {
        "name": "slide_04_fehler_3",
        "prompt": """Flat vector illustration, warm pastel tones (mint, peach, soft yellow). 
Child independently organizing school materials with colorful wall calendar and planner on desk. 
Parent standing nearby watching supportively but NOT taking over. 
Empowering scene of developing independence. 
Clean modern bedroom/study setting. 
Minimalist style, no text in image. Professional children's illustration quality."""
    },
    {
        "name": "slide_05_cta",
        "prompt": """Flat vector illustration, warm pastel colors (golden yellow, soft coral, mint green). 
Happy family scene: relaxed child studying at desk with smile, parents in background looking peaceful and proud. 
Warm sunlight through window. 
Transformation from stress to harmony. 
Cozy modern home interior. 
Minimalist clean design, uplifting mood, no text in image. 
Professional editorial illustration quality."""
    }
]

def generate_image(prompt: str, output_path: Path):
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
    import urllib.request
    image_url = result["images"][0]["url"]
    urllib.request.urlretrieve(image_url, output_path)
    
    print(f"✅ Saved: {output_path}")
    return output_path

def main():
    print("🚀 Generating 5 TikTok Carousel Images")
    print(f"📁 Output: {OUTPUT_DIR}")
    print(f"⚙️  Quality: {CONFIG['num_inference_steps']} inference steps\n")
    
    generated = []
    for slide in SLIDES:
        output_path = OUTPUT_DIR / f"{slide['name']}_flux.png"
        
        try:
            generate_image(slide["prompt"], output_path)
            generated.append(output_path)
        except Exception as e:
            print(f"❌ Error generating {slide['name']}: {e}")
    
    print(f"\n🎉 Complete! Generated {len(generated)}/5 images")
    print(f"💰 Estimated cost: ${len(generated) * 0.036:.2f}")
    
    for img in generated:
        print(f"   • {img.name}")

if __name__ == "__main__":
    main()
